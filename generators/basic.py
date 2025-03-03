from PIL import Image, ImageDraw, ImageFont
import io
import hashlib
import os
from .utils import prepare_text_layout, calculate_text_dimensions

def generate_basic_image(text):
    """
    Generate a basic image with colored background based on text input.
    Returns a BytesIO object containing the PNG image.
    """
    # Convert the text into a color by hashing it
    hash_object = hashlib.md5(text.encode())
    color_hex = hash_object.hexdigest()[:6]
    color = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    
    # Get text layout information
    lines, width, height, font, line_height = prepare_text_layout(text)
    
    # Create the image with the generated color as background
    img = Image.new('RGB', (width, height), color=color)
    draw = ImageDraw.Draw(img)
    
    # Draw each line of text with shadow
    for i, line in enumerate(lines):
        y = i * line_height
        # Calculate x position to center this line
        line_width, _ = calculate_text_dimensions(line, font)
        x = (width - line_width) // 2
        
        # Add text shadow for better visibility
        shadow_offset = 2
        draw.text((x + shadow_offset, y + shadow_offset), line, fill=(0, 0, 0), font=font)
        draw.text((x, y), line, fill=(255, 255, 255), font=font)
    
    # Save the image to a BytesIO object
    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    
    return img_io 