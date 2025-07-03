# AppImage Extractor & Shortcut Generator

A utility script powered by AI (with a bit of human supervision) to automate the extraction of `.AppImage` files and generate convenient desktop shortcuts for Linux users.

---

## 🔧 What It Does

This Python script performs the following tasks:

- Scans a specified directory for `.AppImage` files  
- Extracts each AppImage to access its internal files  
- Locates the appropriate application icon  
- Generates `.desktop` entries for launching the apps from your desktop environment  
- Optionally cleans up the extracted files after creating the shortcuts

---

## 📦 How to Use

1. Run the script:
   ```bash
   python3 appimage_extractor.py
````

2. Enter the path to the directory containing your `.AppImage` files when prompted
3. Wait while the script processes, extracts, and creates shortcuts
4. Choose whether to delete the extracted folders afterward
5. Done — your applications should now be accessible via your desktop or application menu

---

## 🖥 Requirements

* Python 3
* A Linux system with a desktop environment that supports `.desktop` files
* (Optional) A default icon file if the script cannot locate one inside the AppImage

---

## 📌 Notes

* The script attempts to automatically detect and assign the correct application icon
* If an icon is not found, it falls back to a default placeholder (you can customize this)
* Extraction is temporary unless you choose to keep the folders for inspection or modification

---

## 🤖 Authorship & Acknowledgment

This script was developed with the help of AI (ChatGPT), guided and refined by human oversight.
It demonstrates how AI tools can simplify routine tasks while offering flexibility for customization.

---

## 📁 Why This Exists

AppImages are a convenient way to distribute portable Linux applications —
but they can be cumbersome to integrate into the desktop environment.
This tool bridges that gap by automating the otherwise manual process of extraction and shortcut creation.

---

