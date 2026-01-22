
from agents import Agent, Runner, function_tool
from prompt import RESUME_ANALYZER_PROMPT, HTML_AGENT_PROMPT
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()

@function_tool
def sendEmail(message: str, subject: str = "Demo"):
    """Function Tool to send emails to the user"""

    api_key = os.environ.get("SENDGRID_API_KEY")
    from_email = os.environ.get("FROM_EMAIL")
    to_email = os.environ.get("TO_EMAIL")

    if not api_key or not from_email or not to_email:
        return {
            "status": "error",
            "error": "Missing SENDGRID_API_KEY, FROM_EMAIL or TO_EMAIL env variables."
        }

    mail = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=message
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(mail)
        return {"status": "success", "status_code": response.status_code}
    except Exception as e:
        return {"status": "failed", "error": str(e)}



resume_analyzer_agent = Agent(name = "AI Resume Analyzer", instructions=RESUME_ANALYZER_PROMPT )

email_agent = Agent(name = "Email Agent", instructions = HTML_AGENT_PROMPT, tools = [sendEmail])
