#!/usr/bin/env python3
"""Core functionality for generating Tianzige (田字格) writing grids."""

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4, A5, A6, A3, B4, B5, LETTER, LEGAL
from typing import Tuple, Literal, Union
import re

# Define page sizes in mm for easier reference
PAGE_SIZES = {
    'a4': A4,
    'a5': A5,
    'a6': A6,
    'a3': A3,
    'b4': B4,
    'b5': B5,
    'letter': LETTER,
    'legal': LEGAL
}

PageSizeType = Literal['a4', 'a5', 'a6', 'a3', 'b4', 'b5', 'letter', 'legal']

def calculate_dimensions(
    page_width: float,
    page_height: float,
    margin_left: float,
    margin_right: float,
    margin_top: float,
    margin_bottom: float,
    square_size: float
) -> Tuple[int, int]:
    """Calculate how many squares can fit in each dimension.
    
    Args:
        page_width: Page width in points
        page_height: Page height in points
        margin_left: Left margin in points
        margin_right: Right margin in points
        margin_top: Top margin in points
        margin_bottom: Bottom margin in points
        square_size: Size of each square in points
        
    Returns:
        Tuple of (horizontal_boxes, vertical_boxes)
    """
    available_width = page_width - margin_left - margin_right
    available_height = page_height - margin_top - margin_bottom
    
    horizontal_boxes = int(available_width / square_size)
    vertical_boxes = int(available_height / square_size)
    
    return horizontal_boxes, vertical_boxes

def calculate_required_size(
    page_width: float,
    page_height: float,
    margin_left: float,
    margin_right: float,
    margin_top: float,
    margin_bottom: float,
    min_horizontal: int,
    min_vertical: int
) -> float:
    """Calculate required square size to fit minimum number of boxes.
    
    Args:
        page_width: Page width in points
        page_height: Page height in points
        margin_left: Left margin in points
        margin_right: Right margin in points
        margin_top: Top margin in points
        margin_bottom: Bottom margin in points
        min_horizontal: Minimum number of horizontal boxes
        min_vertical: Minimum number of vertical boxes
        
    Returns:
        Required square size in mm
    """
    available_width = page_width - margin_left - margin_right
    available_height = page_height - margin_top - margin_bottom
    
    max_square_size = min(
        available_width / min_horizontal,
        available_height / min_vertical
    )
    
    # Convert to mm and round down to nearest 0.5mm for cleaner sizes
    return float(int((max_square_size / mm) * 2) / 2)

def hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
    """Convert hex color to RGB tuple (0-1 range).
    
    Args:
        hex_color: Color in hex format (e.g., '#808080' or '808080')
        
    Returns:
        Tuple of RGB values in 0-1 range
    """
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return tuple(x/255 for x in rgb)

def validate_hex_color(color: str) -> bool:
    """Validate hex color format.
    
    Args:
        color: Color string to validate
        
    Returns:
        True if valid hex color format, False otherwise
    """
    pattern = r'^#?[0-9A-Fa-f]{6}$'
    return bool(re.match(pattern, color))

def create_tianzige(
    output_file: str,
    line_color: str = "#808080",
    square_size: Union[float, None] = None,
    margin_top: float = 15,
    margin_bottom: float = 15,
    margin_left: float = 20,
    margin_right: float = 10,
    show_inner_grid: bool = True,
    page_size: PageSizeType = 'a4',
    min_horizontal: Union[int, None] = None,
    min_vertical: Union[int, None] = None
) -> None:
    """Create a PDF with tian zi ge grid.
    
    Args:
        output_file: Path to save the PDF
        line_color: Hex color code for grid lines
        square_size: Size of each square in mm
        margin_top: Top margin in mm
        margin_bottom: Bottom margin in mm
        margin_left: Left margin in mm
        margin_right: Right margin in mm
        show_inner_grid: Whether to show internal grid lines
        
    Raises:
        ValueError: If hex color format is invalid
    """
    if not validate_hex_color(line_color):
        raise ValueError("Invalid hex color format. Use format: #RRGGBB")

    # Convert margins to points (PDF units)
    margins = {
        'top': margin_top * mm,
        'bottom': margin_bottom * mm,
        'left': margin_left * mm,
        'right': margin_right * mm
    }

    # Get page size
    page_width, page_height = PAGE_SIZES[page_size.lower()]
    
    # Create PDF with selected page size
    c = canvas.Canvas(output_file, pagesize=PAGE_SIZES[page_size.lower()])
    
    # Set line color
    rgb_color = hex_to_rgb(line_color)
    c.setStrokeColorRGB(*rgb_color)
    
    # Handle square size and minimum box requirements
    if square_size is None:
        # Use default minimums if none provided
        min_h = min_horizontal if min_horizontal is not None else 10
        min_v = min_vertical if min_vertical is not None else 10
        square_size = calculate_required_size(
            page_width, page_height,
            margins['left'], margins['right'],
            margins['top'], margins['bottom'],
            min_h, min_v
        )
    else:
        # If size is provided, check against minimums if they're specified
        square_size_pt = square_size * mm
        h_boxes, v_boxes = calculate_dimensions(
            page_width, page_height,
            margins['left'], margins['right'],
            margins['top'], margins['bottom'],
            square_size_pt
        )
        
        if (min_horizontal is not None or min_vertical is not None):
            error_msg = []
            if min_horizontal is not None and h_boxes < min_horizontal:
                required_size = calculate_required_size(
                    page_width, page_height,
                    margins['left'], margins['right'],
                    margins['top'], margins['bottom'],
                    min_horizontal, 1  # Only consider horizontal requirement
                )
                error_msg.append(
                    f"Can only fit {h_boxes} horizontal boxes with {square_size}mm squares. "
                    f"Maximum square size for {min_horizontal} horizontal boxes would be {required_size}mm."
                )
            
            if min_vertical is not None and v_boxes < min_vertical:
                required_size = calculate_required_size(
                    page_width, page_height,
                    margins['left'], margins['right'],
                    margins['top'], margins['bottom'],
                    1, min_vertical  # Only consider vertical requirement
                )
                error_msg.append(
                    f"Can only fit {v_boxes} vertical boxes with {square_size}mm squares. "
                    f"Maximum square size for {min_vertical} vertical boxes would be {required_size}mm."
                )
            
            if error_msg:
                raise ValueError("\n".join(error_msg))
    
    # Convert square size to points
    square_size_pt = square_size * mm
    
    # Calculate available space
    width = page_width - margins['left'] - margins['right']
    height = page_height - margins['top'] - margins['bottom']
    
    # Calculate number of complete squares that fit
    cols = int(width // square_size_pt)
    rows = int(height // square_size_pt)
    
    # Calculate actual grid width and height
    grid_width = cols * square_size_pt
    grid_height = rows * square_size_pt
    
    # Draw vertical lines
    for i in range(cols + 1):
        x = margins['left'] + i * square_size_pt
        c.line(x, margins['bottom'], x, margins['bottom'] + grid_height)
    
    # Draw horizontal lines
    for i in range(rows + 1):
        y = margins['bottom'] + i * square_size_pt
        c.line(margins['left'], y, margins['left'] + grid_width, y)
    
    # Draw inner grid lines if requested
    if show_inner_grid:
        c.setDash([1, 2])  # Set dashed line style for inner grid
        
        # Draw vertical inner lines
        for i in range(cols):
            x = margins['left'] + i * square_size_pt + square_size_pt/2
            c.line(x, margins['bottom'], x, margins['bottom'] + grid_height)
        
        # Draw horizontal inner lines
        for i in range(rows):
            y = margins['bottom'] + i * square_size_pt + square_size_pt/2
            c.line(margins['left'], y, margins['left'] + grid_width, y)
    
    c.save()
