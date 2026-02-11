"""
Full text fetching functionality for PubMed articles.

This module focuses solely on retrieving full text content from PMC
using Bio.Entrez.
"""
import logging
from typing import Optional
import xml.etree.ElementTree as ET
from Bio import Entrez, Medline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pubmed-fetch")

class PubMedFetch:
    """Client for fetching full text from PubMed Central."""
    
    def _clean_text(self, text: Optional[str]) -> Optional[str]:
        """Clean text content.
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text with normalized whitespace
        """
        if text is None:
            return None
            
        return ' '.join(text.split())

    def _extract_text_from_pmc_xml(self, xml_content: bytes) -> str:
        """Extract readable text content from PMC XML.
        
        Args:
            xml_content: PMC article XML
            
        Returns:
            Extracted text content
        """
        try:
            root = ET.fromstring(xml_content)
            
            # Dictionary for text parts
            parts = {}
            
            # Get article title
            title_elem = root.find(".//article-title")
            if title_elem is not None and title_elem.text:
                parts['title'] = self._clean_text(title_elem.text)
            
            # Get abstract
            abstract_parts = []
            for abstract in root.findall(".//abstract//p"):
                if abstract.text:
                    abstract_parts.append(self._clean_text(abstract.text))
            if abstract_parts:
                parts['abstract'] = " ".join(abstract_parts)
            
            # Get main body text
            body_parts = []
            for section in root.findall(".//body//sec"):
                # Get section title if available
                title = section.find("title")
                if title is not None and title.text:
                    body_parts.append(f"\n\n{title.text}\n")
                
                # Get paragraphs in section
                for p in section.findall(".//p"):
                    if p.text:
                        body_parts.append(self._clean_text(p.text))
            
            if body_parts:
                parts['body'] = "\n\n".join(body_parts)
            
            # Combine all parts
            text_parts = []
            if 'title' in parts:
                text_parts.append(parts['title'])
            if 'abstract' in parts:
                text_parts.append("\nABSTRACT\n" + parts['abstract'])
            if 'body' in parts:
                text_parts.append("\nMAIN TEXT\n" + parts['body'])
                
            if not text_parts:
                raise ValueError("No text content found in PMC XML")
                
            return "\n\n".join(text_parts)
            
        except ET.ParseError as e:
            logger.error(f"Error parsing PMC XML: {str(e)}")
            raise ValueError(f"Could not parse PMC XML content: {str(e)}")
        except Exception as e:
            logger.error(f"Error extracting text from PMC XML: {str(e)}")
            raise ValueError(f"Error processing PMC content: {str(e)}")

    async def get_full_text(self, pmid: str) -> str:
        """Get full text of an article if available.
        
        Args:
            pmid: PubMed ID of the article
            
        Returns:
            Full text content if available, otherwise an error message
            explaining why the text is not available.
            
        Raises:
            ValueError: If there are issues accessing or parsing the content
        """
        try:
            # First get PMC ID if available
            logger.info(f"Fetching article {pmid}")
            handle = Entrez.efetch(db="pubmed", id=pmid, rettype="medline", retmode="text")
            record = Medline.read(handle)
            handle.close()
            
            if 'PMC' in record:
                pmc_id = record['PMC']
                logger.info(f"Found PMC ID {pmc_id}, fetching full text")
                
                # Get full text from PMC
                pmc_handle = Entrez.efetch(db='pmc', id=pmc_id, rettype='full', retmode='xml')
                xml_content = pmc_handle.read()
                pmc_handle.close()
                
                # Parse XML and extract text
                return self._extract_text_from_pmc_xml(xml_content)
                    
            elif 'DOI' in record:
                return f"Full text not available in PMC. Article has DOI {record['DOI']} - full text may be available through publisher"
            else:
                return "Full text not available - article is not in PMC and has no DOI"
                
        except Exception as e:
            logger.exception(f"Error getting full text for article {pmid}")
            return f"Error retrieving full text: {str(e)}"