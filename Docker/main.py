from fastapi import FastAPI, UploadFile, File
from doc_api import predict
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/predict")
async def process_image(file: UploadFile = File(...)):
    try:
        # Read the image from the uploaded file
        image_data = await file.read()
        
        # You need to handle file writing or pass it directly to the predict function
        output = predict(image_data)
        
        return JSONResponse(content={"output": output})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

# Start the server using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", reload=True)
