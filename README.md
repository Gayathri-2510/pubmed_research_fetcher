# pubmed_research_fetcher

A command-line Python application that fetches research papers from PubMed based on a user-specified query, filters for papers with at least one author affiliated with a pharmaceutical or biotech company, and outputs the results as a CSV file or to the console.

## Overview

This project is organized into two main components:

- **Module (`pubmed_fetcher.py`)**: Contains core logic for interacting with PubMed's API, processing data, filtering results, and extracting required information.
- **CLI Script (`main.py`)**: Handles command-line argument parsing, invokes module functions, and manages output.

The program supports options for help, debug mode, and specifying output filename.


## Features

- Supports full PubMed query syntax for flexible searching.
- Fetches papers with detailed info: PubMedID, Title, Publication Date, Authors, Affiliations, email.
- Filters for papers with at least one author affiliated with pharmaceutical or biotech companies.
- Extracts author names, affiliations, and corresponding author email.
- Outputs results as a CSV file or prints to the console.
- Supports command-line options:
  - `-h` or `--help`: Show usage instructions.
  - `-d` or `--debug`: Enable debug mode.
  - `-f` or `--file`: Specify output filename.

---

## Installation

### Prerequisites

- Python 3.8 or higher

### Using Poetry

```bash
# Clone the repository
git clone https://github.com/yourusername/pubmed_research_fetcher.git
cd pubmed_research_fetcher

# Install dependencies
poetry install