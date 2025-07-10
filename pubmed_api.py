
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
EMAIL = "your-email@example.com"  # Replace with your actual email (required by NCBI)

def search_pubmed(query: str, retmax: int = 100) -> List[str]:
    """Fetch PubMed IDs for a given query using ESearch."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax,
        "email": EMAIL,
    }
    response = requests.get(BASE_URL + "esearch.fcgi", params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_details(pmid_list: List[str]) -> List[Dict]:
    """Fetch metadata for a list of PMIDs using EFetch."""
    if not pmid_list:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(pmid_list),
        "retmode": "xml",
        "email": EMAIL,
    }
    response = requests.get(BASE_URL + "efetch.fcgi", params=params)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    results = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date = extract_publication_date(article)
        authors_info = extract_authors_info(article)

        results.append({
            "PubmedID": pmid,
            "Title": title,
            "PublicationDate": pub_date,
            "Authors": authors_info,
        })

    return results

def extract_publication_date(article_xml: ET.Element) -> str:
    """Extracts the publication date in YYYY-MM-DD format if available."""
    date_el = article_xml.find(".//PubDate")
    if date_el is not None:
        year = date_el.findtext("Year") or "1900"
        month = date_el.findtext("Month") or "01"
        day = date_el.findtext("Day") or "01"
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    return "1900-01-01"

def extract_authors_info(article_xml: ET.Element) -> List[Dict]:
    """Extract authors' names, affiliations, and emails."""
    authors = []
    for author in article_xml.findall(".//Author"):
        last = author.findtext("LastName") or ""
        fore = author.findtext("ForeName") or ""
        name = f"{fore} {last}".strip()
        affiliations = [aff.text for aff in author.findall(".//AffiliationInfo/Affiliation") if aff.text]
        authors.append({
            "name": name,
            "affiliations": affiliations,
        })
    return authors
'''if __name__ == "__main__":
    query = "cancer immunotherapy"
    pmids = search_pubmed(query)
    papers = fetch_details(pmids[:5])
    for paper in papers:
        print(paper)'''
