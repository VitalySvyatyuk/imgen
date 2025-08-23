from django.shortcuts import render

import io
import os
import random
from PIL import Image
from django.core.files.base import ContentFile
from .models import GeneratedImage
from asgiref.sync import sync_to_async
from datetime import datetime


@sync_to_async
def generate_image(width: int, height: int, target_size: int, format: str) -> (bool, str):
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    filename = f'{width}x{height}_{target_size}bytes.{format}'
    try:
        buffer = io.BytesIO()
        img = Image.new('RGB', (width, height), color)
        if format == 'jpg':
            img.save(buffer, 'JPEG', quality=1, optimize=True, subsempling=2)
        else:
            img.save(buffer, 'PNG', quality=1, optimize=True, subsempling=2, progressive=True)

        image_file = ContentFile(buffer.getvalue())

        # If file smaller than target, pad it
        if image_file.size < target_size:
            image_file.seek(0, 2)  # jump to the end of a file
            image_file.write(b'\0' * (target_size - image_file.size))

        obj = GeneratedImage(
            width=width,
            height=height,
            size=image_file.size,
            format=format,
            color=f'r{color[0]}g{color[1]}b{color[2]}',
        )
        obj.image.save(filename, image_file)
        obj.save()
        return True, False, os.path.basename(obj.image.name)
    except Exception as e:
        return False, True, e


@sync_to_async
def get_images():
    return [{
        'url': im.image.url,
        'filename': os.path.basename(im.image.name),
        'r': im.color.split('g')[0][1:],
        'g': im.color.split('g')[1].split('b')[0],
        'b': im.color.split('b')[-1],
        'date': datetime.strftime(im.created_at, '%d.%m.%Y %H:%M:%S')
    } for im in GeneratedImage.objects.filter().order_by('-created_at')[:10]]


@sync_to_async()
def serialize(width: int, height: int, size: int, format: str) -> (bool, str):
    if width > 10000:
        return False, 'Width cannot exceed 10000 px'
    if height > 10000:
        return False, 'Height cannot exceed 10000 px'
    if size > 50_000_000:
        return False, 'Size cannot exceed 50_000_000 bytes'
    if format.lower() not in ['png', 'jpg']:
        return False, f'Unsupported format {format}'
    return True, ''


async def index(request):
    is_success, is_error, message = False, False, ''
    if request.method == 'POST':
        width = int(request.POST.get('width', 320))
        height = int(request.POST.get('height', 240))
        size = int(request.POST.get('size', 10))
        format = request.POST.get('format', 'png')
        is_serialized, error = await serialize(width, height, size, format)
        if is_serialized:
            is_success, is_error, message = await generate_image(width, height, size, format)
        else:
            is_success, is_error, message = False, True, error
    context = {
        'is_success': is_success,
        'is_error': is_error,
        'message': message,
        'images': await get_images()
    }
    return render(request, 'index.html', context)
