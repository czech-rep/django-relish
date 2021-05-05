from PIL import Image as PIL_Image
from django.core.files.base import ContentFile
from io import StringIO, BytesIO
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect


def resize_and_send(path, size: tuple, name):
    img_io = BytesIO()

    if path[0] == '/': # mind the first character
        path = path[1:]

    img = PIL_Image.open(path)
    img2 = img.resize(size)
    img2.save(img_io, format='JPEG')     # saved 'virtually' - into stream
    img_content = ContentFile(img_io.getvalue(), 'resized.jpg')     # type: Raw content. NO! this IS raw content
    
    filename = name
    responce = HttpResponse(img_content)
    responce['Content-Disposition'] = f'attachment; filename="{filename}"'
    return responce


# io.BytesIO() - strem for representing bytes - you can write them in memory

class resize_params_error(Exception):
    def __init__(self, ms):
        self.ms = ms


def calculate_dims(new_dims, a, ratio):
    h, w = new_dims['height'], new_dims['width']
    if a:
        if h and w:
            raise resize_params_error('contradiction in input params')
        elif h:
            w = int(h) / ratio
        elif w:
            h = int(w) * ratio
    if not (h and w):
        raise resize_params_error('no sufficient input')
    
    # opther cases -> h, w = h, w
    return int(h), int(w)