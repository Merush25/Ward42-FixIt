
# Ward 42 Fix-It - Secure Photo Uploads

from pathlib import Path
from io import BytesIO
import uuid

from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename


# Folder for storing uploaded photographs
UPLOAD_FOLDER = (
    Path(__file__).resolve().parent
    / "instance"
    / "uploads"
)

# Maximum permitted photo size: 2 MB
MAX_PHOTO_SIZE = 2 * 1024 * 1024

# Permitted file extensions, MIME types and image formats
ALLOWED_IMAGES = {
    ".jpg": ("image/jpeg", "JPEG"),
    ".jpeg": ("image/jpeg", "JPEG"),
    ".png": ("image/png", "PNG"),
    ".webp": ("image/webp", "WEBP")
}


def save_photo(photo):

    # A photo is optional
    if photo is None or not photo.filename:
        return None

    # Make the original filename safe
    filename = secure_filename(photo.filename)

    if not filename:
        raise ValueError("Invalid photo filename.")

    # Check the file extension
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_IMAGES:
        raise ValueError(
            "Only JPEG, PNG and WebP images are allowed."
        )

    expected_mime, expected_format = ALLOWED_IMAGES[extension]

    # Check the declared content type
    if photo.mimetype != expected_mime:
        raise ValueError(
            "The photo's content type is not allowed."
        )

    # Read no more than 2 MB plus one byte
    photo_data = photo.read(MAX_PHOTO_SIZE + 1)

    if len(photo_data) > MAX_PHOTO_SIZE:
        raise ValueError(
            "The photograph must be smaller than 2 MB."
        )

    if not photo_data:
        raise ValueError("The photograph is empty.")

    # Check the actual image format and structure
    try:
        with Image.open(BytesIO(photo_data)) as image:
            actual_format = image.format
            image.verify()

    except (UnidentifiedImageError, OSError, ValueError) as error:
        raise ValueError(
            "The uploaded file is not a valid image."
        ) from error

    if actual_format != expected_format:
        raise ValueError(
            "The actual image format does not match "
            "the filename."
        )

    # Generate a unique filename
    unique_filename = (
        f"{uuid.uuid4().hex}_{filename}"
    )

    # Create the upload folder if necessary
    UPLOAD_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save the photograph
    file_path = UPLOAD_FOLDER / unique_filename
    file_path.write_bytes(photo_data)

    # Return the relative path for database storage
    return f"uploads/{unique_filename}"

