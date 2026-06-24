# main/mixins.py
import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

class WebPImageMixin:
    def convert_to_webp(self, image_field):
        if not image_field:
            return
        img = Image.open(image_field)
        img = img.convert("RGB")  # Ensure RGB for WebP
        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=80)
        file_name = os.path.splitext(image_field.name)[0] + ".webp"
        image_field.save(file_name, ContentFile(buffer.getvalue()), save=False)
