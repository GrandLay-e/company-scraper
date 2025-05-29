import sqlite3
import json

from Company import Company, get_json

class Companies:
    def __init__(self, companies: list[Company]):
        self.companies = companies

    def show_companies(self):
        for company in self.companies:
            company.show_company()

    def save_companies_to_json(self, file):
        for company in self.companies:
            company.save_data_to_json(file)

    def save_companies_to_sqlite(self, db):
        for company in self.companies:
            company.save_to_sqlite(db)

    def get_companies_from_sqlite(self, db):
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM companies')
            all_companies = cursor.fetchall()

            return Companies([
                Company(
                    name=row[0],
                    url=row[1],
                    web_site=row[2],
                    domain=row[3],
                    location=row[4],
                    number_salaries=row[5],
                    average_age=row[6],
                    offers=row[7],
                    all_offers= json.loads(row[8]),
                    spontaneous_application=row[9],
                    email=row[10],
                    phone_number=row[11]
                ) for row in all_companies
            ])

    def get_companies_from_json(self, file):
        all_companies = get_json(file)
        return Companies([
            Company(
                name,
                company.get("URL Page", "Unknown"),
                company.get("Web Site", "Unknown"),
                company.get("Domain", "Unknown"),
                company.get("Location", "Unknown"),
                company.get("Number of Salaries", "Unknown"),
                company.get("Average Age", "Unknown"),
                company.get("Offers Number", "Unknown"),
                company.get("Offers List", "Unknown"),
                company.get("Spontaneous application", "Unknown"),
                company.get("E-Mail", "Unknown"),
                company.get("Phone", "Unknown")
            ) for name, company in all_companies.items()
        ])

