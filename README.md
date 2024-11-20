# Business Card Generator

This project generates a customizable business card in SVG format using Python. The business card details and design elements are configurable through a JSON configuration file.

## Features

- Customizable business card details (name, phone, email, job title, organization, URL)
- Configurable colors and design elements
- Generates a QR code with contact information
- Supports random seed for reproducible designs

## Requirements

- Python 3.10 or higher
- `svgwrite` library
- `segno` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/noatgnu/businesscard.git
    cd businesscard
    ```

2. Install the required Python packages:
    ```sh
    pip install svgwrite segno
    ```

## Configuration

Create a `config.json` file in the project directory with the following structure:

```json
{
  "name": "",
  "phone": "",
  "email": "",
  "job_title": "",
  "org": "",
  "url": "",
  "fill_color": "#4365E1",
  "back_color": "white",
  "qr_code_x": 10,
  "qr_code_y": 10,
  "qr_code_size": 60,
  "border_width": 5,
  "panel_width": 25,
  "panel_height": 15,
  "panel_x_offset": 10,
  "panel_y_offset": 10,
  "seed": "optional-seed-value"
}
```

- `seed` is optional. If not provided, a new seed will be generated.

## Usage

Run the script to generate the business card:

```sh
python main.py
```

The script will generate two SVG files: `business_card.svg` and `business_card_back.svg`.

## License

This project is licensed under the MIT License.