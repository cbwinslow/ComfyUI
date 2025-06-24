# Painting Masks on People with ComfyUI

This guide explains how to create and refine masks for people in images using ComfyUI.

## Overview
1. Load your source image.
2. Automatically detect the person to create an initial mask.
3. Refine the mask by painting details.
4. Apply inpainting or editing workflows using the refined mask.

## Steps

### 1. Load the Image
Use the **Load Image** node to bring your picture into the workflow. This node outputs both the image and an optional mask from the image's alpha channel.

### 2. Generate an Initial Mask
If you have access to segmentation models (for example, SAM or other custom nodes), use the model's node to create a mask that covers the person. Otherwise, manually draw a rough mask externally and import it with **Load Image (as Mask)**.

### 3. Refine by Painting
Add an **Image Composite** or similar mask-editing node to paint directly on the mask. Use a graphics tablet or mouse to refine edges, ensuring hair and body outlines are crisp.

### 4. Inpaint or Edit
Connect the refined mask to **VAE Encode (for Inpainting)** and build your inpainting or editing workflow. Nodes like **KSampler (Advanced)** and **Inpaint Model Conditioning** allow you to modify only the masked area while preserving the rest of the image.

### 5. Save the Results
Finally, decode the latent with **VAE Decode** and save the edited image using **Save Image**. You can also preview intermediate results with **Preview Image** during the workflow.

## Tips
- Use the **Image Blur** node on the mask to soften edges for smoother blending.
- Combine multiple masks with **Conditioning (Set Mask)** if you need to edit several regions.
- Remember to keep source and mask resolutions consistent to avoid artifacts.

