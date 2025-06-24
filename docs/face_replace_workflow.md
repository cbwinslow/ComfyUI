# Replacing Faces with ComfyUI

This guide describes how to use masks to replace a person's face with another in both images and video frames.

## Overview
1. Load your footage or image sequence.
2. Detect face regions and create masks.
3. Insert a new face using blending or inpainting nodes.
4. For videos, process each frame and reassemble.

## Steps

### 1. Load Images or Video Frames
Use **Video Load** or a script to split your video into individual frames. For a single image, use **Load Image**.

### 2. Detect Faces and Create Masks
Apply a face detection node (such as **Mediapipe Face Detection**) to each frame. Convert detection boxes into masks using **Crop Face** followed by **Set Mask**. You can refine these masks manually with **Image Composite** if needed.

### 3. Insert a New Face
Load the source face image with **Load Image**. Align it using **Transform Image** so it matches the target mask. Blend the new face into the frame with **Image Composite** or run an **Inpainting** workflow conditioned on the mask and the source face.

### 4. Save or Reassemble Video
For images, save with **Save Image**. For video, export each edited frame and use a video encoder (e.g., `ffmpeg`) outside ComfyUI to reassemble them.

## Tips
- Keep mask edges soft to avoid harsh transitions between the new face and the original frame.
- Batch processing nodes can speed up handling many frames.
- Consistent lighting between source and target faces yields better results.
