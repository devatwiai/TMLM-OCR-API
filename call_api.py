import requests
import cv2
import time
from urllib.parse import urljoin

"""
Instructions: 
1. Read an image in binary format and send it to the API using a POST request.
2. The API returns a dictionary containing bounding box coordinates and detected text in the image.
"""

# API URL and the local path of the image
ENDPOINT_URL = "http://localhost:8000/"
image_path = "tmp.jpg"

# Open the image file in binary mode
with open(image_path, "rb") as image_file:
    files = {"file": image_file}
    start_time = time.time()
    
    # Send a POST request to the API
    response = requests.post(urljoin(ENDPOINT_URL, 'predict'), files=files)
    
    print(f"Time taken: {(time.time() - start_time):.2f} seconds")

    # Parse the JSON response
    try: 
        output = response.json()
    except Exception as e:
        print(f"Error: {e}")
        print(f"Response: {response.text}")
        output = {'output': []}    

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
    Draw bounding boxes on the image based on API output using OpenCV.
    You can use any other library to draw bounding boxes.
    
    Args:
        image_path (str): The path to the input image.
        outputs (list): The list of bounding boxes and detected text.

    Returns:
        numpy.ndarray: The image with bounding boxes drawn.
    """
    
    image = cv2.imread(image_path)  # Read the image

    # Loop through each bounding box and draw it on the image
    for line in outputs:
        x, y, w, h = line["x"], line["y"], line["w"], line["h"]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2) 
        print(f"Detected text: {line['text']}")  
        
    return image

# Draw bounding boxes on the original image
img = draw_bbox(image_path, output.get("output", [])) 
cv2.imwrite("output.jpg", img)  # Save the output image with bounding boxes