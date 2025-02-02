# Tianzige (田字格)

A Python tool to generate Tianzige (田字格) writing grid PDFs for Chinese character practice.

## Installation

```bash
pip install tianzige
```

## Usage

Basic usage:
```bash
tianzige output.pdf
```

This will create a PDF file with default settings (A4 size, auto-calculated square size ensuring at least 10 boxes in each direction, gray lines, optimized margins).

### Options

- `-c, --color`: Line color in hex format (default: #808080)
- `-p, --page-size`: Page size (choices: a4, a5, a6, a3, b4, b5, letter, legal) (default: a4)
- `-s, --size`: Size of each square in mm (default: auto-calculated to ensure minimum boxes)
- `--min-horizontal`: Minimum number of horizontal boxes (default: 10 if size not specified)
- `--min-vertical`: Minimum number of vertical boxes (default: 10 if size not specified)
- `--margin-top`: Top margin in mm (default: 15)
- `--margin-bottom`: Bottom margin in mm (default: 15)
- `--margin-left`: Left margin in mm (default: 20)
- `--margin-right`: Right margin in mm (default: 10)
- `--no-inner-grid`: Disable inner grid lines
- `-v, --version`: Show version information

### Square Size and Box Count Behavior

1. When no size or minimum boxes specified:
   - Automatically calculates square size to fit at least 10 boxes in both directions

2. When only size specified:
   - Uses the exact size specified
   - No minimum box requirements enforced

3. When size and minimum boxes specified:
   - Uses specified size
   - Validates that minimum box requirements can be met
   - Provides detailed error message if requirements cannot be met, showing:
     * How many boxes would fit with the specified size
     * What maximum size would allow the minimum box count

### Examples

Generate grid with black lines:
```bash
tianzige -c "#000000" output.pdf
```

Generate A5-sized grid:
```bash
tianzige -p a5 output.pdf
```

Generate grid with custom square size (no minimum box requirement):
```bash
tianzige -s 25 output.pdf
```

Generate grid with at least 12 horizontal boxes:
```bash
tianzige --min-horizontal 12 output.pdf
```

Generate grid with specific requirements:
```bash
tianzige --min-horizontal 12 --min-vertical 15 -p a4 output.pdf
```

Generate grid without inner lines:
```bash
tianzige --no-inner-grid output.pdf
```

Generate A3-sized grid with black lines:
```bash
tianzige -p a3 -c "#000000" output.pdf
```

Generate template files for all formats and sizes:
```bash
tianzige --create-templates templates/    # Create in specified directory
tianzige --create-templates              # Create in sample_pdf/ directory
```

The template generator creates PDFs for all combinations of:
- Paper sizes: A3, A4, A5, A6, B4, B5, Letter, Legal
- Square sizes: 10mm, 12mm, 15mm, 20mm, 25mm

Files are named as `tianzige_[papersize]_[square size]mm.pdf`. Combinations where the square size would be too large for the paper format are automatically skipped.

## Python API

You can also use Tianzige in your Python code:

```python
from tianzige import create_tianzige

create_tianzige(
    "output.pdf",
    line_color="#808080",
    square_size=None,  # Auto-calculated based on page size and minimum boxes
    margin_top=15,
    margin_bottom=15,
    margin_left=20,
    margin_right=10,
    show_inner_grid=True,
    page_size='a4',  # Options: 'a4', 'a5', 'a6', 'a3', 'b4', 'b5', 'letter', 'legal'
    min_horizontal=None,  # Default: 10 if square_size is None
    min_vertical=None    # Default: 10 if square_size is None
)
```

## Sample PDFs

The `sample_pdf` directory contains example outputs:
- `a5_example.pdf`: A5-sized grid with default settings
- `black_20mm.pdf`: Grid with 20mm squares and black lines
- `15x15_boxes.pdf`: Grid with minimum 15 boxes in both directions

## Development

### Git Configuration

The repository includes a `.gitignore` file configured for Python development with specific rules for PDF files:
- Ignores all PDF files by default (`*.pdf`)
- Allows sample PDFs in the `sample_pdf` directory (`!sample_pdf/*.pdf`)
- Includes standard Python, virtual environment, and IDE ignores

## License

MIT License - see the [LICENSE](LICENSE) file for details.
