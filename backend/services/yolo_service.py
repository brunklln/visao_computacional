import os
from ultralytics import YOLO
import cv2, numpy as np, io

# Caminho relativo à pasta do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', '..', 'weights', 'best.pt')

# Permite sobrescrever via variável de ambiente (opcional)
MODEL_PATH = os.environ.get('YOLO_MODEL_PATH', MODEL_PATH)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Modelo não encontrado em: {MODEL_PATH}\n"
        "Coloque o arquivo best.pt na pasta weights/ do projeto."
    )

print(f"Carregando modelo de: {MODEL_PATH}")
model = YOLO(MODEL_PATH)

def process_image_with_yolo(image_bytes: bytes):
    np_img = np.frombuffer(image_bytes, np.uint8)
    img_cv2 = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    
    if img_cv2 is None:
        raise ValueError("Não foi possível decodificar a imagem enviada.")
        
    # 1. Desativamos o TTA pois ele inflou a confiança dos ruídos de fundo (bordas do pote).
    # 2. conf=0.35: Limiar moderado para não perder larvas fracas.
    # 3. iou=0.25: Mescla muito agressiva para impedir caixas duplicadas na mesma larva.
    # 4. imgsz=800: Resolução um pouco maior que a nativa para ajudar na nitidez.
    results = model.predict(
        source=img_cv2, 
        conf=0.35, 
        iou=0.25, 
        imgsz=800, 
        augment=False
    )
    result = results[0]
    
    # Filtro Espacial (Pós-processamento):
    # O modelo às vezes confunde o reflexo da água ou a borda da ovitrampa com uma larva gigante.
    # Sabendo que larvas são pequenas, descartamos sumariamente qualquer marcação que ocupe mais de 10% da foto.
    img_h, img_w = img_cv2.shape[:2]
    total_area = img_h * img_w
    
    keep_indices = []
    for i, box in enumerate(result.boxes):
        w = box.xywh[0][2].item()
        h = box.xywh[0][3].item()
        
        # Se a caixa for menor que 10% da área da imagem, é uma larva válida
        if (w * h) / total_area < 0.10:
            keep_indices.append(i)
            
    # Aplica o filtro de tamanho
    result.boxes = result.boxes[keep_indices]
    
    # Conta quantas larvas foram detectadas
    count = len(result.boxes)
    
    annotated_frame = result.plot()
    
    success, buffer = cv2.imencode('.jpg', annotated_frame)
    if not success:
        raise RuntimeError("Falha ao recodificar a imagem para JPEG.")
        
    return buffer.tobytes(), count
