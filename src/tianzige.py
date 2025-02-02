#!/usr/bin/env python3
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import argparse
from typing import Tuple
import re

def hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
    """Convert hex color to RGB tuple (0-1 range)."""
    # Remove '#' if present
    hex_color = hex_color.lstrip('#')
    # Convert to RGB
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    # Convert to 0-1 range
    return tuple(x/255 for x in rgb)

def validate_hex_color(color: str) -> bool:
    """Validate hex color format."""
    pattern = r'^#?[0-9A-Fa-f]{6}$'
    return bool(re.match(pattern, color))

def create_tianzige(
    output_file: str,
    line_color: str = "#808080",
    square_size: float = 20,
    margin_top: float = 20,
    margin_bottom: float = 20,
    margin_left: float = 20,
    margin_right: float = 20,
    show_inner_grid: bool = True
) -> None:
    """
    Create a PDF with tian zi ge grid.
    
    Args:
        output_file: Path to save the PDF
        line_color: Hex color code for grid lines
        square_size: Size of each square in mm
        margin_top: Top margin in mm
        margin_bottom: Bottom margin in mm
        margin_left: Left margin in mm
        margin_right: Right margin in mm
        show_inner_grid: Whether to show internal grid lines
    """
    # Validate color format
    if not validate_hex_color(line_color):
        raise ValueError("Invalid hex color format. Use format: #RRGGBB")

    # Convert measurements to points (PDF units)
    square_size_pt = square_size * mm
    margins = {
        'top': margin_top * mm,
        'bottom': margin_bottom * mm,
        'left': margin_left * mm,
        'right': margin_right * mm
    }

    # Create PDF
    c = canvas.Canvas(output_file, pagesize=(210*mm, 297*mm))  # A4 size
    
    # Set line color
    rgb_color = hex_to_rgb(line_color)
    c.setStrokeColorRGB(*rgb_color)
    
    # Calculate available space
    width = 210*mm - margins['left'] - margins['right']
    height = 297*mm - margins['top'] - margins['bottom']
    
    # Calculate number of squares that fit
    cols = int(width // square_size_pt)
    rows = int(height // square_size_pt)
    
    # Draw vertical lines
    for i in range(cols + 1):
        x = margins['left'] + i * square_size_pt
        c.line(x, margins['bottom'], x, 297*mm - margins['top'])
    
    # Draw horizontal lines
    for i in range(rows + 1):
        y = margins['bottom'] + i * square_size_pt
        c.line(margins['left'], y, 210*mm - margins['right'], y)
    
    # Draw inner grid lines if requested
    if show_inner_grid:
        c.setDash([1, 2])  # Set dashed line style for inner grid
        
        # Draw vertical inner lines
        for i in range(cols):
            x = margins['left'] + i * square_size_pt + square_size_pt/2
            c.line(x, margins['bottom'], x, 297*mm - margins['top'])
        
        # Draw horizontal inner lines
        for i in range(rows):
            y = margins['bottom'] + i * square_size_pt + square_size_pt/2
            c.line(margins['left'], y, 210*mm - margins['right'], y)
    
    c.save()

def main():
    parser = argparse.ArgumentParser(description='Generate Tian Zi Ge PDF')
    parser.add_argument('--output', '-o', default='tianzige.pdf',
                      help='Output PDF file name')
    parser.add_argument('--color', '-c', default='#808080',
                      help='Line color in hex format (e.g., #808080)')
    parser.add_argument('--size', '-s', type=float, default=20,
                      help='Size of each square in mm')
    parser.add_argument('--margin-top', type=float, default=20,
                      help='Top margin in mm')
    parser.add_argument('--margin-bottom', type=float, default=20,
                      help='Bottom margin in mm')
    parser.add_argument('--margin-left', type=float, default=20,
                      help='Left margin in mm')
    parser.add_argument('--margin-right', type=float, default=20,
                      help='Right margin in mm')
    parser.add_argument('--no-inner-grid', action='store_true',
                      help='Disable inner grid lines')
    
    args = parser.parse_args()
    
    create_tianzige(
        args.output,
        args.color,
        args.size,
        args.margin_top,
        args.margin_bottom,
        args.margin_left,
        args.margin_right,
        not args.no_inner_grid
    )

if __name__ == "__main__":
    main()