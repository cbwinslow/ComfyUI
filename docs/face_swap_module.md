# Face Swap Module

This document describes the `FaceSwap` custom node and the helper script for swapping faces in images and videos.

## Node Usage
1. Copy `custom_nodes/face_swap.py` into your `custom_nodes` folder.
2. Restart ComfyUI so it picks up the new node.
3. Use the **FaceSwap** node with a source face image and a target image. The node automatically detects the first face in each image and blends the source face into the target.

## Video Processing
The script `scripts/face_swap_video.py` automates swapping faces in a video:

```bash
python scripts/face_swap_video.py input.mp4 face.jpg output.mp4
```

Each frame is processed with the same logic as the node and written to a new video file.

## Notes
- This implementation relies on OpenCV's Haar cascade face detector and `seamlessClone` for blending.
- Results are best when faces are oriented similarly and well lit.
