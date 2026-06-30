from fastapi import APIRouter, UploadFile, File, HTTPException
import base64
from backend.services.yolo_service import process_image_with_yolo

router = APIRouter()

@router.post("/predict", summary="Detecta larvas e retorna JSON com contagem e imagem base64")
async def predict_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="O arquivo enviado não é uma imagem.")
        
    try:
        image_bytes = await file.read()
        processed_image_bytes, count = process_image_with_yolo(image_bytes)
        
        image_b64 = base64.b64encode(processed_image_bytes).decode('utf-8')
        
        return {
            "count": count,
            "image": f"data:image/jpeg;base64,{image_b64}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar a imagem: {str(e)}")
