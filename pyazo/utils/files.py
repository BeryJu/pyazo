"""pyazo image-related utilities"""
import hashlib

import magic
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!


def get_mime_type(file_path: str) -> str:
    """Return mime-type for file"""
    return magic.from_file(file_path, mime=True)

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
               (image_height-text_height)/2), extension, fill="#E9ECEF", font=font)
    img.save(settings.THUMBNAIL_ROOT+out_name+'.png', 'PNG')

def generate_hashes(file_handle):
    """Return dict with md5, sha256 and sha512 keys containing file hashes"""
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    sha512 = hashlib.sha512()
    while True:
        data = file_handle.read(BUF_SIZE)
        if not data:
            break
        md5.update(data)
        sha256.update(data)
        sha512.update(data)
    return {
        'md5': md5.hexdigest(),
        'sha256': sha256.hexdigest(),
        'sha512': sha512.hexdigest(),
    }


def save_from_post(content, extension):
    """Takes a file from post, calculates sha512, saves it to media dir and returns path"""
    sha512 = hashlib.sha512()
    sha512.update(content)
    filename = '%s/%s.%s' % (settings.MEDIA_ROOT, sha512.hexdigest(), extension)
    with open(filename, 'wb') as out_file:
        out_file.write(content)
    return filename
