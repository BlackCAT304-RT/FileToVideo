# FileToVideo

> Encode any file into a video. Store it anywhere. Decode it back.

FileToVideo converts arbitrary binary files into color-coded MP4 videos using a 16-color block encoding scheme. The video can be uploaded to platforms like YouTube and later decoded back to the original file — perfectly intact.

---

## How it works

Each byte of the input file is split into 4-bit nibbles. Each nibble maps to one of 16 distinct colors, which are painted as blocks onto video frames at **1920×1080 @ 6 FPS**. Corner markers anchor the grid so decoding is robust even after re-encoding or slight resolution changes. An optional XOR encryption key can scramble the data before encoding.

```
File → bytes → 4-bit blocks → color grid → MP4 frames → video
Video → frames → color grid → 4-bit blocks → bytes → File
```

---

## Features

- 🎨 16-color block encoding with redundant regions per frame
- 🔐 Optional XOR encryption via key file (`key.txt`) or manual input
- 🎬 FFmpeg output (falls back to OpenCV if FFmpeg is not available)
- 🖥️ Clean GUI — encode, decode, settings tabs
- 🌍 12 interface languages (EN, RU, UK, DE, FR, ES, PL, PT, IT, ZH, JA, KO)
- 📋 Built-in console showing all operation output
- ✅ EOF marker + 5 guard frames for reliable decoding

---

## Requirements

```
pip install opencv-python numpy
```

Python 3.8+ required. FFmpeg is optional but recommended for better compression.

---

## Usage

Run the GUI:

```bash
python FileToVideo.py
```

### Encode tab
1. Select the input file
2. Choose output MP4 path (auto-filled)
3. Optionally enter an encryption key
4. Click **Start Encoding**

### Decode tab
1. Select the encoded MP4 video
2. Choose output folder
3. Enter the same encryption key (if used)
4. Click **Start Decoding**

### Encryption
Create a `key.txt` file next to the script with your key, or load any `.txt` file via the **Load key.txt** button. Leave the key field empty to disable encryption.

---

## File structure

```
FileToVideo.py      — main application
key.txt             — (optional) encryption key
DATA/
  ico.ico           — application icon
```

---

## Credits

Original encoding/decoding logic by **KorocheVolgin**
→ https://github.com/KorocheVolgin/YouTube-Cloude/

UI and additional features by **BlackCAT304**
→ https://github.com/BlackCAT304-RT/FileToVideo
