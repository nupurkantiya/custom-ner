# quick_annotator.py
"""
Quick annotation tool for resume entities
This helps you annotate 30-40 resumes quickly
"""

import json
import re

class QuickAnnotator:
    def __init__(self):
        self.annotations = []
        self.current_index = 0
        
        # Common skills to help with quick annotation
        self.common_skills = {
            'python', 'java', 'javascript', 'c++', 'react', 'angular', 'node.js',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'sql',
            'aws', 'azure', 'docker', 'kubernetes', 'git', 'django', 'flask',
            'data science', 'nlp', 'computer vision', 'mysql', 'mongodb', 'redis'
        }
        
        self.common_titles = {
            'software engineer', 'data scientist', 'data analyst', 'ml engineer',
            'full stack developer', 'backend developer', 'frontend developer',
            'devops engineer', 'project manager', 'product manager'
        }
    
    def find_entities_auto(self, text):
        """Auto-detect common entities to speed up annotation"""
        entities = []
        text_lower = text.lower()
        
        # Find skills
        for skill in self.common_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            for match in re.finditer(pattern, text_lower):
                start = match.start()
                end = match.end()
                # Get actual cased text
                actual_text = text[start:end]
                entities.append((start, end, "SKILL", actual_text))
        
        # Find job titles
        for title in self.common_titles:
            pattern = r'\b' + re.escape(title) + r'\b'
            for match in re.finditer(pattern, text_lower):
                start = match.start()
                end = match.end()
                actual_text = text[start:end]
                entities.append((start, end, "JOB_TITLE", actual_text))
        
        # Remove duplicates
        entities = list(set(entities))
        entities.sort(key=lambda x: x[0])
        
        return entities
    
    def annotate_resume(self, resume_text, filename):
        """Annotate a single resume"""
        print("\n" + "="*80)
        print(f"RESUME: {filename}")
        print("="*80)
        print(resume_text[:500] + "..." if len(resume_text) > 500 else resume_text)
        print("\n")
        
        # Auto-detect entities
        auto_entities = self.find_entities_auto(resume_text)
        
        print(f"Auto-detected {len(auto_entities)} entities:")
        for i, (start, end, label, text) in enumerate(auto_entities):
            print(f"  {i+1}. [{label}] {text}")
        
        print("\nOptions:")
        print("  1. Accept all auto-detected entities (press ENTER)")
        print("  2. Add more entities manually (type 'add')")
        print("  3. Skip this resume (type 'skip')")
        
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == 'skip':
            return None
        
        final_entities = [(s, e, l) for s, e, l, _ in auto_entities]
        
        if choice == 'add':
            print("\nAdd more entities (or type 'done' to finish):")
            while True:
                entity_text = input("  Entity text (or 'done'): ").strip()
                if entity_text.lower() == 'done':
                    break
                
                # Find position in text
                pos = resume_text.lower().find(entity_text.lower())
                if pos == -1:
                    print("    ❌ Not found in text. Try again.")
                    continue
                
                label = input("  Label (SKILL/JOB_TITLE/COMPANY/DEGREE): ").strip().upper()
                
                start = pos
                end = pos + len(entity_text)
                final_entities.append((start, end, label))
                print(f"    ✓ Added: [{label}] {entity_text}")
        
        return (resume_text, {"entities": final_entities})
    
    def annotate_batch(self, resumes, num_to_annotate=30):
        """Annotate a batch of resumes"""
        print(f"\n🎯 Annotating {num_to_annotate} resumes...")
        print("This will take 1-2 hours. Stay focused!\n")
        
        annotations = []
        
        for i, resume in enumerate(resumes[:num_to_annotate]):
            annotation = self.annotate_resume(resume['text'], resume['filename'])
            if annotation:
                annotations.append(annotation)
            
            print(f"\n✅ Progress: {i+1}/{num_to_annotate}")
        
        # Save annotations
        with open('training_data.json', 'w', encoding='utf-8') as f:
            json.dump(annotations, f, indent=2, ensure_ascii=False)
        
        print(f"\n🎉 Annotated {len(annotations)} resumes!")
        print("Saved to: training_data.json")
        
        return annotations

def main():
    # Load extracted resumes
    with open('extracted_resumes.json', 'r', encoding='utf-8') as f:
        resumes = json.load(f)
    
    print(f"Loaded {len(resumes)} resumes")
    
    # Ask how many to annotate
    num_to_annotate = input(f"\nHow many resumes to annotate? (recommended: 30-40): ").strip()
    num_to_annotate = int(num_to_annotate) if num_to_annotate else 30
    
    annotator = QuickAnnotator()
    annotator.annotate_batch(resumes, num_to_annotate)

if __name__ == "__main__":
    main()