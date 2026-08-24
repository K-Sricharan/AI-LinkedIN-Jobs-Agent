import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

DEFAULT_MODEL = "llama-3.3-70b-versatile"
BACKUP_MODEL = "llama-3.1-8b-instant"

def get_groq_client():
    """
    Initializes and returns the Groq client using GROQ_API_KEY from environment or .env.
    """
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        return None
    return Groq(api_key=api_key)

def score_job_match(cv_text, job_title, job_company, job_description, model=DEFAULT_MODEL):
    """
    Calls the Groq API to evaluate the match quality between the candidate's CV and the job posting.
    
    System prompt instructs the LLM to score the candidate match from 0 to 10.
    
    Returns a dictionary containing:
    - 'score': float (0.0 to 10.0)
    - 'match_status': str ('Strong Match', 'Moderate Match', 'Low Match')
    - 'reasoning': str (concise summary of match quality)
    """
    client = get_groq_client()
    if not client:
        return {
            "score": 0.0,
            "match_status": "API Key Missing",
            "reasoning": "GROQ_API_KEY is not set. Please add it to your .env file or environment variables."
        }

    system_prompt = (
        "You are an expert technical recruiter and AI hiring specialist.\n"
        "Your task is to evaluate how well a candidate's CV matches a specific job description.\n\n"
        "Evaluation Guidelines:\n"
        "- Score the candidate's qualification match on a scale of 0 to 10.\n"
        "- 0 to 4.0: Poor match / lacks core required skills or experience.\n"
        "- 4.1 to 6.0: Partial match / possesses some relevant skills but misses key requirements.\n"
        "- 6.1 to 8.0: Good match / solid overlap with required core skills and experience.\n"
        "- 8.1 to 10.0: Outstanding match / meets or exceeds required skills, tools, and background.\n\n"
        "You MUST respond ONLY with a valid JSON object matching this schema:\n"
        "{\n"
        '  "score": <number between 0 and 10, e.g. 7.5>,\n'
        '  "match_status": "<Strong Match / Moderate Match / Low Match>",\n'
        '  "reasoning": "<1-2 concise sentences explaining the score based on candidate skills vs job requirements>"\n'
        "}\n"
        "Do not include any extra text or explanation outside of the JSON object."
    )

    user_message = (
        f"### Candidate CV:\n{cv_text}\n\n"
        f"### Job Opening:\n"
        f"Title: {job_title}\n"
        f"Company: {job_company}\n"
        f"Job Description:\n{job_description}\n"
    )

    models_to_try = [model, BACKUP_MODEL]

    for target_model in models_to_try:
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                model=target_model,
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content.strip()
            data = json.loads(content)
            
            score = float(data.get("score", 0.0))
            return {
                "score": score,
                "match_status": data.get("match_status", "Evaluated"),
                "reasoning": data.get("reasoning", "")
            }
        except Exception as e:
            err_msg = str(e)
            # If rate limited or model error, try backup model
            continue

    return {
        "score": 0.0,
        "match_status": "API Error",
        "reasoning": "Could not connect to Groq API. Please verify your GROQ_API_KEY is valid and active."
    }
