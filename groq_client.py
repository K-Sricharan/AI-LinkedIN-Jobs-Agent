import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

DEFAULT_MODEL = "llama-3.3-70b-versatile"

def get_match_score(cv_text, job_title, job_company, job_description, model="llama-3.1-8b-instant"):
    """
    Calls the Groq API to evaluate the match quality between the CV and the job description.
    Returns a dict with:
    - 'score': int (0-10)
    - 'match_score_pct': int (0-100)
    - 'acceptance_chance_pct': int (0-100)
    - 'interview_prep_topics': list of strings (concise prep topics)
    - 'reasoning': str
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set. Please add it to your environment or a .env file.")

    client = Groq(api_key=api_key)

    system_prompt = (
        "You are an expert technical recruiter analyzing job fits. "
        "Your task is to compare the candidate's CV with the job details and evaluate if they are a good match.\n\n"
        "You must output ONLY a valid JSON object with the following keys:\n"
        "- \"score\": an integer between 0 and 10 (inclusive)\n"
        "- \"match_score_pct\": an integer between 0 and 100 representing the match percentage quality (e.g. 90 for 9/10 alignment)\n"
        "- \"acceptance_chance_pct\": an integer between 0 and 100 representing the estimated probability of getting an interview call/offer based on match quality and job requirements\n"
        "- \"interview_prep_topics\": a list of 3-5 concise, specific strings representing technical and behavioral topics the candidate should prepare for (tailored to this specific job and the candidate's profile)\n"
        "- \"reasoning\": a brief (maximum two sentences) explanation of your scoring decision.\n"
        "Do not include any extra text, markdown formatting blocks (like ```json), or explanations outside of the JSON."
    )

    user_message = (
        f"Candidate CV:\n---\n{cv_text}\n---\n\n"
        f"Job Details:\n"
        f"Title: {job_title}\n"
        f"Company: {job_company}\n"
        f"Description:\n{job_description}\n"
    )

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model=model,
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except Exception as e:
        print(f"Error calling Groq API for '{job_title}' match score: {e}")
        # Fallback values
        return {
            "score": 0,
            "match_score_pct": 0,
            "acceptance_chance_pct": 0,
            "interview_prep_topics": ["General Machine Learning", "Python Programming", "Behavioral Interview Prep"],
            "reasoning": f"Error during evaluation: {str(e)}"
        }

def generate_tailored_cv(cv_text, job_title, job_company, job_description, model=DEFAULT_MODEL):
    """
    Calls the Groq API to generate tailored CV content in JSON format.
    Ensures complete factual accuracy without inventing any new details.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")

    client = Groq(api_key=api_key)

    system_prompt = (
        "You are an expert CV editor and recruiter specializing in ATS optimization.\n"
        "Your task is to edit and tailor a candidate's CV for a specific job description.\n\n"
        "STRICT RULES:\n"
        "1. NO INVENTING: Do not invent any new experience, skills, projects, certifications, or achievements. If a technology or skill is in the job description but not in the candidate's CV, you MUST NOT add it to the CV.\n"
        "2. NO FABRICATION: Do not add any new responsibilities, companies, durations, degrees, or details. All entries must match the candidate's original CV exactly in terms of factual contents.\n"
        "3. REPHRASE & REORGANIZE: You may rephrase bullets, change their order, and emphasize details that are already present in the candidate's CV, prioritizing keywords and projects that align with the job description.\n"
        "4. FOCUS: Ensure the professional summary, experience bullets, and skills are optimized to match the target job's keywords and requirements as closely as possible, using ONLY the facts from the original CV.\n"
        "5. JSON FORMAT: You must output ONLY a valid JSON object matching the exact structure below, with no markdown formatting blocks (like ```json), no leading/trailing text, and no explanations.\n\n"
        "JSON Schema:\n"
        "{\n"
        "  \"name\": \"Jane Doe\",\n"
        "  \"title\": \"Candidate's professional title, tailored for the target role (e.g. AI Engineer or ML Engineer)\",\n"
        "  \"contact\": {\n"
        "    \"email\": \"jane.doe@email.com\",\n"
        "    \"phone\": \"+44 7700 900077\",\n"
        "    \"location\": \"London, UK\",\n"
        "    \"linkedin\": \"linkedin.com/in/janedoe\",\n"
        "    \"github\": \"github.com/janedoe\"\n"
        "  },\n"
        "  \"summary\": \"A short professional summary (2-3 sentences) tailored to the target role, highlighting relevant skills and experience from the CV.\",\n"
        "  \"skills\": {\n"
        "    \"Programming\": [\"Python\", \"Java\", \"SQL\"], (Include only items from this list that are in the original CV and relevant)\n"
        "    \"Machine Learning\": [\"Scikit-learn\", \"TensorFlow\", \"PyTorch\"], (Include only items from this list that are in the original CV and relevant)\n"
        "    \"Generative AI\": [\"LLMs\", \"RAG\", \"Prompt Engineering\", \"Vector Databases\"], (Include only items from this list that are in the original CV and relevant)\n"
        "    \"Cloud & MLOps\": [\"AWS\", \"Docker\", \"Kubernetes\", \"CI/CD\", \"MLflow\"], (Include only items from this list that are in the original CV and relevant)\n"
        "    \"Data\": [\"Pandas\", \"NumPy\", \"Spark\"] (Include only items from this list that are in the original CV and relevant)\n"
        "  },\n"
        "  \"experience\": [\n"
        "    {\n"
        "      \"role\": \"AI Engineer\",\n"
        "      \"company\": \"InnovateAI Solutions\",\n"
        "      \"duration\": \"Jul 2024 – Present\",\n"
        "      \"bullets\": [4 tailored bullet points based ONLY on original CV bullets, rephrased to emphasize keywords and skills relevant to the target job]\n"
        "    },\n"
        "    {\n"
        "      \"role\": \"Machine Learning Engineer\",\n"
        "      \"company\": \"DataVision Technologies\",\n"
        "      \"duration\": \"Jul 2023 – Jun 2024\",\n"
        "      \"bullets\": [4 tailored bullet points based ONLY on original CV bullets, rephrased to emphasize keywords and skills relevant to the target job]\n"
        "    }\n"
        "  ],\n"
        "  \"education\": [\n"
        "    {\n"
        "      \"degree\": \"Bachelor of Science (B.Sc.) in Software Engineering\",\n"
        "      \"institution\": \"Tech Valley University\",\n"
        "      \"duration\": \"Graduated: 2023\"\n"
        "    }\n"
        "  ],\n"
        "  \"projects\": [\n"
        "    {\n"
        "      \"name\": \"Enterprise Knowledge Assistant using Retrieval-Augmented Generation (RAG)\",\n"
        "      \"description\": \"A description of the project (1-2 sentences) based strictly on original CV facts but optimized for keywords.\"\n"
        "    },\n"
        "    {\n"
        "      \"name\": \"Customer Churn Prediction Platform serving business analytics teams.\",\n"
        "      \"description\": \"Description based strictly on original CV facts but optimized for keywords.\"\n"
        "    },\n"
        "    {\n"
        "      \"name\": \"Automated Document Processing pipeline using NLP and OCR technologies.\",\n"
        "      \"description\": \"Description based strictly on original CV facts but optimized for keywords.\"\n"
        "    }\n"
        "  ]\n"
        "}"
    )

    user_message = (
        f"Candidate CV:\n---\n{cv_text}\n---\n\n"
        f"Job Details:\n"
        f"Title: {job_title}\n"
        f"Company: {job_company}\n"
        f"Description:\n{job_description}\n"
    )

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model=model,
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except Exception as e:
        print(f"Error calling Groq API for '{job_title}' CV generation: {e}")
        # Return a fallback using the original content structures
        return {
            "name": "Jane Doe",
            "title": "AI Engineer",
            "contact": {
                "email": "jane.doe@email.com",
                "phone": "+44 7700 900077",
                "location": "London, UK",
                "linkedin": "linkedin.com/in/janedoe",
                "github": "github.com/janedoe"
            },
            "summary": "AI Engineer with 3 years of experience designing, developing, and deploying machine learning and generative AI solutions. Experienced in Python, deep learning, NLP, MLOps, cloud platforms, and production-grade AI systems. Strong software engineering background with a Bachelor's degree in Software Engineering.",
            "skills": {
                "Programming": ["Python", "Java", "SQL"],
                "Machine Learning": ["Scikit-learn", "TensorFlow", "PyTorch"],
                "Generative AI": ["LLMs", "RAG", "Prompt Engineering", "Vector Databases"],
                "Cloud & MLOps": ["AWS", "Docker", "Kubernetes", "CI/CD", "MLflow"],
                "Data": ["Pandas", "NumPy", "Spark"]
            },
            "experience": [
                {
                    "role": "AI Engineer",
                    "company": "InnovateAI Solutions",
                    "duration": "Jul 2024 – Present",
                    "bullets": [
                        "Developed and deployed LLM-powered applications for enterprise clients.",
                        "Built RAG pipelines using vector databases and embedding models.",
                        "Improved model inference performance by 30% through optimization techniques.",
                        "Collaborated with product and engineering teams to integrate AI services into production systems."
                    ]
                },
                {
                    "role": "Machine Learning Engineer",
                    "company": "DataVision Technologies",
                    "duration": "Jul 2023 – Jun 2024",
                    "bullets": [
                        "Designed predictive analytics models for customer behavior forecasting.",
                        "Implemented end-to-end ML pipelines using Python and cloud infrastructure.",
                        "Automated model monitoring and retraining workflows.",
                        "Reduced model deployment time by 40% through CI/CD improvements."
                    ]
                }
            ],
            "education": [
                {
                    "degree": "Bachelor of Science (B.Sc.) in Software Engineering",
                    "institution": "Tech Valley University",
                    "duration": "Graduated: 2023"
                }
            ],
            "projects": [
                {
                    "name": "Enterprise Knowledge Assistant using Retrieval-Augmented Generation (RAG).",
                    "description": "Enterprise Knowledge Assistant using Retrieval-Augmented Generation (RAG)."
                },
                {
                    "name": "Customer Churn Prediction Platform serving business analytics teams.",
                    "description": "Customer Churn Prediction Platform serving business analytics teams."
                },
                {
                    "name": "Automated Document Processing pipeline using NLP and OCR technologies.",
                    "description": "Automated Document Processing pipeline using NLP and OCR technologies."
                }
            ]
        }

def generate_cover_letter(cv_text, job_title, job_company, job_description, model=DEFAULT_MODEL):
    """
    Calls the Groq API to generate a tailored cover letter in JSON format.
    Ensures complete factual accuracy without inventing any new details.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")

    client = Groq(api_key=api_key)

    system_prompt = (
        "You are an expert professional cover letter writer.\n"
        "Your task is to write a tailored cover letter for a candidate applying to a specific job.\n\n"
        "STRICT RULES:\n"
        "1. NO INVENTING: Do not invent any experience, skills, projects, certifications, or achievements. Rely ONLY on the candidate's CV. If the job description asks for something not in the CV, do not claim the candidate has it.\n"
        "2. ALIGNMENT: Connect the candidate's actual accomplishments (e.g. building RAG pipelines, improving model inference by 30%, customer churn prediction, automating document processing NLP/OCR) to the specific requirements of the job description.\n"
        "3. TONE & STRUCTURE: Write a highly professional, engaging, and polite cover letter consisting of 3-4 paragraphs. State the target role, express interest, align candidate's experience/projects with the core responsibilities, and conclude with a professional call to action.\n"
        "4. JSON FORMAT: You must output ONLY a valid JSON object matching the exact structure below, with no markdown formatting blocks (like ```json), no leading/trailing text, and no explanations.\n\n"
        "JSON Schema:\n"
        "{\n"
        "  \"date\": \"June 4, 2026\",\n"
        "  \"recipient\": \"Hiring Team\",\n"
        "  \"company\": \"Target Company Name\",\n"
        "  \"subject\": \"Application for <Job Title> at <Company>\",\n"
        "  \"salutation\": \"Dear Hiring Team at <Company>,\",\n"
        "  \"paragraphs\": [\n"
        "     \"Paragraph 1: Introduction. State the position being applied for, express enthusiasm for the company/role, and provide a brief overview of qualifications.\",\n"
        "     \"Paragraph 2: Experience alignment. Talk about the candidate's experience at InnovateAI Solutions and DataVision Technologies, mapping achievements to the job's core needs.\",\n"
        "     \"Paragraph 3: Key projects/skills. Mention the candidate's technical skills and projects (like RAG pipeline, document processing NLP/OCR, predictive analytics models) that fit the job.\",\n"
        "     \"Paragraph 4: Conclusion. Reiterate interest, state availability, and thank the reader.\"\n"
        "  ],\n"
        "  \"sign_off\": \"Sincerely,\\n\\nJane Doe\"\n"
        "}"
    )

    user_message = (
        f"Candidate CV:\n---\n{cv_text}\n---\n\n"
        f"Job Details:\n"
        f"Title: {job_title}\n"
        f"Company: {job_company}\n"
        f"Description:\n{job_description}\n"
    )

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model=model,
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except Exception as e:
        print(f"Error calling Groq API for '{job_title}' Cover Letter generation: {e}")
        # Return a fallback using generic structures
        return {
            "date": "June 4, 2026",
            "recipient": "Hiring Team",
            "company": job_company,
            "subject": f"Application for {job_title} at {job_company}",
            "salutation": f"Dear Hiring Team at {job_company},",
            "paragraphs": [
                f"I am writing to express my strong interest in the {job_title} position at {job_company}. With three years of professional experience as an AI and Machine Learning Engineer, I am excited about the opportunity to contribute to your engineering efforts.",
                "In my current role at InnovateAI Solutions, I develop and deploy LLM-powered applications, build robust RAG pipelines, and optimize model inference performance by 30%. Prior to this, at DataVision Technologies, I designed predictive models and improved model deployment workflows by 40% using CI/CD and cloud platforms. My experience aligns closely with the core technical requirements of this role.",
                "I bring a solid educational foundation with a B.Sc. in Software Engineering, and technical proficiency across Python, PyTorch, Docker, AWS, and modern generative AI frameworks. I am eager to apply these skills to solve real-world problems and deliver high-impact solutions for your team.",
                "Thank you for your time and consideration. I welcome the opportunity to discuss how my background and technical expertise align with your goals."
            ],
            "sign_off": "Sincerely,\n\nJane Doe"
        }
