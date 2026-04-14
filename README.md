# Local Chrome Cookie Manager

A standalone Python desktop application that allows you to view, search, and delete Google Chrome cookies directly from your local SQLite database.

## Features
* **AES-256-GCM Decryption:** Automatically handles Windows DPAPI and AES decryption to reveal encrypted cookie values.
* **Safe Reading:** Copies the database to a temporary file, allowing you to read cookies even while Chrome is running.
* **Graphical Interface:** Built with `tkinter` for a clean, lightweight desktop UI.
* **Search & Delete:** Filter cookies by domain and delete specific cookies permanently.

## Prerequisites
* Windows OS (Required for DPAPI decryption)
* Python 3.8+
* Google Chrome installed locally

## Disclaimer
*This tool is for educational purposes and local web development testing. It accesses highly sensitive local data. Do not run this script on computers you do not own.
## Installation

1. Clone the repository:
   ```bash
   git clone [[https://github.com/Raj123-0/Cookie-Manager-main](https://github.com/Raj123-0/Cookie-Manager-main)]
   cd ChromeCookieManager
