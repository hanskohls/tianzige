"""Tests for the tianzige package."""

import os
import pytest
from tianzige import create_tianzige

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
