from .node import SaveImage
from .node import MultilineString

NODE_CLASS_MAPPINGS = {
    "Save Image (Selective Metadata)": SaveImage,
    "Multiline String": MultilineString,
}

__all__ = ['NODE_CLASS_MAPPINGS']