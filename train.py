from ultralytics import YOLO

if __name__ == '__main__':
    # Escolha do modelo base: yolov8n.pt (Nano) é leve e rápido.
    # O YOLO converterá os polígonos do seu dataset para Bounding Boxes automaticamente.
    model = YOLO('yolov8n.pt')

    print("Iniciando o treinamento do YOLOv8...")
    
    # Inicia o treinamento
    # Você pode alterar parâmetros como 'epochs', 'imgsz' e 'batch'
    results = model.train(
        data=r'c:\Users\Bruna\Documents\visao_computacional\Larva Aedes Aegypti.v4i.yolov8\data.yaml',
        epochs=50,          # Número de épocas
        imgsz=640,          # Tamanho da imagem
        batch=16,           # Tamanho do batch
        project='runs',     # Pasta onde os resultados serão salvos
        name='larva_aedes'  # Nome do experimento
    )
    
    print("Treinamento finalizado com sucesso!")
