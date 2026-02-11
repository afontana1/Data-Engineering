from typing import Dict, Any, List
from pathlib import Path
import logging
from io import BytesIO
import base64

from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    WordFormatOption,
    PowerpointFormatOption,
    HTMLFormatOption,
    ImageFormatOption
)
from docling.datamodel.base_models import InputFormat, ConversionStatus
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling.utils.export import generate_multimodal_pages

from graphs.chat_graph import get_model

# Set up logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DoclingProcessor:
    def __init__(self):
        """Initialize Docling processor with proper format configurations."""
        # Configure pipeline options for PDF
        pdf_pipeline_options = PdfPipelineOptions()
        
        # Configure text extraction without OCR
        pdf_pipeline_options.do_ocr = False
        
        # Configure table detection
        pdf_pipeline_options.do_table_structure = True
        pdf_pipeline_options.table_structure_options.do_cell_matching = False
        
        # Configure image extraction
        pdf_pipeline_options.images_scale = 2.0  # Higher resolution for better quality
        pdf_pipeline_options.generate_page_images = True
        pdf_pipeline_options.generate_picture_images = True
        
        # Initialize document converter with format-specific options
        self.converter = DocumentConverter(
            allowed_formats=[
                InputFormat.PDF,
                InputFormat.DOCX,
                InputFormat.PPTX,
                InputFormat.HTML,
                InputFormat.MD
            ],
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_cls=StandardPdfPipeline,
                    pipeline_options=pdf_pipeline_options
                ),
                InputFormat.DOCX: WordFormatOption(),
                InputFormat.PPTX: PowerpointFormatOption(),
                InputFormat.HTML: HTMLFormatOption()
            }
        )
        
        # Get vision-capable model for image analysis
        self.model = get_model()
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """Process a document using Docling and return structured information."""
        logger.info(f"Processing document: {file_path}")
        
        # Convert file path to Path object
        path = Path(file_path)
        
        # Convert and process the document
        conversion_result = self.converter.convert(path)
        
        if conversion_result.status != ConversionStatus.SUCCESS:
            logger.error(f"Document conversion failed: {conversion_result.error_message}")
            raise Exception(f"Document conversion failed: {conversion_result.error_message}")
        
        doc = conversion_result.document
        logger.info("Document converted successfully")
        
        # Process multimodal content
        pages = []
        for content_text, content_md, content_dt, page_cells, page_segments, page in generate_multimodal_pages(conversion_result):
            page_info = {
                "page_number": page.page_no,
                "text": content_text,
                "markdown": content_md,
                "tables": page_cells,
                "sections": page_segments,
                "header": next((seg["text"] for seg in page_segments if seg.get("type") == "header"), None),
                "section_type": next((seg["type"] for seg in page_segments if seg.get("type")), "content"),
                "images": []
            }
            
            # Process page images with LLM
            if hasattr(page, 'image') and page.image:
                try:
                    # Convert page image to bytes for analysis
                    img_byte_arr = BytesIO()
                    page.image.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    # Analyze page content with vision model
                    analysis = self.analyze_image(img_byte_arr)
                    
                    page_info["images"].append({
                        "width": page.image.width,
                        "height": page.image.height,
                        "analysis": analysis
                    })
                except Exception as e:
                    logger.warning(f"Error processing page image: {str(e)}")
            
            pages.append(page_info)
        
        # Extract metadata
        metadata = {}
        try:
            # Try to get title from document properties
            if hasattr(doc, 'title'):
                metadata['title'] = doc.title
            elif hasattr(doc, 'properties') and hasattr(doc.properties, 'title'):
                metadata['title'] = doc.properties.title
            else:
                # Try to find title in the first page
                first_page = next(iter(doc.pages.values()), None)
                if first_page and hasattr(first_page, 'text'):
                    lines = first_page.text.split('\n')
                    if lines:
                        metadata['title'] = lines[0].strip()
            
            # Try to get author
            if hasattr(doc, 'author'):
                metadata['author'] = doc.author
            elif hasattr(doc, 'properties') and hasattr(doc.properties, 'author'):
                metadata['author'] = doc.properties.author
            
            # Try to get date
            if hasattr(doc, 'date'):
                metadata['date'] = doc.date
            elif hasattr(doc, 'properties') and hasattr(doc.properties, 'created'):
                metadata['date'] = doc.properties.created
            
            logger.info(f"Extracted metadata: {metadata}")
        except Exception as e:
            logger.warning(f"Error extracting metadata: {str(e)}")
            metadata = {}
        
        # Prepare final document structure
        doc_structure = {
            "metadata": metadata,
            "pages": pages,
            "tables": [table.export_to_dict() for table in getattr(doc, 'tables', [])],
            "images": [img.export_to_dict() for img in getattr(doc, 'images', [])]
        }
        
        logger.info(f"Document processing complete with {len(pages)} pages")
        return doc_structure
    
    def extract_text_with_context(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract text with context from a document using process_document."""
        doc_structure = self.process_document(file_path)
        
        chunks = []
        for page in doc_structure["pages"]:
            chunk = {
                "text": page["text"],
                "context": {
                    "page_num": page["page_number"],
                    "header": page["header"],
                    "section_type": page["section_type"],
                    "tables": page["tables"],
                    "figures": [],  # Will be populated if figures are on this page
                    "images": page["images"]
                }
            }
            chunks.append(chunk)
        
        return chunks
    
    def analyze_image(self, image_data: bytes) -> str:
        """Analyze image using LLM with vision capabilities."""
        try:
            logger.info("Starting image analysis")
            
            # Validate image data
            if not image_data:
                logger.error("Empty image data received")
                return "Error: No image data provided"
            
            logger.debug(f"Image data size: {len(image_data)} bytes")
            
            try:
                # Convert image to base64
                base64_image = base64.b64encode(image_data).decode('utf-8')
                logger.debug(f"Successfully encoded image to base64 (length: {len(base64_image)})")
            except Exception as e:
                logger.error(f"Failed to encode image to base64: {str(e)}")
                return f"Error encoding image: {str(e)}"
            
            # Create messages for the model using the correct format for OpenAI's vision API
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze this image and provide a detailed description of its contents.
                            Focus on:
                            1. Main elements and their relationships
                            2. Any text visible in the image
                            3. Charts, diagrams, or visual data
                            4. Key information that would be relevant for document understanding
                            
                            Provide the description in a clear, concise format."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
            
            logger.info("Sending image to vision model for analysis")
            
            try:
                # Use model's vision capabilities
                response = self.model.invoke(messages)
                
                logger.info("Successfully received response from vision model")
                return response.content
                
            except Exception as e:
                logger.error(f"Error during model invocation: {str(e)}", exc_info=True)
                return f"Error analyzing image with model: {str(e)}"
                
        except Exception as e:
            logger.error(f"Unexpected error in analyze_image: {str(e)}", exc_info=True)
            return f"Unexpected error analyzing image: {str(e)}"
