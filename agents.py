from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import get_search, scrape_url
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")

#1st agent
def build_search_agent(model=None):
    return create_agent(
        model=model or llm,
        tools=[get_search]
    )

#2nd agent
def build_scraper_agent(model=None):
    return create_agent(
        model=model or llm,
        tools=[scrape_url]
    )

#writter chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured, and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

    Topic: {topic}
    Research Gathered:
    {research}
    
    Structure the report as:
    - Introduction
    - Key findings (minimum 3 key well explained points)
    - Conclusion
    - Source (List all urls found in the research)

    Be detailed, factual and professional.""")
])

def get_writer_chain(model=None):
    active_llm = model or llm
    return writer_prompt | active_llm | StrOutputParser()

writer_chain = get_writer_chain()

#critic chain
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert research critic and analytical reviewer.

        Your responsibility is to rigorously evaluate research reports
        for accuracy, completeness, depth, relevance, and overall quality.

        You must be objective, critical, and constructive.

        IMPORTANT RULES:
        1. Never assume that a claim is correct without supporting evidence.
        2. Identify unsupported claims, potential hallucinations, outdated information, and misleading statements.
        3. Do not invent facts, statistics, or references.
        4. Distinguish between factual errors and missing information.
        5. Give specific and actionable recommendations.
        6. Do not give a high score merely because the report is lengthy or well-written.
        7. Evaluate the report based on the provided content.
        8. If you cannot independently verify a claim, explicitly mention that it requires verification.
        """
    ),

    (
        "human",
        """
        Critically evaluate the following research report.

        Research Topic:
        {topic}

        Research Report:
        {report}

        Evaluate the report using these criteria:

        1. Accuracy (30%):
        - Are factual claims correct?
        - Are statistics and figures supported?
        - Are there contradictions or misleading statements?

        2. Completeness (25%):
        - Are important aspects of the topic covered?
        - Are there missing perspectives or explanations?
        - Are relevant areas overlooked?

        3. Depth and Insight (25%):
        - Does the report provide meaningful analysis?
        - Does it identify trends, patterns, and implications?
        - Does it go beyond superficial explanations?

        4. Structure and Clarity (20%):
        - Is the report logically organized?
        - Are explanations clear and easy to understand?
        - Is there unnecessary repetition?

        SCORING:
        Calculate an overall score out of 10 using the above weights.
        Be strict and objective.

        OUTPUT FORMAT:

        Score: X/10

        Your Evaluation:

        - Accuracy:
        - Completeness:
        - Depth and Insight:
        - Structure and Clarity:

        Strengths:
        - List the strongest aspects of the report.

        Areas of Improvement:
        - Identify specific weaknesses.
        - Explain what information is missing.
        - Suggest concrete improvements.

        Potential Hallucinations or Unsupported Claims:
        - Identify claims that require verification.
        - If none are apparent, explicitly state that.

        Final Verdict:
        Provide a concise one-line assessment.

        Be specific, evidence-based, and constructive.
        """
    )
])

def get_critic_chain(model=None):
    active_llm = model or llm
    return critic_prompt | active_llm | StrOutputParser()

critic_chain = get_critic_chain()