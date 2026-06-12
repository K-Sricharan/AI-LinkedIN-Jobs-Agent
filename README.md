# 🤖 AI-Powered Job Application Agent

[![Watch the Demo Video](https://img.youtube.com/vi/mT89wYFOR-E/0.jpg)](https://youtu.be/mT89wYFOR-E)
*(Click above to watch the demo video)*

This repository contains an automated, AI-driven job application assistant. The agent extracts text from your master CV, analyzes multiple target job listings, evaluates match criteria, customizes your CV and cover letter factually for each role, generates print-ready PDF and Word (DOCX) files, and logs everything to a tracking Google Sheet.

---

## 📋 Table of Contents
1. [Overview](#-overview)
2. [Architecture & How It Works](#-architecture--how-it-works)
3. [Project Directory Structure](#-project-directory-structure)
4. [Prerequisites](#-prerequisites)
5. [Step-by-Step Setup Guide](#-step-by-step-setup-guide)
   - [Step 1: Install Dependencies](#step-1-install-dependencies)
   - [Step 2: Configure Environment Variables](#step-2-configure-environment-variables)
   - [Step 3: Setup Google Sheets Integration](#step-3-setup-google-sheets-integration)
   - [Step 4: Prepare Input Files](#step-4-prepare-input-files)
   - [Step 5: Run the Agent](#step-5-run-the-agent)
6. [Document Styling & Design Standards](#-document-styling--design-standards)
7. [Error Handling & Resiliency](#-error-handling--resiliency)

---

## 🔍 Overview

The **AI-Powered Job Application Agent** is designed to streamline the repetitive parts of the job hunt while maintaining strict personalization and quality control. By leveraging the Groq API (models `llama-3.3-70b-versatile` and `llama-3.1-8b-instant`), it performs:
* **Match Evaluation:** Scores alignment, estimates acceptance probability, and suggests 3-5 custom interview preparation topics.
* **Factual Tailoring:** Optimizes CV summaries, bullet points, and skills to highlight target job keywords **without fabricating or inventing** any qualifications.
* **Cover Letter Drafting:** Synthesizes professional 3-4 paragraph cover letters linking the candidate's actual accomplishments to specific job responsibilities.
* **Multi-Format Compiling:** Automatically outputs beautiful, print-ready PDF and Word (`.docx`) files.
* **Auto-Logging:** Appends application records (Title, Company, Match Score, Prep Topics, Acceptance Chance, Application Status, and Date) dynamically to a central tracking Google Sheet, avoiding duplicate entries.

---

## 📐 Architecture & How It Works

```
   +--------------+      +-------------------+
   |  my-cv.pdf   |      | linkedin_jobs.json|
   +------+-------+      +---------+---------+
          |                        |
          v                        v
  [Extract CV Text]         [Parse Job Listings]
          |                        |
          +-----------+------------+
                      |
                      v
      +---------------+---------------+
      |         Evaluator             | (groq_client.py)
      | - Match Scoring & Reasoning   |
      | - Bullet-point Tailoring      |
      | - Cover Letter Content Prep   |
      +---------------+---------------+
                      |
                      v
      +---------------+---------------+
      |        Doc Compiler           | (doc_generator.py)
      | - Generate tailored docx      | (python-docx)
      | - Generate tailored pdf       | (reportlab)
      +---------------+---------------+
                      |
                      +-----------------------------+
                      |                             |
                      v                             v
           +----------+----------+       +----------+----------+
           |   outputs/ Directory|       | Google Sheets Track |
           |  (PDF & DOCX files) |       | (Status & Analytics)|
           +---------------------+       +---------------------+
```

---

## 📁 Project Directory Structure

Below is the layout of the project:

```
├── main.py                     # Main orchestrator (CV parser, sheets updater, CLI controller)
├── groq_client.py              # Groq API wrappers for scoring, CV tailoring, and cover letters
├── doc_generator.py            # Layout templates and compilers for Word (.docx) and PDF files
├── my-cv.pdf                   # YOUR input CV (Master CV)
├── linkedin_ai_jobs.json       # Target job listings parsed from scraping pipelines
├── linkedin_ai_jobs.csv        # Alternative CSV-formatted job listings
├── requirements.txt            # Python dependencies file
├── .env                        # Private local configuration (API keys)
├── client_secret_*.json        # OAuth Client Secret file for Google Sheets access
├── authorized_user.json        # Cached OAuth token for user access
└── outputs/                    # Output directory for customized application files
    └── Company_Job_Title/      # Auto-sanitized folders for each job
        ├── tailored_cv.pdf     # Print-ready tailored CV
        ├── tailored_cv.docx    # Fully editable Word document tailored CV
        ├── cover_letter.pdf    # Print-ready tailored Cover Letter
        └── cover_letter.docx   # Fully editable Word cover letter
```

---

## ⚙️ Prerequisites

* **Python 3.10+**
* A **Groq API Account & API Key** (Get one at [console.groq.com](https://console.groq.com/))
* A **Google Cloud Project** with the Google Sheets API enabled (optional but required for sheets logging)

---

## 🚀 Step-by-Step Setup Guide

### Step 1: Install Dependencies

1. Clone or copy this repository to your local workspace.
2. Open your terminal and navigate to the project directory:
   ```bash
   cd /path/to/ai-jobs-agent
   ```
3. Create and activate a Python virtual environment using `uv`:
   ```bash
   # Create the virtual environment
   uv venv

   # Activate the virtual environment
   # On macOS/Linux:
   source .venv/bin/activate
   # On Windows:
   .venv\Scripts\activate
   ```
4. Install all required packages using `uv`:
   ```bash
   uv pip install -r requirements.txt
   ```

### Step 2: Configure Environment Variables

Create a file named `.env` in the root of the project (if it doesn't already exist) and define your Groq API Key:

```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

### Step 3: Setup Google Sheets Integration

The agent dynamically logs applications to a tracking Google Sheet. 

1. **Get Sheet ID:**
   Open the Google Sheet where you want to track applications. Extract the long ID string from the URL:
   `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE/edit`
   Open [main.py](file:///Users/hassan.mahmood/Desktop/ai-jobs-agent/main.py) and update the `SHEET_ID` constant on line 11:
   ```python
   SHEET_ID = "YOUR_SHEET_ID_HERE"
   ```

2. **Configure Authentication Credentials:**
   You can authenticate with Google Sheets in one of two ways:
   
   * **Method A: Google OAuth Client ID (Recommended for personal use)**
     1. Go to the [Google Cloud Console Credentials Page](https://console.cloud.google.com/apis/credentials).
     2. Create an **OAuth 2.0 Client ID** (Desktop Application type).
     3. Download the credentials JSON file.
     4. Save the file in the project's root directory, naming it exactly as downloaded (e.g., `client_secret_xxxx.json`).
     5. On the first run, the terminal will open a browser window asking you to authenticate. Once approved, it saves a cached token to `authorized_user.json` so you do not have to authenticate again.

   * **Method B: Service Account (Recommended for automated/non-interactive workflows)**
     1. Go to the [Google Cloud Console Service Accounts Page](https://console.cloud.google.com/iam/service-accounts).
     2. Create a **Service Account** and generate a new key in JSON format.
     3. Save the JSON file in the project's root directory as `service_account.json` or `credentials.json`.
     4. Share the target tracking Google Sheet with the Service Account email address (giving it Editor access).

### Step 4: Prepare Input Files

1. **Your Master CV:**
   Place your master resume in the root directory and name it **`my-cv.pdf`**. Ensure it contains factual details about your education, history, skills, and projects.
2. **Job Listings:**
   Place your job listings in **`linkedin_ai_jobs.json`**. The script expects a JSON array of objects with the following format:
   ```json
   [
     {
       "Title": "AI Engineer",
       "Company": "The Premier League",
       "Location": "London, UK",
       "Description": "About the job..."
     }
   ]
   ```

### Step 5: Run the Agent

Execute the agent from your terminal:
```bash
python main.py
```

#### What happens during execution:
1. **CV Extraction:** Parses your `my-cv.pdf` and loads it into memory.
2. **Batch Processing:** Loops through each job listing in `linkedin_ai_jobs.json`.
3. **LLM Evaluation:** Sends the job details and CV text to Groq for matching.
4. **Folder Creation:** Sanitizes the company and job title names to create a directory under `outputs/` (e.g., `outputs/Melotech_AIML_Engineer_Intern`).
5. **Resume & Cover Letter Generation:** 
   - Generates the tailored content using Groq.
   - Compiles Word (`tailored_cv.docx` and `cover_letter.docx`) and PDF (`tailored_cv.pdf` and `cover_letter.pdf`) documents.
   *Note: If these files already exist in the folder, the script will skip LLM query calls to save API tokens.*
6. **Sheet Update:** Logs application details to the designated Google Sheet.
7. **Report:** Displays a comprehensive tabular summary of all matching jobs in your console, showing high-scoring matches (> 6/10) first.

---

## 🎨 Document Styling & Design Standards

The generated files adhere to elite professional layout standards:
* **Palette:** Built around corporate design metrics:
  - **Primary:** Deep Navy (`#1A365D`) for headers and accent lines.
  - **Secondary:** Slate/Charcoal (`#4A5568`) for titles and dates.
  - **Body Text:** Off-black/Dark Grey (`#2D3748`) to enhance readability.
* **Typography:** Calibri is used for Microsoft Word documents, while standard Helvetica is mapped for PDF generation.
* **Layout Structure:**
  - **CV Template:** Formats standard single-page guidelines using 0.5" (PDF) and 0.75" (Word) margins, customized professional sections, tables for clean align-right dates, and neat bullet lists.
  - **Cover Letter Template:** Incorporates professional margins (1.0"), standardized sender headers, formal recipient blocks, and justified paragraphs.

---

## 🛠️ Error Handling & Resiliency

* **File Caching:** Before querying Groq, the orchestrator checks if output documents already exist. If found, it skips token-expensive LLM generations, allowing you to resume interrupted runs instantly.
* **Google Sheets Resilience:** If Sheets API logging fails (due to network limits or credential expiration), the script logs the error message to `sys.stderr` and continues processing the remaining jobs in the queue.
* **Failsafe Content:** If an LLM call fails or times out, the code gracefully returns fallback JSON payloads matching the schema exactly, preventing execution crashes.
