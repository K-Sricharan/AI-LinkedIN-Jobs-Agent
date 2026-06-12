import os
import json
import sys
import re
import datetime
from pypdf import PdfReader
from groq_client import get_match_score, generate_tailored_cv, generate_cover_letter
from doc_generator import generate_cv_docx, generate_cv_pdf, generate_cl_docx, generate_cl_pdf

# Constants
SHEET_ID = "11ICANax2ZMcxDFkM3LmAU9A9nGqWUWlbC0jdVntn24Q"

def extract_pdf_text(pdf_path):
    """
    Extracts text content from a PDF file using pypdf.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}", file=sys.stderr)
        sys.exit(1)

def load_jobs_json(json_path):
    """
    Loads job listings from the scraped JSON file.
    """
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}", file=sys.stderr)
        sys.exit(1)

def sanitize_folder_name(company_name, job_title):
    """
    Sanitizes company name and job title to create a clean, safe folder name.
    """
    combined = f"{company_name}_{job_title}"
    # Remove special characters except alphanumeric, spaces, underscores, and hyphens
    clean = re.sub(r'[^a-zA-Z0-9\s_-]', '', combined)
    # Replace spaces and hyphens with underscores
    clean = re.sub(r'[\s-]+', '_', clean)
    # Remove consecutive underscores
    clean = re.sub(r'_+', '_', clean)
    return clean.strip('_')

def append_to_google_sheet(sheet_id, job_title, company_name, match_score, prep_topics, acceptance_chance):
    """
    Appends a new job application row to Google Sheets using gspread.
    Ensures duplicate rows aren't created for the same company/title combo.
    """
    import gspread
    
    # Try finding credentials file
    creds_file = None
    for name in ['service_account.json', 'credentials.json']:
        full_path = os.path.join("/Users/hassan.mahmood/Desktop/ai-jobs-agent", name)
        if os.path.exists(full_path):
            creds_file = full_path
            break

    # Look for client secret file if no service account file exists
    client_secret_file = None
    root_dir = "/Users/hassan.mahmood/Desktop/ai-jobs-agent"
    for name in os.listdir(root_dir):
        if name.startswith("client_secret") and name.endswith(".json"):
            client_secret_file = os.path.join(root_dir, name)
            break

    if creds_file:
        try:
            with open(creds_file, 'r') as f:
                data = json.load(f)
            if data.get("type") == "service_account":
                print(f"    -> Using Service Account credentials from {os.path.basename(creds_file)}")
                gc = gspread.service_account(filename=creds_file)
            else:
                # Treat as OAuth client secret
                client_secret_file = creds_file
                creds_file = None
        except Exception as e:
            print(f"    -> Error parsing {os.path.basename(creds_file)}: {e}")

    if not creds_file and client_secret_file:
        print(f"    -> Using OAuth Client Secret from {os.path.basename(client_secret_file)}")
        authorized_user_path = os.path.join(root_dir, "authorized_user.json")
        gc = gspread.oauth(
            credentials_filename=client_secret_file,
            authorized_user_filename=authorized_user_path
        )
    elif not creds_file:
        raise FileNotFoundError("Google Sheets credentials file (service_account.json, credentials.json, or client_secret*.json) not found in the workspace root.")

    sh = gc.open_by_key(sheet_id)
    worksheet = sh.get_worksheet(0) # First sheet
    
    # Fetch all existing values
    all_values = worksheet.get_all_values()
    
    # Standard header row if sheet is empty
    headers = [
        "Job Title", 
        "Company Name", 
        "Match Score (%)", 
        "Interview Prep Topics", 
        "Acceptance Chance (%)", 
        "Application Status", 
        "Application Date"
    ]
    
    if not all_values:
        worksheet.append_row(headers)
        all_values = [headers]
        
    header_row = all_values[0]
    
    # Locate Job Title and Company Name columns
    def find_col_idx(col_name, default_idx):
        for idx, col in enumerate(header_row):
            if col.strip().lower() == col_name.lower():
                return idx
        return default_idx
        
    title_idx = find_col_idx("Job Title", 0)
    company_idx = find_col_idx("Company Name", 1)
    
    # Check if entry already exists (case-insensitive check)
    for row in all_values[1:]:
        if len(row) > max(title_idx, company_idx):
            existing_title = row[title_idx].strip().lower()
            existing_company = row[company_idx].strip().lower()
            if existing_title == job_title.strip().lower() and existing_company == company_name.strip().lower():
                print(f"    -> Row already exists for '{job_title}' at '{company_name}' in Google Sheets. Skipping.")
                return False
                
    # Prepare details and append
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    new_row = [
        job_title,
        company_name,
        f"{match_score}%" if not str(match_score).endswith('%') else match_score,
        ", ".join(prep_topics) if isinstance(prep_topics, list) else prep_topics,
        f"{acceptance_chance}%" if not str(acceptance_chance).endswith('%') else acceptance_chance,
        "Applied",
        today_str
    ]
    
    worksheet.append_row(new_row)
    print(f"    -> Added new row to Google Sheets for '{job_title}' at '{company_name}'.")
    return True

def main():
    cv_path = "/Users/hassan.mahmood/Desktop/ai-jobs-agent/my-cv.pdf"
    jobs_path = "/Users/hassan.mahmood/Desktop/ai-jobs-agent/linkedin_ai_jobs.json"
    
    # 1. Check GROQ_API_KEY
    if not os.environ.get("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY environment variable is not set. Please set it in your environment or .env file.", file=sys.stderr)
        sys.exit(1)
    
    # 2. Extract CV text
    print("Extracting text from original CV...")
    cv_text = extract_pdf_text(cv_path)
    print(f"CV text extracted successfully. Characters: {len(cv_text)}")
    
    # 3. Load Jobs JSON
    print("Loading job listings...")
    jobs = load_jobs_json(jobs_path)
    print(f"Loaded {len(jobs)} job listings.")
    
    results = []
    print("\nStarting evaluation and document tailoring for job listings...")
    print("=" * 70)
    
    for i, job in enumerate(jobs):
        title = job.get("Title", "Unknown Title")
        company = job.get("Company", "Unknown Company")
        location = job.get("Location", "")
        description = job.get("Description", "")
        
        print(f"\n[{i+1}/{len(jobs)}] Processing: '{title}' at {company}")
        
        # A. Evaluate match details (including score, acceptance, prep topics)
        evaluation = get_match_score(cv_text, title, company, description)
        score = evaluation.get("score", 0)
        score_pct = evaluation.get("match_score_pct", score * 10)
        acceptance_chance = evaluation.get("acceptance_chance_pct", 50)
        prep_topics = evaluation.get("interview_prep_topics", ["Technical Deep Dive", "System Architecture", "Behavioral Alignment"])
        reasoning = evaluation.get("reasoning", "No explanation provided.")
        
        print(f"    -> Match Score: {score_pct}% (Original: {score}/10)")
        print(f"    -> Acceptance Chance: {acceptance_chance}%")
        print(f"    -> Prep Topics: {', '.join(prep_topics)}")
        print(f"    -> Match Reasoning: {reasoning}")
        
        # B. Tailor folder name and create folder
        folder_name = sanitize_folder_name(company, title)
        output_dir = os.path.join("/Users/hassan.mahmood/Desktop/ai-jobs-agent/outputs", folder_name)
        os.makedirs(output_dir, exist_ok=True)
        print(f"    -> Output directory: outputs/{folder_name}")
        
        # C. Generate Tailored CV Content & Cover Letter Content (Skip if already exist)
        cv_docx_path = os.path.join(output_dir, "tailored_cv.docx")
        cv_pdf_path = os.path.join(output_dir, "tailored_cv.pdf")
        cl_docx_path = os.path.join(output_dir, "cover_letter.docx")
        cl_pdf_path = os.path.join(output_dir, "cover_letter.pdf")
        
        files_exist = os.path.exists(cv_docx_path) and os.path.exists(cv_pdf_path) and os.path.exists(cl_docx_path) and os.path.exists(cl_pdf_path)
        
        if files_exist:
            print("    -> Tailored files already exist. Skipping LLM generation and compiling.")
        else:
            print("    -> Tailoring CV content...")
            tailored_cv_data = generate_tailored_cv(cv_text, title, company, description)
            
            print("    -> Generating cover letter content...")
            tailored_cl_data = generate_cover_letter(cv_text, title, company, description)
            
            print("    -> Saving tailored CV files...")
            generate_cv_docx(tailored_cv_data, cv_docx_path)
            generate_cv_pdf(tailored_cv_data, cv_pdf_path)
            
            print("    -> Saving cover letter files...")
            generate_cl_docx(tailored_cl_data, cl_docx_path)
            generate_cl_pdf(tailored_cl_data, cl_pdf_path)
        
        # E. Google Sheets integration
        try:
            print("    -> Updating Google Sheet...")
            append_to_google_sheet(
                sheet_id=SHEET_ID,
                job_title=title,
                company_name=company,
                match_score=score_pct,
                prep_topics=prep_topics,
                acceptance_chance=acceptance_chance
            )
            print("    -> Google Sheet update process completed.")
        except Exception as e:
            # Guidelines: Log failure and continue processing remaining jobs
            print(f"    -> Google Sheet update FAILED: {e}", file=sys.stderr)
            
        print("    -> Generation complete.")
        
        results.append({
            "title": title,
            "company": company,
            "location": location,
            "score": score,
            "score_pct": score_pct,
            "reasoning": reasoning,
            "folder": f"outputs/{folder_name}"
        })
        print("-" * 70)
        
    # 5. Print final report
    print("\n" + "=" * 70)
    print("                      EVALUATION & PROCESSING SUMMARY")
    print("=" * 70)
    
    print(f"{'Job Title':<35} | {'Company':<22} | {'Score':<5}")
    print("-" * 70)
    for r in results:
        display_title = r["title"][:32] + "..." if len(r["title"]) > 35 else r["title"]
        display_company = r["company"][:19] + "..." if len(r["company"]) > 22 else r["company"]
        print(f"{display_title:<35} | {display_company:<22} | {r['score']}/10")
        
    print("\n" + "=" * 70)
    print("                  RECOMMENDED MATCHES (SCORE > 6)")
    print("=" * 70)
    
    matches = [r for r in results if r["score"] > 6]
    if matches:
        for r in matches:
            print(f"★ {r['title']} at {r['company']} ({r['location']})")
            print(f"  Score: {r['score_pct']}%")
            print(f"  Output folder: {r['folder']}")
            print(f"  Reason: {r['reasoning']}\n")
    else:
        print("No job matches scored above 6/10.")
    print("=" * 70)

if __name__ == "__main__":
    main()
