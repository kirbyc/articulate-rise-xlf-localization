# Rise XLF Translate

Translate Articulate Rise 360 XLIFF (.xlf) files without using expensive translation platforms.
Rise exports an unusual flavor of XLIFF 1.2 that many tools can’t open—or charge ~$1,200/year to process.

This script solves the problem by:

1. Extracting all translatable text into a CSV  
2. Letting you translate the CSV using any method (Excel + Microsoft Translator works great)  
3. Merging the translations back into a clean, Rise-compatible XLF  

It preserves:

- all HTML and inline formatting  
- whitespace before/after formatted text  
- duplicate <trans-unit id="title"> blocks  
- fully valid XLIFF 1.2 structure  

No dependencies. No subscriptions. Just Python, a CSV, and two commands.

---

## Who this is for

- People translating Articulate Rise 360 courses  
- Anyone avoiding expensive translation tools  
- Non-developers who can follow simple instructions  

If you can open a terminal, you can use this.

---

# Installation & Setup

## 1. Install Python

### Windows

1. Download Python: https://www.python.org/downloads  
2. Run the installer  
3. Check the box: “Add Python to PATH”  
4. Finish installation  
5. Open Command Prompt and verify:

        python --version

If that fails:

        py --version

Use “py” instead of “python” in all commands.

---

### macOS

1. Download: https://www.python.org/downloads  
2. Install Python  
3. In Terminal:

        python3 --version

Use “python3” in all commands.

---

## 2. Download the script

Save rise_xlf_extract_merge.py somewhere, e.g.:

Windows:
    C:\Users\<you>\Desktop\rise-xlf-translate

macOS:
    /Users/<you>/Desktop/rise-xlf-translate

Put your .xlf Rise export in the same folder.

Example:

    rise-xlf-translate/
        rise_xlf_extract_merge.py
        my-course-en.xlf

---

# How to Use

## 3. Export an XLF from Rise

In Rise:

1. Open your course  
2. Settings → Translations  
3. Export XLIFF  
4. Save my-course-en.xlf into the same folder as the script  

---

## 4. Step 1 — Extract text to CSV

### Open a terminal in your folder

Windows:
1. Open the folder in File Explorer  
2. Click the address bar  
3. Type “cmd” and press Enter  

macOS:

        cd ~/Desktop/rise-xlf-translate

### Run extract

Windows/macOS:

        python rise_xlf_extract_merge.py extract "my-course-en.xlf" "segments.csv"

macOS alternative:

        python3 rise_xlf_extract_merge.py extract "my-course-en.xlf" "segments.csv"

You should see:

        Extracted 312 segments to segments.csv

CSV created:

        segments.csv

---

## 5. Step 2 — Translate the CSV

Open segments.csv in Excel or Google Sheets.

Columns include:

- file_original  
- unit_index  
- segment_index  
- unit_id  
- leading_ws  
- trailing_ws  
- original_text  
- translated_text  (you fill this)

Do NOT edit:

- file_original  
- unit_index  
- segment_index  
- leading_ws  
- trailing_ws  

Translate only “translated_text”.

---

## Using Microsoft Excel to Translate (Recommended)

Excel formula:

        =TRANSLATE(text, "from", "to")

### 1. Identify columns  
Example:  
- Column G = original_text  
- Column H = translated_text  

### 2. Add translation formula  

Brazilian Portuguese:

        =TRANSLATE(G2, "en", "pt")

Spanish:

        =TRANSLATE(G2, "en", "es")

French:

        =TRANSLATE(G2, "en", "fr")

### 3. Copy formula down  
Drag the cell handle down the entire column.

### 4. Convert formulas to plain text  
1. Select the whole translated_text column  
2. Ctrl+C  
3. Right-click → Paste Values Only  

### 5. Save the file (important)

Save as:

        CSV UTF-8 (Comma delimited)

Example filenames:

        segments_pt-BR.csv  
        segments_es.csv

---

## 6. Step 3 — Merge translations back into XLF

Run:

        python rise_xlf_extract_merge.py merge "my-course-en.xlf" "segments_translated.csv" "my-course-pt-BR.xlf"

macOS:

        python3 rise_xlf_extract_merge.py merge "my-course-en.xlf" "segments_translated.csv" "my-course-pt-BR.xlf"

You should see:

        Applied 312 translated segments.
        Wrote merged XLF to my-course-pt-BR.xlf

---

## 7. Step 4 — Import into Rise

In Rise:

1. Open the original English course  
2. Settings → Translations  
3. Import XLIFF  
4. Choose:

        my-course-pt-BR.xlf

Rise creates a translated version.

---

# Troubleshooting

### “python is not recognized”
Python isn’t on PATH.  
Reinstall and check “Add Python to PATH”,  
or use “py” (Windows) or “python3” (macOS).

### Rise import fails
Check:

- CSV saved as UTF-8  
- You didn’t edit XML manually  
- leading_ws / trailing_ws untouched  
- Same base XLF used for extract + merge  

### Inline formatting odd?
Inline styled text often splits into multiple segments.  
Tweak those translations manually.

---

# Multiple Languages

        python rise_xlf_extract_merge.py extract my-course-en.xlf segments_es.csv
        (translate → segments_es_translated.csv)
        python rise_xlf_extract_merge.py merge my-course-en.xlf segments_es_translated.csv my-course-es.xlf

Repeat for any language.
