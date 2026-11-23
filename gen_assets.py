"""Generate the ding sound (WAV) and PNG icons using only the Python stdlib.

Run from the extension directory:  python3 gen_assets.py
"""
import math
import struct
import wave
import zlib


def make_ding(path: str) -> None:
    rate = 44100
    duration = 0.9  # seconds
    n = int(rate * duration)

    # A bright two-note chime: C6 then E6, each with a quick decay, so it
    # reads as a cheerful "ding" rather than a flat beep.
    notes = [
        (1046.50, 0.00, 0.5),  # C6 starting at t=0
        (1318.51, 0.10, 0.9),  # E6 starting slightly later
    ]

    samples = [0.0] * n
    for freq, start, decay in notes:
        start_i = int(start * rate)
        for i in range(start_i, n):
            t = (i - start_i) / rate
            env = math.exp(-t / decay)  # exponential decay envelope
            # fundamental + a soft second harmonic for a bell-like tone
            val = (
                math.sin(2 * math.pi * freq * t)
                + 0.25 * math.sin(2 * math.pi * 2 * freq * t)
            )
            samples[i] += 0.5 * env * val

    # Short fade-out at the very end to avoid a click.
    fade = int(0.01 * rate)
    for i in range(n - fade, n):
        samples[i] *= (n - i) / fade

    peak = max(1e-9, max(abs(s) for s in samples))
    frames = bytearray()
    for s in samples:
        v = int(max(-1.0, min(1.0, s / peak * 0.9)) * 32767)
        frames += struct.pack("<h", v)

    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(bytes(frames))


def _png(path: str, size: int) -> None:
    # Draw a simple golden cookie: tan disc with brown chocolate chips.
    cx = cy = (size - 1) / 2
    radius = size * 0.46
    chips = [
        (0.30, 0.32, 0.09),
        (0.68, 0.30, 0.08),
        (0.50, 0.55, 0.10),
        (0.28, 0.66, 0.08),
        (0.72, 0.68, 0.09),
        (0.52, 0.22, 0.06),
    ]

    def px(x, y):
        dx, dy = x - cx, y - cy
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > radius:
            return (0, 0, 0, 0)  # transparent outside the cookie
        # base cookie color with a subtle radial shade
        shade = 1.0 - 0.25 * (dist / radius)
        r, g, b = int(0xD9 * shade), int(0xA4 * shade), int(0x41 * shade)
        for fx, fy, fr in chips:
            ccx, ccy = fx * size, fy * size
            if math.hypot(x - ccx, y - ccy) <= fr * size:
                return (0x5a, 0x33, 0x12, 255)  # chocolate chip
        return (r, g, b, 255)

    raw = bytearray()
    for y in range(size):
        raw.append(0)  # filter byte per scanline
        for x in range(size):
            raw += bytes(px(x, y))

    def chunk(tag, data):
        c = tag + data
        return (
            struct.pack(">I", len(data))
            + c
            + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        )

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    with open(path, "wb") as f:
        f.write(sig)
        f.write(chunk(b"IHDR", ihdr))
        f.write(chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
        f.write(chunk(b"IEND", b""))


if __name__ == "__main__":
    import os

    here = os.path.dirname(os.path.abspath(__file__))
    make_ding(os.path.join(here, "ding.wav"))
    os.makedirs(os.path.join(here, "icons"), exist_ok=True)
    _png(os.path.join(here, "icons", "icon-48.png"), 48)
    _png(os.path.join(here, "icons", "icon-96.png"), 96)
    print("Generated ding.wav and icons.")
