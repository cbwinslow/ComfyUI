# Workflow Examples

This directory contains complete workflow examples for common use cases in ComfyUI.

## Available Workflows

### 3D Image Generation and Viewing
- **image_to_3d_multiangle.json** - Convert a single image to 3D and view from multiple angles
- **image_to_3d_video.json** - Create a rotating video from a single image via 3D conversion

### Video Person Modification
- **video_face_replacement.json** - Replace faces in video with different people
- **video_person_editing.json** - Edit details about people in videos (clothing, features, etc.)

### Combined Workflows
- **complete_3d_video_pipeline.json** - Full pipeline from image to 3D to modified video

## Usage

1. Load any workflow file into ComfyUI
2. Replace input files with your own images/videos
3. Adjust parameters as needed
4. Run the workflow

## Requirements

Some workflows require:
- Tripo API key for 3D generation
- Face detection models for person modification
- Appropriate input images/videos in the `input/` directory