import os
import sys
import json
import re

# Ensure UTF-8 console encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from doc_generator import generate_cv_docx, generate_cv_pdf, generate_cl_docx, generate_cl_pdf

# Ensure output directory exists
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_folder_name(company, title):
    combined = f"{company}_{title}"
    clean = re.sub(r'[^a-zA-Z0-9\s_-]', '', combined)
    clean = re.sub(r'[\s-]+', '_', clean)
    clean = re.sub(r'_+', '_', clean)
    return clean.strip('_')

# Load the 10 LinkedIn jobs
with open("linkedin_ai_jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

print(f"Loaded {len(jobs)} jobs for tailoring.")

# Base candidate details
CANDIDATE = {
    "name": "Hassan Mahmood",
    "contact": {
        "email": "hassan.mahmood@email.com",
        "phone": "+91 98765 43210",
        "location": "Hyderabad, Telangana, India",
        "linkedin": "linkedin.com/in/hassan-mahmood",
        "github": "github.com/AIwithhassan"
    },
    "education": [
        {
            "degree": "Bachelor of Science in Statistics and Computer Science",
            "institution": "Jagruti Degree and PG College",
            "duration": "Jul 2018 -- Jul 2021",
            "details": "CGPA: 8.9 / 10.0"
        }
    ]
}

# Tailoring configurations customized for each of the 10 job descriptions
tailored_configs = [
    # 1. Shamrock AI - AI Engineer
    {
        "title": "AI Engineer (Agentic Systems & LLM Validation)",
        "summary": "Data Scientist and AI Engineer with 5 years of experience at Deloitte specializing in production Generative AI, agentic systems, and robust RAG architectures. Proven track record designing enterprise-grade multi-agent platforms with LangGraph and MCP, implementing automated evaluation frameworks (DeepEval, Ragas), and deploying reliable LLM pipelines across complex enterprise data ecosystems.",
        "skills": {
            "Agentic AI & LLMs": ["LangGraph", "Multi-Agent Orchestration", "MCP (Model Context Protocol)", "Claude", "GPT-4", "Prompt Engineering", "Fine-Tuning (PEFT/LoRA)"],
            "RAG & Retrieval": ["RAG Architecture", "FAISS", "Vector Embeddings", "Semantic Search", "Chunking Strategies"],
            "Evaluation & Guardrails": ["DeepEval", "Ragas", "LLM-as-Judge", "Deterministic Guardrails", "Regression Testing"],
            "Engineering & Cloud": ["Python", "FastAPI", "SQL", "Docker", "Git", "REST APIs", "Streamlit"]
        },
        "experience": [
            {
                "role": "Data Scientist / AI Engineer",
                "company": "Deloitte",
                "duration": "Jul 2021 -- Present",
                "bullets": [
                    "Engineered enterprise AI systems, RAG pipelines, and automated reasoning workflows across 3 major AI initiatives using Python, LangGraph, MCP, and FastAPI.",
                    "Architected 'FinPilot AI', a multi-agent financial analysis platform utilizing Deloitte internal LLMs and LangGraph ReAct; supervisor agent managed state and routing across 4 intent categories with deterministic guardrails.",
                    "Engineered an MCP-based multi-format ingestion workflow using FastMCP, SQLite, and local file drivers to process 3 file formats, reducing ingestion latency by ~80%.",
                    "Developed a RAG and calculation engine combining FAISS-based semantic search with deterministic Python tax logic, achieving a 93% evaluation score on DeepEval benchmarks.",
                    "Architected 'ALAN-GPT', a multi-document RAG search engine across 500+ production ML models, indexing documentation and reducing developer lookup time by 75% with a 91% retrieval score.",
                    "Developed a Generative AI pipeline processing 1,000+ audio call recordings into structured call scripts and summaries, reducing manual documentation effort by 80%."
                ]
            }
        ],
        "projects": [
            {
                "name": "FinPilot AI | Multi-Agent Enterprise Reasoning Platform",
                "description": "Integrated LLMs with LangGraph ReAct agent orchestration, FastMCP ingestion, and DeepEval evaluation pipelines (93% score) for high-stakes enterprise financial data."
            },
            {
                "name": "ALAN-GPT | Multi-Document RAG Search Engine",
                "description": "Production indexing and semantic vector retrieval system across 500+ production ML models and developer documentation, boosting retrieval accuracy to 91%."
            }
        ],
        "cover_letter_subject": "Application for AI Engineer Position -- Shamrock AI",
        "cover_letter_paragraphs": [
            "I am writing to express my strong enthusiasm for the AI Engineer position at Shamrock AI in Hyderabad. With 5 years of hands-on experience at Deloitte engineering production-grade Generative AI applications, multi-agent systems, and automated evaluation pipelines, I have focused extensively on the exact challenge you are tackling: making LLMs reliable, deterministic, and enterprise-ready for mission-critical workflows.",
            "In my recent work at Deloitte, I architected FinPilot AI--a multi-agent financial analysis platform utilizing LangGraph ReAct orchestration and the Model Context Protocol (MCP) to ingest complex enterprise data while reducing latency by 80%. To prevent hallucinations and enforce compliance, I built end-to-end evaluation frameworks with DeepEval, achieving a 93% benchmark score across multi-step reasoning tasks. Similarly, I led the architecture of ALAN-GPT, indexing documentation across 500+ production ML models with a 91% retrieval evaluation score.",
            "Shamrock AI's commitment to building production AI at enterprise scale without 'prompt-wrapping' aligns perfectly with my engineering philosophy. I am eager to bring my background in Python, agentic architectures, RAG optimization, and evaluation frameworks to help Shamrock AI deliver resilient, high-performance AI solutions. I welcome the opportunity to discuss how my experience can support your engineering goals."
        ]
    },

    # 2. Tata Consultancy Services - Artificial Intelligence Engineer
    {
        "title": "Artificial Intelligence Engineer",
        "summary": "Results-driven AI & Machine Learning Engineer with 5 years of progressive experience at Deloitte delivering scalable enterprise AI applications. Expert in machine learning workflows, deep neural architectures, RAG pipelines, and generative AI models using Python, PyTorch, Scikit-Learn, and FastAPI for enterprise transformation initiatives.",
        "skills": {
            "Machine Learning & AI": ["PyTorch", "Scikit-Learn", "Deep Learning", "Neural Networks", "Generative AI", "Statistical Modeling"],
            "LLM & RAG Systems": ["RAG Architecture", "FAISS", "Embeddings", "LangGraph", "Prompt Engineering", "Fine-Tuning (LoRA)"],
            "Software & Pipelines": ["Python", "FastAPI", "SQL", "Pandas", "NumPy", "Pydantic", "REST APIs"],
            "Deployment & Tooling": ["Docker", "Git", "Streamlit", "Power BI", "Model Evaluation (DeepEval)"]
        },
        "experience": [
            {
                "role": "AI Engineer / Data Scientist",
                "company": "Deloitte",
                "duration": "Jul 2021 -- Present",
                "bullets": [
                    "Spearheaded the design and deployment of enterprise-scale AI and ML systems, predictive pipelines, and automated reporting across critical client initiatives.",
                    "Designed and implemented high-performance RAG architectures combining FAISS semantic vector search with deterministic application logic (93% DeepEval score).",
                    "Architected documentation search and model indexing systems covering 500+ production ML models, improving developer retrieval speed by 75%.",
                    "Built automated GenAI transcription and analysis pipelines converting 1,000+ unstructured audio recordings into structured summaries.",
                    "Two-time Deloitte Impact Award recipient for innovation in automated intelligence and enterprise analytics."
                ]
            }
        ],
        "projects": [
            {
                "name": "Enterprise RAG & Search Platform (ALAN-GPT)",
                "description": "Architected technical and API search across 500+ ML models, integrating FAISS vector indexing with a 91% retrieval accuracy score."
            },
            {
                "name": "Automated Call & Audio Intelligence System",
                "description": "Built an automated NLP/LLM audio processing pipeline converting 1,000+ recordings into structured data, reducing manual workload by 80%."
            }
        ],
        "cover_letter_subject": "Application for Artificial Intelligence Engineer -- Tata Consultancy Services",
        "cover_letter_paragraphs": [
            "I am pleased to submit my application for the Artificial Intelligence Engineer role at Tata Consultancy Services in Hyderabad. Having spent the past 5 years as a Data Scientist and AI Engineer at Deloitte, I specialize in architecting scalable machine learning systems, deep learning solutions, and generative AI pipelines that deliver tangible business outcomes.",
            "Throughout my tenure at Deloitte, I have engineered full-lifecycle AI solutions--from data preprocessing and model development in PyTorch/Scikit-Learn to deploying containerized FastAPI microservices. My work on ALAN-GPT established a production-grade RAG indexing system across 500+ machine learning models, achieving a 91% retrieval precision and slashing developer lookup times by 75%. Additionally, my multi-agent financial platform (FinPilot AI) achieved a 93% evaluation score on DeepEval.",
            "TCS is renowned for pioneering large-scale enterprise AI transformations. I am excited by the opportunity to bring my technical expertise in Python, machine learning algorithms, and modern LLM frameworks to TCS's high-performing engineering teams. Thank you for your consideration, and I look forward to the possibility of an interview."
        ]
    },

    # 3. Accenture in India - AI / ML Engineer
    {
        "title": "AI / ML Engineer (Production Pipelines & GenAI)",
        "summary": "Versatile AI/ML Engineer with 5 years of Deloitte experience building robust application pipelines, cloud-ready AI services, and Generative AI systems. Proven expertise in machine learning, deep learning, chatbot architectures, NLP, and model lifecycle management with a track record of driving operational efficiency.",
        "skills": {
            "Core ML & Deep Learning": ["Machine Learning (ML)", "Scikit-Learn", "PyTorch", "Neural Networks", "NLP", "Statistical Analysis"],
            "Generative AI & LLMs": ["Prompt Engineering", "Fine-Tuning (PEFT/LoRA)", "LangGraph", "RAG Pipelines", "Chatbots & Conversational AI"],
            "Application Pipelines": ["Python", "FastAPI", "SQL", "Pandas", "NumPy", "Pydantic", "RESTful Microservices"],
            "Cloud & Deployment": ["Docker", "Git", "CI/CD Workflows", "Streamlit", "DeepEval", "Ragas"]
        },
        "experience": [
            {
                "role": "Data Scientist / AI & ML Engineer",
                "company": "Deloitte",
                "duration": "Jul 2021 -- Present",
                "bullets": [
                    "Engineered production-quality AI applications and ML pipelines integrating Generative AI models, deep learning, and automated data workflows.",
                    "Developed multi-agent conversational systems using LangGraph and FastMCP, orchestrating intent routing and reducing data ingestion latency by 80%.",
                    "Built RAG search pipelines combining FAISS vector search with deterministic business rules, scoring 93% on DeepEval evaluation suites.",
                    "Constructed NLP pipelines processing 1,000+ unstructured audio recordings into structured analytical reports, reducing manual effort by 80%.",
                    "Collaborated cross-functionally to mentor junior engineers, establish best practices, and deliver high-impact enterprise solutions (2x Deloitte Impact Award winner)."
                ]
            }
        ],
        "projects": [
            {
                "name": "FinPilot AI | Multi-Agent Conversational Platform",
                "description": "Engineered multi-agent state management and intent classification with LangGraph ReAct and FastMCP, achieving 93% DeepEval score."
            },
            {
                "name": "Unstructured Audio & Text Intelligence Pipeline",
                "description": "Developed an automated GenAI pipeline processing 1,000+ multi-format recordings into structured data for relationship managers."
            }
        ],
        "cover_letter_subject": "Application for AI / ML Engineer (Job ID: 4448355778) -- Accenture in India",
        "cover_letter_paragraphs": [
            "I am writing to apply for the AI / ML Engineer position at Accenture in India (Hyderabad). With 5 years of experience at Deloitte developing AI tools, machine learning pipelines, and production-ready Generative AI applications, I am eager to contribute to Accenture's advanced AI innovation initiatives.",
            "My experience encompasses the complete ML and GenAI lifecycle. At Deloitte, I engineered FinPilot AI--a multi-agent platform orchestrating state management and intent routing using LangGraph and FastMCP, which reduced data ingestion latency by ~80%. I also spearheaded the creation of high-precision RAG search pipelines indexing over 500 machine learning models (91% retrieval score) and developed automated NLP pipelines for unstructured audio analytics.",
            "Accenture's focus on building robust, production-quality AI application pipelines aligns seamlessly with my background in Python, machine learning, and scalable service design. I would be thrilled to bring my problem-solving skills and passion for AI innovation to your engineering team."
        ]
    },

    # 4. Tata Consultancy Services - Generative AI Engineer
    {
        "title": "Generative AI Engineer (LLM Frameworks & Enterprise RAG)",
        "summary": "Senior Generative AI Specialist and Data Scientist with 5 years of intensive experience at Deloitte architecting enterprise LLM applications, RAG systems, and multi-agent workflows. Deep expertise in prompt engineering, fine-tuning (LoRA/PEFT), vector indexing, and model evaluation across cloud and on-premise environments.",
        "skills": {
            "Generative AI & LLMs": ["Prompt Engineering", "Fine-Tuning (PEFT/LoRA)", "LangGraph", "Hugging Face", "Model Context Protocol (MCP)"],
            "RAG & Search Engines": ["RAG Architecture", "FAISS", "Embeddings", "Vector Databases", "Semantic Chunking"],
            "Evaluation & Benchmarking": ["DeepEval", "Ragas", "LLM Guardrails", "AI Safety & Governance"],
            "Programming & Frameworks": ["Python", "PyTorch", "FastAPI", "SQL", "Docker", "Git", "Streamlit"]
        },
        "experience": [
            {
                "role": "Generative AI Engineer / Data Scientist",
                "company": "Deloitte",
                "duration": "Jul 2021 -- Present",
                "bullets": [
                    "Led the technical design and deployment of 3 flagship Generative AI initiatives utilizing LangGraph, MCP, and advanced RAG architectures.",
                    "Engineered 'FinPilot AI' multi-agent platform using LangGraph ReAct and FastMCP, orchestrating 4 intent categories and cutting ingestion latency by 80%.",
                    "Developed high-accuracy RAG search engine (ALAN-GPT) across 500+ production ML models, achieving a 91% retrieval evaluation score.",
                    "Implemented comprehensive LLM evaluation and benchmarking suites using DeepEval and Ragas, ensuring output reliability and minimal hallucination (93% score).",
                    "Automated multi-modal audio call summarization and report generation for 1,000+ files, eliminating 80% of manual documentation time."
                ]
            }
        ],
        "projects": [
            {
                "name": "FinPilot AI | Multi-Agent Reasoning Architecture",
                "description": "Built multi-agent state orchestration and deterministic verification pipelines using LangGraph and FastMCP, achieving 93% DeepEval score."
            },
            {
                "name": "ALAN-GPT | Multi-Document Model Search Engine",
                "description": "Engineered vector retrieval and documentation indexing system across 500+ production ML models with 91% retrieval precision."
            }
        ],
        "cover_letter_subject": "Application for Generative AI Engineer -- Tata Consultancy Services",
        "cover_letter_paragraphs": [
            "I am excited to apply for the Generative AI Engineer role at Tata Consultancy Services in Hyderabad. Over the past 5 years at Deloitte, I have specialized in building production-grade Generative AI systems, sophisticated RAG pipelines, and multi-agent platforms that solve complex enterprise challenges.",
            "My experience includes architecting 'FinPilot AI', an autonomous multi-agent platform built with LangGraph and FastMCP that cut data ingestion latency by ~80% and achieved a 93% evaluation score on DeepEval benchmarks. I also designed 'ALAN-GPT', a technical RAG search engine that indexed over 500 machine learning models, improving retrieval precision to 91% and accelerating developer discovery by 75%.",
            "TCS is a global leader in delivering cutting-edge AI transformations to tier-1 enterprises. I am eager to leverage my deep expertise in LLM frameworks, prompt engineering, vector search, and evaluation guardrails to accelerate TCS's Generative AI delivery. Thank you for your time and consideration."
        ]
    },

    # 5. Accenture in India - Data Platform Engineer (AI Powered)
    {
        "title": "Data Platform Engineer (AI & Agentic Frameworks)",
        "summary": "AI-focused Data Platform Engineer with 5 years of Deloitte experience designing high-throughput data automation workflows, MCP ingestion pipelines, and agentic AI integration layers. Expert in Python, SQL, REST APIs, and combining structured data platforms with Generative AI capabilities.",
        "skills": {
            "Data Platforms & Pipelines": ["Python", "SQL", "Data Automation", "FastMCP", "SQLite", "Data Modeling", "ETL Pipelines"],
            "AI & Agentic Integration": ["Generative AI", "Agentic AI Frameworks", "LangGraph", "RAG Systems", "FAISS", "Prompt Engineering"],
            "Software & Architecture": ["FastAPI", "Pandas", "NumPy", "Pydantic", "REST APIs", "Microservices"],
            "Infrastructure & DevOps": ["Docker", "Git", "Power BI", "Streamlit", "DeepEval"]
        },
        "experience": [
            {
                "role": "Data Scientist / Data Platform Engineer",
                "company": "Deloitte",
                "duration": "Jul 2021 -- Present",
                "bullets": [
                    "Architected unified data ingestion and AI processing pipelines integrating multi-agent reasoning with enterprise data models.",
                    "Designed an MCP-based multi-format ingestion workflow using FastMCP, SQLite, and local file drivers, reducing ingestion latency by ~80%.",
                    "Built RAG indexing pipelines combining vector search with relational tax data logic, attaining 93% DeepEval score.",
                    "Integrated automated document indexing across 500+ production ML models, improving query response time by 75%.",
                    "Collaborated with data and solution architects to ensure seamless integration between data pipelines and downstream AI services."
                ]
            }
        ],
        "projects": [
            {
                "name": "FastMCP High-Speed Ingestion Pipeline",
                "description": "Engineered a high-performance ingestion engine supporting 3 data formats using FastMCP and SQLite, reducing data latency by 80%."
            },
            {
                "name": "Enterprise Model Knowledge Graph & Search",
                "description": "Unified metadata and documentation for 500+ ML models into a searchable RAG repository with 91% retrieval evaluation score."
            }
        ],
        "cover_letter_subject": "Application for Data Platform Engineer (Job ID: 4448322554) -- Accenture in India",
        "cover_letter_paragraphs": [
            "I am applying for the Data Platform Engineer position at Accenture in India. With 5 years of experience at Deloitte designing resilient data platforms, automated ETL pipelines, and Agentic AI integration layers, I bring a strong AI-first mindset to modern enterprise data architectures.",
            "During my time at Deloitte, I architected an MCP-based data ingestion pipeline utilizing FastMCP and SQLite that processed diverse structured and unstructured file formats, slashing ingestion latency by ~80%. I also engineered data indexing pipelines for ALAN-GPT across 500+ production machine learning models, ensuring seamless synchronization between backend data models and user-facing semantic search services.",
            "Accenture's commitment to delivering enterprise-grade AI-powered data platform solutions aligns directly with my background in Python, data architecture, and agentic workflows. I look forward to discussing how my skills can contribute to your team's success."
        ]
    },

    # 6. Gradera - ML Engineer (Agentic AI & RAG)
    {
        "title": "AI/ML Engineer (Agentic AI, LangGraph & GraphRAG)",
        "summary": "AI/ML Engineer with 5 years of specialized experience at Deloitte developing autonomous multi-agent systems, RAG pipelines, and production LLM services. Expert in LangGraph, MCP, vector search, prompt engineering, and evaluation benchmarks (DeepEval, Ragas) with strong foundations in Python and FastAPI.",
        "skills": {
            "Agentic AI & Orchestration": ["LangGraph", "Multi-Agent Systems", "MCP (Model Context Protocol)", "Tool Calling", "Autonomous Agents", "Prompt Engineering"],
            "RAG & Vector Search": ["RAG Pipelines", "FAISS", "Embeddings", "Semantic Search", "Vector Databases", "Knowledge Retrieval"],
            "Machine Learning & LLMs": ["PyTorch", "Scikit-Learn", "Fine-Tuning (PEFT/LoRA)", "Hugging Face", "LLM Guardrails"],
            "Backend & Cloud": ["Python", "FastAPI", "Docker", "Git", "SQL", "Streamlit", "DeepEval", "Ragas"]
        },
        "experience": [
            {
                "role": "AI/ML Engineer & Data Scientist",
                "company": "Deloitte",
                "duration": "Jul 2021 -- Present",
                "bullets": [
                    "Designed, developed, and deployed enterprise-grade Generative AI and multi-agent applications using Python, LangGraph, and MCP.",
                    "Built 'FinPilot AI', an autonomous multi-agent financial platform with LangGraph ReAct orchestration and state routing across 4 intent categories.",
                    "Engineered FastMCP ingestion workflow across 3 file formats, reducing ingestion latency by ~80%.",
                    "Developed RAG calculation engine combining FAISS semantic search with deterministic logic, achieving 93% on DeepEval evaluation.",
                    "Architected 'ALAN-GPT' documentation search engine indexing 500+ production ML models with a 91% retrieval score.",
                    "Built end-to-end evaluation and guardrail pipelines with DeepEval and Ragas to eliminate hallucinations and optimize latency."
                ]
            }
        ],
        "projects": [
            {
                "name": "FinPilot AI | Multi-Agent Autonomous Platform",
                "description": "Multi-agent orchestration with LangGraph ReAct, FastMCP ingestion (80% latency reduction), and DeepEval automated evaluation (93% score)."
            },
            {
                "name": "ALAN-GPT | Enterprise RAG Retrieval Engine",
                "description": "Production search system across 500+ ML models, reducing developer lookup time by 75% with 91% retrieval accuracy."
            }
        ],
        "cover_letter_subject": "Application for ML Engineer (Generative AI & Agentic AI) -- Gradera",
        "cover_letter_paragraphs": [
            "I am thrilled to apply for the ML Engineer (Generative AI & Agentic AI) position at Gradera. As an AI Native Services enthusiast with 5 years of experience at Deloitte architecting multi-agent workflows, RAG pipelines, and autonomous AI systems, Gradera's vision of Software-Orchestrated Services(TM) resonates deeply with my work.",
            "At Deloitte, I designed 'FinPilot AI'--a production multi-agent financial reasoning platform built with LangGraph ReAct and the Model Context Protocol (MCP). The system coordinates supervisor-worker agents across 4 intent categories and achieved a 93% evaluation score on DeepEval. Additionally, I architected ALAN-GPT, indexing over 500 production ML models with 91% retrieval accuracy, and developed FastMCP data pipelines that cut latency by 80%.",
            "My experience directly mirrors Gradera's core AI stack: LangGraph, MCP, vector search, Python/FastAPI, and automated evaluation frameworks. I would love to bring my technical expertise and passion for Agentic AI to help Gradera redefine enterprise orchestration. Thank you for your consideration."
        ]
    },

    # 7. Teradata - AI Engineer (Hyderabad)
    {
        "title": "AI Engineer (Backend Services & Agentic Platform)",
        "summary": "AI Engineer and Data Scientist with 5 years of experience at Deloitte designing scalable backend services, distributed data workflows, and AI platform components. Proficient in Python, SQL, RESTful APIs, Docker, and integrating Agentic AI / LLM capabilities into enterprise architectures.",
        "skills": {
            "AI & Agentic Systems": ["Agentic AI", "LLM Integration", "LangGraph", "MCP", "RAG Pipelines", "FAISS", "Prompt Engineering"],
            "Backend & API Engineering": ["Python", "FastAPI", "RESTful APIs", "SQL", "Data Modeling", "Distributed System Patterns"],
            "ML & Frameworks": ["PyTorch", "Scikit-Learn", "Pandas", "NumPy", "Pydantic"],
            "DevOps & Quality": ["Docker", "Git", "Unit & Integration Testing", "DeepEval", "Streamlit"]
        },
        "experience": [
            {
                "role": "AI Engineer / Data Scientist",
                "company": "Deloitte",
                "duration": "Jul 2021 -- Present",
                "bullets": [
                    "Engineered robust, high-performance backend AI services, data ingestion pipelines, and agentic workflows using Python, FastAPI, and MCP.",
                    "Architected 'FinPilot AI' multi-agent system with LangGraph ReAct orchestration and FastMCP drivers, reducing ingestion latency by ~80%.",
                    "Built RAG computation engine combining FAISS vector search with deterministic data models (93% DeepEval score).",
                    "Constructed ALAN-GPT documentation search engine across 500+ production ML models with 91% retrieval accuracy.",
                    "Implemented automated testing, code reviews, and containerized Docker deployments to ensure platform reliability."
                ]
            }
        ],
        "projects": [
            {
                "name": "Autonomous Knowledge & Multi-Agent Platform (FinPilot)",
                "description": "Engineered multi-agent orchestration, FastMCP ingestion, and deterministic calculation logic with 93% evaluation score."
            },
            {
                "name": "ALAN-GPT Model Repository Search",
                "description": "Unified 500+ production models into an API-accessible RAG search platform with 91% retrieval accuracy."
            }
        ],
        "cover_letter_subject": "Application for AI Engineer Position -- Teradata",
        "cover_letter_paragraphs": [
            "I am writing to apply for the AI Engineer position at Teradata in Hyderabad. With 5 years of experience at Deloitte engineering backend AI services, distributed data pipelines, and agentic platform components, I am excited about Teradata's mission to activate enterprise intelligence through autonomous knowledge.",
            "Throughout my career, I have focused on building scalable, reliable services that unify data and AI. At Deloitte, I architected FinPilot AI using LangGraph and FastMCP, creating an autonomous agent system that reduced data ingestion latency by ~80% and achieved a 93% DeepEval benchmark score. I also engineered ALAN-GPT to index and query over 500 production ML models, delivering a 91% retrieval score through robust RESTful APIs.",
            "My strong background in Python, API design, data modeling, and Agentic AI aligns directly with the requirements for this role. I am eager to contribute to Teradata's next-generation AI platform and look forward to speaking with your team."
        ]
    },

    # 8. Teradata - AI Engineer (Telangana)
    {
        "title": "AI Platform Engineer (LLMs & Distributed Services)",
        "summary": "AI Engineer with 5 years of progressive experience at Deloitte building enterprise AI platform components, REST APIs, and autonomous agent workflows. Skilled in Python, Docker, SQL, FAISS, and LangGraph with a strong focus on system performance, reliability, and code quality.",
        "skills": {
            "AI Systems & LLMs": ["Agentic AI", "LLM Pipelines", "LangGraph", "MCP", "RAG Systems", "FAISS Vector Search"],
            "Backend Development": ["Python", "FastAPI", "RESTful APIs", "SQL Data Modeling", "Microservices Architecture"],
            "Machine Learning": ["PyTorch", "Scikit-Learn", "Model Evaluation (DeepEval, Ragas)", "Prompt Engineering"],
            "Platform Engineering": ["Docker", "Git", "CI/CD", "Streamlit", "Performance Tuning"]
        },
        "experience": [
            {
                "role": "Data Scientist / AI Engineer",
                "company": "Deloitte",
                "duration": "Jul 2021 -- Present",
                "bullets": [
                    "Designed and maintained scalable AI platform services and automated workflows across 3 enterprise initiatives.",
                    "Implemented LangGraph ReAct agent orchestration and FastMCP ingestion, achieving 80% reduction in data ingestion latency.",
                    "Developed RAG semantic search engine with deterministic logic verification, scoring 93% on DeepEval benchmarks.",
                    "Indexed and deployed search systems for 500+ production ML models, improving developer discovery speed by 75%.",
                    "Enforced code quality through rigorous unit testing, API contracts, and containerized Docker deployments."
                ]
            }
        ],
        "projects": [
            {
                "name": "FinPilot AI | Multi-Agent Platform",
                "description": "Multi-agent state routing with LangGraph, FastMCP ingestion, and DeepEval evaluation benchmarking (93% score)."
            },
            {
                "name": "Enterprise Model Search Engine",
                "description": "Indexed 500+ ML models into a high-performance vector search service with 91% retrieval accuracy."
            }
        ],
        "cover_letter_subject": "Application for AI Engineer Position -- Teradata (Telangana)",
        "cover_letter_paragraphs": [
            "I am pleased to submit my application for the AI Engineer position at Teradata. With 5 years of experience at Deloitte specializing in backend AI development, agentic workflows, and distributed data systems, I am eager to help build Teradata's next-generation AI capabilities.",
            "My work has consistently focused on building high-performance AI services. I engineered FinPilot AI, orchestrating autonomous agents with LangGraph and FastMCP to cut data ingestion latency by ~80% with a 93% DeepEval score. Additionally, I led the development of ALAN-GPT, building a high-throughput vector search system that indexed 500+ production ML models with 91% retrieval accuracy.",
            "Teradata's focus on enterprise intelligence and agentic platforms is a natural fit for my background in Python, REST APIs, SQL, and LLM frameworks. I look forward to the opportunity to discuss how my experience can benefit Teradata."
        ]
    },

    # 9. Agilisium Consulting - Artificial Intelligence Engineer
    {
        "title": "Artificial Intelligence Engineer (GenAI & MLOps)",
        "summary": "AI Engineer and Data Scientist with 5 years of experience at Deloitte designing AI/ML-enabled architectures, Generative AI models, and RAG pipelines. Expert in Python, PyTorch, FAISS vector search, prompt engineering, MLOps, and cloud-ready microservices.",
        "skills": {
            "Generative AI & LLMs": ["Generative AI Models", "LLM Fine-Tuning (PEFT/LoRA)", "Prompt Engineering", "LangGraph", "MCP", "Hugging Face"],
            "RAG & Vector Databases": ["RAG Architecture", "FAISS", "Vector Search", "Embeddings", "Semantic Indexing"],
            "Machine Learning & MLOps": ["PyTorch", "Scikit-Learn", "Model Lifecycle Management", "DeepEval", "Ragas", "AI Safety"],
            "Engineering & Cloud": ["Python", "FastAPI", "SQL", "Docker", "Git", "Streamlit", "REST APIs"]
        },
        "experience": [
            {
                "role": "AI Engineer & Data Scientist",
                "company": "Deloitte",
                "duration": "Jul 2021 -- Present",
                "bullets": [
                    "Architected and deployed enterprise Generative AI and ML solutions across 3 initiatives using Python, LangGraph, and PyTorch.",
                    "Engineered multi-agent platform (FinPilot AI) with LangGraph ReAct and FastMCP, reducing ingestion latency by 80% with 93% DeepEval score.",
                    "Designed multi-document RAG search engine (ALAN-GPT) indexing 500+ production ML models (91% retrieval evaluation score).",
                    "Built GenAI audio transcription and summarization pipeline processing 1,000+ files with 80% manual effort reduction.",
                    "Implemented MLOps best practices, model evaluation guardrails, and Dockerized microservices."
                ]
            }
        ],
        "projects": [
            {
                "name": "FinPilot AI | Multi-Agent Reasoning System",
                "description": "Multi-agent orchestration and deterministic calculation engine scoring 93% on DeepEval evaluation suites."
            },
            {
                "name": "ALAN-GPT | Multi-Document RAG Search",
                "description": "Vector indexing and semantic retrieval platform covering 500+ ML models with 91% retrieval accuracy."
            }
        ],
        "cover_letter_subject": "Application for Artificial Intelligence Engineer -- Agilisium Consulting",
        "cover_letter_paragraphs": [
            "I am writing to apply for the Artificial Intelligence Engineer position at Agilisium Consulting in Hyderabad. With 5 years of experience at Deloitte designing AI/ML architectures, fine-tuning LLMs, and deploying Generative AI applications, I am excited about the opportunity to deliver innovative AI solutions for Agilisium's enterprise clients.",
            "At Deloitte, I have led the technical execution of multiple GenAI initiatives. I built FinPilot AI using LangGraph and FastMCP, creating an autonomous agent system that reduced data ingestion latency by ~80% and scored 93% on DeepEval benchmarks. I also architected ALAN-GPT, indexing over 500 production machine learning models with 91% retrieval accuracy, and developed automated NLP pipelines for unstructured data analytics.",
            "My proficiency in Python, PyTorch, vector search, MLOps, and generative AI frameworks matches the requirements of this role. I would welcome the opportunity to discuss how my background can support Agilisium's AI practice."
        ]
    },

    # 10. Innova ESI - AI/GenAI Engineer
    {
        "title": "AI/GenAI Engineer (Vertex AI, Gemini & Agentic Workflows)",
        "summary": "AI/GenAI Engineer with 5 years of Deloitte experience building production-ready Generative AI systems, RAG pipelines, and autonomous agent workflows. Proficient in Python, prompt engineering, structured outputs, function calling, MLOps, and deploying explainable AI models for financial and business process automation.",
        "skills": {
            "Generative AI & LLMs": ["Prompt Engineering", "Structured Outputs", "Function Calling", "Gemini & LLM APIs", "LangGraph", "MCP"],
            "Machine Learning & MLOps": ["PyTorch", "Scikit-Learn", "MLOps", "Model Versioning", "Evaluation (Precision, Recall, F1, DeepEval)"],
            "RAG & Data Pipelines": ["RAG Architecture", "FAISS", "Embeddings", "Vector Search", "FastMCP", "Data Extraction"],
            "Backend & Cloud": ["Python", "FastAPI", "SQL", "Docker", "Git", "REST APIs", "Streamlit"]
        },
        "experience": [
            {
                "role": "AI/GenAI Engineer & Data Scientist",
                "company": "Deloitte",
                "duration": "Jul 2021 -- Present",
                "bullets": [
                    "Engineered enterprise AI systems, RAG pipelines, and automated reasoning workflows across 3 AI initiatives using Python, LangGraph, and FastAPI.",
                    "Built 'FinPilot AI' multi-agent financial analysis platform utilizing LangGraph ReAct and FastMCP; implemented structured output validation and deterministic logic with 93% DeepEval score.",
                    "Designed FastMCP ingestion workflow across 3 file formats, reducing data ingestion latency by ~80%.",
                    "Architected 'ALAN-GPT' search engine indexing 500+ production ML models with 91% retrieval accuracy.",
                    "Developed GenAI pipeline converting 1,000+ unstructured audio recordings into structured analytical reports, reducing manual effort by 80%.",
                    "Implemented AI evaluation frameworks, confidence scoring, human-in-the-loop controls, and explainable AI outputs."
                ]
            }
        ],
        "projects": [
            {
                "name": "FinPilot AI | Financial Automation & Reasoning Platform",
                "description": "Multi-agent state routing with LangGraph, structured outputs, FastMCP ingestion (80% latency cut), and 93% DeepEval score."
            },
            {
                "name": "ALAN-GPT | Enterprise Knowledge & Model Search Engine",
                "description": "High-accuracy vector indexing and semantic retrieval platform covering 500+ ML models (91% retrieval accuracy)."
            }
        ],
        "cover_letter_subject": "Application for AI/GenAI Engineer (Immediate Joiner) -- Innova ESI",
        "cover_letter_paragraphs": [
            "I am excited to apply for the AI/GenAI Engineer position at Innova ESI in Hyderabad. With 5 years of experience at Deloitte developing production-ready Generative AI systems, agentic workflows, and financial automation pipelines, I am well-prepared to make an immediate impact on your UC-003 Billing Prep program.",
            "My experience includes architecting FinPilot AI, an autonomous financial analysis platform built with LangGraph and FastMCP that implemented structured outputs, anomaly detection, and deterministic rule validation with a 93% DeepEval benchmark score. Additionally, I built automated GenAI pipelines for extracting financial details from over 1,000 recordings and engineered ALAN-GPT across 500+ production ML models with 91% retrieval accuracy.",
            "I possess strong expertise in Python, prompt engineering, function calling, MLOps, and enterprise LLM integration. As an immediate joiner based in Hyderabad, I look forward to discussing how my experience can support Innova ESI's AI Core team."
        ]
    }
]

print(f"Generating tailored documents for {len(tailored_configs)} job openings...")

generated_folders = []

for idx, (job, config) in enumerate(zip(jobs, tailored_configs), 1):
    company = job.get("Company", "Company")
    title = job.get("Title", "AI Engineer")
    
    folder_name = sanitize_folder_name(company, title)
    folder_path = os.path.join(OUTPUT_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    print(f"\n[{idx}/10] Processing: {title} @ {company} -> {folder_name}")
    
    # 1. Prepare CV Data structure
    cv_data = {
        "name": CANDIDATE["name"],
        "title": config["title"],
        "contact": CANDIDATE["contact"],
        "summary": config["summary"],
        "skills": config["skills"],
        "experience": config["experience"],
        "projects": config["projects"],
        "education": CANDIDATE["education"]
    }
    
    cv_docx_path = os.path.join(folder_path, "Tailored_CV.docx")
    cv_pdf_path = os.path.join(folder_path, "Tailored_CV.pdf")
    
    generate_cv_docx(cv_data, cv_docx_path)
    generate_cv_pdf(cv_data, cv_pdf_path)
    print(f"   [+] Generated CV (.docx & .pdf)")
    
    # 2. Prepare Cover Letter Data structure
    cl_data = {
        "name": CANDIDATE["name"],
        "title": config["title"],
        "contact": CANDIDATE["contact"],
        "date": "August 25, 2026",
        "recipient": "Hiring Manager / Talent Acquisition Team",
        "company": company,
        "subject": config["cover_letter_subject"],
        "salutation": f"Dear Hiring Team at {company},",
        "paragraphs": config["cover_letter_paragraphs"],
        "sign_off": f"Sincerely,\n\n{CANDIDATE['name']}"
    }
    
    cl_docx_path = os.path.join(folder_path, "Cover_Letter.docx")
    cl_pdf_path = os.path.join(folder_path, "Cover_Letter.pdf")
    
    generate_cl_docx(cl_data, cl_docx_path)
    generate_cl_pdf(cl_data, cl_pdf_path)
    print(f"   [+] Generated Cover Letter (.docx & .pdf)")
    
    generated_folders.append({
        "company": company,
        "title": title,
        "folder": folder_path,
        "cv_docx": cv_docx_path,
        "cv_pdf": cv_pdf_path,
        "cl_docx": cl_docx_path,
        "cl_pdf": cl_pdf_path
    })

print("\n" + "=" * 70)
print(f"SUCCESS: Generated tailored CVs and Cover Letters for all {len(generated_folders)} jobs in '{OUTPUT_DIR}/'!")
print("=" * 70)
