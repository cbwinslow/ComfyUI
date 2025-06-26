#!/usr/bin/env python3
"""Swap faces in a video using the FaceSwap node."""

import argparse
import cv2
from PIL import Image
import numpy as np
from custom_nodes.face_swap import FaceSwap


def pil_to_cv(img: Image.Image):
    return cv2.cvtColor(np.array(img.convert("RGB")), cv2.COLOR_RGB2BGR)


def cv_to_pil(arr):
    return Image.fromarray(cv2.cvtColor(arr, cv2.COLOR_BGR2RGB))


def main():
    parser = argparse.ArgumentParser(description="Swap faces in a video")
    parser.add_argument("video", help="input video path")
    parser.add_argument("source_face", help="image containing face to insert")
    parser.add_argument("output", help="output video path")
    args = parser.parse_args()

    source_img = Image.open(args.source_face)
    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        raise SystemExit("Could not open video")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(args.output, fourcc, fps, (width, height))

    node = FaceSwap()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_pil = cv_to_pil(frame)
        swapped_pil = node.swap(source_img, frame_pil)[0]
        out.write(pil_to_cv(swapped_pil))

    cap.release()
    out.release()


if __name__ == "__main__":
    main()
