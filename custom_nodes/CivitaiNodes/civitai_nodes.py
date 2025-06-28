import os
import requests
from typing import Tuple

try:
    from civitai import models as civitai_models
except Exception as e:
    civitai_models = None

class CivitaiModelDownloader:
    """Download models from Civitai by query."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "query": ("STRING", {"default": ""}),
                "save_directory": ("STRING", {"default": "models"})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "download"
    CATEGORY = "Civitai"

    def download(self, query: str, save_directory: str) -> Tuple[str]:
        if civitai_models is None:
            raise RuntimeError("civitai package not installed")
        resp = civitai_models.get(limit=1, query=query)
        if not resp.items:
            raise RuntimeError("No models found for query")
        model = resp.items[0]
        version = model.modelVersions[0]
        url = version.downloadUrl
        os.makedirs(save_directory, exist_ok=True)
        filename = os.path.join(save_directory, os.path.basename(url))
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        return (filename,)

NODE_CLASS_MAPPINGS = {
    "CivitaiModelDownloader": CivitaiModelDownloader,
}
