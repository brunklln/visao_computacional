# Sistema de Contagem Automática de Larvas de *Aedes aegypti* (YOLOv8)

> **Universidade Federal do Oeste do Pará (UFOPA)**  
> **Instituto de Engenharia e Geociências - Programa de Computação**  
> **Disciplina:** Inteligência Artificial | **Período:** 2026  
> **Equipe:** Bruna Kellen

Este repositório contém o código-fonte do Trabalho Final da disciplina de Inteligência Artificial. Trata-se de uma aplicação web híbrida de Visão Computacional (AI Clássica) projetada para detectar e contar larvas de *Aedes aegypti* em imagens de ovitrampas de forma automatizada, mitigando o erro humano na vigilância epidemiológica.

## 🗂️ Arquitetura e Tecnologias
- **Modelo de IA:** Ultralytics YOLOv8 (Small) treinado com Hard Negative Mining e Filtros Espaciais para rejeição de falsos positivos (água e reflexos plásticos).
- **Backend:** Python 3.10+, FastAPI, OpenCV-Python, PyTorch.
- **Frontend:** Node.js 18+, Next.js (React), CSS3 (Responsivo Mobile).
- **Dataset:** [Larva Aedes Aegypti v4i](https://roboflow.com/) (1.442 imagens anotadas).

---

## 🚀 Pré-requisitos
Certifique-se de ter instalado em sua máquina:
- Python 3.10 ou superior
- Node.js 18 ou superior
- (Obrigatório) O arquivo contendo os pesos treinados da IA: `best.pt`. Este arquivo deve ser colocado manualmente na pasta `weights/` na raiz do projeto.

---

## 💻 Instruções de Instalação e Execução

### Passo 1: Iniciando a Inteligência Artificial (Backend)
Abra um terminal na raiz do projeto e execute:
```bash
# 1. Entre na pasta do backend (se os requirements estiverem lá, ou instale pela raiz)
pip install -r backend/requirements.txt

# 2. Inicie o servidor FastAPI (deve ser executado da raiz do projeto)
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
O servidor da IA estará rodando em `http://localhost:8000`.

### Passo 2: Iniciando a Interface de Usuário (Frontend)
Abra um **segundo terminal** e navegue até a pasta do frontend:
```bash
# 1. Entre na pasta
cd frontend

# 2. Instale as dependências do React/Next
npm install

# 3. Inicie o servidor web
npm run dev
```

---

## 📱 Exemplo de Uso
Com ambos os servidores rodando, abra o seu navegador e acesse:
**👉 http://localhost:3000**

1. Clique em "Câmera" ou "Galeria" para tirar/anexar a foto de uma ovitrampa.
2. Clique em "Analisar Ovitrampa".
3. A imagem será enviada para o Backend, processada pela rede YOLOv8, passará pelos nossos filtros espaciais, e o Laudo Final (imagem com as caixas vermelhas desenhadas e contagem total) aparecerá na tela.

*(Adicione aqui, no GitHub, uma imagem do sistema funcionando na prática. Dica: tire um print da tela com a contagem das larvas e cole no README usando `![Demonstração](link-da-imagem.png)`)*

---

## 📊 Extração de Métricas do Modelo
Conforme exigido pelos parâmetros de avaliação, você pode checar as métricas de performance do modelo (Precision, Recall, mAP50) a qualquer momento. Para isso, rode o script utilitário na raiz do projeto:

```bash
python gerar_metricas.py
```
*(As matrizes de confusão e gráficos de curva P/R podem ser encontrados na pasta `resultados_modelo/`)*
