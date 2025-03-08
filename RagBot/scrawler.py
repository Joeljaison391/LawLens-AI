import requests
from bs4 import BeautifulSoup
from docx import Document
import pdfkit
from urllib.parse import urlparse
import re


websites = [
    'https://www.comply4hr.com/docs/ker/kesoa/KESOAS1.htm',
    'https://en.wikipedia.org/wiki/Department_of_Industries_(Kerala)',
    'https://en.wikipedia.org/wiki/Kerala_State_Industrial_Development_Corporation'
]


def fetch_page(url):
    """Fetch the page content using requests."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception for 4xx/5xx codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_html_to_text(html_content):
    """Parse the HTML content to extract text."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the title from the page to use in filenames
    title_tag = soup.find('title')
    title = title_tag.get_text() if title_tag else "Untitled"

    # Example: Extract all paragraphs <p> (modify this based on your needs)
    paragraphs = soup.find_all('p')
    extracted_text = '\n'.join([p.get_text() for p in paragraphs])

    return extracted_text, title


def save_to_docx(text, filename):
    """Save the extracted text into a DOCX file."""
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)
    print(f"Document saved as {filename}")


def save_to_pdf(text, filename):
    """Save the extracted text into a PDF file."""
    pdfkit.from_string(text, filename)
    print(f"PDF saved as {filename}")


def sanitize_filename(filename):
    """Sanitize the filename to remove invalid characters."""
    return re.sub(r'[\\/*?:"<>|]', "_", filename)


def scrape_and_convert(url):
    """Fetch, parse, and save content to DOCX or PDF."""
    html_content = fetch_page(url)
    if html_content:
        text_content, page_title = parse_html_to_text(html_content)

        # Use the page title or domain name as part of the filename
        domain_name = urlparse(url).netloc
        sanitized_title = sanitize_filename(page_title)

        # Generate dynamic filenames
        docx_filename = f"{domain_name}_{sanitized_title}.docx"
        pdf_filename = f"{domain_name}_{sanitized_title}.pdf"

        # Save to DOCX
        save_to_docx(text_content, docx_filename)
        # Save to PDF
        save_to_pdf(text_content, pdf_filename)


# Loop over the websites and process each
for website in websites:
    scrape_and_convert(website)
