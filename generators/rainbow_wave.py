from PIL import Image, ImageDraw, ImageFont
import io
import os
import numpy as np
from .utils import prepare_text_layout

def generate_rainbow_wave(text):
    """
    Generate text with a rainbow wave effect on transparent background.
    Returns a BytesIO object containing the PNG image.
    """
    # Get text layout information
    lines, width, height, font, line_height = prepare_text_layout(text)
    
    # Create base image
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw each line of text in white
    for i, line in enumerate(lines):
        y = i * line_height
        draw.text((0, y), line, fill=(255, 255, 255, 255), font=font)
    
    # Convert to numpy array for wave effect
    img_array = np.array(img)
    
    # Create wave pattern
    x = np.arange(width)
    y = np.arange(height)
    X, Y = np.meshgrid(x, y)
    wave = np.sin(X * 0.1 + Y * 0.2) * 0.5 + 0.5
    
    # Create rainbow colors
    hue = (X * 0.02) % 1.0  # Horizontal rainbow gradient
    
    # Convert HSV to RGB
    C = wave
    X = C * (1 - np.abs((hue * 6) % 2 - 1))
    m = 1 - C
    
    # RGB components based on hue
    mask = img_array[:, :, 3] > 0
    
    # Calculate RGB values for each hue region
    R = np.zeros_like(hue)
    G = np.zeros_like(hue)
    B = np.zeros_like(hue)
    
    # Hue regions
    idx = (hue < 1/6)
    R[idx], G[idx], B[idx] = C[idx], X[idx], 0
    
    idx = (1/6 <= hue) & (hue < 2/6)
    R[idx], G[idx], B[idx] = X[idx], C[idx], 0
    
    idx = (2/6 <= hue) & (hue < 3/6)
    R[idx], G[idx], B[idx] = 0, C[idx], X[idx]
    
    idx = (3/6 <= hue) & (hue < 4/6)
    R[idx], G[idx], B[idx] = 0, X[idx], C[idx]
    
    idx = (4/6 <= hue) & (hue < 5/6)
    R[idx], G[idx], B[idx] = X[idx], 0, C[idx]
    
    idx = (5/6 <= hue)
    R[idx], G[idx], B[idx] = C[idx], 0, X[idx]
    
    # Apply colors to non-transparent pixels
    img_array[mask, 0] = (R[mask] * 255).astype(np.uint8)
    img_array[mask, 1] = (G[mask] * 255).astype(np.uint8)
    img_array[mask, 2] = (B[mask] * 255).astype(np.uint8)
    
    # Convert back to PIL Image
    rainbow_img = Image.fromarray(img_array)
    
    # Save to BytesIO
    img_io = io.BytesIO()
    rainbow_img.save(img_io, format='PNG')
    img_io.seek(0)
    
    return img_io 