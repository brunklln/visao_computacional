import os, glob
from ultralytics import YOLO

if __name__ == '__main__':
    # 1. Carregar o modelo treinado (os melhores pesos encontrados)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(BASE_DIR, 'weights', 'best.pt')
    model = YOLO(model_path)

    # 2. Localizar algumas imagens de teste no dataset
    test_images_dir = os.path.join(
        BASE_DIR,
        'Larva Aedes Aegypti.v4i.yolov8',
        'test', 'images'
    )
    
    # Pegar as primeiras 5 imagens de teste disponíveis
    test_images = glob.glob(os.path.join(test_images_dir, '*.*'))[:5]
    
    if not test_images:
        print("Nenhuma imagem encontrada na pasta de testes!")
    else:
        print(f"Executando predições em {len(test_images)} imagens...")
        
        # 3. Rodar a predição e salvar o resultado com as caixas desenhadas (save=True)
        # Os resultados serão salvos na pasta especificada em project e name
        results = model.predict(
            source=test_images, 
            save=True, 
            project='runs/predict', 
            name='larva_aedes_test'
        )
        
        print("\nPronto! A inferência terminou.")
        print(r"Você pode verificar as imagens com as detecções salvas na pasta: C:\Users\Bruna\Documents\visao_computacional\runs\predict\larva_aedes_test")
