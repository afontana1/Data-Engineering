"""
Client for retrieving full text content of PubMed articles.
Separate from main PubMed client to maintain code separation and stability.
"""
import logging
import time
import http.client
from typing import Optional, Tuple
from Bio import Entrez
import xml.etree.ElementTree as ET

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pubmed-fulltext")

class FullTextClient:
    """Client for retrieving full text content from PubMed Central."""

    def __init__(self, email: str, tool: str, api_key: Optional[str] = None):
        """Initialize full text client with required credentials.

        Args:
            email: Valid email address for API access
            tool: Unique identifier for the tool
            api_key: Optional API key for higher rate limits
        """
        self.email = email
        self.tool = tool
        self.api_key = api_key
        
        # Configure Entrez
        Entrez.email = email
        Entrez.tool = tool
        if api_key:
            Entrez.api_key = api_key

    async def check_full_text_availability(self, pmid: str) -> Tuple[bool, Optional[str]]:
        """Check if full text is available in PMC and get PMC ID if it exists.
        
        Args:
            pmid: PubMed ID of the article
            
        Returns:
            Tuple of (availability boolean, PMC ID if available)
        """
        try:
            logger.info(f"Checking PMC availability for PMID {pmid}")
            handle = Entrez.elink(dbfrom="pubmed", db="pmc", id=pmid)
            
            if not handle:
                logger.info(f"No PMC link found for PMID {pmid}")
                return False, None
                
            xml_content = handle.read()
            handle.close()
            
            # Parse XML to get PMC ID
            root = ET.fromstring(xml_content)
            linksetdb = root.find(".//LinkSetDb")
            if linksetdb is None:
                logger.info(f"No PMC ID found for PMID {pmid}")
                return False, None
                
            id_elem = linksetdb.find(".//Id")
            if id_elem is None:
                logger.info(f"No PMC ID element found for PMID {pmid}")
                return False, None
                
            pmc_id = id_elem.text
            logger.info(f"Found PMC ID {pmc_id} for PMID {pmid}")
            return True, pmc_id
            
        except Exception as e:
            logger.exception(f"Error checking PMC availability for PMID {pmid}: {str(e)}")
            return False, None

    async def get_full_text(self, pmid: str) -> Optional[str]:
        """Get full text of the article if available through PMC.
        
        Handles truncated responses by making additional requests.
        
        Args:
            pmid: PubMed ID of the article
            
        Returns:
            Full text content if available, None otherwise
        """
        try:
            # First check availability and get PMC ID
            available, pmc_id = await self.check_full_text_availability(pmid)
            if not available or pmc_id is None:
                logger.info(f"Full text not available in PMC for PMID {pmid}")
                return None

            logger.info(f"Fetching full text for PMC ID {pmc_id}")
            content = ""
            retstart = 0
            
            while True:
                full_text_handle = Entrez.efetch(
                    db="pmc", 
                    id=pmc_id, 
                    rettype="xml",
                    retstart=retstart
                )
                
                if not full_text_handle:
                    break
                    
                chunk = full_text_handle.read()
                full_text_handle.close()
                
                if isinstance(chunk, bytes):
                    chunk = chunk.decode('utf-8')
                
                content += chunk
                
                # Check if there might be more content
                if "[truncated]" not in chunk and "Result too long" not in chunk:
                    break
                    
                # Increment retstart for next chunk
                retstart += len(chunk)
                
                # Add small delay to respect API rate limits
                time.sleep(0.5)
                
            return content
            
        except Exception as e:
            logger.exception(f"Error getting full text for PMID {pmid}: {str(e)}")
            return None