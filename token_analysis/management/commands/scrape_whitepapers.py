# token_analysis/management/commands/scrape_and_extract_whitepapers.py

import requests
import pandas as pd
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
import fitz  # PyMuPDF

class Command(BaseCommand):
    help = 'Scrape whitepaper URLs from allcryptowhitepapers.com and extract text from the PDFs'

    def handle(self, *args, **kwargs):
        base_url = 'https://www.allcryptowhitepapers.com/whitepaper-overview/'
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        whitepapers = []

        for row in soup.select('table tbody tr'):
            columns = row.find_all('td')
            if len(columns) > 2:
                project_name = columns[0].text.strip()
                category = columns[1].text.strip()
                whitepaper_url = columns[2].find('a')['href']

                whitepapers.append({
                    'project_name': project_name,
                    'category': category,
                    'whitepaper_url': whitepaper_url
                })

        df = pd.DataFrame(whitepapers)
        extracted_data = []

        for index, row in df.iterrows():
            url = row['whitepaper_url']
            try:
                text = self.extract_text_from_pdf(url)
                extracted_data.append({
                    'project_name': row['project_name'],
                    'category': row['category'],
                    'text': text
                })
                self.stdout.write(self.style.SUCCESS(f"Extracted text from {row['project_name']}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to extract text from {url}: {e}"))

        extracted_df = pd.DataFrame(extracted_data)
        extracted_df.to_csv('extracted_whitepapers.csv', index=False)
        self.stdout.write(self.style.SUCCESS(f'Scraped and processed {len(extracted_df)} whitepapers.'))

    def extract_text_from_pdf(self, url):
        response = requests.get(url)
        response.raise_for_status()
        pdf_data = response.content

        # Open the PDF file
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

        # Extract text from each page
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        return text
