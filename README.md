
# TMLM-OCR-API

## Run Docker Image Directly
```
docker pull deveshwi/tmlm-ocr:docai
gcloud auth application-default login
docker run -p 8000:8000 -v {$.env_file_path}:/app/.env -v  {$homedir_path}/.config/gcloud:/root/.config/gcloud deveshwi/tmlm-ocr:docai
```
### Call API using python
```
python call_api.py
```
### Call API using cURL
Send a POST Request: Use the following cURL command to send the image to the API:

```
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@tmp.jpg"
```
Output:
`{
    "output": [
        {
            "x": 100,
            "y": 47,
            "w": 600,
            "h": 122,
            "text": "(མཛད་རྣམ་རྒྱ་ཆེན་སྙིང་རྗེའི་"
        },
        {
            "x": 310,
            "y": 175,
            "w": 204,
            "h": 70,
            "text": "རོལ་མཚོ།"
        },
        {
            "x": 188,
            "y": 1098,
            "w": 475,
            "h": 45,
            "text": "ནོར་གླིང་མཛད་རྣམ་སྡེ་ཚན་ནས་རྩོམ་སྒྲིག་དང་།"
        }
    ]
}`

## Installation instructions for running it locally 

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
