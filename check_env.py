import sys
import os

def check_environment():
    """Check if the virtual environment is set up correctly."""
    # Check if we're running in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print(f"✓ Virtual environment is active.")
        print(f"  - Python executable: {sys.executable}")
        print(f"  - Python version: {sys.version}")
    else:
        print("✗ Virtual environment is NOT active.")
        print("  Please activate the virtual environment before running this script.")
    
    # Check required packages
    try:
        import flask
        print(f"✓ Flask is installed (version: {flask.__version__})")
    except ImportError:
        print("✗ Flask is not installed.")
    
    try:
        import openai
        print(f"✓ OpenAI is installed (version: {openai.__version__})")
    except ImportError:
        print("✗ OpenAI is not installed.")
    
    try:
        import pytest
        print(f"✓ pytest is installed (version: {pytest.__version__})")
    except ImportError:
        print("✗ pytest is not installed.")
    
    # Check for .env file
    env_file = os.path.join('instance', '.env')
    if os.path.exists(env_file):
        print(f"✓ .env file exists in instance folder.")
    else:
        print(f"✗ .env file not found in instance folder. Please create one from .env.example")
        
if __name__ == "__main__":
    print("Checking virtual environment setup...")
    check_environment()
    print("\nIf all checks passed, your environment is ready!")
    print("If any checks failed, please refer to the README.md for setup instructions.")