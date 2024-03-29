
from dotenv import load_dotenv
import os
load_dotenv()

import google.generativeai as genai
gemini_key = os.getenv("apikey")
genai.configure(api_key = gemini_key)

model = genai.GenerativeModel('models/gemini-1.0-pro-latest')

def getsolution(status):
    if(status[0] == "Healthy"):
        return model.generate_content(f"give advice for potato {status[0]} of {status[1]} percentage in a very small para, the paragraph strictly sould not excede 4 ine").text
    return model.generate_content(f"give solution for potato {status[0]} of {status[1]} infected percentage in a very small para, the paragraph strictly sould not excede 4 ine").text