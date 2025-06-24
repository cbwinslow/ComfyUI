# Batch Face Blur Workflow

This workflow demonstrates how to detect and blur faces across a folder of images using ComfyUI nodes.

## Overview
1. Load all images in a directory.
2. Detect faces and generate masks.
3. Apply blur to masked regions.
4. Save the processed images.

## Steps

### 1. Load a Folder
Use the **Load Image Sequence** node to read all images from a directory. Each image flows into the pipeline as an individual batch item.

### 2. Detect Faces
Connect **Mediapipe Face Detection** (or any available face detector) to generate bounding boxes. Convert them to masks with **Crop Face** and **Set Mask**.

### 3. Blur Faces
Link each mask to **Gaussian Blur** or **Box Blur** nodes. These nodes blur only the masked areas, leaving the rest of the image unchanged.

### 4. Save Images
Finally, attach **Save Image** to store the blurred results in an output folder.

## Tips
- Adjust blur strength to conceal faces effectively.
- Batch size control nodes help manage memory when processing large folders.
