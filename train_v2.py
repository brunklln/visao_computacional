from ultralytics import YOLO

if __name__ == '__main__':
    # Usando o modelo Small (yolov8s) para maior capacidade de acerto
    # Ele é mais inteligente que o modelo Nano que usamos na V1
    model = YOLO('yolov8s.pt')

    print("Iniciando o treinamento de OTIMIZACAO do YOLOv8...")
    
    # Treinamento longo e profundo
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATASET_YAML = os.path.join(
        BASE_DIR,
        'Larva Aedes Aegypti.v4i.yolov8',
        'data.yaml'
    )
    
    results = model.train(
        data=DATASET_YAML,
        epochs=100,
        patience=25,
        imgsz=640,
        batch=16,
        project='runs',
        name='larva_aedes_v2'
    )
    
    import shutil

    # Após model.train(...)
    metrics_src = os.path.join('runs', 'detect', 'larva_aedes_v2')
    metrics_dst = os.path.join(BASE_DIR, 'resultados_modelo')
    os.makedirs(metrics_dst, exist_ok=True)

    # Copia arquivos de métricas gerados pelo YOLOv8
    for fname in ['results.csv', 'confusion_matrix.png', 
                  'P_curve.png', 'R_curve.png', 'PR_curve.png']:
        src = os.path.join(metrics_src, fname)
        if os.path.exists(src):
            shutil.copy(src, metrics_dst)
            print(f'Métricas salvas: {fname}')

    # Copia também os pesos do modelo
    weights_dst = os.path.join(BASE_DIR, 'weights')
    os.makedirs(weights_dst, exist_ok=True)
    best_pt = os.path.join(metrics_src, 'weights', 'best.pt')
    if os.path.exists(best_pt):
        shutil.copy(best_pt, weights_dst)
        print('best.pt copiado para weights/')
    
    print("Treinamento de otimização finalizado com sucesso!")
