# Local Chrome Cookie Manager

A standalone Python desktop application that allows you to view, search, and delete Google Chrome cookies directly from your local SQLite database.

## Features

- **AES-256-GCM Decryption:** Automatically handles Windows DPAPI and AES decryption to reveal encrypted cookie values.
- **Safe Reading:** Copies the database to a temporary file, allowing you to read cookies even while Chrome is running.
- **Graphical Interface:** Built with `tkinter` for a clean, lightweight desktop UI.
- **Search & Delete:** Filter cookies by domain and delete specific cookies permanently.

## Prerequisites

- Windows OS (Required for DPAPI decryption)
- Python 3.8+
- Google Chrome installed locally

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Raj123-0/Cookie-Manager-main.git
   cd Cookie-Manager-main
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure Google Chrome is installed on your machine.
2. Run the application:
   ```bash
   python cookie_manager.py
   ```
3. Click **Load / Refresh** to view all stored cookies.
4. Use the **Search Domain** field to filter by domain name.
5. Select a cookie and click **Delete Selected** to remove it (Chrome must be closed).

## Security Notice

This tool accesses sensitive local browser data. Only run it on computers you own. Deleted cookies cannot be recovered. Always close Chrome completely before deleting cookies to avoid database lock errors.

## License

This project is provided as-is for educational purposes and local web development testing.
