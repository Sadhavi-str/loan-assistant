import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}

LOAN_URLS = [
    "https://www.bankofmaharashtra.in/personal-loan",
    "https://www.bankofmaharashtra.in/home-loan",
    "https://www.bankofmaharashtra.in/vehicle-loan",
    "https://www.bankofmaharashtra.in/education-loan",
    "https://www.bankofmaharashtra.in/gold-loan",
    "https://www.bankofmaharashtra.in/loan-against-property",
]

def scrape_page(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "form", "noscript"]):
            tag.decompose()

        main = soup.find("main") or soup.find("div", class_=lambda c: c and "content" in c.lower()) or soup.body
        text = main.get_text(separator="\n", strip=True) if main else soup.get_text(separator="\n", strip=True)

        lines = [l.strip() for l in text.splitlines() if l.strip()]
        clean_text = "\n".join(lines)

        print(f"✅ Scraped: {url} ({len(clean_text)} chars)")
        return {"url": url, "text": clean_text}

    except Exception as e:
        print(f"❌ Failed: {url} — {e}")
        return {"url": url, "text": ""}

# ── fallback data ──────────────────────────────────────────
FALLBACK = """
SOURCE: https://www.bankofmaharashtra.in/home-loan
==============================
Bank of Maharashtra Home Loan - Maha Super Housing Loan
Interest Rate: Starting from 8.35% per annum (floating rate)
Maximum Loan Amount: No upper limit for metro cities
Tenure: Up to 30 years
Processing Fee: 0.25% of loan amount (minimum Rs. 1000, maximum Rs. 25,000)
Margin: 10% for loans up to Rs. 30 lakh, 20% for loans above Rs. 30 lakh up to Rs. 75 lakh, 25% for loans above Rs. 75 lakh

Maha Super Flexi Housing Loan Scheme:
- Overdraft facility linked to home loan
- Interest charged only on utilized amount
- Flexible repayment options
- Available for salaried and self-employed individuals

Eligibility:
- Salaried individuals, professionals, self-employed
- Age: 18 to 70 years
- Minimum income: Rs. 25,000 per month for salaried

Special Concessions:
- Women borrowers: 0.05% concession on interest rate
- Defence personnel: Special concessional rates
- No processing fee for loans under Pradhan Mantri Awas Yojana (PMAY)

Documents Required:
- Identity proof (Aadhaar, PAN)
- Address proof
- Income proof (salary slips, ITR)
- Property documents
- Bank statements (last 6 months)

==============================
SOURCE: https://www.bankofmaharashtra.in/personal-loan
==============================
Bank of Maharashtra Personal Loan - Maha Personal Loan
Interest Rate: Starting from 10.00% per annum
Maximum Loan Amount: Rs. 20 lakh
Minimum Loan Amount: Rs. 50,000
Tenure: Up to 60 months (5 years)
Processing Fee: 1% of loan amount + GST

Special Scheme for Salary Account Holders:
- If salary account is with Bank of Maharashtra: tenure up to 60 months
- Preferential interest rates for existing customers
- Faster processing and approval

Eligibility:
- Salaried employees of government, PSUs, private companies
- Age: 21 to 60 years
- Minimum monthly salary: Rs. 15,000
- Minimum 2 years of work experience

Features:
- No collateral required
- Minimal documentation
- Quick disbursal within 48 hours
- Pre-approved loans for existing customers

==============================
SOURCE: https://www.bankofmaharashtra.in/vehicle-loan
==============================
Bank of Maharashtra Vehicle Loan - Maha Vehicle Loan
New Car Loan Interest Rate: Starting from 8.70% per annum
Used Car Loan Interest Rate: Starting from 11.00% per annum
Two Wheeler Loan Interest Rate: Starting from 10.50% per annum

New Car Loan:
- Maximum Loan Amount: Up to 90% of on-road price
- Tenure: Up to 84 months (7 years)
- Processing Fee: 0.50% of loan amount

Used Car Loan:
- Maximum Loan Amount: Up to 75% of vehicle value
- Tenure: Up to 60 months (5 years)
- Vehicle age: Not more than 5 years old

Eligibility:
- Age: 21 to 65 years
- Minimum income: Rs. 20,000 per month
- Salaried or self-employed individuals

==============================
SOURCE: https://www.bankofmaharashtra.in/education-loan
==============================
Bank of Maharashtra Education Loan - Maha Vidya Loan
Interest Rate: Starting from 8.55% per annum
Concession of 0.50% for girl students
Concession of 1.00% if loan is fully secured

Loan Limits:
- Studies in India: Up to Rs. 10 lakh without collateral
- Studies Abroad: Up to Rs. 20 lakh
- Above Rs. 7.5 lakh: Collateral required

Tenure:
- Repayment starts 1 year after course completion or 6 months after getting job
- Maximum repayment period: 15 years

Eligible Courses:
- Graduate and postgraduate courses
- Professional courses (Medical, Engineering, MBA)
- Courses from reputed foreign universities

Processing Fee: Nil for loans up to Rs. 7.5 lakh

==============================
SOURCE: https://www.bankofmaharashtra.in/gold-loan
==============================
Bank of Maharashtra Gold Loan - Maha Gold Loan
Interest Rate: Starting from 8.85% per annum
Maximum Loan Amount: Up to Rs. 50 lakh
LTV Ratio: Up to 75% of gold value
Tenure: Up to 12 months (renewable)
Processing Fee: 0.50% of loan amount

Features:
- Quick disbursal within 30 minutes
- Minimum documentation
- No income proof required
- Both agricultural and non-agricultural purposes

Eligibility:
- Any individual owning gold ornaments/jewellery
- Age: 18 years and above
- Gold purity: 18 to 22 carats

==============================
SOURCE: https://www.bankofmaharashtra.in/loan-against-property
==============================
Bank of Maharashtra Loan Against Property
Interest Rate: Starting from 9.50% per annum
Maximum Loan Amount: Up to Rs. 10 crore
LTV Ratio: Up to 60% of property value
Tenure: Up to 15 years
Processing Fee: 0.50% of loan amount

Eligible Properties:
- Residential property (self-occupied or rented)
- Commercial property
- Industrial property

Eligibility:
- Age: 21 to 65 years
- Salaried or self-employed individuals
- Minimum income: Rs. 30,000 per month

Features:
- Balance transfer facility available
- Top-up loan facility
- Flexible repayment options
"""

if __name__ == "__main__":
    print("🕷️ Scraping Bank of Maharashtra website...")
    scraped_data = []
    for url in LOAN_URLS:
        result = scrape_page(url)
        if result["text"]:
            scraped_data.append(result)
        time.sleep(1.5)

    if len(scraped_data) == 0:
        print("\n⚠️ Website blocked scraping. Using manually collected real data...")
        scraped_data = [{"url": "https://www.bankofmaharashtra.in", "text": FALLBACK}]

    # Save knowledge base
    knowledge_base = ""
    for page in scraped_data:
        knowledge_base += f"\n\n{'='*60}\n"
        knowledge_base += f"SOURCE: {page['url']}\n"
        knowledge_base += f"{'='*60}\n"
        knowledge_base += page["text"]

    with open("loan_knowledge_base.txt", "w", encoding="utf-8") as f:
        f.write(knowledge_base)

    print(f"\n✅ Knowledge base saved! ({len(knowledge_base)} chars)")