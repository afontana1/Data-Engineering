"""
Search functionality for PubMed using Bio.Entrez.
"""
import os
import time
import logging
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Any
from Bio import Entrez

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pubmed-search")

class PubMedSearch:
    """Client for searching PubMed articles using Bio.Entrez."""

    def __init__(self, email: str, tool: str, api_key: Optional[str] = None):
        """Initialize PubMed search client with required credentials.

        Args:
            email: Valid email address for API access
            tool: Unique identifier for the tool
            api_key: Optional API key for higher rate limits
        """
        if not email:
            raise ValueError("Email is required for PubMed search")
            
        self.email = email
        self.tool = tool
        self.api_key = api_key
        
        # Configure Entrez
        Entrez.email = email
        Entrez.tool = tool
        if api_key:
            Entrez.api_key = api_key
            
        logger.info(f"PubMed search initialized with email: {email}, tool: {tool}")

    async def search_articles(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for articles matching the query.

        Args:
            query: Search query string
            max_results: Maximum number of results to return

        Returns:
            List of article metadata dictionaries
        """
        try:
            # Replace [Date - Publication] with [PDAT] in query
            if "[Date - Publication]" in query:
                query = query.replace("[Date - Publication]", "[PDAT]")
                # Make sure date ranges are properly formatted
                if ":" in query:
                    parts = query.split(":")
                    if len(parts) == 2:
                        before_range = parts[0].strip()
                        after_range = parts[1].strip()
                        if all(c not in before_range for c in '"()') and "[PDAT]" in before_range:
                            # Add quotes and parentheses for date range
                            date = before_range.replace("[PDAT]", "").strip()
                            query = f'("{date}"[PDAT] : {after_range}'
                            
            logger.info(f"Searching PubMed with query: {query}")
            
            # Step 1: Search for article IDs
            try:
                handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
                search_results = Entrez.read(handle)
                handle.close()
                
                # Debug info
                logger.info(f"Total results found: {search_results.get('Count', 'Unknown')}")
                
            except Exception as e:
                logger.error(f"Error in PubMed search: {str(e)}")
                return []

            if not 'IdList' in search_results or not search_results['IdList']:
                logger.info("No results found")
                return []
                
            pmids = search_results['IdList']
            logger.info(f"Found {len(pmids)} articles")
            
            # Step 2: Get details for each article
            results = []
            for pmid in pmids:
                logger.info(f"Fetching details for PMID {pmid}")
                try:
                    detail_handle = Entrez.efetch(db="pubmed", id=pmid, rettype="xml")
                    article_xml = detail_handle.read()
                    detail_handle.close()
                    
                    # Parse article details
                    article_root = ET.fromstring(article_xml)
                    
                    # Get basic article data
                    article = {
                        "pmid": pmid,
                        "title": self._get_xml_text(article_root, './/ArticleTitle') or "No title",
                        "abstract": self._get_xml_text(article_root, './/Abstract/AbstractText') or "No abstract available",
                        "journal": self._get_xml_text(article_root, './/Journal/Title') or "",
                        "authors": []
                    }
                    
                    # Get authors
                    author_list = article_root.findall('.//Author')
                    for author in author_list:
                        last_name = self._get_xml_text(author, 'LastName') or ""
                        fore_name = self._get_xml_text(author, 'ForeName') or ""
                        if last_name or fore_name:
                            article["authors"].append(f"{last_name} {fore_name}".strip())
                    
                    # Get publication date
                    pub_date = article_root.find('.//PubDate')
                    if pub_date is not None:
                        year = self._get_xml_text(pub_date, 'Year')
                        month = self._get_xml_text(pub_date, 'Month')
                        day = self._get_xml_text(pub_date, 'Day')
                        article["publication_date"] = {
                            "year": year,
                            "month": month,
                            "day": day
                        }
                        
                    # Get article identifiers (DOI, PMC)
                    article_id_list = article_root.findall('.//ArticleId')
                    for article_id in article_id_list:
                        id_type = article_id.get('IdType')
                        if id_type == 'doi':
                            article["doi"] = article_id.text
                        elif id_type == 'pmc':
                            article["pmc_id"] = article_id.text
                            
                    # Add URLs
                    article["urls"] = self._generate_urls(pmid, 
                                                     article.get("doi"), 
                                                     article.get("pmc_id"))
                    
                    # Add resource URIs
                    article["abstract_uri"] = f"pubmed://{pmid}/abstract"
                    article["full_text_uri"] = f"pubmed://{pmid}/full_text"
                            
                    results.append(article)
                except Exception as e:
                    logger.error(f"Error fetching details for PMID {pmid}: {str(e)}")
                    continue
            
            return results

        except Exception as e:
            logger.exception(f"Error in search_articles: {str(e)}")
            return []
            
    def _get_xml_text(self, elem: Optional[ET.Element], xpath: str) -> Optional[str]:
        """Helper method to safely get text from XML element."""
        if elem is None:
            return None
        found = elem.find(xpath)
        return found.text if found is not None else None
        
    def _generate_urls(self, pmid: str, doi: Optional[str] = None, pmc_id: Optional[str] = None) -> Dict[str, str]:
        """Generate URLs for human access.
        
        Args:
            pmid: PubMed ID
            doi: Optional DOI
            pmc_id: Optional PMC ID
            
        Returns:
            Dictionary with URLs
        """
        urls = {
            "pubmed": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "pubmed_mobile": f"https://m.pubmed.ncbi.nlm.nih.gov/{pmid}/"
        }
        
        if doi:
            urls["doi"] = f"https://doi.org/{doi}"
        if pmc_id:
            urls["pmc"] = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/"
            
        return urls