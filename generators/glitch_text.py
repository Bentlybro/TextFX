from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
import io
import numpy as np
import random
from .utils import prepare_text_layout

# Zalgo-like combining characters for corruption effect
ZALGO_CHARS = [
    chr(x) for x in list(range(0x0300, 0x036F)) +  # Combining Diacritical Marks
                    list(range(0x1DC0, 0x1DFF)) +   # Combining Diacritical Marks Supplement
                    list(range(0x20D0, 0x20FF))     # Combining Diacritical Marks for Symbols
]

def corrupt_text(text, intensity=0.3):
    """Add zalgo-like corruption to text."""
    result = ""
    for char in text:
        result += char
        # Add random combining characters
        num_corruptions = int(random.random() * 5 * intensity) + 1
        for _ in range(num_corruptions):
            result += random.choice(ZALGO_CHARS)
    return result

def create_glitch_frame(lines, width, height, font, line_height, padding, frame_num):
    """Create a single frame of the glitch animation."""
    base = Image.new('RGBA', (width + padding, height + padding), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    
    # Use frame number to create varying effects
    time_offset = frame_num * 0.2
    
    for i, line in enumerate(lines):
        y = i * line_height + padding//2
        
        # Create three versions of corrupted text with different intensities
        # Vary corruption intensity with time
        intensity_mod = (np.sin(time_offset) + 1) * 0.2
        corrupted_text1 = corrupt_text(line, 0.2 + intensity_mod)
        corrupted_text2 = corrupt_text(line, 0.3 + intensity_mod)
        corrupted_text3 = corrupt_text(line, 0.4 + intensity_mod)
        
        # Draw main text
        draw.text((padding//2, y), line, font=font, fill=(255, 255, 255, 255))
        
        # Draw glitch layers with animated offsets
        base_offsets = [(-2, -1), (2, 1), (-1, 2)]
        offsets = [
            (x + int(np.sin(time_offset + idx) * 2), 
             y + int(np.cos(time_offset + idx) * 2))
            for idx, (x, y) in enumerate(base_offsets)
        ]
        
        colors = [
            (255, 0, 0, 80),
            (0, 255, 255, 80),
            (255, 0, 255, 80)
        ]
        corrupted_texts = [corrupted_text1, corrupted_text2, corrupted_text3]
        
        for offset, color, glitched_text in zip(offsets, colors, corrupted_texts):
            draw.text((padding//2 + offset[0], y + offset[1]), 
                     glitched_text, font=font, fill=color)
    
    # Convert to numpy array for additional glitch effects
    img_array = np.array(base)
    
    # Add controlled glitch lines that move with time
    num_glitch_lines = 5
    for _ in range(num_glitch_lines):
        # Position glitch lines using frame number
        y_pos = int(np.sin(time_offset + _ * 1.5) * height/3 + height/2)
        glitch_height = np.random.randint(1, 4)
        glitch_shift = int(np.sin(time_offset * 2 + _) * 8)
        
        # Shift a horizontal slice of the image
        slice_start = max(0, y_pos)
        slice_end = min(height + padding, y_pos + glitch_height)
        img_array[slice_start:slice_end] = np.roll(img_array[slice_start:slice_end], glitch_shift, axis=1)
    
    # Add scan lines that move
    scan_lines = np.ones_like(img_array)
    scan_offset = int(frame_num * 2) % 2
    scan_lines[(2 + scan_offset)::4, :, :] = 0.9
    img_array = (img_array * scan_lines).astype(np.uint8)
    
    # Convert back to PIL Image for final effects
    glitch_img = Image.fromarray(img_array)
    
    # Add subtle bloom effect
    bloom_layer = glitch_img.copy()
    bloom_layer = bloom_layer.filter(ImageFilter.GaussianBlur(radius=1))
    glitch_img = Image.blend(glitch_img, bloom_layer, 0.3)
    
    return glitch_img

def generate_glitch_text(text):
    """
    Generate text with an animated glitch effect on transparent background.
    Returns a BytesIO object containing the animated GIF.
    """
    # Get text layout information
    lines, width, height, font, line_height = prepare_text_layout(text)
    padding = 30
    
    # Create multiple frames
    frames = []
    num_frames = 20  # Number of frames in animation
    
    for frame in range(num_frames):
        frame_img = create_glitch_frame(lines, width, height, font, line_height, padding, frame)
        # Convert to P mode (palette) for better GIF compatibility
        frame_img = frame_img.convert('RGBA').convert('P', palette=Image.ADAPTIVE, colors=255)
        frames.append(frame_img)
    
    # Save as animated GIF
    img_io = io.BytesIO()
    # Save first frame
    frames[0].save(
        img_io, 
        format='GIF',
        save_all=True,
        append_images=frames[1:],
        duration=50,  # 50ms per frame = 20fps
        loop=0,
        optimize=True,
        disposal=2,  # Clear each frame before rendering next
        transparency=255  # Set last palette index as transparent
    )
    img_io.seek(0)
    
    return img_io 