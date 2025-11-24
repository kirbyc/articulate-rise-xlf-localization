#!/usr/bin/env python3
"""
Rise 360 XLIFF helper: extract text segments to CSV, then merge translations back.

Usage:

  # 1) Extract segments from XLF to CSV
  python rise_xlf_extract_merge.py extract input.xlf segments.csv

  # 2) After you fill "translated_text" in segments.csv (e.g., via MS Translate),
  #    merge them back into a new XLF with <target> elements populated:
  python rise_xlf_extract_merge.py merge input.xlf segments_translated.csv output_pt_BR.xlf

Notes:
- Designed for Articulate Rise 360 XLIFF 1.2 exports.
- XLF must have <source> elements; script will create <target> elements on merge.
- CSV columns:
    file_original, unit_index, segment_index, unit_id,
    leading_ws, trailing_ws, original_text, translated_text
"""

import sys
import csv
import copy
import re
import xml.etree.ElementTree as ET
from typing import Iterator, Tuple, Dict

NS_XLIFF = "urn:oasis:names:tc:xliff:document:1.2"
NS_HTML = "http://www.w3.org/1999/xhtml"

ET.register_namespace("", NS_XLIFF)
ET.register_namespace("html", NS_HTML)

NS = {"x": NS_XLIFF}


def iter_text_slots(elem: ET.Element) -> Iterator[Tuple[ET.Element, str, str]]:
    """
    Yield (node, field_name, text_value) for each translatable text 'slot'
    in the subtree of `elem`.

    field_name is 'text' or 'tail'.

    We skip pure-whitespace strings but preserve everything else.
    """
    if elem.text and elem.text.strip():
        yield (elem, "text", elem.text)

    for child in list(elem):
        # Recurse into child first
        yield from iter_text_slots(child)

        if child.tail and child.tail.strip():
            yield (child, "tail", child.tail)


def split_whitespace(text: str) -> Tuple[str, str, str]:
    """
    Split text into (leading_ws, core, trailing_ws).
    Whitespace is anything matched by \s (spaces, tabs, newlines).
    """
    m = re.match(r'^(\s*)(.*?)(\s*)$', text, flags=re.DOTALL)
    if not m:
        return "", text, ""
    return m.group(1), m.group(2), m.group(3)


def extract_to_csv(xlf_path: str, csv_path: str) -> None:
    tree = ET.parse(xlf_path)
    root = tree.getroot()

    rows = []

    for file_elem in root.findall("x:file", NS):
        body = file_elem.find("x:body", NS)
        if body is None:
            continue

        file_original = file_elem.get("original", "")

        # unit_index is a running index for each trans-unit in this file
        for unit_index, tu in enumerate(body.findall(".//x:trans-unit", NS)):
            unit_id = tu.get("id", "")
            src = tu.find("x:source", NS)
            if src is None:
                continue

            seg_index = 0
            for _node, _field, text_value in iter_text_slots(src):
                leading_ws, core, trailing_ws = split_whitespace(text_value)

                rows.append({
                    "file_original": file_original,
                    "unit_index": str(unit_index),
                    "segment_index": str(seg_index),
                    "unit_id": unit_id,
                    "leading_ws": leading_ws,
                    "trailing_ws": trailing_ws,
                    "original_text": core,
                    "translated_text": ""
                })
                seg_index += 1

    fieldnames = [
        "file_original",
        "unit_index",
        "segment_index",
        "unit_id",
        "leading_ws",
        "trailing_ws",
        "original_text",
        "translated_text",
    ]
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Extracted {len(rows)} segments to {csv_path}")


def load_translations(csv_path: str) -> Dict[Tuple[str, int, int], Tuple[str, str, str]]:
    """
    Load translations from CSV into a dict keyed by
    (file_original, unit_index, segment_index), with values:
    (leading_ws, translated_core, trailing_ws).
    """
    translations: Dict[Tuple[str, int, int], Tuple[str, str, str]] = {}
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            file_original = row.get("file_original", "")
            unit_index_str = row.get("unit_index", "")
            seg_index_str = row.get("segment_index", "")
            leading_ws = row.get("leading_ws", "") or ""
            trailing_ws = row.get("trailing_ws", "") or ""
            translated = row.get("translated_text", "")

            if not file_original or unit_index_str == "" or seg_index_str == "":
                continue

            try:
                unit_index = int(unit_index_str)
                seg_index = int(seg_index_str)
            except ValueError:
                continue

            # Only store if we actually have a translation (non-empty).
            # If empty, we leave the original text as-is.
            if translated is not None and translated.strip() != "":
                translations[(file_original, unit_index, seg_index)] = (
                    leading_ws,
                    translated,
                    trailing_ws,
                )

    return translations


def merge_from_csv(xlf_in: str, csv_path: str, xlf_out: str) -> None:
    translations = load_translations(csv_path)
    if not translations:
        print("No translations found in CSV (translated_text column empty?). Aborting.")
        return

    tree = ET.parse(xlf_in)
    root = tree.getroot()

    total_applied = 0

    for file_elem in root.findall("x:file", NS):
        body = file_elem.find("x:body", NS)
        if body is None:
            continue

        file_original = file_elem.get("original", "")

        for unit_index, tu in enumerate(body.findall(".//x:trans-unit", NS)):
            src = tu.find("x:source", NS)
            if src is None:
                continue

            # Quick check: any translations for this (file_original, unit_index)?
            has_any = any(
                (file_original, unit_index, seg_idx) in translations
                for seg_idx in range(0, 10000)
            )
            if not has_any:
                continue

            # Deep-copy <source> to create <target>
            target = copy.deepcopy(src)
            target.tag = f"{{{NS_XLIFF}}}target"

            seg_index = 0
            for node, field, old_text in iter_text_slots(target):
                key = (file_original, unit_index, seg_index)
                if key in translations:
                    leading_ws, translated_core, trailing_ws = translations[key]

                    # Strip the core from translator, but preserve original outer whitespace
                    new_core = translated_core.strip()
                    new_text = f"{leading_ws}{new_core}{trailing_ws}"

                    if field == "text":
                        node.text = new_text
                    else:
                        node.tail = new_text

                    total_applied += 1

                seg_index += 1

            # Remove any existing <target> first
            for old_target in tu.findall("x:target", NS):
                tu.remove(old_target)

            tu.append(target)

    tree.write(xlf_out, encoding="utf-8", xml_declaration=True)
    print(f"Applied {total_applied} translated segments.")
    print(f"Wrote merged XLF to {xlf_out}")


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) < 1:
        print(__doc__)
        sys.exit(1)

    mode = argv[0].lower()

    if mode == "extract":
        if len(argv) != 3:
            print("Usage: python rise_xlf_extract_merge.py extract input.xlf segments.csv")
            sys.exit(1)
        xlf_in, csv_out = argv[1], argv[2]
        extract_to_csv(xlf_in, csv_out)

    elif mode == "merge":
        if len(argv) != 4:
            print("Usage: python rise_xlf_extract_merge.py merge input.xlf segments_translated.csv output.xlf")
            sys.exit(1)
        xlf_in, csv_in, xlf_out = argv[1], argv[2], argv[3]
        merge_from_csv(xlf_in, csv_in, xlf_out)

    else:
        print(f"Unknown mode: {mode}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
