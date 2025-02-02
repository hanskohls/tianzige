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

def calculate_square_size(
    page_width: float,
    page_height: float,
    margin_left: float,
    margin_right: float,
    margin_top: float,
    margin_bottom: float,
    min_squares: int = 10
) -> float:
    """Calculate optimal square size to ensure minimum number of squares fit.
    
    Args:
        page_width: Page width in points
        page_height: Page height in points
        margin_left: Left margin in points
        margin_right: Right margin in points
        margin_top: Top margin in points
        margin_bottom: Bottom margin in points
        min_squares: Minimum number of squares required per row/column
        
    Returns:
        Optimal square size in mm
    """
    # Available space in points
    available_width = page_width - margin_left - margin_right
    available_height = page_height - margin_top - margin_bottom
    
    # Calculate maximum square size that allows min_squares in both dimensions
    max_square_size = min(
        available_width / min_squares,
        available_height / min_squares
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
    margin_left: float = 10,
    margin_right: float = 20,
    show_inner_grid: bool = True,
    page_size: PageSizeType = 'a4'
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
    
    # Calculate square size if not provided
    if square_size is None:
        square_size = calculate_square_size(
            page_width, page_height,
            margins['left'], margins['right'],
            margins['top'], margins['bottom']
        )
    
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
