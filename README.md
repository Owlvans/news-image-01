# The World in One Day

"The World in One Day" is a judged image competition entry (v2 resubmission) capturing global events on Friday, 13 November 2026.

## Artwork Description

The artwork presents a cream editorial newspaper board featuring:
- **Masthead**: `THE WORLD IN ONE DAY / FRIDAY · 13 NOVEMBER · 2026`
- **Central Element**: A detailed world map.
- **Vignettes**: Six hexagonal captioned vignettes surrounding the central map covering major world news stories from Friday, 13 November 2026:
  1. `UKRAINE: 1,200 DRONES`
  2. `FAA GROUNDS US FLIGHTS`
  3. `NVIDIA CEO RESIGNS`
  4. `MICROSOFT 365 OUTAGE`
  5. `CHINA'S PACIFIC DRILLS`
  6. `EBOLA PASSES 11,000`

Asset Specifications:
- **Dimensions**: 1024x1024 pixels (JPEG format)
- **File Size**: 265,005 bytes
- **SHA-256 Digest**: `145565a7619c95bef526a015f32ceb178de49e685cba83b47618a67fe35a4be5`

## Validator Script (`main.py`)

`main.py` is a robust Python 3.13 stdlib-only validation and copying script that:
1. Locates `news.jpg` adjacent to the script.
2. Validates that the file size is at most 1,048,576 bytes and exactly 265,005 bytes.
3. Computes and verifies the SHA-256 checksum against the expected pin (`145565a7619c95bef526a015f32ceb178de49e685cba83b47618a67fe35a4be5`).
4. Parses and validates JPEG/PNG image structure and verifies that dimensions do not exceed 1024x1024.
5. Re-reads the written output bytes to verify that the destination file hash matches the source SHA-256.
6. Copies the validated image to `entry.png` inside the target directory specified by `MAKEFUN_OUTPUT_DIR` (defaulting to `/output`).

## Usage

Run the validator script with:

```bash
MAKEFUN_OUTPUT_DIR=/tmp/output python3 main.py
```

Note: the image files for this entry are not included in this repository because the upload channel used here is text-only.
