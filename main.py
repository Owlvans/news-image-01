#!/usr/bin/env python3
import os
import sys
import hashlib
import struct

ENTRY_TITLE = "The World in One Day"
EXPECTED_SHA256 = "145565a7619c95bef526a015f32ceb178de49e685cba83b47618a67fe35a4be5"
EXPECTED_BYTES = 265005

def parse_jpeg_dims(data: bytes):
    if not data.startswith(b'\xff\xd8') or not data.endswith(b'\xff\xd9'):
        raise ValueError("Invalid JPEG start/end markers")
    i = 2
    while i < len(data) - 1:
        if data[i] != 0xff:
            i += 1
            continue
        # skip padding 0xff bytes
        while i < len(data) and data[i] == 0xff:
            i += 1
        if i >= len(data):
            break
        marker = data[i]
        i += 1
        # Standalone markers without length
        if marker in (0xd8, 0xd9, 0x01) or (0xd0 <= marker <= 0xd7):
            continue
        if i + 2 > len(data):
            break
        length = struct.unpack('>H', data[i:i+2])[0]
        # SOF0 through SOF3 (0xc0 to 0xc3) and SOF5 through SOF7 (0xc5 to 0xc7), SOF9 through SOF11 (0xc9 to 0xcb)
        if marker in (0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb):
            if i + length >= len(data):
                raise ValueError("Invalid JPEG SOF length")
            # payload starts after length (2 bytes)
            # precision (1), height (2), width (2)
            if length < 7:
                raise ValueError("Invalid SOF segment length")
            height = struct.unpack('>H', data[i+3:i+5])[0]
            width = struct.unpack('>H', data[i+5:i+7])[0]
            return width, height
        i += length
    raise ValueError("JPEG SOF segment not found")

def parse_png_dims(data: bytes):
    png_sig = b'\x89PNG\r\n\x1a\n'
    if not data.startswith(png_sig):
        raise ValueError("Invalid PNG signature")
    if not data.endswith(b'IEND\xaeB`\x82'):
        # Check general IEND presence near end or exact chunk
        if b'IEND' not in data[-12:]:
            raise ValueError("Invalid PNG IEND marker")
    # IHDR is expected at offset 8 (length 4, type 'IHDR' 4, width 4, height 4)
    if len(data) < 24 or data[12:16] != b'IHDR':
        raise ValueError("PNG IHDR chunk not found at start")
    width, height = struct.unpack('>II', data[16:24])
    return width, height

def validate_and_process():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    news_path = os.path.join(script_dir, "news.jpg")
    
    if not os.path.exists(news_path):
        print(f"Error: news.jpg not found at {news_path}", file=sys.stderr)
        sys.exit(1)
        
    file_size = os.path.getsize(news_path)
    if file_size > 1048576:
        print(f"Error: file size {file_size} exceeds maximum allowed 1048576 bytes", file=sys.stderr)
        sys.exit(1)
        
    if file_size != EXPECTED_BYTES:
        print(f"Error: file size {file_size} does not match expected {EXPECTED_BYTES} bytes", file=sys.stderr)
        sys.exit(1)
        
    with open(news_path, "rb") as f:
        data = f.read()
        
    actual_sha256 = hashlib.sha256(data).hexdigest()
    if actual_sha256 != EXPECTED_SHA256:
        print(f"Error: sha256 mismatch: {actual_sha256} != {EXPECTED_SHA256}", file=sys.stderr)
        sys.exit(1)
        
    # Determine image format and dimensions
    try:
        width, height = parse_jpeg_dims(data)
    except Exception as e_jpeg:
        try:
            width, height = parse_png_dims(data)
        except Exception as e_png:
            print(f"Error: failed to parse image dimensions as JPEG or PNG. JPEG err: {e_jpeg}, PNG err: {e_png}", file=sys.stderr)
            sys.exit(1)
            
    if width > 1024 or height > 1024:
        print(f"Error: image dimensions {width}x{height} exceed maximum 1024x1024", file=sys.stderr)
        sys.exit(1)
        
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "entry.png")
    
    with open(output_path, "wb") as f:
        f.write(data)
        
    with open(output_path, "rb") as f:
        written_data = f.read()
    written_sha256 = hashlib.sha256(written_data).hexdigest()
    if written_sha256 != actual_sha256:
        print(f"Error: written output sha256 mismatch: {written_sha256} != {actual_sha256}", file=sys.stderr)
        sys.exit(1)
    print("Output verified successfully: written entry.png matches source sha256.")
        
    print(f"{ENTRY_TITLE}: {width}x{height}, {file_size} bytes, sha256 {actual_sha256}")

if __name__ == "__main__":
    validate_and_process()
