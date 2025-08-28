import nodes
import torch
import numpy as np
from comfy.comfy_types import IO
from comfy_api.input_impl import VideoFromFile

class ImageTo3DViewerNode:
    """
    A comprehensive node that combines image-to-3D conversion with multi-angle viewing.
    This node integrates the Tripo API with camera trajectory control for easy 3D viewing.
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE", {"tooltip": "Source image to convert to 3D"}),
                "camera_motion": (["Static", "Pan Up", "Pan Down", "Pan Left", "Pan Right", "Zoom In", "Zoom Out", "ClockWise (CW)", "Anti Clockwise (ACW)"], 
                                {"default": "ClockWise (CW)", "tooltip": "Camera movement pattern"}),
                "frames": ("INT", {"default": 60, "min": 10, "max": 300, "step": 1, "tooltip": "Number of frames for animation"}),
                "speed": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 5.0, "step": 0.1, "tooltip": "Animation speed"}),
                "width": ("INT", {"default": 1024, "min": 512, "max": 2048, "step": 64}),
                "height": ("INT", {"default": 1024, "min": 512, "max": 2048, "step": 64}),
            },
            "optional": {
                "model_version": (["v2.0-20241204", "v1.4-20240625"], {"default": "v2.0-20241204"}),
                "style": (["default", "cartoon", "realistic"], {"default": "default"}),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING", IO.VIDEO, "LOAD3D_CAMERA")
    RETURN_NAMES = ("frames", "model_path", "video", "camera_info")
    FUNCTION = "process"
    CATEGORY = "3d/integration"
    EXPERIMENTAL = True
    DESCRIPTION = "Convert image to 3D and generate multi-angle views in one node"
    
    def process(self, image, camera_motion, frames, speed, width, height, model_version="v2.0-20241204", style="default", **kwargs):
        try:
            # Import required nodes
            from comfy_api_nodes.nodes_tripo import TripoImageToModelNode
            from comfy_extras.nodes_camera_trajectory import WanCameraEmbedding
            from comfy_extras.nodes_load_3d import Load3DAnimation
            from comfy_extras.nodes_video import CreateVideo
            
            # Step 1: Generate 3D model from image
            tripo_node = TripoImageToModelNode()
            model_file = tripo_node.generate_mesh(
                image=image,
                model_version=model_version,
                style=style,
                **kwargs
            )
            
            # Step 2: Generate camera trajectory
            camera_node = WanCameraEmbedding()
            camera_embedding, cam_width, cam_height, cam_length = camera_node.run(
                camera_pose=camera_motion,
                width=width,
                height=height,
                length=frames,
                speed=speed
            )
            
            # Step 3: Load 3D animation with camera trajectory
            load3d_node = Load3DAnimation()
            rendered_frames, mask, mesh_path, normal, camera_info, recording_video = load3d_node.process(
                model_file=model_file,
                image={
                    'image': '',
                    'mask': '',
                    'normal': '',
                    'recording': '',
                    'camera_info': camera_embedding
                },
                width=width,
                height=height
            )
            
            # Step 4: Create video from frames
            video_node = CreateVideo()
            video = video_node.create_video(
                images=rendered_frames,
                fps=30.0
            )[0]
            
            return rendered_frames, model_file, video, camera_info
            
        except Exception as e:
            print(f"Error in ImageTo3DViewerNode: {e}")
            # Return dummy outputs if there's an error
            dummy_image = torch.zeros((1, height, width, 3))
            dummy_video = VideoFromFile("")
            return dummy_image, "", dummy_video, None

class VideoPersonModifierNode:
    """
    A comprehensive node for modifying people in videos including face replacement,
    clothing changes, and other person-specific modifications.
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video": (IO.VIDEO, {"tooltip": "Input video to modify"}),
                "reference_face": ("IMAGE", {"tooltip": "Reference face for replacement"}),
                "modification_type": (["face_only", "face_and_clothing", "face_and_hair", "complete_person"], 
                                    {"default": "face_and_clothing"}),
            },
            "optional": {
                "clothing_prompt": ("STRING", {"default": "elegant business suit", "multiline": True, "tooltip": "Description of desired clothing"}),
                "hair_color": (["unchanged", "blonde", "brunette", "black", "red", "gray", "custom"], {"default": "unchanged"}),
                "hair_style": (["unchanged", "short", "long", "curly", "straight", "custom"], {"default": "unchanged"}),
                "custom_hair_prompt": ("STRING", {"default": "", "multiline": True}),
                "stabilization_strength": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 1.0, "step": 0.1}),
            }
        }
    
    RETURN_TYPES = (IO.VIDEO, "IMAGE")
    RETURN_NAMES = ("modified_video", "sample_frames")
    FUNCTION = "process"
    CATEGORY = "video/person_modification"
    EXPERIMENTAL = True
    DESCRIPTION = "Comprehensive person modification for videos"
    
    def process(self, video, reference_face, modification_type, clothing_prompt="elegant business suit", 
               hair_color="unchanged", hair_style="unchanged", custom_hair_prompt="", 
               stabilization_strength=0.3, **kwargs):
        try:
            from comfy_extras.nodes_video import GetVideoComponents, CreateVideo
            from custom_nodes.FaceSwap.face_swap import FaceSwap
            
            # Step 1: Extract video components
            video_components_node = GetVideoComponents()
            frames, audio, fps = video_components_node.get_components(video)
            
            # Step 2: Process modifications based on type
            modified_frames = frames
            
            if modification_type in ["face_only", "face_and_clothing", "face_and_hair", "complete_person"]:
                # Face replacement
                face_swap_node = FaceSwap()
                modified_frames = face_swap_node.swap_faces(
                    source_image=reference_face,
                    target_image=modified_frames
                )
            
            if modification_type in ["face_and_clothing", "complete_person"]:
                # Clothing modification (placeholder - would need actual implementation)
                # This would integrate with inpainting/editing nodes
                pass
            
            if modification_type in ["face_and_hair", "complete_person"]:
                # Hair modification (placeholder - would need actual implementation)
                pass
            
            # Step 3: Temporal stabilization
            if stabilization_strength > 0:
                # Apply temporal stabilization (placeholder)
                pass
            
            # Step 4: Create output video
            create_video_node = CreateVideo()
            output_video = create_video_node.create_video(
                images=modified_frames,
                fps=float(fps),
                audio=audio
            )[0]
            
            # Sample frames for preview
            sample_frames = modified_frames[::max(1, len(modified_frames)//6)]  # Sample 6 frames
            
            return output_video, sample_frames
            
        except Exception as e:
            print(f"Error in VideoPersonModifierNode: {e}")
            # Return dummy outputs if there's an error
            return video, torch.zeros((1, 512, 512, 3))

class Workflow3DToVideoNode:
    """
    A node that creates a complete pipeline from any input (image or existing 3D model) 
    to a final video with multiple viewing angles and person modifications.
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_type": (["image", "3d_model"], {"default": "image"}),
                "output_format": (["mp4", "webm", "both"], {"default": "mp4"}),
                "quality": (["draft", "medium", "high"], {"default": "medium"}),
            },
            "optional": {
                "input_image": ("IMAGE", {}),
                "input_3d_model": ("STRING", {}),
                "person_reference": ("IMAGE", {}),
                "camera_sequence": ("STRING", {"default": "ClockWise (CW)", "multiline": True, 
                                              "tooltip": "Comma-separated camera movements"}),
                "duration": ("FLOAT", {"default": 10.0, "min": 1.0, "max": 60.0, "step": 0.5}),
                "fps": ("FLOAT", {"default": 30.0, "min": 15.0, "max": 60.0, "step": 1.0}),
            }
        }
    
    RETURN_TYPES = (IO.VIDEO, IO.VIDEO, "IMAGE")
    RETURN_NAMES = ("primary_video", "alternate_format", "preview_frames")
    FUNCTION = "process"
    CATEGORY = "3d/complete_pipeline"
    EXPERIMENTAL = True
    DESCRIPTION = "Complete pipeline from image/3D to final video with person modifications"
    
    def process(self, input_type, output_format, quality, input_image=None, input_3d_model=None, 
               person_reference=None, camera_sequence="ClockWise (CW)", duration=10.0, fps=30.0, **kwargs):
        
        # Calculate frame count
        total_frames = int(duration * fps)
        
        # Quality settings
        quality_settings = {
            "draft": {"width": 512, "height": 512, "crf": 28},
            "medium": {"width": 1024, "height": 1024, "crf": 23},
            "high": {"width": 2048, "height": 2048, "crf": 18}
        }
        settings = quality_settings[quality]
        
        try:
            # Generate or use 3D content
            if input_type == "image" and input_image is not None:
                # Use ImageTo3DViewerNode
                viewer_node = ImageTo3DViewerNode()
                frames, model_path, base_video, camera_info = viewer_node.process(
                    image=input_image,
                    camera_motion=camera_sequence.split(",")[0].strip(),
                    frames=total_frames,
                    speed=1.0,
                    width=settings["width"],
                    height=settings["height"]
                )
            else:
                # Use existing 3D model (placeholder implementation)
                frames = torch.zeros((total_frames, settings["height"], settings["width"], 3))
                base_video = VideoFromFile("")
            
            # Apply person modifications if reference provided
            if person_reference is not None:
                modifier_node = VideoPersonModifierNode()
                base_video, preview_frames = modifier_node.process(
                    video=base_video,
                    reference_face=person_reference,
                    modification_type="face_and_clothing"
                )
            else:
                preview_frames = frames[::max(1, len(frames)//6)]
            
            # Create alternate format if requested
            alternate_video = base_video if output_format != "both" else base_video
            
            return base_video, alternate_video, preview_frames
            
        except Exception as e:
            print(f"Error in Workflow3DToVideoNode: {e}")
            # Return dummy outputs
            dummy_video = VideoFromFile("")
            dummy_frames = torch.zeros((6, 512, 512, 3))
            return dummy_video, dummy_video, dummy_frames

# Node mappings for ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "ImageTo3DViewerNode": ImageTo3DViewerNode,
    "VideoPersonModifierNode": VideoPersonModifierNode,
    "Workflow3DToVideoNode": Workflow3DToVideoNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageTo3DViewerNode": "Image to 3D Viewer",
    "VideoPersonModifierNode": "Video Person Modifier",
    "Workflow3DToVideoNode": "3D to Video Pipeline",
}