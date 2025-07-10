import re
from typing import List, Dict, Tuple

ACADEMIC_KEYWORDS = [
    "university", "college", "institute", "school", "hospital", "center", "centre", "clinic", "department"
]

COMPANY_KEYWORDS = [
    "pharma", "biotech", "therapeutics", "inc", "ltd", "gmbh", "corporation", "corp", "llc", "labs", "technologies"
]

EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

def is_non_academic(affiliation: str) -> bool:
    aff_lower = affiliation.lower()
    return (
        not any(keyword in aff_lower for keyword in ACADEMIC_KEYWORDS)
        and any(keyword in aff_lower for keyword in COMPANY_KEYWORDS)
    )

def extract_email(affiliation: str) -> str:
    match = re.search(EMAIL_REGEX, affiliation)
    return match.group(0) if match else ""

def extract_company_name(affiliation: str) -> str:
    for keyword in COMPANY_KEYWORDS:
        pattern = rf"([A-Z][A-Za-z0-9&\s,.-]*{keyword}[A-Za-z0-9&\s,.-]*)"
        match = re.search(pattern, affiliation, re.IGNORECASE)
        if match:
            return match.group(0).strip()
    return ""

def parse_non_academic_authors(authors: List[Dict]) -> Tuple[List[str], List[str], str]:
    non_academic_authors = []
    company_names = []
    email = ""

    for author in authors:
        name = author["name"]
        affiliations = author.get("affiliations", [])
        for aff in affiliations:
            if is_non_academic(aff):
                non_academic_authors.append(name)
                company = extract_company_name(aff)
                if company:
                    company_names.append(company)
            if not email:
                email_candidate = extract_email(aff)
                if email_candidate:
                    email = email_candidate

    return list(set(non_academic_authors)), list(set(company_names)), email
'''if __name__ == "__main__":
    authors = [
        {
            "name": "John Smith",
            "affiliations": [
                "Genentech Inc, South San Francisco, CA, USA. john.smith@genentech.com"
            ]
        },
        {
            "name": "Alice Doe",
            "affiliations": [
                "Department of Immunology, Stanford University"
            ]
        }
    ]
    non_acad, companies, email = parse_non_academic_authors(authors)
    print("Non-academic Authors:", non_acad)
    print("Companies:", companies)
    print("Email:", email)'''
