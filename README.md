# Rise XLF Translate

Translate **Articulate Rise 360** XLIFF (.xlf) files without using expensive translation platforms.  
Rise exports a slightly odd version of XLIFF 1.2 that many tools can’t process—or want to charge ~$1,200/year to handle.  

This script takes a simpler approach:

1. **Extract** all translatable text from a Rise XLF into a CSV  
2. Translate the CSV using any tool you want (Excel + Microsoft Translator works great)  
3. **Merge** your translations back into a clean, Rise-compatible XLF  

It preserves:

- all nested HTML and inline formatting  
- whitespace before/after bold/italic segments  
- duplicate IDs (like multiple `<trans-unit id="title">`)  
- fully valid XLIFF 1.2 for Rise import  

No dependencies. No subscriptions.  
Just Python, a CSV, and a couple of commands.

---

## Who this is for

- People who build or maintain **Articulate Rise 360** courses  
- Anyone who needs to translate courses into multiple languages  
- Folks who don’t want to pay for platform subscriptions  
- Non-developers comfortable with following simple instructions  

If you can open a terminal and copy/paste commands, you can use this.

---

# Installation & Setup

## 1. Install Python

### **Windows**

1. Download Python: https://www.python.org/downloads/  
2. Run the installer  
3. **Important:** Check the box:  
   **Add Python to PATH**  
4. Finish installation  
5. Open Command Prompt and confirm:

   ```bash
   python --version
If that fails, try:

bash
Copy code
py --version
Use py instead of python in later commands.

macOS
Download Python: https://www.python.org/downloads/

Run installer

In Terminal:

bash
Copy code
python3 --version
Use python3 for all commands below.

2. Download the script
Place the file rise_xlf_extract_merge.py somewhere on your computer — for example:

Windows:
C:\Users\<you>\Desktop\rise-xlf-translate

macOS:
/Users/<you>/Desktop/rise-xlf-translate

Then put your .xlf Rise export into the same folder.

Example folder:

perl
Copy code
rise-xlf-translate/
  rise_xlf_extract_merge.py
  my-course-en.xlf
How to Use
3. Export an XLF from Rise
In Rise 360:

Open your course

Go to Settings → Translations

Click Export XLIFF

Save the .xlf file in the same folder as the script

Example: my-course-en.xlf

4. Step 1 — Extract text to CSV
Open a terminal in your folder
Windows:

Open the folder in File Explorer

Click the address bar

Type cmd → press Enter

macOS:

bash
Copy code
cd ~/Desktop/rise-xlf-translate
Run the extract command
bash
Copy code
python rise_xlf_extract_merge.py extract "my-course-en.xlf" "segments.csv"
or on macOS:

bash
Copy code
python3 rise_xlf_extract_merge.py extract "my-course-en.xlf" "segments.csv"
You’ll see something like:

css
Copy code
Extracted 312 segments to segments.csv
This creates a new file:

Copy code
segments.csv
5. Step 2 — Translate the CSV
Open segments.csv in Excel or Google Sheets.

You’ll see columns:

file_original

unit_index

segment_index

unit_id

leading_ws

trailing_ws

original_text

translated_text ← you fill this in

Do NOT modify:

file_original

unit_index

segment_index

leading_ws

trailing_ws

Translate only the translated_text column.
⭐ Using Microsoft Excel to Translate the CSV (Recommended)

Excel has a built-in =TRANSLATE() function that uses Microsoft Translator.
You can translate the entire Rise CSV with one formula.

1. Open segments.csv in Excel

You will see a column called:

original_text


and an empty column:

translated_text


You will fill only translated_text.

2. Add a translation formula

Click the first empty cell under translated_text (same row as the first original_text).

Then enter a formula like:

=TRANSLATE(G2, "en", "pt")


Where:

G2 = the original_text cell (adjust column if needed)

"en" = the source language (English)

"pt" = Brazilian Portuguese

"es" = Spanish

"fr" = French

etc.

Examples:

Brazilian Portuguese:

=TRANSLATE(G2, "en", "pt")


Spanish:

=TRANSLATE(G2, "en", "es")


French:

=TRANSLATE(G2, "en", "fr")

3. Copy the formula down the entire column

Hover over the bottom-right corner of the cell (the square “handle”), then click and drag down until all rows have translations.

Excel will automatically translate each segment.

4. Convert formulas to real text (IMPORTANT)

The merge script cannot read Excel formulas — it needs actual text.

So:

Select the entire translated_text column

Press Ctrl+C

Right-click → Paste Values Only

Now the column contains real text instead of formulas.

5. Save the file as UTF-8 CSV

Go to:

File → Save As → CSV UTF-8 (Comma delimited)

Name it something like:

segments_pt-BR.csv
segments_es.csv


This file is what you’ll use in the merge step.

That’s it — Excel does the heavy lifting, and the Python script reconstructs the XLF with perfect formatting and whitespace.

Save your translated file
Save as:

Copy code
segments_translated.csv
CSV UTF-8 (Comma delimited) is important.

6. Step 3 — Merge translations back into XLF
Run:

bash
Copy code
python rise_xlf_extract_merge.py merge "my-course-en.xlf" "segments_translated.csv" "my-course-es.xlf"
(macOS)

bash
Copy code
python3 rise_xlf_extract_merge.py merge "my-course-en.xlf" "segments_translated.csv" "my-course-es.xlf"
You should see:

css
Copy code
Applied 312 translated segments.
Wrote merged XLF to my-course-es.xlf
This new file is your translated Rise XLIFF.

7. Step 4 — Import into Rise
In Rise:

Open the original English course

Go to Settings → Translations

Click Import XLIFF

Choose your translated file:

perl
Copy code
my-course-es.xlf
Rise will create a fully translated version of the course.

Troubleshooting
“python is not recognized”
Python isn’t on PATH.
Reinstall and check Add Python to PATH,
or use py (Windows) or python3 (macOS).

Rise refuses to import the file
Check:

You didn’t alter the XML manually

CSV was saved as UTF-8

leading_ws and trailing_ws columns are intact

You extracted and merged using the same source XLF

Weird formatting inside inline HTML
Check those specific rows.
Inline formatting often splits into multiple segments — adjust the translation manually if needed.

Multiple Languages
You can run the script repeatedly:

bash
Copy code
# Spanish
python rise_xlf_extract_merge.py extract my-course-en.xlf segments_es.csv
# translate → segments_es_translated.csv
python rise_xlf_extract_merge.py merge my-course-en.xlf segments_es_translated.csv my-course-es.xlf
Repeat for any language.
