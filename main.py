import requests
from bs4 import BeautifulSoup
from google import genai
from docx import Document

client = genai.Client()

job_url = "https://www.isnetworld.com/en/careers/5977058004?gh_src=e5150d284us#application"
page = requests.get(job_url)
soup = BeautifulSoup(page.content, "html.parser")
job_posting_text = soup.get_text()

resume_doc = Document('IsabellaMann_Resume.docx')
full_resume_text = "\n".join([p.text for p in resume_doc.paragraphs])

prompt=f"""
I am applying for this job: {job_posting_text}
Here is my current resume: {full_resume_text}

Rewrite my 'Professional Summary', 'Experience', 'Projects', and 'Skills' sections
to align with the job's key requirements.
"""

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=prompt
)

ai_results = response.text

output_doc = Document('IsabellaMann_Resume.docx')
for paragraph in output_doc.paragraphs:
    if "{{SUMMARY}}" in paragraph.text:
        paragraph.text = paragraph.text.replace("{{SUMMARY}}", ai_results)

output_doc.save("IsabellaMann_Updated_resume.docx")
print("Done!")