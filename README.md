# Custom NER (Named Entity Recognition) Project

A Named Entity Recognition system built with spaCy for extracting and parsing information from resumes.

## ⚠️ Important Notice

**This is a demonstration/learning project.** The pre-trained model included in this repository was trained on a specific resume dataset and is optimized for that particular data structure and format. 

**Key Points:**
- The model may not work accurately on different resume formats or datasets
- For production use, you should retrain the model with your own labeled resume data
- This project serves as a template and learning resource for building custom NER systems
- The training scripts and methodology can be adapted to your specific use case

## Overview

This project implements a custom NER model trained on resume data to extract relevant entities such as names, emails, skills, experiences, and other resume-specific information.

## Features

- Resume extraction and parsing
- Custom NER model training
- Entity annotation interface
- Visualization tools for analysis
- Evaluation metrics

## Project Structure

```
.
├── resume_ner_model/          # Trained NER model
├── train_ner_model.py         # Script to train the NER model
├── resume_parser.py           # Resume parsing module
├── extract_resumes.py         # Resume extraction script
├── quick_annotator.py         # Quick annotation tool
├── evaluate_visualise.py      # Evaluation and visualization
├── simple_visualize.py        # Simple visualization script
├── training_data.json         # Training data in JSON format
├── setup.py                   # Setup script
└── README.md                  # This file
```

**Note:** The `resumes/` folder is not included in this repository for privacy reasons. You need to provide your own resume dataset to train or test the model.

## Installation

### Prerequisites
- Python 3.7+
- pip

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd custom_ner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Install the package:
```bash
python setup.py install
```

## Usage

### Preparing Your Dataset

1. Create a `resumes/` folder in the project root
2. Add your resume PDF files to this folder
3. The folder is git-ignored for privacy

### Training a Custom NER Model

```bash
python train_ner_model.py
```

### Parsing Resumes

```bash
python resume_parser.py
```

### Quick Annotation

```bash
python quick_annotator.py
```

### Extracting Resumes

```bash
python extract_resumes.py
```

### Visualization

```bash
python simple_visualize.py
```

## Model Details

The trained model is located in `resume_ner_model/` and includes:
- NER component trained on resume data
- Tokenizer configuration
- Vocabulary and vectors

**Note:** This pre-trained model is specific to the dataset it was trained on. For best results with your own resumes, retrain the model using your data and the provided training scripts.

## Data Format

Training data is provided in `training_data.json` with the following format:
```json
{
  "text": "Resume text",
  "entities": [
    {"start": 0, "end": 5, "label": "ENTITY_TYPE"}
  ]
}
```

## Evaluation

Run evaluation and visualization with:
```bash
python evaluate_visualise.py
```

## License

[Specify your license here]

## Authors

[Your name/team]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built with [spaCy](https://spacy.io/)
- This project demonstrates custom NER training for resume parsing
- Dataset not included - users must provide their own resume data

## Contact

[Your contact information]
