# Catering Execution Generator

A web app that turns a stack of catering order receipts into a single **catering execution sheet**: an Excel prep sheet listing how many of each sandwich, wrap, box and side to make, the meat and cheese portions to slice, bread totals, and each order's ready time.

Built in summer 2024 to replace the hand-tallying a sandwich shop's staff did before every large catering day.

## How it works

```
Upload receipts (PDF / JPG / PNG)          React frontend
        │  POST /upload
        ▼
Flask server saves files ──► ReceiptScanner   PDF text extraction (PyMuPDF),
                                 │            falling back to Google Cloud Vision OCR
                                 ▼
                             Organizer        regex parsing of menu items and quantities
                                 │            into per-item counts, plus ingredient math
                                 ▼
                          SpreadsheetMaker    formatted .xlsx (openpyxl): order totals,
                                              slicing prep, sides needed, highlights
        ◄── download catering_execution_sheet.xlsx
```

- **OCR pipeline:** each PDF page goes through plain-text extraction first. Only image-only pages are sent to Google Vision, which keeps API calls down.
- **Parsing:** menu items are kept in dictionaries that map each item to its ingredient portions, so the total slicing prep (ham, turkey, roast beef, cheese, bacon and so on) falls out of the order counts.
- **Output:** a styled spreadsheet with merged headers, highlighted ranges and auto-sized columns, ready to print.

## Tech

Python · Flask · Google Cloud Vision · PyMuPDF · Pillow · pandas · openpyxl · React · Axios

## Running locally

Requires Python 3.11+, Node 18+, and a Google Cloud service account with the Vision API enabled.

```sh
# backend
cd backend
pip install -r requirements.txt
# put your service-account key at backend/googlevisionapi.json (gitignored)
python server.py            # http://localhost:5000

# frontend (separate terminal)
cd frontend
npm install
npm start                   # http://localhost:3000
```

## Status

A working prototype that was used on real orders. The menu is hardcoded to one shop's items in `backend/Organizer.py`.
