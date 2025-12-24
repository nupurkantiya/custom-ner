# resume_parser.py
"""
Complete Resume Parser using trained NER model
Usage: python resume_parser.py
"""

import spacy
import json
import os
from collections import defaultdict

class ResumeParser:
    def __init__(self, model_path='./resume_ner_model'):
        """Initialize parser with trained model"""
        print(f"Loading model from {model_path}...")
        self.nlp = spacy.load(model_path)
        print("✅ Model loaded successfully")
    
    def parse_resume(self, text):
        """Parse a single resume and extract entities"""
        doc = self.nlp(text)
        
        # Organize entities by type
        entities = defaultdict(list)
        for ent in doc.ents:
            entities[ent.label_].append(ent.text)
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return dict(entities)
    
    def parse_resume_file(self, file_path):
        """Parse resume from file"""
        # Extract text based on file type
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        elif file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                text = data.get('text', '')
        else:
            print(f"Unsupported file type: {file_path}")
            return None
        
        return self.parse_resume(text)
    
    def parse_multiple_resumes(self, resume_folder='./resumes'):
        """Parse all resumes in a folder"""
        results = []
        
        # Load extracted resumes
        if os.path.exists('extracted_resumes.json'):
            with open('extracted_resumes.json', 'r', encoding='utf-8') as f:
                resumes = json.load(f)
            
            print(f"\nParsing {len(resumes)} resumes...")
            
            for resume in resumes:
                entities = self.parse_resume(resume['text'])
                results.append({
                    'filename': resume['filename'],
                    'entities': entities
                })
                print(f"✓ Parsed: {resume['filename']}")
        
        return results
    
    def display_results(self, entities):
        """Display parsed entities in a nice format"""
        print("\n" + "="*80)
        print("EXTRACTED ENTITIES")
        print("="*80)
        
        for entity_type, values in entities.items():
            print(f"\n{entity_type}:")
            for value in values:
                print(f"  • {value}")
    
    def save_results(self, results, output_file='parsed_resumes.json'):
        """Save parsing results to file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Results saved to: {output_file}")

def demo_single_resume():
    """Demo: Parse a single resume text"""
    parser = ResumeParser()
    
    sample_resume = """
    John Doe
    Senior Software Engineer
    
    Experience:
    - Software Engineer at Google (2018-2023)
    - Worked on machine learning projects using Python, TensorFlow, and PyTorch
    - Built scalable APIs with Django and Flask
    - Deployed applications on AWS and Google Cloud Platform
    
    Skills:
    - Programming: Python, Java, JavaScript, C++
    - ML/AI: Machine Learning, Deep Learning, NLP, Computer Vision
    - Web: React, Node.js, Django, Flask
    - Cloud: AWS, Azure, GCP
    - Tools: Docker, Kubernetes, Git, Jenkins
    
    Education:
    - B.Tech in Computer Science from IIT Delhi (2014-2018)
    """
    
    entities = parser.parse_resume(sample_resume)
    parser.display_results(entities)

def parse_all_resumes():
    """Parse all resumes in the dataset"""
    parser = ResumeParser()
    
    results = parser.parse_multiple_resumes()
    
    # Display sample result
    if results:
        print("\n" + "="*80)
        print(f"SAMPLE RESULT - {results[0]['filename']}")
        print("="*80)
        parser.display_results(results[0]['entities'])
        
        # Save all results
        parser.save_results(results)
        
        print(f"\n✅ Parsed {len(results)} resumes successfully!")

def interactive_mode():
    """Interactive mode - paste resume text and get results"""
    parser = ResumeParser()
    
    print("\n" + "="*80)
    print("INTERACTIVE RESUME PARSER")
    print("="*80)
    print("Paste resume text below (press Ctrl+D or Ctrl+Z when done):\n")
    
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    text = "\n".join(lines)
    
    if text.strip():
        entities = parser.parse_resume(text)
        parser.display_results(entities)

def main():
    print("="*80)
    print("RESUME PARSER - Choose Mode")
    print("="*80)
    print("1. Demo with sample resume")
    print("2. Parse all resumes in dataset")
    print("3. Interactive mode (paste resume text)")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == '1':
        demo_single_resume()
    elif choice == '2':
        parse_all_resumes()
    elif choice == '3':
        interactive_mode()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()