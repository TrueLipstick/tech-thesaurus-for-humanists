# Open WebUI with Tesseract OCR support
# Extends the official Open WebUI image with OCR dependencies
#
# Build:
#   docker build -t open-webui-ocr .
#
# Run:
#   docker run -d \
#     --name open-webui-ocr \
#     -p 3000:8080 \
#     -v open-webui-data:/app/backend/data \
#     open-webui-ocr

FROM ghcr.io/open-webui/open-webui:main

# Install Tesseract OCR engine and language packs
# Add more tesseract-ocr-<lang> packages for additional languages
# Full list: https://packages.debian.org/search?keywords=tesseract-ocr-
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-swe \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies for the OCR tool
RUN pip install --no-cache-dir \
    PyMuPDF \
    pytesseract \
    Pillow

# Verify Tesseract installation
RUN tesseract --version && tesseract --list-langs
