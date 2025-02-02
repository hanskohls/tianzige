"""Tests for the tianzige package."""

import os
import sys
import pytest
from unittest.mock import patch
from tianzige import create_tianzige
from tianzige.core import (
    calculate_dimensions,
    calculate_required_size,
    hex_to_rgb,
    validate_hex_color,
    PAGE_SIZES
)
from tianzige.__main__ import main

# Utility function tests
def test_calculate_dimensions():
    """Test calculation of grid dimensions."""
    # Test with sample values (100pt square page, 10pt margins, 20pt squares)
    h_boxes, v_boxes = calculate_dimensions(
        100, 100,  # page width, height
        10, 10,    # left, right margins
        10, 10,    # top, bottom margins
        20         # square size
    )
    assert h_boxes == 4  # (100 - 10 - 10) / 20 = 4
    assert v_boxes == 4  # (100 - 10 - 10) / 20 = 4

def test_calculate_required_size():
    """Test calculation of required square size."""
    # Test with sample values (100pt square page, 10pt margins, min 3 boxes)
    size = calculate_required_size(
        100, 100,  # page width, height
        10, 10,    # left, right margins
        10, 10,    # top, bottom margins
        3, 3       # min horizontal, vertical boxes
    )
    # Available space: 80pt, need 3 boxes
    # 80/3 ≈ 26.67pt ≈ 9.4mm, should round down to 9mm
    assert size <= 9.5  # Allow for floating point imprecision

def test_hex_to_rgb():
    """Test hex color to RGB conversion."""
    # Test with and without hash prefix
    assert hex_to_rgb('#FF0000') == (1.0, 0.0, 0.0)  # Red
    assert hex_to_rgb('00FF00') == (0.0, 1.0, 0.0)   # Green
    assert hex_to_rgb('#0000FF') == (0.0, 0.0, 1.0)  # Blue
    # Test gray with floating point comparison
    rgb = hex_to_rgb('808080')
    assert len(rgb) == 3
    assert all(abs(x - 0.5019607843137255) < 0.001 for x in rgb)  # Gray

def test_validate_hex_color():
    """Test hex color validation."""
    assert validate_hex_color('#FF0000') is True
    assert validate_hex_color('00FF00') is True
    assert validate_hex_color('#0000FF') is True
    assert validate_hex_color('invalid') is False
    assert validate_hex_color('#12345') is False   # Too short
    assert validate_hex_color('#1234567') is False # Too long
    assert validate_hex_color('#GHIJKL') is False  # Invalid characters

# Basic functionality tests (existing)
def test_create_tianzige_basic():
    """Test basic PDF creation with default parameters."""
    output_file = "test_output.pdf"
    create_tianzige(output_file)
    assert os.path.exists(output_file)
    os.remove(output_file)

def test_create_tianzige_custom_color():
    """Test PDF creation with custom color."""
    output_file = "test_color.pdf"
    create_tianzige(output_file, line_color="#000000")
    assert os.path.exists(output_file)
    os.remove(output_file)

def test_invalid_color():
    """Test that invalid color raises ValueError."""
    with pytest.raises(ValueError):
        create_tianzige("test.pdf", line_color="invalid")

def test_create_tianzige_no_inner_grid():
    """Test PDF creation without inner grid."""
    output_file = "test_no_inner.pdf"
    create_tianzige(output_file, show_inner_grid=False)
    assert os.path.exists(output_file)
    os.remove(output_file)

def test_create_tianzige_custom_size():
    """Test PDF creation with custom square size."""
    output_file = "test_size.pdf"
    create_tianzige(output_file, square_size=25)
    assert os.path.exists(output_file)
    os.remove(output_file)

def test_create_tianzige_custom_margins():
    """Test PDF creation with custom margins."""
    output_file = "test_margins.pdf"
    create_tianzige(
        output_file,
        margin_top=30,
        margin_bottom=30,
        margin_left=30,
        margin_right=30
    )
    assert os.path.exists(output_file)
    os.remove(output_file)

# Page size tests
@pytest.mark.parametrize("page_size", ['a3', 'a4', 'a5', 'a6', 'b4', 'b5', 'letter', 'legal'])
def test_page_sizes(page_size):
    """Test PDF creation with different page sizes."""
    output_file = f"test_{page_size}.pdf"
    create_tianzige(output_file, page_size=page_size)
    assert os.path.exists(output_file)
    os.remove(output_file)

def test_invalid_page_size():
    """Test that invalid page size raises ValueError."""
    with pytest.raises(ValueError):
        create_tianzige("test.pdf", page_size="invalid")

# Minimum box requirement tests
def test_min_boxes():
    """Test minimum box requirements."""
    output_file = "test_min_boxes.pdf"
    create_tianzige(output_file, min_horizontal=12, min_vertical=15)
    assert os.path.exists(output_file)
    os.remove(output_file)

def test_min_boxes_with_size_conflict():
    """Test error when square size conflicts with minimum box requirements."""
    with pytest.raises(ValueError) as exc_info:
        create_tianzige(
            "test.pdf",
            square_size=30,  # Large size
            min_horizontal=20  # Many boxes
        )
    assert "horizontal boxes" in str(exc_info.value)

# CLI interface tests
def test_cli_basic(tmp_path):
    """Test basic CLI functionality."""
    output_file = str(tmp_path / "cli_test.pdf")
    with patch.object(sys, 'argv', ['tianzige', output_file]):
        main()
    assert os.path.exists(output_file)

def test_cli_with_options(tmp_path):
    """Test CLI with various options."""
    output_file = str(tmp_path / "cli_options.pdf")
    with patch.object(sys, 'argv', [
        'tianzige',
        '--color', '#000000',
        '--size', '20',
        '--page-size', 'a5',
        '--no-inner-grid',
        output_file
    ]):
        main()
    assert os.path.exists(output_file)

def test_cli_create_templates(tmp_path):
    """Test template creation functionality."""
    output_dir = str(tmp_path / "templates")
    with patch.object(sys, 'argv', [
        'tianzige',
        '--create-templates',
        output_dir
    ]):
        main()
    # Check if at least one template was created
    assert len(os.listdir(output_dir)) > 0

def test_cli_invalid_args():
    """Test CLI with invalid arguments."""
    # Test invalid color
    with patch.object(sys, 'argv', ['tianzige', '--color', 'invalid', 'test.pdf']):
        with pytest.raises(SystemExit):
            main()
    
    # Test invalid size
    with patch.object(sys, 'argv', ['tianzige', '--size', '-5', 'test.pdf']):
        with pytest.raises(SystemExit):
            main()

def test_cli_unexpected_error():
    """Test CLI handling of unexpected errors."""
    with patch.object(sys, 'argv', ['tianzige', 'test.pdf']):
        with patch('tianzige.__main__.create_tianzige', side_effect=Exception("Unexpected error")):
            with pytest.raises(SystemExit):
                main()

def test_cli_template_errors(tmp_path):
    """Test template creation error handling."""
    output_dir = str(tmp_path / "templates")
    
    # Test template creation with invalid square size
    with patch.object(sys, 'argv', [
        'tianzige',
        '--create-templates',
        output_dir
    ]):
        with patch('tianzige.create_tianzige', side_effect=[ValueError("Square size too large")] * 40):
            main()  # Should continue despite errors
            assert os.path.exists(output_dir)  # Directory should still be created

    # Test template creation with permission error
    with patch.object(sys, 'argv', [
        'tianzige',
        '--create-templates',
        '/invalid/path'
    ]):
        with pytest.raises(SystemExit):
            main()

    # Test template creation with unexpected error
    with patch.object(sys, 'argv', [
        'tianzige',
        '--create-templates',
        output_dir
    ]):
        with patch('tianzige.__main__.create_tianzige', side_effect=Exception("Unexpected error")) as mock:
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1  # Check exit code

# Edge cases and error handling
def test_invalid_margins():
    """Test with invalid margin values."""
    with pytest.raises(ValueError):
        create_tianzige("test.pdf", margin_top=-1)

def test_square_size_too_large():
    """Test with square size too large for page."""
    with pytest.raises(ValueError):
        create_tianzige("test.pdf", square_size=1000)  # Unreasonably large

@patch('reportlab.pdfgen.canvas.Canvas.save')
def test_file_system_error(mock_save):
    """Test handling of file system errors."""
    mock_save.side_effect = IOError("Permission denied")
    with pytest.raises(IOError):
        create_tianzige("/invalid/path/test.pdf")

def test_boundary_square_sizes():
    """Test boundary conditions for square sizes."""
    # Test minimum reasonable size
    create_tianzige("test_min.pdf", square_size=5)
    assert os.path.exists("test_min.pdf")
    os.remove("test_min.pdf")

    # Test maximum reasonable size that should still work with A4
    create_tianzige("test_max.pdf", square_size=50)
    assert os.path.exists("test_max.pdf")
    os.remove("test_max.pdf")

def test_grid_drawing():
    """Test grid drawing with various configurations."""
    # Test with odd number of boxes to ensure proper grid drawing
    output_file = "test_odd.pdf"
    create_tianzige(
        output_file,
        square_size=30,
        margin_top=10,
        margin_bottom=10,
        margin_left=10,
        margin_right=10,
        page_size='a5'  # Smaller page to force odd number of boxes
    )
    assert os.path.exists(output_file)
    os.remove(output_file)

    # Test with minimum margins to test edge cases in grid drawing
    output_file = "test_min_margins.pdf"
    create_tianzige(
        output_file,
        square_size=20,
        margin_top=5,
        margin_bottom=5,
        margin_left=5,
        margin_right=5
    )
    assert os.path.exists(output_file)
    os.remove(output_file)

    # Test with single box to cover edge case in grid drawing
    output_file = "test_single_box.pdf"
    create_tianzige(
        output_file,
        square_size=200,  # Large size to force single box
        margin_top=10,
        margin_bottom=10,
        margin_left=10,
        margin_right=10,
        page_size='a4'
    )
    assert os.path.exists(output_file)
    os.remove(output_file)
