from fastapi import FastAPI, File, UploadFile
import shutil
import os

app = FastAPI()

UPLOAD_FOLDER = "uploads"
MODIFIED_FOLDER = "modified"

# Asegurar que las carpetas existen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODIFIED_FOLDER, exist_ok=True)

@app.post("/modify_file/")
async def modify_file(file: UploadFile, modification_type: str):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Guardar el archivo original
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    modified_file_path = os.path.join(MODIFIED_FOLDER, f"mod_{file.filename}")

    # Aquí implementamos la lógica de modificación según el tipo
    if modification_type == "invert":
        with open(file_path, "rb") as f:
            data = f.read()
        with open(modified_file_path, "wb") as f:
            f.write(data[::-1])  # Ejemplo: invertir bytes

    elif modification_type == "dummy_edit":
        with open(file_path, "rb") as f:
            data = f.read()
        with open(modified_file_path, "wb") as f:
            f.write(data[:100] + b"MODIFIED" + data[100:])  # Insertar texto en binario

    else:
        return {"error": "Modificación no soportada"}

    return {"message": f"Archivo {file.filename} modificado con {modification_type}", "download_link": f"/download/{file.filename}"}

@app.get("/download/{filename}")
async def download_file(filename: str):
    modified_file_path = os.path.join(MODIFIED_FOLDER, f"mod_{filename}")
    if os.path.exists(modified_file_path):
        return {"message": f"Descarga el archivo modificado aquí: {modified_file_path}"}
    return {"error": "Archivo no encontrado"}
