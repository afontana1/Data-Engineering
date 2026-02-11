import os
from typing import Tuple, Any
import fitz
import camelot
import concurrent.futures
import glob
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from camelot.core import TableList
from .image_preprocessor import ImageHasher, ImageDescriber


class PDFProcessor(ImageDescriber, ImageHasher):
    def __init__(self, file_path, api_key):

        ImageDescriber.__init__(self, api_key)
        self.entities = None
        self.file_path = file_path
        self.file_name = os.path.basename(file_path).replace('.pdf', '')
        self.tables = []
        self.image_hashes = {}  # Maps hashes to filenames

    def extract_images(self, page_number) -> list[str]:
        with fitz.open(self.file_path) as doc:  # This ensures the document is properly closed after use
            page = doc.load_page(page_number)
            image_list = page.get_images(full=True)
            extracted_images = []

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                image_hash = self.combined_hash(image_bytes)
                if image_hash in self.image_hashes:
                    image_name = self.image_hashes[image_hash]
                else:
                    image_name = f'image_{self.file_name}_page_{page_number + 1}_{img_index}.png'
                    with open(image_name, "wb") as img_file:
                        img_file.write(image_bytes)

                    self.image_hashes[image_hash] = image_name  # Store the hash and filename

                extracted_images.append(image_name)

        return extracted_images

    def process_page(self, page_number) -> tuple[Any, TableList, str | Any] | tuple[Any, list[str], list[str]]:
        try:
            # This method will handle the processing of a single page
            extracted_images = self.extract_images(page_number)
            page_text, page_images, page_tables = "", [], []

            with fitz.open(self.file_path) as doc:
                page_text = doc[page_number].get_text()

                for image_name in extracted_images:
                    page_images.append(image_name)
                    if image_name not in self.image_hashes:  # Only describe new images
                        self.image_hashes[image_name] = None  # Placeholder for description

                # Extract tables
                tables = camelot.read_pdf(self.file_path, pages=str(page_number + 1))
                for table_index, table in enumerate(tables):
                    table_name = f'table_page_{page_number + 1}_{table_index}'
                    page_tables.append(table_name)
                    table_text = table.df.to_string(index=False)
                    page_text += f'Table:\n {table_text}'
        except Exception as e:
            print(f"Error processing page {page_number}: {e}")
            return self.image_hashes[image_name], tables, page_text   # Or some indication of failure
        return page_text, page_images, page_tables

    def parse_pdf(self) -> Tuple[str, int]:
        os.write(1, f"{self.file_path}\n".encode())
        num_pages = fitz.open(self.file_path).page_count

        self.image_hashes = {}  # Reset image hashes
        # # Using multiprocessing for CPU-bound tasks
        with ProcessPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(self.process_page, range(num_pages)))

        # refactor code above to not use ProcessPoolExecutor
        # results = []
        # for page_number in range(num_pages):
        #     results.append(self.process_page(page_number))

        # Extract image names and filter duplicates based on hashes
        unique_images = {}
        for page_text, images, _ in results:
            for image_name in images:
                if image_name not in unique_images:
                    image_hash = self.combined_hash(self.get_image_bytes(image_name))
                    if image_hash not in self.image_hashes:
                        self.image_hashes[image_hash] = image_name
                        unique_images[image_name] = None  # Placeholder for description

        # Use threading for I/O-bound tasks (image description)
        with ThreadPoolExecutor() as executor:
            future_to_image = {executor.submit(self.describe_image, image_name): image_name for image_name in
                               unique_images.keys()}
            for future in concurrent.futures.as_completed(future_to_image):
                image_name = future_to_image[future]
                description = future.result()
                unique_images[image_name] = description

        # Compile all text content, inserting image descriptions
        text_content = []
        for page_text, page_images, page_tables in results:
            for image_name in page_images:
                if image_name in unique_images and page_text[-len(f'\n[Image: {image_name}]'):] != f'\n[Image: {image_name}]':
                    page_text += f'\n[Image Description: {unique_images[image_name]}] \n[Image: {image_name}]'
            text_content.append(page_text)
            self.tables.extend(page_tables)

        return '\n'.join(text_content), num_pages

    @staticmethod
    def get_image_bytes(image_name) -> bytes:
        # Utility function to retrieve image bytes
        with open(image_name, "rb") as img_file:
            return img_file.read()

    def delete_duplicate_images(self):
        """
        Deletes images that are duplicates based on the image_hashes dictionary.
        """
        all_images = set(os.path.basename(path) for path in glob.glob(f'image_{self.file_name}_page_*_*.png'))
        unique_images = set(self.image_hashes.values())

        duplicates = all_images - unique_images

        for duplicate in duplicates:
            try:
                os.remove(duplicate)
            except OSError as e:
                print(f"Error deleting file {duplicate}: {e}")
