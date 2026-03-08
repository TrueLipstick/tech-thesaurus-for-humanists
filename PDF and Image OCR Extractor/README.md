# 📄 Open WebUI PDF & Image OCR Text Extractor

A fully offline Open WebUI **Tool** that enables LLM models to extract text from PDFs and images using **Tesseract OCR**.

## Features

- **Text-based PDF extraction** — Fast direct text extraction using PyMuPDF
- **Scanned/image PDF OCR** — Automatic detection of image-only pages with Tesseract OCR fallback
- **Standalone image OCR** — OCR for PNG, JPG, JPEG, TIFF, BMP, GIF, WEBP
- **Smart page detection** — Automatically determines if a page needs OCR based on text content threshold
- **Multi-language support** — English + Swedish by default, easily configurable for any Tesseract language
- **Dual input modes** — Process chat-uploaded files OR files by server path/URL
- **Multiple output formats** — Plain text, Markdown, or save-to-file options
- **Real-time progress** — Status updates via Open WebUI event emitters
- **Fully offline** — No external API calls, all processing happens locally

## Prerequisites

- Docker installed on your system
- An existing Open WebUI setup (or willingness to set one up)

## Quick Start

### 1. Build the Docker Image

The custom Dockerfile extends the official Open WebUI image with Tesseract OCR and Python dependencies.

```bash
cd openwebui-ocr-tool

# Option A: Using docker-compose (recommended)
docker-compose up -d --build

# Option B: Manual build and run
docker build -t open-webui-ocr .
docker run -d \
  --name open-webui-ocr \
  -p 3000:8080 \
  -v open-webui-data:/app/backend/data \
  open-webui-ocr
```

### 2. Install the Tool in Open WebUI

1. Open your Open WebUI instance (default: `http://localhost:3000`)
2. Navigate to **Workspace** → **Tools** → **Create New Tool** (+ button)
3. Give it a name: `PDF & Image OCR Extractor`
4. Copy the entire contents of [`pdf_ocr_tool.py`](pdf_ocr_tool.py) and paste it into the code editor
5. Click **Save**

### 3. Configure Valves (Optional)

After saving the tool, click the **gear icon** ⚙️ to configure:

| Setting | Default | Description |
|---|---|---|
| `ocr_languages` | `eng+swe` | Tesseract language codes (`+` separated) |
| `text_threshold` | `50` | Min chars per page before OCR kicks in |
| `dpi` | `300` | Image rendering quality for OCR |
| `max_pages` | `250` | Max PDF pages to process (0 = unlimited) |
| `output_format` | `markdown` | Output style: `text`, `markdown`, `save_txt`, `save_md` |

### 4. Enable the Tool for Your Models

1. Go to **Workspace** → **Models**
2. Select a model (e.g., your Ollama model or OpenAI model)
3. Under **Tools**, enable **PDF & Image OCR Extractor**
4. Save

### 5. Use It!

Upload a PDF or image to the chat and ask the model to extract text:

> "Extract all text from this PDF"

> "OCR this scanned document"

> "Read the text in this image"

Or provide a file path:

> "Extract text from /app/backend/data/uploads/report.pdf"

## Adding More Languages

### Step 1: Install language packs in Docker

Edit the `Dockerfile` and add more `tesseract-ocr-<lang>` packages:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-swe \
    tesseract-ocr-deu \
    tesseract-ocr-fra \
    tesseract-ocr-nor \
    tesseract-ocr-dan \
    && rm -rf /var/lib/apt/lists/*
```

Rebuild the image:

```bash
docker-compose up -d --build
```

### Step 2: Update the Valve

In Open WebUI, update the `ocr_languages` valve to include the new languages:

```
eng+swe+deu+fra+nor+dan
```

### Available Language Codes

| Code | Language |
|---|---|
| `eng` | English |
| `swe` | Swedish |
| `deu` | German |
| `fra` | French |
| `nor` | Norwegian |
| `dan` | Danish |
| `fin` | Finnish |
| `spa` | Spanish |
| `ita` | Italian |
| `nld` | Dutch |
| `por` | Portuguese |
| `pol` | Polish |
| `rus` | Russian |
| `chi_sim` | Chinese (Simplified) |
| `chi_tra` | Chinese (Traditional) |
| `jpn` | Japanese |
| `kor` | Korean |
| `ara` | Arabic |

Full list: [Tesseract Language Data](https://github.com/tesseract-ocr/tessdata)

## Output Formats

### `text` — Plain Text

```
Source: report.pdf
Pages: 3 of 3 | OCR'd: 1

--- Page 1 ---
Lorem ipsum dolor sit amet...

--- Page 2 [OCR] ---
Scanned text extracted via OCR...

--- Page 3 ---
More text content...
```

### `markdown` — Markdown (Default)

```markdown
# Extracted Text: report.pdf

**Pages processed:** 3 of 3 | **OCR'd pages:** 1

---

## Page 1

Lorem ipsum dolor sit amet...

## Page 2 *(OCR)*

Scanned text extracted via OCR...

## Page 3

More text content...
```

### `save_txt` / `save_md` — Save to File

Same as `text`/`markdown` respectively, but also saves the output as a `.txt` or `.md` file alongside the source file.

## Migrating an Existing Open WebUI Instance

If you already have Open WebUI running in Docker:

### Option A: Rebuild with the custom Dockerfile

1. Stop your current container:
   ```bash
   docker stop open-webui
   ```

2. Build the new image:
   ```bash
   docker build -t open-webui-ocr -f Dockerfile .
   ```

3. Start with the same volume:
   ```bash
   docker run -d \
     --name open-webui-ocr \
     -p 3000:8080 \
     -v open-webui-data:/app/backend/data \
     open-webui-ocr
   ```

### Option B: Install into running container (temporary)

```bash
docker exec -it open-webui bash
apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-swe
pip install PyMuPDF pytesseract Pillow
exit
```

> ⚠️ **Warning:** Option B changes are lost when the container restarts. Use Option A for production.

## Troubleshooting

### "Tesseract is not installed or not in PATH"

Tesseract is not available in the container. Rebuild with the custom Dockerfile:

```bash
docker-compose up -d --build
```

### "Error: Could not find uploaded file with ID '...'"

The tool couldn't locate the file in Open WebUI's storage. This can happen if:
- The file ID is incorrect
- Open WebUI stores files in a non-standard location

Check your Open WebUI data directory structure:
```bash
docker exec -it open-webui-ocr ls -la /app/backend/data/uploads/
```

### OCR quality is poor

Try these adjustments:
1. **Increase DPI** — Set the `dpi` valve to `400` or `600` (slower but better quality)
2. **Check language** — Ensure the correct language pack is installed and configured
3. **Image quality** — Higher resolution source images produce better OCR results

### Tool not appearing in chat

1. Ensure the tool is saved in **Workspace → Tools**
2. Ensure the tool is enabled for the model you're using
3. Try refreshing the page

## File Structure

```
openwebui-ocr-tool/
├── pdf_ocr_tool.py       # The Open WebUI Tool (paste into Tools UI)
├── Dockerfile            # Custom Docker image with Tesseract
├── docker-compose.yml    # Docker Compose configuration
└── README.md             # This file
```

## License

MIT — Use freely in your Open WebUI deployment.
