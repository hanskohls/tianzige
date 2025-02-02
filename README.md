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

This will create a PDF file with default settings (20mm squares, gray lines).

### Options

- `-c, --color`: Line color in hex format (default: #808080)
- `-s, --size`: Size of each square in mm (default: 20)
- `--margin-top`: Top margin in mm (default: 20)
- `--margin-bottom`: Bottom margin in mm (default: 20)
- `--margin-left`: Left margin in mm (default: 20)
- `--margin-right`: Right margin in mm (default: 20)
- `--no-inner-grid`: Disable inner grid lines
- `-v, --version`: Show version information

### Examples

Generate grid with black lines:
```bash
tianzige -c "#000000" output.pdf
```

Generate grid with larger squares:
```bash
tianzige -s 25 output.pdf
```

Generate grid without inner lines:
```bash
tianzige --no-inner-grid output.pdf
```

## Python API

You can also use Tianzige in your Python code:

```python
from tianzige import create_tianzige

create_tianzige(
    "output.pdf",
    line_color="#808080",
    square_size=20,
    margin_top=20,
    margin_bottom=20,
    margin_left=20,
    margin_right=20,
    show_inner_grid=True
)
```

## License

MIT License - see the [LICENSE](LICENSE) file for details.
