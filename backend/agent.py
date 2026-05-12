import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from drive_tool import search_drive
from datetime import datetime, timedelta

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

today = datetime.utcnow()

today_date = today.strftime("%Y-%m-%dT00:00:00")

last_week_date = (today - timedelta(days=7)).strftime("%Y-%m-%dT00:00:00")

month_start_date = today.replace(day=1).strftime("%Y-%m-%dT00:00:00")

def generate_drive_query(user_input):

    prompt = f"""
You are a Google Drive search assistant.

Convert the user's natural language request into a valid Google Drive API q parameter.

Rules:
- PDFs → mimeType='application/pdf'
- Images → mimeType contains 'image/'
- Videos → mimeType contains 'video/'
- Folders → mimeType='application/vnd.google-apps.folder'

Date Handling:
- today → modifiedTime > '{today_date}'
- last week → modifiedTime > '{last_week_date}'
- this month → modifiedTime > '{month_start_date}'

Examples:
User: Find PDFs
Query: mimeType='application/pdf'

User: Find images from last week
Query: mimeType contains 'image/' and modifiedTime > '2026-05-05T00:00:00'

User: Find invoices this month
Query: name contains 'invoice' and modifiedTime > '2026-05-01T00:00:00'

Return ONLY the query.
User Request: {user_input}
"""
    
    response = llm.invoke(prompt)

    return response.content.strip()

def handle_query(user_input):

    drive_query = generate_drive_query(user_input)

    print("Generated Query:", drive_query)

    results = search_drive(drive_query)

    if not results:
        return "❌ No matching files found."

    response = "## 📁 Matching Files\n\n"

    for file in results:

        file_name = file.get("name", "Unknown File")
        file_type = file.get("mimeType", "")
        file_link = file.get("webViewLink", "#")

        # File type icons
        if "pdf" in file_type:
            icon = "📄"
        elif "image" in file_type:
            icon = "🖼️"
        elif "spreadsheet" in file_type:
            icon = "📊"
        elif "document" in file_type:
            icon = "📝"
        else:
            icon = "📁"

        response += f"{icon} **{file_name}**\n\n"
        response += f"[Open File]({file_link})\n\n"
        response += "---\n"

    return response