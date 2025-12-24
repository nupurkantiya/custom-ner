# train_ner_model.py
"""
Train custom NER model for resume parsing
Usage: python train_ner_model.py
"""

import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
import random
import json
from pathlib import Path

def load_training_data(file_path='training_data.json'):
    """Load annotated training data"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Loaded {len(data)} training examples")
    return data

def train_ner_model(train_data, n_iter=30, output_dir='./resume_ner_model'):
    """Train custom NER model"""
    
    # Create blank English model
    nlp = spacy.blank("en")
    
    # Add NER pipe
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")
    else:
        ner = nlp.get_pipe("ner")
    
    # Add entity labels
    print("\nAdding entity labels...")
    for _, annotations in train_data:
        for ent in annotations.get("entities", []):
            ner.add_label(ent[2])
    
    # Get other pipes to disable during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    
    print(f"\nTraining for {n_iter} iterations...")
    print("This will take 10-30 minutes...\n")
    
    # Training loop
    with nlp.disable_pipes(*other_pipes):
        # Initialize optimizer
        optimizer = nlp.initialize()
        
        for iteration in range(n_iter):
            random.shuffle(train_data)
            losses = {}
            
            # Batch examples
            batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
            
            for batch in batches:
                examples = []
                for text, annotations in batch:
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, annotations)
                    examples.append(example)
                
                # Update model
                nlp.update(examples, drop=0.5, losses=losses, sgd=optimizer)
            
            if (iteration + 1) % 5 == 0:
                print(f"Iteration {iteration + 1}/{n_iter} - Loss: {losses['ner']:.2f}")
    
    # Save model
    output_path = Path(output_dir)
    if not output_path.exists():
        output_path.mkdir()
    
    nlp.to_disk(output_path)
    print(f"\n✅ Model saved to: {output_dir}")
    
    return nlp

def test_model(model_path='./resume_ner_model'):
    """Test the trained model"""
    nlp = spacy.load(model_path)
    
    # Test examples
    test_texts = [
        "Software Engineer with 5 years experience in Python, Machine Learning, and AWS",
        "Data Scientist at Google with expertise in TensorFlow and Deep Learning",
        "Full Stack Developer proficient in React, Node.js, and MongoDB"
    ]
    
    print("\n" + "="*80)
    print("TESTING MODEL")
    print("="*80)
    
    for text in test_texts:
        doc = nlp(text)
        print(f"\nText: {text}")
        print("Entities found:")
        for ent in doc.ents:
            print(f"  - [{ent.label_}] {ent.text}")
    
    return nlp

def main():
    print("="*80)
    print("RESUME NER MODEL TRAINING")
    print("="*80)
    
    # Load training data
    train_data = load_training_data()
    
    # Split into train and validation
    split_point = int(len(train_data) * 0.8)
    train_set = train_data[:split_point]
    val_set = train_data[split_point:]
    
    print(f"\nTrain set: {len(train_set)} examples")
    print(f"Validation set: {len(val_set)} examples")
    
    # Train model
    nlp = train_ner_model(train_set, n_iter=30)
    
    # Test model
    test_model()
    
    print("\n🎉 Training complete!")
    print("\nNext steps:")
    print("1. Test the model with: python test_ner_model.py")
    print("2. Use it in your application")

if __name__ == "__main__":
    main()