from PIL import Image
import cv2
import numpy as np

class FaceSwap:
    """Simple face swap node using OpenCV."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "source_image": ("IMAGE",),
                "target_image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "swap"
    CATEGORY = "Face"

    def swap(self, source_image, target_image):
        src = self._pil_to_cv(source_image)
        tgt = self._pil_to_cv(target_image)
        swapped = self._swap_faces(src, tgt)
        return (Image.fromarray(cv2.cvtColor(swapped, cv2.COLOR_BGR2RGB)),)

    def _pil_to_cv(self, img: Image.Image):
        arr = np.array(img.convert("RGB"))
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

    def _swap_faces(self, src, tgt):
        detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        tgt_gray = cv2.cvtColor(tgt, cv2.COLOR_BGR2GRAY)
        src_faces = detector.detectMultiScale(src_gray, 1.1, 5)
        tgt_faces = detector.detectMultiScale(tgt_gray, 1.1, 5)
        if len(src_faces) == 0 or len(tgt_faces) == 0:
            return tgt
        sx, sy, sw, sh = src_faces[0]
        tx, ty, tw, th = tgt_faces[0]
        src_face = src[sy:sy+sh, sx:sx+sw]
        src_resized = cv2.resize(src_face, (tw, th))
        mask = 255 * np.ones(src_resized.shape, src_resized.dtype)
        center = (tx + tw // 2, ty + th // 2)
        output = cv2.seamlessClone(src_resized, tgt, mask, center, cv2.NORMAL_CLONE)
        return output
