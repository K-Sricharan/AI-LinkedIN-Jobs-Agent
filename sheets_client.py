import os
import sys
import glob
import json
from functools import partial

# Ensure all prints flush immediately to stdout
print = partial(print, flush=True)

import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

SHEET_ID = os.environ.get("GOOGLE_SHEET_ID", "1wJ8rtc9rJ7S7uMxM81sNc4rgkhK1AzP_sBN2eddMeR0")

HEADERS = [
    "Job Title",
    "Company Name",
    "Match Score (%)",
    "Interview Prep Topics",
    "Acceptance Chance (%)",
    "Application Status"
]

def find_service_account_file():
    """
    Searches for a Google Service Account JSON key.
    """
    env_paths = [
        os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
        os.environ.get("GOOGLE_SHEET_CREDENTIALS"),
        os.environ.get("CREDENTIALS_FILE"),
        os.environ.get("SERVICE_ACCOUNT_FILE")
    ]
    for p in env_paths:
        if p and os.path.exists(p):
            return p

    standard_names = [
        "service_account.json",
        "service-account.json",
        "credentials.json",
        "google_credentials.json",
        "google_creds.json"
    ]
    for name in standard_names:
        if os.path.exists(name):
            return name

    for json_file in glob.glob("*.json"):
        if json_file in ["linkedin_ai_jobs.json", "package.json", "tsconfig.json"]:
            continue
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and data.get("type") == "service_account":
                    return json_file
        except Exception:
            continue

    return None

def find_oauth_client_file():
    """
    Searches for an OAuth Desktop client secret JSON file.
    """
    client_secret_files = glob.glob("client_secret*.json") + glob.glob("client_secrets.json")
    if client_secret_files:
        return client_secret_files[0]
    return None

def get_sheets_client():
    """
    Initializes and returns an authenticated gspread client.
    Supports Service Account and OAuth Desktop Client.
    """
    # 1. Check for Service Account Key (Headless)
    sa_file = find_service_account_file()
    if sa_file:
        try:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = Credentials.from_service_account_file(sa_file, scopes=scopes)
            client = gspread.authorize(creds)
            return client, f"Service Account ({sa_file})"
        except Exception as e:
            print(f"[!] Service account auth error with '{sa_file}': {e}", file=sys.stderr)

    # 2. Check for OAuth Client Secret
    oauth_file = find_oauth_client_file()
    if oauth_file:
        try:
            client = gspread.oauth(
                credentials_filename=oauth_file,
                authorized_user_filename="authorized_user.json"
            )
            return client, f"OAuth Client ({oauth_file})"
        except Exception as e:
            print(f"[!] OAuth auth error with '{oauth_file}': {e}", file=sys.stderr)

    return None, None

def append_application_to_sheet(
    sheet_id: str,
    job_title: str,
    company: str,
    match_score: str,
    prep_topics: str,
    acceptance_chance: str,
    status: str = "Applied"
) -> bool:
    """
    Appends a new job application row to the tracking Google Sheet.
    Prevents duplicate entries for the same Job Title and Company.
    """
    client, auth_type = get_sheets_client()
    if not client:
        print("       [!] Google Sheets: Unable to authenticate with Google Sheets.")
        return False

    try:
        spreadsheet = client.open_by_key(sheet_id)
        worksheet = spreadsheet.sheet1
        
        # Check / initialize headers if sheet is empty
        all_values = worksheet.get_all_values()
        if not all_values:
            worksheet.append_row(HEADERS)
            all_values = [HEADERS]

        # Check for duplicate entry (same Job Title and Company)
        for row in all_values[1:]:
            if len(row) >= 2 and row[0].strip().lower() == job_title.strip().lower() and row[1].strip().lower() == company.strip().lower():
                print(f"       [i] Google Sheet ({auth_type}): Entry for '{job_title}' @ '{company}' already exists (Duplicate skipped).\n")
                return True

        # Append row
        new_row = [
            job_title,
            company,
            match_score,
            prep_topics,
            acceptance_chance,
            status
        ]
        worksheet.append_row(new_row)
        print(f"       [+] Google Sheet ({auth_type}): Appended row for '{company}' ({match_score} Match | Status: {status}).\n")
        return True
    except Exception as e:
        print(f"       [!] Google Sheet Error: {e}\n", file=sys.stderr)
        return False
