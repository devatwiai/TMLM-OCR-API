
# TMLM-OCR-API

## Installation Instructions

1. Installation:
   ```
   sudo apt-get update
   sudo apt-get install libgl1-mesa-glx
   pip install -r requirements.txt
   ```
   

4. Copy the PROJECT_ID, LOCATION, and PROCESSOR_ID values into the .env file.

5. Start the API server:
   ```
   uvicorn app:app --port 8000 --host 0.0.0.0
   python call_api.py
   ```