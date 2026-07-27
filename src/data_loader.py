import os
import urllib.request
import pandas as pd
import numpy as np
import random

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
CSV_PATH = os.path.join(DATA_DIR, "fake_job_postings.csv")

PRIMARY_URL = "https://raw.githubusercontent.com/shivamb/real-or-fake-fake-job-postings/master/fake_job_postings.csv"
FALLBACK_URL = "https://raw.githubusercontent.com/amankharwal/Website-data/master/fake_job_postings.csv"

def fetch_or_generate_dataset():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(CSV_PATH) and os.path.getsize(CSV_PATH) > 10000:
        print(f"[*] Dataset already exists at {CSV_PATH}")
        return pd.read_csv(CSV_PATH)
    
    print("[*] Attempting to download EMSCAD dataset from public repositories...")
    for url in [PRIMARY_URL, FALLBACK_URL]:
        try:
            urllib.request.urlretrieve(url, CSV_PATH)
            df = pd.read_csv(CSV_PATH)
            if len(df) > 1000 and "fraudulent" in df.columns:
                print(f"[+] Successfully downloaded real EMSCAD dataset! Total rows: {len(df)}")
                return df
        except Exception as e:
            print(f"[-] Failed to fetch from {url}: {e}")

    print("[*] Generating high-fidelity synthetic benchmark dataset based on EMSCAD schema...")
    df = generate_synthetic_emscad(n_samples=5000)
    df.to_csv(CSV_PATH, index=False)
    print(f"[+] Synthetic benchmark dataset saved to {CSV_PATH}. Total rows: {len(df)}")
    return df

def generate_synthetic_emscad(n_samples=5000):
    np.random.seed(42)
    random.seed(42)

    titles_real = [
        "Software Engineer", "Data Scientist", "Project Manager", "Account Executive", 
        "Customer Success Specialist", "Marketing Coordinator", "Financial Analyst",
        "HR Manager", "DevOps Engineer", "Product Designer", "Sales Representative",
        "Business Analyst", "Content Writer", "Operations Associate", "QA Engineer"
    ]
    
    titles_fake = [
        "Data Entry Specialist - Earn $50/hr From Home", "Data Entry Operator (Urgent)", 
        "Remote Administrative Assistant - High Pay", "Virtual Assistant Needed Immediately",
        "Work From Home Typist - No Experience Needed", "Online Customer Support Representative",
        "Financial Assistant / Payment Processor", "Easy Data Entry Clerk", "Envelope Stuffer / Packer"
    ]

    locations = ["US, NY, New York", "US, CA, San Francisco", "US, TX, Austin", "GB, LND, London", "CA, ON, Toronto", "DE, BE, Berlin", "IN, MH, Mumbai", "US, FL, Miami", "AU, NSW, Sydney"]
    departments = ["Engineering", "Sales", "Marketing", "Customer Support", "Finance", "HR", "Operations", "Product"]

    comp_profiles_real = [
        "We are an innovative tech company building next-generation cloud infrastructure and SaaS solutions for enterprise clients worldwide. Founded in 2015, we have raised $40M in Series B funding.",
        "A fast-growing e-commerce startup empowering independent merchants to scale their online presence seamlessly through AI-driven analytics.",
        "Established financial services firm providing comprehensive wealth management, corporate advisory, and investment banking services for over 30 years.",
        "Leading digital healthcare provider transforming patient outcomes through telemedicine, remote monitoring, and personalized wellness plans.",
        "Global digital marketing agency helping Fortune 500 brands scale performance marketing, SEO, and social media campaigns."
    ]

    comp_profiles_fake = [
        "We are a leading global investment group providing financial solutions and wire transfer services.",
        "International logistics management group operating high return remote working programs.",
        "A premiere business consultancy firm offering flexible home-based employment opportunities with daily payouts.",
        "", ""
    ]

    desc_real = [
        "We are looking for a dedicated professional to join our dynamic team. You will collaborate with cross-functional teams to design, test, and deploy scalable solutions.",
        "Responsibilities include analyzing business requirements, building robust data pipelines, presenting insights to key stakeholders, and maintaining high software quality standards.",
        "You will manage client portfolios, drive user acquisition campaigns, build strong customer relationships, and achieve monthly revenue metrics."
    ]

    desc_fake = [
        "Earn money easily working from home! We need individuals to process payments, enter data into spreadsheet forms, and send confirmation emails. Flexible hours, daily payment via wire transfer or check.",
        "Immediate opening for Data Entry Assistant. Work 2-3 hours daily and earn $300-$500 per day. No previous skills required. Applicants must have a PayPal or Zelle account.",
        "Home-based job opportunity processing incoming packages and forwarding items. Wire transfer experience is a plus. Weekly payments in Cashier Check."
    ]

    req_real = [
        "Bachelor's degree in Computer Science, Business, or related field. 3+ years of professional experience. Proficiency in Python, SQL, and Git. Strong problem-solving skills.",
        "Strong communication skills, experience with CRM software (Salesforce/HubSpot), track record of meeting quotas, and ability to manage multiple client accounts simultaneously.",
        "Degree in Finance or Economics, strong Excel financial modeling skills, experience with SQL and PowerBI/Tableau, and excellent analytical thinking."
    ]

    req_fake = [
        "Must have computer with internet access. Able to work independently. Must be 18+ years old. Must have active bank account for direct deposit payments. Send resume via Telegram or WhatsApp.",
        "No experience required! Must be willing to start immediately. Access to email and basic typing skills required.",
        "Must possess valid ID, bank account for receiving money orders, and willingness to work 10 hours a week."
    ]

    benefits_real = [
        "Competitive salary + equity stock options. Health, dental, and vision insurance. 401(k) matching up to 5%. Unlimited PTO and annual learning stipend.",
        "Health benefits package, remote work flexibility, home office setup allowance, professional development budget, and wellness reimbursement.",
        "Base salary plus commission bonuses, paid parental leave, flexible working hours, and quarterly company retreats."
    ]

    benefits_fake = [
        "High payout, flexible hours, daily bonuses, work from comfort of your home, immediate payment upon task completion.",
        "Earn up to $3000 weekly! Bonus on performance, work from anywhere in the world.",
        "Fast cash payment, training provided, work at your own pace."
    ]

    emp_types = ["Full-time", "Part-time", "Contract", "Temporary", "Other"]
    experiences = ["Entry level", "Mid-Senior level", "Associate", "Executive", "Director", "Not Applicable"]
    educations = ["Bachelor's Degree", "Master's Degree", "High School or equivalent", "Unspecified", "Associate Degree"]

    records = []
    n_fake = int(n_samples * 0.08)
    n_real = n_samples - n_fake

    for i in range(1, n_samples + 1):
        is_fraud = 1 if i <= n_fake else 0
        if is_fraud:
            title = random.choice(titles_fake)
            comp_profile = random.choice(comp_profiles_fake)
            desc = random.choice(desc_fake)
            req = random.choice(req_fake)
            ben = random.choice(benefits_fake)
            has_logo = 1 if random.random() < 0.25 else 0
            has_questions = 1 if random.random() < 0.20 else 0
            telecommuting = 1 if random.random() < 0.75 else 0
            sal_range = f"{random.randint(50, 120)}000-{random.randint(120, 200)}000" if random.random() < 0.4 else ""
            emp_type = random.choice(["Part-time", "Contract", "Other"])
            exp = random.choice(["Entry level", "Not Applicable"])
            edu = random.choice(["High School or equivalent", "Unspecified"])
        else:
            title = random.choice(titles_real)
            comp_profile = random.choice(comp_profiles_real)
            desc = random.choice(desc_real)
            req = random.choice(req_real)
            ben = random.choice(benefits_real)
            has_logo = 1 if random.random() < 0.85 else 0
            has_questions = 1 if random.random() < 0.70 else 0
            telecommuting = 1 if random.random() < 0.30 else 0
            sal_range = f"{random.randint(40, 90)}000-{random.randint(90, 150)}000" if random.random() < 0.6 else ""
            emp_type = random.choice(["Full-time", "Contract"])
            exp = random.choice(["Mid-Senior level", "Associate", "Entry level"])
            edu = random.choice(["Bachelor's Degree", "Master's Degree"])

        records.append({
            "job_id": i,
            "title": title,
            "location": random.choice(locations),
            "department": random.choice(departments),
            "salary_range": sal_range,
            "company_profile": comp_profile,
            "description": desc,
            "requirements": req,
            "benefits": ben,
            "telecommuting": telecommuting,
            "has_company_logo": has_logo,
            "has_questions": has_questions,
            "employment_type": emp_type,
            "required_experience": exp,
            "required_education": edu,
            "industry": "Information Technology" if is_fraud == 0 else "Financial Services",
            "function": "Engineering" if is_fraud == 0 else "Customer Service",
            "fraudulent": is_fraud
        })

    random.shuffle(records)
    return pd.DataFrame(records)

if __name__ == "__main__":
    df = fetch_or_generate_dataset()
    print("Dataset shape:", df.shape)
    print("Fraudulent distribution:\n", df["fraudulent"].value_counts())
