# extract_resumes.py
"""
Extract text from PDF/DOCX/TXT resumes
Usage: python extract_resumes.py
"""

import os
import PyPDF2
import docx
import json

def extract_text_from_pdf(file_path):
    """Extract text from PDF"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""

def extract_text_from_docx(file_path):
    """Extract text from DOCX"""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
        return ""

def extract_text_from_txt(file_path):
    """Extract text from TXT"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading TXT {file_path}: {e}")
        return ""

def extract_all_resumes(resume_folder):
    """Extract text from all resumes in a folder"""
    extracted_data = []
    
    # Get all files
    files = os.listdir(resume_folder)
    print(f"Found {len(files)} files")
    
    for filename in files:
        file_path = os.path.join(resume_folder, filename)
        
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        elif filename.endswith('.txt'):
            text = extract_text_from_txt(file_path)
        else:
            continue
        
        if text.strip():
            extracted_data.append({
                'filename': filename,
                'text': text
            })
            print(f"✓ Extracted: {filename}")
    
    # Save extracted texts
    with open('extracted_resumes.json', 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Extracted {len(extracted_data)} resumes")
    print("Saved to: extracted_resumes.json")
    
    return extracted_data

if __name__ == "__main__":
    # UPDATE THIS PATH to your resume folder
    RESUME_FOLDER = "./resumes"  # Change this to your folder path
    
    if not os.path.exists(RESUME_FOLDER):
        print(f"❌ Folder not found: {RESUME_FOLDER}")
        print("Please create a 'resumes' folder and add your resume files")
    else:
        extract_all_resumes(RESUME_FOLDER)