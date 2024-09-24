import os
import cv2
import numpy as np
import json
from typing import Optional
from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore
from google.protobuf.json_format import MessageToJson
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv('PROJECT_ID')
LOCATION = os.getenv('LOCATION')
PROCESSOR_ID = os.getenv('PROCESSOR_ID')

# Check if any of the variables are None and raise an exception if they are
if PROJECT_ID is None or LOCATION is None or PROCESSOR_ID is None:
    raise EnvironmentError(
        "One or more environment variables are not set: "
        f"PROJECT_ID={PROJECT_ID}, LOCATION={LOCATION}, PROCESSOR_ID={PROCESSOR_ID}"
    )


mime_type="image/jpeg"

def predict(
    img_data: bytes,
    field_mask: Optional[str] = None,
    processor_version_id: Optional[str] = None,
) -> None:

    opts = ClientOptions(api_endpoint=f"{LOCATION}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    if processor_version_id:
        # The full resource name of the processor version, e.g.:
        # `projects/{PROJECT_ID}/LOCATIONs/{LOCATION}/processors/{PROCESSOR_ID}/processorVersions/{processor_version_id}`
        name = client.processor_version_path(
            PROJECT_ID, LOCATION, PROCESSOR_ID, processor_version_id
        )
    else:
        name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

    # Read the file into memory
    # with open(file_path, "rb") as image:
    #     image_content = image.read()
    image_content = img_data

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
    process_options = documentai.ProcessOptions(
        # Process only specific pages
        individual_page_selector=documentai.ProcessOptions.IndividualPageSelector(
            pages=[1]
        )
    )

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
        field_mask=field_mask,
        process_options=process_options,
    )

    result = client.process_document(request=request)
    json_output = MessageToJson(result._pb)
    # clean the json before dumping
    json_output = json.loads(json_output)
    bbox_to_output = postprocess(json_output)
    return bbox_to_output



def postprocess(ori_data):
    '''
    Extracts bounding boxes and corresponding text from the doc-ai output
    '''
    
    lines = ori_data["document"]["pages"][0]["lines"]
    text = ori_data["document"]["text"]
    original_text_dict = []
    for i, line in enumerate(lines):
        output_dict = {}
        try:
            start_index = int(line["layout"]["textAnchor"]["textSegments"][0].get("startIndex", 0))
            end_index = int(line["layout"]["textAnchor"]["textSegments"][0].get("endIndex", 0))
            text_ = text[start_index:end_index]
            vertices = line["layout"]["boundingPoly"]["vertices"]
            pts = np.array([[v["x"], v["y"]] for v in vertices], np.int32)
            pts = pts.reshape((-1, 1, 2))
            bbox = cv2.boundingRect(pts)
            output_dict["x"] = bbox[0]; output_dict["y"] = bbox[1]; output_dict["w"] = bbox[2]; output_dict["h"] = bbox[3]
            output_dict["text"] = text_.strip()
            original_text_dict.append(output_dict)
            
        except Exception as e:
            pass
            
    return original_text_dict


