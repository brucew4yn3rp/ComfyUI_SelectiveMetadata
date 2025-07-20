import os
import json
import numpy as np
from PIL import ExifTags, Image, PngImagePlugin
from comfy.cli_args import args
import folder_paths

class SaveImage:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.quality = 95  # Default quality for WebP
        self.method = 6    # Compression method for WebP
        self.compress_level = 4  # Default PNG compression level

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", {"tooltip": "The images to save."}),
                "filename_prefix": ("STRING", {"default": "ComfyUI", "tooltip": "The prefix for the file to save."})
            },
            "optional": {
                "key_1": ("STRING", {"default": "", "tooltip": "Metadata key 1"}),
                "metadata_1": ("STRING", {"default": "", "tooltip": "Metadata value 1"}),
                "key_2": ("STRING", {"default": "", "tooltip": "Metadata key 2"}),
                "metadata_2": ("STRING", {"default": "", "tooltip": "Metadata value 2"}),
                "key_3": ("STRING", {"default": "", "tooltip": "Metadata key 3"}),
                "metadata_3": ("STRING", {"default": "", "tooltip": "Metadata value 3"}),
                "key_4": ("STRING", {"default": "", "tooltip": "Metadata key 4"}),
                "metadata_4": ("STRING", {"default": "", "tooltip": "Metadata value 4"}),
                "key_5": ("STRING", {"default": "", "tooltip": "Metadata key 5"}),
                "metadata_5": ("STRING", {"default": "", "tooltip": "Metadata value 5"}),
            }
        }



    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "image"
    DESCRIPTION = "Saves the input images as PNG or WebP with dynamic metadata key-value pairs."

    def save_images(self, images, filename_prefix="ComfyUI", unique_id=None, **kwargs):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
            filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0]
        )
        results = list()

        # Extract dynamic metadata from kwargs
        dynamic_metadata = {}
        for i in range(1, 6):
            key = kwargs.get(f"key_{i}", "").strip()
            value = kwargs.get(f"metadata_{i}", "").strip()
            if key:
                dynamic_metadata[key] = value

        for batch_number, image in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"

            metadata = None
            if not args.disable_metadata and dynamic_metadata:
                metadata = PngImagePlugin.PngInfo()
                for key, value in dynamic_metadata.items():
                    metadata.add_text(key, value)

            img.save(
                os.path.join(full_output_folder, file),
                pnginfo=metadata,
                compress_level=self.compress_level
            )

            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

        return {"ui": {"images": results}}

# Node registration
NODE_CLASS_MAPPINGS = {
    "SaveImage": SaveImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImage": "Save Image with Dynamic Metadata"
}