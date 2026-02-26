"""
Create app icon (book) for Sticky Notes executable.
Uses Pillow if available, otherwise creates a minimal icon.
"""

import struct
from pathlib import Path


def create_icon_pillow() -> bool:
    """Create icon using Pillow. Returns True if successful."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return False

    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = size // 8
    left, top = margin, margin
    right, bottom = size - margin, size - margin
    mid = size // 2
    spine_w = max(2, size // 24)

    draw.rectangle([left, top, mid - spine_w // 2, bottom], fill="#FFF9C4", outline="#333", width=1)
    draw.rectangle([mid + spine_w // 2, top, right, bottom], fill="#FFF9C4", outline="#333", width=1)
    draw.rectangle([mid - spine_w // 2, top, mid + spine_w // 2, bottom], fill="#E6D96A", outline="#333", width=1)

    for i in range(3):
        y = top + (i + 1) * (bottom - top) // 4
        draw.line([left + 2, y, mid - spine_w // 2 - 2, y], fill="#333", width=1)
        draw.line([mid + spine_w // 2 + 2, y, right - 2, y], fill="#333", width=1)

    img.save("icon.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    return True


def create_icon_minimal() -> None:
    """Create minimal valid ICO file without Pillow - book with spine and page lines."""
    w, h = 48, 48
    m = 5
    left, right = m, w - m - 1
    top, bottom = m, h - m - 1
    mid = w // 2
    spine_left, spine_right = mid - 4, mid + 4  # Wider spine

    def pixel(x: int, y: int) -> tuple[int, int, int]:
        if not (left <= x <= right and top <= y <= bottom):
            return (0, 0, 0)
        if spine_left <= x <= spine_right:
            return (0x6B, 0x5B, 0x2B)  # Darker brown spine
        if x <= left + 1 or x >= right - 1 or y <= top + 1 or y >= bottom - 1:
            return (0x2A, 0x2A, 0x2A)  # Book border
        if x == spine_left - 1 or x == spine_right + 1:
            return (0x4A, 0x3A, 0x1A)  # Spine edge
        r, g, b = 0xFF, 0xF5, 0xB8  # Cream page
        for i in (1, 2, 3, 4):
            ly = top + (bottom - top) * i // 5
            if abs(y - ly) <= 1 and (x < spine_left - 1 or x > spine_right + 1):
                return (0xBB, 0xAA, 0x77)  # Page line
        return (r, g, b)

    # ICO header
    data = bytearray()
    data += struct.pack("<HHH", 0, 1, 1)
    bpp = 32
    row_bytes = ((w * bpp + 31) // 32) * 4
    and_size = ((w + 31) // 32) * 4 * h
    img_size = 40 + h * row_bytes + and_size
    data += struct.pack("<BBBBHHII", w, h, 0, 0, 1, bpp, img_size, 22)
    data += struct.pack("<IIIHHIIIIII", 40, w, h, 1, bpp, 0, 0, 0, 0, 0, 0)
    for y in range(h - 1, -1, -1):
        for x in range(w):
            r, g, b = pixel(x, y)
            a = 255 if (r or g or b) else 0
            data += struct.pack("<BBBB", b, g, r, a)
        data += b"\x00" * (row_bytes - w * 4)
    data += b"\x00" * and_size

    Path("icon.ico").write_bytes(bytes(data))


def main() -> None:
    if create_icon_pillow():
        print("Created icon.ico (book icon)")
    else:
        print("Pillow not available, creating minimal icon...")
        create_icon_minimal()
        print("Created icon.ico (minimal)")


if __name__ == "__main__":
    main()
