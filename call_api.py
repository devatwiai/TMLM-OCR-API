import requests
import cv2
import numpy as np
import os
"""
Instruction: 
1. Read an image in binary format and send it to the API using a POST request.
2. The API returns a dictionary containing bounding box coordinates and detected text in the image.
"""

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/devesh_wadhwaniai_org/person/TMLM-OCR-API/cred.json'

# API URL and the local path of the image
url = "http://localhost:8000/predict/"
image_path = "./temp.jpg"

# Open the image in binary format to send it in the POST request

with open('temp.jpg', "rb") as image_file:
    files = {"file": image_file}  # File data for the request
    response = requests.post(url, files=files, verify=False)  # Send POST request
    output = response.json()  # Get the API's JSON response
    print(output)
    '''
    Example output:
    {
        'output': [
            {'x': 100, 'y': 47, 'w': 600, 'h': 122, 'text': '(མཛད་རྣམ་རྒྱ་ཆེན་སྙིང་རྗེའི་'},
            {'x': 310, 'y': 175, 'w': 204, 'h': 70, 'text': 'རོལ་མཚོ།'},
            {'x': 188, 'y': 1098, 'w': 475, 'h': 45, 'text': 'ནོར་གླིང་མཛད་རྣམ་སྡེ་ཚན་ནས་རྩོམ་སྒྲིག་དང་།'}
        ]
    }
    '''

def draw_bbox(image_path, outputs):
    """
    Draw bounding boxes on the image based on API output.
    """
    
    image = cv2.imread(image_path)  # Read the image

    # Loop through each bounding box and draw it on the image
    for line in outputs:
        x, y, w, h = line["x"], line["y"], line["w"], line["h"]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2) 
        print(f"Detected text: {line['text']}")  
        
    return image

img = draw_bbox(image_path, output["output"]) 
cv2.imwrite("output.jpg", img) 
