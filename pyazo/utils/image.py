"""pyazo image-related utilities"""

from django.conf import settings
from PIL import Image, ImageDraw, ImageFont


def generate_ext_thumb(extension):
    """Create 200x200 thumbnail for filetype"""
    # ext still has a leading dot, which we don't want for saving
    out_name = extension[1:]
    # Create a 200x200 image and write extension on it
    image_width, image_height = 200, 200
    img = Image.new('RGBA', (image_width, image_height), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(
        settings.STATIC_ROOT+'fonts/Metropolis-Regular.ttf', 18)
    text_width, text_height = draw.textsize(extension, font=font)
    draw.text(((image_width-text_width)/2,
               (image_height-text_height)/2), extension, fill="#E9ECEF")
    img.save(settings.THUMBNAIL_ROOT+out_name+'.png', 'PNG')
