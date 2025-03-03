from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import os
import numpy as np
from .utils import prepare_text_layout

def generate_neon_text(text):
    """
    Generate text with a neon glow effect on transparent background.
    Returns a BytesIO object containing the PNG image.
    """
    # Get text layout information
    lines, width, height, font, line_height = prepare_text_layout(text)
    
    # Create base image with some padding for glow
    base = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    
    # Draw the glow layers for each line
    glow_color = (0, 255, 255, 50)  # Cyan glow
    for i, line in enumerate(lines):
        y = i * line_height
        for j in range(3):
            glow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            glow_draw = ImageDraw.Draw(glow)
            glow_draw.text((0, y), line, font=font, fill=glow_color)
            glow = glow.filter(ImageFilter.GaussianBlur(radius=2-j))
            base = Image.alpha_composite(base, glow)
        
        # Draw the main text for this line
        draw.text((0, y), line, font=font, fill=(0, 255, 255, 255))  # Bright cyan
    
    # Save to BytesIO
    img_io = io.BytesIO()
    base.save(img_io, format='PNG')
    img_io.seek(0)
    
    return img_io 