# Complete 3D Image and Video Workflow Guide

This guide demonstrates how to use ComfyUI to convert single images into 3D models, view them from different angles, and create videos with person modifications.

## Overview

ComfyUI now provides complete workflows for:

1. **Image to 3D Conversion**: Transform any image into a 3D model
2. **Multi-Angle Viewing**: View 3D models from different camera angles
3. **3D Video Creation**: Generate rotating videos from 3D models
4. **Person Modification**: Replace faces and modify people in videos
5. **Complete Pipeline**: End-to-end workflow combining all features

## Quick Start

### 1. Basic Image to 3D Conversion

**What you need:**
- A source image (preferably with clear subject)
- Tripo API key (optional, for enhanced 3D generation)

**Steps:**
1. Load the `image_to_3d_multiangle.json` workflow
2. Replace the input image with your photo
3. Run the workflow
4. View the 3D model from multiple angles

**Result:** 3D model viewable from 4 different camera angles

### 2. Create Rotating Video from Image

**What you need:**
- A source image
- Desired video duration and quality settings

**Steps:**
1. Load the `image_to_3d_video.json` workflow
2. Set your source image
3. Adjust camera motion (Clockwise, Pan Left, Zoom, etc.)
4. Set frame count and quality
5. Run the workflow

**Result:** MP4 and WEBM videos showing 360° rotation of your 3D model

### 3. Video Face Replacement

**What you need:**
- Source video file
- Reference face image

**Steps:**
1. Load the `video_face_replacement.json` workflow
2. Set your input video and reference face
3. Run the workflow

**Result:** Video with faces replaced throughout all frames

### 4. Advanced Person Modification

**What you need:**
- Source video
- Reference images for faces/features
- Modification descriptions

**Steps:**
1. Load the `video_person_editing.json` workflow
2. Configure face, clothing, and hair modifications
3. Set temporal stabilization settings
4. Run the workflow

**Result:** Video with comprehensive person modifications

### 5. Complete 3D to Video Pipeline

**What you need:**
- Source image or 3D model
- Person reference (optional)
- Output preferences

**Steps:**
1. Load the `complete_3d_video_pipeline.json` workflow
2. Set all input parameters
3. Run the complete pipeline

**Result:** Professional-quality video with 3D conversion and person modifications

## Detailed Workflow Explanations

### Image to 3D Multi-Angle Workflow

This workflow converts a single image to a 3D model and renders it from multiple camera angles:

```
Image Input → 3D Generation → Camera Trajectories → Multi-Angle Preview
```

**Key Nodes:**
- `LoadImage`: Input your source image
- `TripoImageToModelNode`: Generates 3D model from image
- `WanCameraEmbedding` (x4): Creates different camera angles
- `Preview3D` (x4): Shows rendered views

**Camera Angles:**
- Pan Left: Side view from left
- Pan Right: Side view from right  
- Clockwise: Rotating view
- Zoom In: Close-up view

### 3D Video Creation Workflow

This workflow creates smooth video animations from 3D models:

```
Image → 3D Model → Camera Animation → Frame Rendering → Video Export
```

**Key Parameters:**
- **Camera Motion**: ClockWise, Anti-ClockWise, Pan movements, Zoom
- **Frame Count**: Number of frames (affects video length)
- **Speed**: Animation speed multiplier
- **Quality**: Resolution and compression settings

### Video Person Modification Workflow

This workflow provides comprehensive person editing in videos:

```
Video Input → Face Detection → Person Segmentation → Modifications → Stabilization → Output
```

**Modification Types:**
- **Face Replacement**: Swap faces with reference image
- **Clothing Changes**: Modify outfits using text descriptions
- **Hair Modifications**: Change hair color and style
- **Temporal Stabilization**: Smooth frame-to-frame consistency

### Complete Pipeline Workflow

The most comprehensive workflow combining all features:

```
Input → 3D Generation → Camera Animation → Person Modification → Multi-Format Output
```

**Features:**
- Automatic quality scaling
- Multiple output formats (MP4, WEBM)
- Preview frame generation
- Error handling and fallbacks

## Advanced Configuration

### Camera Trajectory Options

The camera system supports these movements:

- **Static**: No movement
- **Pan Up/Down/Left/Right**: Linear camera movements
- **Zoom In/Out**: Forward/backward movement
- **Clockwise/Anti-Clockwise**: Rotation around subject
- **Custom**: Define your own camera path

### Quality Settings

Three quality presets are available:

| Setting | Resolution | Frame Rate | Quality | Use Case |
|---------|------------|------------|---------|----------|
| Draft   | 512x512    | 24 FPS     | Fast    | Testing  |
| Medium  | 1024x1024  | 30 FPS     | Good    | Preview  |
| High    | 2048x2048  | 30 FPS     | Best    | Final    |

### Person Modification Options

**Face Replacement:**
- Automatic face detection and alignment
- Expression preservation
- Lighting consistency
- Multi-face support

**Clothing Modification:**
- Text-based clothing descriptions
- Style transfer capabilities
- Temporal consistency across frames
- Custom reference images

**Hair Modification:**
- Color changes (blonde, brunette, black, red, etc.)
- Style modifications (length, texture)
- Natural lighting preservation
- Custom text descriptions

## Tips and Best Practices

### For Best 3D Results:
1. Use images with clear, well-lit subjects
2. Avoid cluttered backgrounds
3. Ensure the subject faces forward
4. Higher resolution inputs produce better 3D models

### For Video Quality:
1. Use temporal stabilization for smooth results
2. Keep modification prompts specific but not overly complex
3. Test with draft quality first, then increase for final output
4. Consider video length vs. processing time

### For Person Modification:
1. Use high-quality reference images for face replacement
2. Match lighting conditions between source and reference
3. Keep clothing descriptions realistic and detailed
4. Use stabilization strength 0.3-0.5 for most cases

## Troubleshooting

### Common Issues:

**3D Generation Fails:**
- Check Tripo API key configuration
- Verify image format and size
- Try simpler images first

**Video Output Problems:**
- Ensure adequate disk space
- Check video codec support
- Reduce quality settings if needed

**Person Modification Issues:**
- Verify face detection works on input
- Use clearer reference images
- Adjust modification strength

**Performance Optimization:**
- Use draft quality for testing
- Reduce frame count for faster processing
- Close other applications during processing

## API Integration

For programmatic access, these workflows can be triggered via the ComfyUI API:

```python
import json
import requests

# Load workflow
with open('complete_3d_video_pipeline.json', 'r') as f:
    workflow = json.load(f)

# Modify parameters
workflow["1"]["inputs"]["image"] = "your_image.jpg"
workflow["5"]["inputs"]["person_reference"] = "reference_face.jpg"

# Submit to ComfyUI
response = requests.post(
    "http://localhost:8188/prompt",
    json={"prompt": workflow}
)
```

## File Organization

Organize your files as follows:

```
ComfyUI/
├── input/
│   ├── images/           # Source images
│   ├── videos/           # Source videos  
│   └── 3d/              # 3D model files
├── output/
│   ├── videos/          # Generated videos
│   └── images/          # Preview frames
└── workflow_examples/   # Workflow JSON files
```

## Next Steps

1. **Experiment** with different camera movements and quality settings
2. **Customize** workflows for your specific needs
3. **Combine** multiple workflows for complex projects
4. **Optimize** settings for your hardware capabilities

For advanced users, consider:
- Creating custom camera trajectories
- Developing specialized person modification prompts
- Integrating with external 3D modeling tools
- Building automated batch processing systems