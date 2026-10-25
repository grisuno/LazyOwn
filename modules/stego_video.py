#!/usr/bin/env python3
"""Video steganography addon for LazyOwn.

Hides a ZIP archive inside a video file (encode) and extracts it back (decode).

A silent carrier video is generated with ffmpeg. The ZIP is appended after the
video payload, followed by an 8-byte little-endian size trailer so the decoder
locates the hidden archive without parsing the video container.
"""

import json
import os
import struct
import subprocess
import sys

PAYLOAD_PATH = "payload.json"
VIDEO_EXTENSIONS = (".mp4", ".avi", ".mkv", ".mov")
CARRIER_DURATION = 5
CARRIER_SIZE = "640x480"
CARRIER_RATE = 30
AUDIO_FREQUENCY = 440
TRAILER_SIZE = 8


def load_payload_file():
    """Return the ``file`` value from payload.json, or None."""
    try:
        with open(PAYLOAD_PATH, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data.get("file")
    except Exception:
        return None


def is_zip(path):
    return bool(path) and os.path.isfile(path) and path.lower().endswith(".zip")


def is_video(path):
    return bool(path) and os.path.isfile(path) and path.lower().endswith(VIDEO_EXTENSIONS)


def prompt_path(message):
    while True:
        path = input(message).strip()
        if path:
            return path
        print("Error: path cannot be empty.")


def resolve_path(arg_path, payload_file, validator, kind):
    """Resolve the target path using argument -> payload.json -> interactive prompt."""
    if arg_path and validator(arg_path):
        return arg_path
    if payload_file and validator(payload_file):
        return payload_file
    return prompt_path("Enter path to the %s: " % kind)


def generate_carrier(output):
    """Generate a silent carrier video with ffmpeg."""
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", "testsrc=duration=%d:size=%s:rate=%d"
        % (CARRIER_DURATION, CARRIER_SIZE, CARRIER_RATE),
        "-f", "lavfi", "-i", "sine=frequency=%d:duration=%d"
        % (AUDIO_FREQUENCY, CARRIER_DURATION),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
        "-movflags", "faststart", "-shortest", "-y", output,
    ]
    subprocess.run(command, check=True)


def encode(zip_path, output_video):
    """Hide zip_path inside output_video."""
    directory = os.path.dirname(os.path.abspath(output_video)) or "."
    carrier = os.path.join(directory, ".stego_carrier.mp4")
    generate_carrier(carrier)
    with open(carrier, "rb") as handle:
        carrier_data = handle.read()
    with open(zip_path, "rb") as handle:
        zip_data = handle.read()
    trailer = struct.pack("<Q", len(zip_data))
    with open(output_video, "wb") as handle:
        handle.write(carrier_data)
        handle.write(zip_data)
        handle.write(trailer)
    os.remove(carrier)
    return output_video


def decode(stego_video, output_zip):
    """Extract the hidden zip from stego_video into output_zip."""
    with open(stego_video, "rb") as handle:
        handle.seek(0, os.SEEK_END)
        size = handle.tell()
        if size < TRAILER_SIZE:
            raise ValueError("File too small to contain a hidden zip.")
        handle.seek(size - TRAILER_SIZE)
        trailer = handle.read(TRAILER_SIZE)
    zip_size = struct.unpack("<Q", trailer)[0]
    if zip_size == 0 or zip_size > size - TRAILER_SIZE:
        raise ValueError("No hidden zip found in the video file.")
    with open(stego_video, "rb") as handle:
        handle.seek(size - TRAILER_SIZE - zip_size)
        zip_data = handle.read(zip_size)
    with open(output_zip, "wb") as handle:
        handle.write(zip_data)
    return output_zip


def default_output(zip_path):
    base = os.path.splitext(os.path.basename(zip_path))[0]
    return base + ".stego.mp4"


def main(argv):
    if len(argv) < 2:
        print("Usage: stego_video.py <encode|decode> [path]")
        return 1
    mode = argv[1].lower()
    arg_path = argv[2] if len(argv) > 2 else None
    payload_file = load_payload_file()

    if mode == "encode":
        zip_path = resolve_path(arg_path, payload_file, is_zip, "zip file")
        if not is_zip(zip_path):
            print("Error: selected file is not a zip.")
            return 1
        output_video = default_output(zip_path)
        print("Encoding %s into %s ..." % (zip_path, output_video))
        encode(zip_path, output_video)
        print("Done: %s" % output_video)
    elif mode == "decode":
        video_path = resolve_path(arg_path, payload_file, is_video, "video file")
        if not is_video(video_path):
            print("Error: selected file is not a video.")
            return 1
        output_zip = prompt_path("Enter output zip path [recovered.zip]: ") or "recovered.zip"
        print("Decoding %s into %s ..." % (video_path, output_zip))
        decode(video_path, output_zip)
        print("Done: %s" % output_zip)
    else:
        print("Error: mode must be 'encode' or 'decode'.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
