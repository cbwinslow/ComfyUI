import os
from typing import List, Tuple

try:
    import face_recognition
except Exception:
    face_recognition = None
from PIL import Image
import numpy as np

class FaceGrouping:
    """Group images by detected faces."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", {"forceInput": True}),
                "distance_threshold": ("FLOAT", {"default": 0.6, "min": 0.1, "max": 1.0, "step": 0.05})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "group"
    CATEGORY = "Face"

    def group(self, images: List[Image.Image], distance_threshold: float) -> Tuple[str]:
        if face_recognition is None:
            raise RuntimeError("face_recognition package not installed")
        groups = {}
        encodings = []
        for idx, img in enumerate(images):
            arr = np.array(img.convert("RGB"))
            enc = face_recognition.face_encodings(arr)
            if not enc:
                continue
            encodings.append((idx, enc[0]))
        for idx, encoding in encodings:
            placed = False
            for gid, group in groups.items():
                if any(face_recognition.face_distance([e], encoding)[0] < distance_threshold for e in group['encodings']):
                    group['indices'].append(idx)
                    group['encodings'].append(encoding)
                    placed = True
                    break
            if not placed:
                gid = len(groups)
                groups[gid] = {'indices': [idx], 'encodings': [encoding]}
        result = {gid: g['indices'] for gid, g in groups.items()}
        return (str(result),)

NODE_CLASS_MAPPINGS = {
    "FaceGrouping": FaceGrouping,
}
