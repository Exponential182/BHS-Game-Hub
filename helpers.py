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


def FileSizeLimit(lim_in_mb, message="File too Large"):
    def file_size_checker(form, field):
        total_bytes = len(field.data.read())

        if total_bytes > lim_in_mb * (1024 ** 2):
            raise StopValidation(message)

        # Reset Pointer
        field.data.seek(0)

    return file_size_checker


def AllowedWebZip(max_total_size_mb, max_file_count=1000):
    def valid_zip_checker(form, field: FileField):
        if field.data:
            byte_stream = io.BytesIO(field.data.read())

            zip_file = ZipFile(byte_stream, "r")
            info_list = zip_file.infolist()

            if len(info_list) > max_file_count:
                raise StopValidation("Too many files in zip.")

            total_bytes = 0
            has_index = False
            for info in info_list:
                if info.filename == 'index.html':
                    has_index = True
                if info.filename.endswith(".pck"):
                    if info.file_size > 200 * (1024 ** 2):
                        raise StopValidation("PCK too large")

                total_bytes += info.file_size

            if not has_index:
                raise StopValidation("No index.html")

            if total_bytes > max_total_size_mb * (1024 ** 2):
                raise StopValidation("ZIP archive to large.")

    return valid_zip_checker
