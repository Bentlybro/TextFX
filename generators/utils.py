from PIL import Image, ImageDraw, ImageFont
import os

def get_font(base_size=14):
    """Get the font with specified base size."""
    try:
        font_paths = [
            "C:\\Windows\\Fonts\\arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Helvetica.ttc"
        ]
        font = None
        for path in font_paths:
            if os.path.exists(path):
                font = ImageFont.truetype(path, base_size)
                break
        if font is None:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()
    return font

def calculate_text_dimensions(text, font):
    """Calculate text dimensions using a temporary image."""
    temp_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    text_bbox = temp_draw.textbbox((0, 0), text, font=font)
    return text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

def smart_text_wrap(text, target_width, font):
    """
    Wrap text to fit within target_width, breaking at word boundaries.
    Now uses a more natural approach to line breaks.
    """
    words = text.split()
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        # Calculate width with space
        word_width, _ = calculate_text_dimensions(word + " ", font)
        
        if current_line and current_width + word_width > target_width:
            # Line would be too long, start a new line
            lines.append(" ".join(current_line))
            current_line = [word]
            current_width = word_width
        else:
            # Add word to current line
            current_line.append(word)
            current_width += word_width

    # Add the last line if there's anything left
    if current_line:
        lines.append(" ".join(current_line))
    
    return lines

def get_dynamic_dimensions(text):
    """
    Calculate dynamic dimensions based on text length.
    Returns (target_width, height, font_size)
    """
    text_length = len(text)
    
    # Adjust font size based on text length
    if text_length < 100:
        font_size = 14
    elif text_length < 200:
        font_size = 12
    else:
        font_size = 10
    
    font = get_font(font_size)
    
    # First calculate the full text width
    full_width, _ = calculate_text_dimensions(text, font)
    
    # Set maximum width based on text length
    if text_length > 500:
        target_width = 800
    elif text_length > 200:
        target_width = 600
    elif full_width > 400:
        target_width = 400
    else:
        target_width = full_width
    
    # Calculate number of lines needed
    temp_lines = smart_text_wrap(text, target_width, font)
    num_lines = len(temp_lines)
    
    # Calculate height based on number of lines and font size
    line_spacing = font_size * 1.5  # Add some spacing between lines
    height = int(num_lines * line_spacing) + 20  # Add padding
    
    # Ensure minimum dimensions
    height = max(height, 20)
    target_width = max(target_width, 100)
    
    return target_width, height, font_size

def prepare_text_layout(text):
    """
    Prepare text layout with dynamic sizing and wrapping.
    Returns (wrapped_lines, width, height, font, line_height)
    """
    # Get initial dimensions
    target_width, height, font_size = get_dynamic_dimensions(text)
    font = get_font(font_size)
    
    # Wrap text
    lines = smart_text_wrap(text, target_width, font)
    
    # Calculate actual width needed
    max_line_width = 0
    for line in lines:
        line_width, _ = calculate_text_dimensions(line, font)
        max_line_width = max(max_line_width, line_width)
    
    # Add padding to width
    width = max_line_width + 20  # Add some horizontal padding
    
    # Calculate proper line height with padding
    _, single_line_height = calculate_text_dimensions("Ay", font)  # Use "Ay" to get proper height with ascenders/descenders
    line_height = int(single_line_height * 1.5)  # 1.5x line spacing
    
    # Recalculate total height with proper spacing
    total_height = (line_height * len(lines)) + 20  # Add padding at top and bottom
    
    return lines, width, total_height, font, line_height 