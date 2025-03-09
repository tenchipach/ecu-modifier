from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/modify_binary_file/")
async def modify_binary_file(file: UploadFile = File(...), modification_type: str = "invert"):
    contents = await file.read()
    return {"message": f"Archivo {file.filename} recibido con modificación {modification_type}"}
