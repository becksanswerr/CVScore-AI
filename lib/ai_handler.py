# lib/ai_handler.py
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class AIHandler:
    def __init__(self, model_name="gemini-2.5-flash"):
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found. Please check your .env file.")
        self.model = ChatGoogleGenerativeAI(model=model_name, temperature=0.2, convert_system_message_to_human=True)
        self.output_parser = JsonOutputParser()
        self.prompt_template = self._create_prompt_template()

    def _create_prompt_template(self):
        template = """
        SYSTEM INSTRUCTION:
        You are an expert HR Technology Specialist AI. Your task is to analyze a given CV text against
        the provided job description and criteria with nuance and context.
        You MUST ONLY provide the output in the specified JSON format.

        --- SCORING GUIDELINES ---
        Use the following guide to determine the score. Be fair and consider related skills.
        - 90-100 (Perfect Match 🔥): Candidate meets all 'Must-Haves' and most 'Nice-to-Haves'. Clear evidence of success in similar roles.
        - 75-89 (Great Candidate 🌟): Meets all 'Must-Haves' but has some gaps in 'Nice-to-Haves'. A very strong contender.
        - 60-74 (Good Candidate 👍): Meets the core 'Must-Haves' but has noticeable gaps. Has potential.
        - 45-59 (Fair Candidate 🤔): Partially meets 'Must-Haves' but has significant gaps or lacks key experience.
        - 25-44 (Weak Fit 😔): Lacks the primary skills for the role BUT possesses some relevant *domain knowledge*. Give partial credit.
        - 0-24 (Not a Fit 💀): Completely unrelated background and skills.

        --- JOB DESCRIPTION AND CRITERIA ---
        - Position: {job_title}
        - Job Description: {job_description}
        - Must-Have Skills: {must_haves}
        - Nice-to-Have Skills: {nice_to_haves}
        - Deal-Breakers: {deal_breakers}

        --- CANDIDATE'S CV TEXT ---
        {cv_text}

        --- YOUR TASK - STEP BY STEP ---
        1. First, identify the candidate's full name.
        2. Write a brief, 1-2 sentence summary of their profile and fit.
        3. Use the **Scoring Guidelines** above to assign a score from 0 to 100.
        4. List the top 3-4 key advantages (strengths).
        5. List the top 3-4 key disadvantages or gaps.
        6. Generate 3 insightful interview questions based on the disadvantages.

        {format_instructions}
        """
        
        return PromptTemplate(
            template=template,
            input_variables=["job_title", "job_description", "must_haves", "nice_to_haves", "deal_breakers", "cv_text"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )

    def analyze_cv(self, cv_text: str, job_details: dict):
        if not cv_text or not cv_text.strip():
            print("AI Handler received empty text. Skipping analysis.")
            return {
                "candidate_name": "Unknown",
                "summary": "Analysis could not be performed as the content could not be read.",
                "score": 0,
                "advantages": [],
                "disadvantages": ["Could not extract readable text from the CV file."],
                "interview_questions": []
            }

        try:
            chain = self.prompt_template | self.model | self.output_parser
            response = chain.invoke({
                "job_title": job_details.get("title"),
                "job_description": job_details.get("description"),
                "must_haves": job_details.get("must_haves"),
                "nice_to_haves": job_details.get("nice_to_haves"),
                "deal_breakers": job_details.get("deal_breakers"),
                "cv_text": cv_text
            })
            return response
        except Exception as e:
            print(f"An error occurred during AI analysis: {e}")
            return {
                "candidate_name": "Error",
                "summary": "Analysis failed due to an error.",
                "score": 0,
                "advantages": [],
                "disadvantages": [f"An error occurred while communicating with the AI model: {e}"],
                "interview_questions": []
            }