import argparse
import logging
import csv
from pubmed_api import search_pubmed, fetch_details
from filter import parse_non_academic_authors
from typing import Optional

def setup_logger(debug: bool):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(levelname)s: %(message)s"
    )

def get_papers(query: str, debug: bool = False) -> list[dict]:
    setup_logger(debug)
    logging.info(f"Searching PubMed for query: {query}")
    pmids = search_pubmed(query)
    logging.info(f"Found {len(pmids)} papers. Fetching details...")

    papers = fetch_details(pmids)
    results = []

    for paper in papers:
        pubmed_id = paper["PubmedID"]
        title = paper["Title"]
        pub_date = paper["PublicationDate"]
        authors = paper["Authors"]

        non_acad_authors, company_affs, email = parse_non_academic_authors(authors)

        if non_acad_authors:
            results.append({
                "PubmedID": pubmed_id,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": "; ".join(non_acad_authors),
                "Company Affiliation(s)": "; ".join(company_affs),
                "Corresponding Author Email": email,
            })

    logging.info(f"Found {len(results)} papers with non-academic authors.")
    return results

def write_csv(filename: str, data: list[dict]):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors.")
    parser.add_argument("query", help="PubMed query (use quotes)")
    parser.add_argument("-f", "--file", help="Output CSV file name")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    parser.add_argument("-v", "--version", action="version", version="get-papers-list 1.0")

    args = parser.parse_args()

    try:
        results = get_papers(args.query, debug=args.debug)

        if not results:
            print("No papers with non-academic authors found.")
            return

        if args.file:
            write_csv(args.file, results)
            print(f"Results saved to {args.file}")
        else:
            for row in results:
                print("-" * 60)
                for k, v in row.items():
                    print(f"{k}: {v}")

    except Exception as e:
        logging.exception("An error occurred.")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
