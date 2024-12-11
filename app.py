from dotenv import load_dotenv

load_dotenv()

import os
import io
import base64
import streamlit as st
import PyPDF2 as pdf
from PyPDF2 import PdfReader 
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Repsonse

def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in reader.pages:
        #page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt

input_prompt="""
You are an expericed and highly skilled recruiter with hands on with Application Tracking System with deep understanding of all the IT Jobs like Software Development, Data Science, Machine Learning, Data Analyst, Data Engineer and Testing. Now your task is to evaluate the give resume based on the provided job description. Please make sure the job market right is now highly competitive. Your job is to provide the percentage of resume matching with the job description, and any suggestions that can imporve the resume.

I want the response in a structure manner.
Resume matching: %
Suggestions: }}
""" 

#App
st.title("Application Tracking System")
jd=st.text_area("Paste the correct Job Description")
uploaded_file=st.file_uploader("Upload your Resume in PDF format",type="pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)
 