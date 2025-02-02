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

This will create a PDF file with default settings (A4 size, auto-calculated square size, gray lines, optimized margins).

### Options

- `-c, --color`: Line color in hex format (default: #808080)
- `-p, --page-size`: Page size (choices: a4, a5, a6, a3, b4, b5, letter, legal) (default: a4)
- `-s, --size`: Size of each square in mm (default: auto-calculated to ensure at least 10 squares per row/column)
- `--margin-top`: Top margin in mm (default: 10)
- `--margin-bottom`: Bottom margin in mm (default: 10)
- `--margin-left`: Left margin in mm (default: 20)
- `--margin-right`: Right margin in mm (default: 10)
- `--no-inner-grid`: Disable inner grid lines
- `-v, --version`: Show version information

### Examples

Generate grid with black lines:
```bash
tianzige -c "#000000" output.pdf
```

Generate A5-sized grid:
```bash
tianzige -p a5 output.pdf
```

Generate grid with custom square size:
```bash
tianzige -s 25 output.pdf
```

Generate grid without inner lines:
```bash
tianzige --no-inner-grid output.pdf
```

Generate A3-sized grid with black lines:
```bash
tianzige -p a3 -c "#000000" output.pdf
```

## Python API

You can also use Tianzige in your Python code:

```python
from tianzige import create_tianzige

create_tianzige(
    "output.pdf",
    line_color="#808080",
    square_size=None,  # Auto-calculated based on page size
    margin_top=15,
    margin_bottom=15,
    margin_left=10,
    margin_right=20,
    show_inner_grid=True,
    page_size='a4'  # Options: 'a4', 'a5', 'a6', 'a3', 'b4', 'b5', 'letter', 'legal'
)
```

## License

MIT License - see the [LICENSE](LICENSE) file for details.
