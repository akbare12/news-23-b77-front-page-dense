#!/usr/bin/env python3
"""news-23 b77 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    return 1


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not outdir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    outdir_abs = os.path.abspath(outdir)
    repo = os.path.abspath(os.path.dirname(__file__))
    if outdir_abs == repo or outdir_abs.startswith(repo + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if not os.path.isfile(SRC):
        return fail(f"entry.png not found next to main.py: {SRC}")
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) > 1024 * 1024:
        return fail(f"entry.png is {len(data)} bytes (> 1 MiB)")
    # Parse PNG header manually (struct): signature + IHDR.
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("not a PNG file")
    if len(data) < 33 or data[12:16] != b"IHDR":
        return fail("missing IHDR chunk")
    width, height, depth, ctype = struct.unpack(">IIBB", data[16:26])
    if (width, height) != (1024, 1024):
        return fail(f"expected 1024x1024, got {width}x{height}")
    if depth != 8 or ctype not in (2, 6):
        return fail(f"unexpected bit depth {depth} / colour type {ctype}")
    # IHDR CRC check.
    crc_stored = struct.unpack(">I", data[29:33])[0]
    import binascii
    if binascii.crc32(data[12:29]) & 0xFFFFFFFF != crc_stored:
        return fail("IHDR CRC mismatch")
    # Must contain at least one IDAT chunk and a well-formed IEND trailer.
    # Walk the chunk list to confirm the final chunk really is IEND (len 0,
    # correct CRC) instead of trusting a fixed byte suffix.
    if b"IDAT" not in data:
        return fail("no IDAT chunk found")
    pos = 8
    last_type = None
    while pos + 8 <= len(data):
        (clen,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + clen > len(data):
            return fail("truncated PNG chunk")
        crc_stored = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0]
        if binascii.crc32(data[pos + 4:pos + 8 + clen]) & 0xFFFFFFFF != crc_stored:
            return fail(f"CRC mismatch in {ctype!r} chunk")
        last_type = ctype
        pos += 12 + clen
        if ctype == b"IEND":
            break
    if last_type != b"IEND" or pos != len(data):
        return fail("missing or malformed IEND trailer")
    os.makedirs(outdir_abs, exist_ok=True)
    dst = os.path.join(outdir_abs, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        return fail("output differs from source (not byte-identical)")
    print(f"wrote {dst} ({len(data)} bytes)")
    print(f"sha256 {hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
