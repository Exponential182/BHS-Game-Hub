import io
from zipfile import ZipFile

from PIL import Image
from wtforms import FileField
from wtforms.validators import StopValidation


def crop_and_centre_cover_image(image_stream):
    """
    Target Attributes:
     - Aspect ratio must match 630:500 (w:h)
     - Maximum width of 630 px
    """
    target_aspect_ratio = 630 / 500
    image = Image.open(image_stream)

    real_aspect_ratio = image.width / image.height
    if real_aspect_ratio != target_aspect_ratio:

        centre = (image.width / 2, image.height / 2)  # (width, height)
        # width/height = target_aspect_ratio
        if real_aspect_ratio > target_aspect_ratio:
            height = image.height
            width = height * target_aspect_ratio
        else:
            width = image.width
            height = width / target_aspect_ratio

        # Corners
        left = centre[0] - width / 2
        upper = centre[1] - height / 2
        right = centre[0] + width / 2
        lower = centre[1] + height / 2

        image = image.crop((left, upper, right, lower))

    if image.width > 630:
        # Fixed dimesions allowed due to cropping
        image.resize([630, 500])

    output_data = io.BytesIO()
    image.save(output_data, "PNG")
    output_data.seek(0)

    return output_data

