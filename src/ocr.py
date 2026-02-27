# from typing import List
# from pathlib import Path
# import numpy as np
# import os

# os.environ["FLAGS_use_mkldnn"] = "0"
# os.environ["FLAGS_use_mkl"] = "0"
# os.environ["OMP_NUM_THREADS"] = "1"

# import paddle
# from paddleocr import PaddleOCR
# from pdf2image import convert_from_path

# # 2. Modern Paddle 3.x flag setting (Replacing the fluid call)
# # In 3.x, flags are managed through the core directly or via the global config
# try:
#     paddle.set_flags({"FLAGS_use_mkldnn": 0})
# except AttributeError:
#     # If the above isn't available in your specific build:
#     pass

# paddle.device.set_device('cpu')

# # 3. Initialize OCR Engine
# # Note: I've updated this to PP-OCRv4 for better Win/3.x compatibility
# ocr_engine = PaddleOCR(
#     use_angle_cls=True, 
#     lang="en", 
#     use_gpu=False,          
#     show_log=False,      
#     ocr_version="PP-OCRv4" 
# )


# def ocr_pdf(path: Path) -> str:

#     if not path.exists():
#         raise FileNotFoundError(f"File not found: {path}")

#     text: List[str] = []

#     pages = convert_from_path(path, dpi=300)

#     for page_num, page_img in enumerate(pages, 1):

#         img_arr = np.array(page_img)[:, :, ::-1]  # RGB → BGR

#         result = ocr_engine.ocr(img_arr, cls=True)

#         if result and result[0]:
#             for line in result[0]:
#                 text.append(line[1][0])

#         if page_num < len(pages):
#             text.append(f"\n--- Page {page_num} ---\n")

#     return "\n".join(text)


# def ocr_image(path: str | Path) -> str:

#     path = Path(path)

#     if not path.exists():
#         raise FileNotFoundError(f"File not found: {path}")

#     result = ocr_engine.ocr(str(path), cls=True)

#     text = []

#     if result and result[0]:
#         for line in result[0]:
#             text.append(line[1][0])

#     return "\n".join(text)


# def need_ocr(text: str, min_length: int = 100) -> bool:

#     if not text:
#         return True

#     if len(text.strip()) < min_length:
#         return True

#     return False

import logging
from pathlib import Path
from typing import List, Optional

# Docling imports
from docling.datamodel.accelerator_options import AcceleratorOptions, AcceleratorDevice
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat

# Optional: suppress noisy logs
logging.basicConfig(level=logging.ERROR)

class OCRProcessor:
    def __init__(self):
        pipeline_options = PdfPipelineOptions()
        
        # 1. Hardware acceleration is set here, not in ocr_options
        pipeline_options.accelerator_options = AcceleratorOptions(
            device=AcceleratorDevice.CPU  # Forces CPU for stability on Windows
        )
        
        # 2. Configure OCR behavior
        pipeline_options.do_ocr = True
        
        # If you specifically want to use EasyOCR and force full page
        # you must use the specific engine options class
        pipeline_options.ocr_options = EasyOcrOptions(
            force_full_page_ocr=True,
            lang=["en"]
        )

        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

    def extract_content(self, path: Path) -> str:
        if not path.exists():
            return ""
        try:
            result = self.converter.convert(path)
            # Markdown will preserve the "--- PAGE X ---" structure you need
            return result.document.export_to_markdown()
        except Exception as e:
            print(f"Extraction failed: {e}")
            return ""
        


# Global instance for easy importing
_processor = OCRProcessor()

def ocr_pdf(path: Path) -> str:
    return _processor.extract_content(path)

def ocr_image(path: Path) -> str:
    return _processor.extract_content(path)

def need_ocr(text: str, min_length: int = 100) -> bool:
    """Check if the extracted text is too sparse."""
    if not text or len(text.strip()) < min_length:
        return True
    return False