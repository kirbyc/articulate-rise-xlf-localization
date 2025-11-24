# articulate-rise-xlf-localization
Translate Articulate Rise 360 XLIFF files without paid platforms. This script extracts all text into a CSV, lets you translate it however you want (Excel + Microsoft Translator, etc.), and merges everything back into a clean, Rise-compatible XLF. Preserves HTML, spacing, and structure.
# Rise XLF Translate

Small Python script to translate **Articulate Rise 360** XLIFF (.xlf) files **without** paying for a specialized platform.

Rise exports a slightly weird XLIFF 1.2 file. A lot of translation tools either:

- refuse to open it, or  
- break the formatting, or  
- want you to pay ~$1,200/year for the privilege.

This script takes a more boring approach:

1. **Extracts** all translatable text from a Rise XLF into a CSV file  
2. You translate that CSV however you like (Excel + Microsoft Translator, etc.)  
3. **Merges** the translations back into a new XLF that Rise can import

It preserves:

- all tags and nested HTML  
- whitespace around inline formatting (e.g., `<strong>…</strong>`)  
- multiple `<trans-unit id="title">` blocks that share the same `id`  

Result: translated Rise modules, no subscription platform required.

---

## What this does (in plain language)

Given a Rise 360 export like:

- `my-course-en.xlf`

You can:

1. Run `extract` → get `segments.csv` with all the English text
2. Translate the `translated_text` column to, say, Brazilian Portuguese or Spanish
3. Run `merge` → get `my-course-pt-BR.xlf`
4. Import that back into Rise as a translation

The original English stays in `<source>`. The script creates a `<target>` for each segment with your translated text.

---

## Who this is for

People who:

- work with **Articulate Rise 360**  
- need to localize courses into other languages  
- don’t want to pay for big translation platforms  
- are comfortable installing Python and running a couple of commands  
- are not necessarily developers

If you can open a terminal / command prompt and copy-paste, you can use this.

---

## Requirements

- Python 3.9 or newer  
- A Rise 360 XLIFF export (`.xlf` file, version 1.2)
- A way to translate CSV text (Excel + Microsoft Translate, Google Sheets, etc.)

There are **no extra Python dependencies**. This script uses only the Python standard library.

---

## 1. Install Python

### Windows

1. Go to: https://www.python.org/downloads/
2. Download the latest **Python 3.x** for Windows.
3. Run the installer.
4. **Important:** on the first screen, check the box:

   > Add Python to PATH

5. Finish the installation.

To confirm it worked:

1. Open **Command Prompt**  
2. Type:

   ```bash
   python --version
You should see something like Python 3.11.4.

If that fails, try:

py --version

macOS

Go to: https://www.python.org/downloads/

Download the latest macOS installer.

Run it.

Open Terminal and type:

python3 --version


You should see a Python 3.x version.

Use python3 in the commands below.
