from pilkit.lib import Image


class WatermarkOverlay(object):
    def __init__(self, watermark_image):
        self.watermark_image = watermark_image

    def process(self, img):
        original = img.convert("RGBA")
        overlay = Image.open(self.watermark_image).convert("RGBA")
        fg_resized = overlay.resize((100, 100))
        original.paste(fg_resized, box=(700, 0), mask=fg_resized)
        return original
