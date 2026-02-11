import os
import shutil
from datetime import datetime
from pathlib import Path
from .utils.pdf_preprocessor import PDFProcessor
from .utils.audio_preprocessor import AudioProcessor
from .utils.image_preprocessor import ImageDescriber

current_file = Path(__file__)
save_directory = current_file.parent.parent / 'LTM' / 'LearnedMaterial'
processed_directory = current_file.parent.parent.parent / 'sources' / 'processed'


def call_image_preprocess(image_path: str,  openai_api: str) -> tuple[str, dict]:
    id = ImageDescriber(openai_api)
    extracted_text = id.describe_image(image_path)

    time_stamp_micro = datetime.now().strftime("%Y%m%d%H%M%S%f")
    image_name = os.path.basename(image_path).replace('.png', '')
    save_path = save_directory / f'{image_name}_image_extracted_text_{time_stamp_micro}.txt'
    metadata = id.get_image_metadata(image_path)

    # Save extracted text as a text file
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(extracted_text)

    return extracted_text, metadata


def call_audio_preprocess(audio_path: str) -> tuple[str, int]:
    ap = AudioProcessor()
    extracted_text, duration = ap.process_audio_file(audio_path)

    time_stamp_micro = datetime.now().strftime("%Y%m%d%H%M%S%f")
    audio_name = os.path.basename(audio_path).replace('.wav', '')
    save_path = save_directory / f'{audio_name}_audio_extracted_text_{time_stamp_micro}.txt'

    # Save extracted text as a text file
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(extracted_text)

    return extracted_text, duration


def call_pdf_preprocess(pdf_path: str, openai_api: str) -> tuple[str, int]:
    api_key = openai_api

    if not api_key:
        print('API key not found. Set the OPENAI_API_KEY environment variable.')
        raise

    # Initialize PDFProcessor
    pdf_processor = PDFProcessor(pdf_path, api_key)
    extracted_text, page_count = pdf_processor.parse_pdf()
    time_stamp_micro = datetime.now().strftime("%Y%m%d%H%M%S%f")
    ebook_name = os.path.basename(pdf_path).replace('.pdf', '')
    save_path = save_directory / f'{ebook_name}_pdf_extracted_text_{time_stamp_micro}.txt'

    # Save extracted text as a text file
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(extracted_text)

    for file_path in save_directory.glob(f'image_{ebook_name}_page_*_*.png'):
        shutil.move(str(file_path), processed_directory / file_path.name)

    # Delete duplicate images if needed
    pdf_processor.delete_duplicate_images()
    return extracted_text, page_count
