from PIL import Image, ImageDraw, ImageFont
import io
import os
import numpy as np
from .utils import prepare_text_layout

def generate_gradient_text(text):
    """
    Generate text with RGB gradient effect on transparent background.
    Returns a BytesIO object containing the PNG image.
    """
    # Get text layout information
    lines, width, height, font, line_height = prepare_text_layout(text)
    
    # Create the actual image with transparent background
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw each line of text in white
    for i, line in enumerate(lines):
        y = i * line_height
        draw.text((0, y), line, fill=(255, 255, 255, 255), font=font)
    
    # Convert to numpy array for easier manipulation
    img_array = np.array(img)
    
    # Create gradient array
    x = np.linspace(0, 2*np.pi, width)
    r = np.sin(x) * 127 + 128
    g = np.sin(x + 2*np.pi/3) * 127 + 128
    b = np.sin(x + 4*np.pi/3) * 127 + 128
    
    # Apply gradient only to non-transparent pixels
    for i in range(width):
        mask = img_array[:, i, 3] > 0
        img_array[mask, i, 0] = r[i]
        img_array[mask, i, 1] = g[i]
        img_array[mask, i, 2] = b[i]
    
    # Convert back to PIL Image
    gradient_img = Image.fromarray(img_array)
    
    # Save the image to a BytesIO object
    img_io = io.BytesIO()
    gradient_img.save(img_io, format='PNG')
    img_io.seek(0)
    
    return img_io

def generate_animated_gradient_text(text, num_frames=30):
    """
    Generate animated text with scrolling RGB gradient effect.
    Returns a BytesIO object containing the animated GIF.
    """
    # Get text layout information
    lines, width, height, font, line_height = prepare_text_layout(text)
    
    frames = []
    
    # Create base frames
    for frame in range(num_frames):
        # Create the image with transparent background
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw each line of text in white
        for i, line in enumerate(lines):
            y = i * line_height
            draw.text((0, y), line, fill=(255, 255, 255, 255), font=font)
        
        # Convert to numpy array for easier manipulation
        img_array = np.array(img)
        
        # Create scrolling gradient array
        phase = 2 * np.pi * frame / num_frames  # Phase shift for animation
        x = np.linspace(0, 2*np.pi, width) + phase
        r = np.sin(x) * 127 + 128
        g = np.sin(x + 2*np.pi/3) * 127 + 128
        b = np.sin(x + 4*np.pi/3) * 127 + 128
        
        # Apply gradient only to non-transparent pixels
        for i in range(width):
            mask = img_array[:, i, 3] > 0
            img_array[mask, i, 0] = r[i]
            img_array[mask, i, 1] = g[i]
            img_array[mask, i, 2] = b[i]
        
        # Convert back to PIL Image
        gradient_frame = Image.fromarray(img_array)
        frames.append(gradient_frame)
    
    # Save the animation to a BytesIO object
    img_io = io.BytesIO()
    # Save as GIF with 50ms delay between frames (20 fps)
    frames[0].save(
        img_io,
        format='GIF',
        save_all=True,
        append_images=frames[1:],
        duration=50,
        loop=0,
        optimize=False
    )
    img_io.seek(0)
    
    return img_io 