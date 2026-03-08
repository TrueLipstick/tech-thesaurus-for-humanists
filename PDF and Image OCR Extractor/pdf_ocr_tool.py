"""
title: PDF & Image OCR Text Extractor
author: OpenWebUI Community
version: 1.0.0
description: Extracts text from PDFs and images using Tesseract OCR. Supports text-based PDFs (direct extraction) and scanned/image PDFs (OCR). Fully offline.
required_open_webui_version: 0.4.0
requirements: PyMuPDF, pytesseract, Pillow
"""

import os
import io
import tempfile
import asyncio
from typing import Optional
from pathlib import Path

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from pydantic import BaseModel, Field


class Tools:
    """
    PDF & Image OCR Text Extractor for Open WebUI.

    Provides two tool methods:
    - extract_text_from_upload: processes files uploaded to the chat
    - extract_text_from_path: processes files by server path or URL

    Uses PyMuPDF for text-based PDF extraction and Tesseract OCR for
    scanned/image-based PDFs and standalone images.
    """

    class Valves(BaseModel):
        ocr_languages: str = Field(
            default="eng+swe",
            description="Tesseract OCR language codes, '+' separated (e.g., 'eng+swe+deu'). "
            "Must have corresponding tesseract-ocr-<lang> packages installed.",
        )
        text_threshold: int = Field(
            default=50,
            description="Minimum number of characters per PDF page to consider it text-based. "
            "Pages with fewer characters will be OCR'd instead.",
        )
        dpi: int = Field(
            default=300,
            description="DPI resolution for rendering PDF pages to images before OCR. "
            "Higher values = better quality but slower processing.",
        )
        max_pages: int = Field(
            default=250,
            description="Maximum number of PDF pages to process. Set to 0 for unlimited.",
        )
        output_format: str = Field(
            default="markdown",
            description="Output format: 'text' (plain with --- separators), "
            "'markdown' (with ## headers), 'save_txt' (return + save .txt), "
            "'save_md' (return + save .md).",
        )

    def __init__(self):
        """Initialize the PDF & OCR Tool."""
        self.valves = self.Valves()

    # ─────────────────────────────────────────────
    # Public Tool Methods (called by the LLM)
    # ─────────────────────────────────────────────

    async def extract_text_from_upload(
        self,
        file_id: str,
        __event_emitter__=None,
        __user__: Optional[dict] = None,
    ) -> str:
        """
        Extract text from a file uploaded to the chat.
        Supports PDF, PNG, JPG, JPEG, TIFF, BMP, GIF, and WEBP files.
        Uses direct text extraction for text-based PDFs and Tesseract OCR for scanned/image content.

        :param file_id: The ID of the uploaded file in Open WebUI (from the chat attachment).
        :return: The extracted text content from the file.
        """
        await self._emit_status(__event_emitter__, "Starting text extraction from uploaded file...", done=False)

        try:
            # Resolve the file path from the Open WebUI file storage
            file_path = self._resolve_upload_path(file_id)

            if not file_path:
                return f"Error: Could not find uploaded file with ID '{file_id}'. Please ensure the file is attached to the chat."

            if not os.path.exists(file_path):
                return f"Error: File not found at path '{file_path}'."

            result = await self._process_file(file_path, __event_emitter__)
            return result

        except Exception as e:
            error_msg = f"Error extracting text from uploaded file: {str(e)}"
            await self._emit_status(__event_emitter__, error_msg, done=True)
            return error_msg

    async def extract_text_from_path(
        self,
        file_path: str,
        __event_emitter__=None,
    ) -> str:
        """
        Extract text from a file at a given server path or URL.
        Supports PDF, PNG, JPG, JPEG, TIFF, BMP, GIF, and WEBP files.
        Uses direct text extraction for text-based PDFs and Tesseract OCR for scanned/image content.

        :param file_path: Absolute path to a file on the server, or an HTTP/HTTPS URL to download.
        :return: The extracted text content from the file.
        """
        await self._emit_status(__event_emitter__, f"Starting text extraction from: {file_path}", done=False)

        temp_file = None
        try:
            actual_path = file_path

            # Handle URLs - download to temp file
            if file_path.startswith(("http://", "https://")):
                await self._emit_status(__event_emitter__, "Downloading file from URL...", done=False)
                temp_file = await self._download_url(file_path)
                if temp_file is None:
                    return f"Error: Failed to download file from URL '{file_path}'."
                actual_path = temp_file

            if not os.path.exists(actual_path):
                return f"Error: File not found at path '{actual_path}'."

            result = await self._process_file(actual_path, __event_emitter__)
            return result

        except Exception as e:
            error_msg = f"Error extracting text from file: {str(e)}"
            await self._emit_status(__event_emitter__, error_msg, done=True)
            return error_msg

        finally:
            # Clean up temp file if we downloaded from URL
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except OSError:
                    pass

    # ─────────────────────────────────────────────
    # Internal Processing Methods
    # ─────────────────────────────────────────────

    async def _process_file(self, file_path: str, event_emitter=None) -> str:
        """Route file to the appropriate processor based on extension."""
        ext = Path(file_path).suffix.lower()

        pdf_extensions = {".pdf"}
        image_extensions = {".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".gif", ".webp"}

        if ext in pdf_extensions:
            return await self._process_pdf(file_path, event_emitter)
        elif ext in image_extensions:
            return await self._process_image(file_path, event_emitter)
        else:
            supported = ", ".join(sorted(pdf_extensions | image_extensions))
            return (
                f"Error: Unsupported file type '{ext}'. "
                f"Supported types: {supported}"
            )

    async def _process_pdf(self, file_path: str, event_emitter=None) -> str:
        """
        Process a PDF file:
        - Extract text directly from text-based pages (PyMuPDF)
        - Render and OCR image-based/scanned pages (Tesseract)
        """
        try:
            doc = fitz.open(file_path)
        except Exception as e:
            return f"Error: Could not open PDF file: {str(e)}"

        total_pages = len(doc)
        max_pages = self.valves.max_pages if self.valves.max_pages > 0 else total_pages
        pages_to_process = min(total_pages, max_pages)
        truncated = total_pages > pages_to_process

        await self._emit_status(
            event_emitter,
            f"Processing PDF: {pages_to_process} of {total_pages} pages...",
            done=False,
        )

        pages_text = []
        ocr_count = 0

        for page_num in range(pages_to_process):
            page = doc[page_num]

            # Try direct text extraction first
            text = page.get_text("text").strip()

            if len(text) >= self.valves.text_threshold:
                # Page has sufficient text — use direct extraction
                pages_text.append((page_num + 1, text, False))
            else:
                # Page is likely scanned/image-based — render and OCR
                await self._emit_status(
                    event_emitter,
                    f"Running OCR on page {page_num + 1} of {pages_to_process} (scanned/image page)...",
                    done=False,
                )

                ocr_text = await self._ocr_pdf_page(page)
                ocr_count += 1

                if ocr_text.strip():
                    pages_text.append((page_num + 1, ocr_text.strip(), True))
                else:
                    pages_text.append((page_num + 1, "[No text detected on this page]", True))

            # Emit progress every 10 pages
            if (page_num + 1) % 10 == 0:
                await self._emit_status(
                    event_emitter,
                    f"Processed {page_num + 1} of {pages_to_process} pages...",
                    done=False,
                )

        doc.close()

        # Format output
        output = self._format_output(pages_text, file_path, total_pages, ocr_count, truncated)

        # Optionally save to file
        saved_path = self._save_output_if_needed(output, file_path)

        summary = f"Extraction complete! Processed {pages_to_process} pages ({ocr_count} via OCR)."
        if truncated:
            summary += f" Truncated at {max_pages} pages (total: {total_pages})."
        if saved_path:
            summary += f" Saved to: {saved_path}"

        await self._emit_status(event_emitter, summary, done=True)

        return output

    async def _process_image(self, file_path: str, event_emitter=None) -> str:
        """Process a standalone image file with Tesseract OCR."""
        await self._emit_status(event_emitter, "Running OCR on image...", done=False)

        try:
            image = Image.open(file_path)
        except Exception as e:
            return f"Error: Could not open image file: {str(e)}"

        try:
            text = await self._ocr_image(image)
        except Exception as e:
            return f"Error during OCR: {str(e)}"
        finally:
            image.close()

        if not text.strip():
            await self._emit_status(event_emitter, "OCR complete — no text detected.", done=True)
            return "No text was detected in the image. The image may be blank, contain only graphics, or the text may be unreadable."

        # Format as single page
        pages_text = [(1, text.strip(), True)]
        output = self._format_output(pages_text, file_path, 1, 1, False)

        saved_path = self._save_output_if_needed(output, file_path)

        summary = "OCR extraction complete!"
        if saved_path:
            summary += f" Saved to: {saved_path}"

        await self._emit_status(event_emitter, summary, done=True)

        return output

    async def _ocr_pdf_page(self, page) -> str:
        """Render a PDF page to an image and run OCR on it."""
        # Render page at configured DPI
        zoom = self.valves.dpi / 72  # 72 is the default PDF DPI
        matrix = fitz.Matrix(zoom, zoom)
        pixmap = page.get_pixmap(matrix=matrix)

        # Convert pixmap to PIL Image
        img_data = pixmap.tobytes("png")
        image = Image.open(io.BytesIO(img_data))

        try:
            text = await self._ocr_image(image)
        finally:
            image.close()

        return text

    async def _ocr_image(self, image) -> str:
        """Run Tesseract OCR on a PIL Image."""
        # Run OCR in a thread pool to avoid blocking the event loop
        loop = asyncio.get_event_loop()
        text = await loop.run_in_executor(
            None,
            lambda: pytesseract.image_to_string(
                image,
                lang=self.valves.ocr_languages,
            ),
        )
        return text

    # ─────────────────────────────────────────────
    # Output Formatting
    # ─────────────────────────────────────────────

    def _format_output(
        self,
        pages_text: list,
        source_path: str,
        total_pages: int,
        ocr_count: int,
        truncated: bool,
    ) -> str:
        """Format extracted text according to the configured output format."""
        fmt = self.valves.output_format.lower().replace("save_", "")
        filename = Path(source_path).name

        if fmt == "text":
            return self._format_plain_text(pages_text, filename, total_pages, ocr_count, truncated)
        else:  # markdown (default)
            return self._format_markdown(pages_text, filename, total_pages, ocr_count, truncated)

    def _format_plain_text(
        self, pages_text: list, filename: str, total_pages: int, ocr_count: int, truncated: bool
    ) -> str:
        """Format output as plain text with simple separators."""
        lines = []
        lines.append(f"Source: {filename}")
        lines.append(f"Pages: {len(pages_text)} of {total_pages} | OCR'd: {ocr_count}")
        if truncated:
            lines.append(f"[TRUNCATED — only first {len(pages_text)} pages processed]")
        lines.append("")

        for page_num, text, was_ocr in pages_text:
            method = " [OCR]" if was_ocr else ""
            lines.append(f"--- Page {page_num}{method} ---")
            lines.append(text)
            lines.append("")

        return "\n".join(lines)

    def _format_markdown(
        self, pages_text: list, filename: str, total_pages: int, ocr_count: int, truncated: bool
    ) -> str:
        """Format output as markdown with headers."""
        lines = []
        lines.append(f"# Extracted Text: {filename}")
        lines.append("")
        lines.append(f"**Pages processed:** {len(pages_text)} of {total_pages} | **OCR'd pages:** {ocr_count}")
        if truncated:
            lines.append(f"> ⚠️ **Truncated** — only the first {len(pages_text)} pages were processed.")
        lines.append("")
        lines.append("---")
        lines.append("")

        for page_num, text, was_ocr in pages_text:
            method = " *(OCR)*" if was_ocr else ""
            lines.append(f"## Page {page_num}{method}")
            lines.append("")
            lines.append(text)
            lines.append("")

        return "\n".join(lines)

    def _save_output_if_needed(self, output: str, source_path: str) -> Optional[str]:
        """Save output to a file if the output_format is save_txt or save_md."""
        fmt = self.valves.output_format.lower()

        if fmt == "save_txt":
            ext = ".txt"
        elif fmt == "save_md":
            ext = ".md"
        else:
            return None

        # Save alongside the source file or in a temp directory
        source = Path(source_path)
        output_filename = source.stem + "_extracted" + ext

        # Try to save in the same directory as the source
        output_path = source.parent / output_filename
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output)
            return str(output_path)
        except (PermissionError, OSError):
            # Fall back to temp directory
            temp_dir = tempfile.gettempdir()
            output_path = Path(temp_dir) / output_filename
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(output)
                return str(output_path)
            except Exception:
                return None

    # ─────────────────────────────────────────────
    # File Resolution Helpers
    # ─────────────────────────────────────────────

    def _resolve_upload_path(self, file_id: str) -> Optional[str]:
        """
        Resolve an Open WebUI file ID to a filesystem path.

        Open WebUI stores uploaded files in its data directory.
        Common paths:
        - /app/backend/data/uploads/<file_id>_<filename>
        - /app/backend/data/cache/uploads/<file_id>
        """
        # Common Open WebUI upload directories
        upload_dirs = [
            "/app/backend/data/uploads",
            "/app/backend/data/cache/uploads",
            "/app/backend/data/files",
        ]

        for upload_dir in upload_dirs:
            if not os.path.isdir(upload_dir):
                continue

            # Look for files matching the file_id
            try:
                for entry in os.listdir(upload_dir):
                    if file_id in entry:
                        full_path = os.path.join(upload_dir, entry)
                        if os.path.isfile(full_path):
                            return full_path
            except OSError:
                continue

        # Try treating file_id as a direct path
        if os.path.isfile(file_id):
            return file_id

        return None

    async def _download_url(self, url: str) -> Optional[str]:
        """Download a file from a URL to a temporary location."""
        try:
            import httpx

            async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
                response = await client.get(url)
                response.raise_for_status()

                # Determine file extension from URL or content type
                url_path = Path(url.split("?")[0])
                ext = url_path.suffix.lower() if url_path.suffix else ""

                if not ext:
                    content_type = response.headers.get("content-type", "")
                    ext = self._content_type_to_ext(content_type)

                # Write to temp file
                temp_fd, temp_path = tempfile.mkstemp(suffix=ext)
                try:
                    with os.fdopen(temp_fd, "wb") as f:
                        f.write(response.content)
                    return temp_path
                except Exception:
                    os.close(temp_fd)
                    os.unlink(temp_path)
                    return None

        except ImportError:
            # Fall back to requests if httpx is not available
            try:
                import requests

                response = requests.get(url, timeout=60, allow_redirects=True)
                response.raise_for_status()

                url_path = Path(url.split("?")[0])
                ext = url_path.suffix.lower() if url_path.suffix else ""

                if not ext:
                    content_type = response.headers.get("content-type", "")
                    ext = self._content_type_to_ext(content_type)

                temp_fd, temp_path = tempfile.mkstemp(suffix=ext)
                try:
                    with os.fdopen(temp_fd, "wb") as f:
                        f.write(response.content)
                    return temp_path
                except Exception:
                    os.close(temp_fd)
                    os.unlink(temp_path)
                    return None

            except Exception:
                return None

        except Exception:
            return None

    @staticmethod
    def _content_type_to_ext(content_type: str) -> str:
        """Map content-type header to file extension."""
        mapping = {
            "application/pdf": ".pdf",
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/tiff": ".tiff",
            "image/bmp": ".bmp",
            "image/gif": ".gif",
            "image/webp": ".webp",
        }
        for ct, ext in mapping.items():
            if ct in content_type:
                return ext
        return ""

    # ─────────────────────────────────────────────
    # Event Emitter Helper
    # ─────────────────────────────────────────────

    @staticmethod
    async def _emit_status(event_emitter, description: str, done: bool = False):
        """Emit a status event to the Open WebUI UI."""
        if event_emitter:
            await event_emitter(
                {
                    "type": "status",
                    "data": {"description": description, "done": done},
                }
            )
