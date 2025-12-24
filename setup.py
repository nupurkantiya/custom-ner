import subprocess
import sys

def install_packages():
    packages = [
        'spacy',
        'pandas',
        'PyPDF2',
        'python-docx',
        'scikit-learn',
        'matplotlib'
    ]
    
    print("Installing required packages...")
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    
    # Download spaCy English model
    print("\nDownloading spaCy English model...")
    subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'])
    
    print("\n✅ Setup complete!")

if __name__ == "__main__":
    install_packages()