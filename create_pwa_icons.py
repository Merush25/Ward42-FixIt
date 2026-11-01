
# ==========================================
# WARD 42 FIX-IT
# PWA Application Icon Generator
# ==========================================

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


# Folder for our application icons
ROOT = Path(__file__).resolve().parent

ICON_FOLDER = ROOT / "static" / "icons"

ICON_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# Street Smart Mamelodi theme colours
TERRACOTTA = "#B9532B"
CREAM = "#F5F1EA"
WHITE = "#FFFFFF"


# ==========================================
# LOAD A FONT
# ==========================================

def get_font(size):

    font_options = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]

    for font_path in font_options:

        if Path(font_path).exists():
            return ImageFont.truetype(
                font_path,
                size
            )

    return ImageFont.load_default()


# ==========================================
# CREATE AN APPLICATION ICON
# ==========================================

def create_icon(size, filename, maskable=False):

    # Create the background
    background = TERRACOTTA if maskable else CREAM

    image = Image.new(
        "RGB",
        (size, size),
        background
    )

    draw = ImageDraw.Draw(image)

    # Create a rounded terracotta badge
    if not maskable:

        margin = int(size * 0.08)

        draw.rounded_rectangle(
            (
                margin,
                margin,
                size - margin,
                size - margin
            ),
            radius=int(size * 0.20),
            fill=TERRACOTTA
        )

    # Make the number smaller for maskable icons
    font_size = int(
        size * (0.34 if maskable else 0.42)
    )

    font = get_font(font_size)

    text = "42"

    # Calculate text size
    bounds = draw.textbbox(
        (0, 0),
        text,
        font=font
    )

    text_width = bounds[2] - bounds[0]
    text_height = bounds[3] - bounds[1]

    # Centre the number
    x = (size - text_width) / 2 - bounds[0]
    y = (size - text_height) / 2 - bounds[1]

    draw.text(
        (x, y),
        text,
        font=font,
        fill=WHITE
    )

    # Save the icon
    file_path = ICON_FOLDER / filename

    image.save(
        file_path,
        format="PNG",
        optimize=True
    )

    print("Created:", file_path.name)


# ==========================================
# GENERATE OUR THREE ICONS
# ==========================================

create_icon(
    192,
    "icon-192.png"
)

create_icon(
    512,
    "icon-512.png"
)

create_icon(
    512,
    "icon-maskable-512.png",
    maskable=True
)

print("\nPWA icons created successfully!")
