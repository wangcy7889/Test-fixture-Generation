from typing import Any,Optional
from pptx.shapes.base import BaseShape
def get_default_font_size(shape: BaseShape, slide_layout: Any) -> Optional[float]:
        try:
            if not hasattr(shape, "placeholder_format"):
                return None
            shape_type = shape.placeholder_format.type
            for layout_placeholder in slide_layout.placeholders:
                if layout_placeholder.placeholder_format.type == shape_type:
                    for elem in layout_placeholder.element.iter():
                        if "defRPr" in elem.tag and (sz := elem.get("sz")):
                            return float(sz) / 100.0
                    break
        except Exception:
            pass
        return None
