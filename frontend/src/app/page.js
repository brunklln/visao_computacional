"use client";

import { useState, useEffect } from "react";
import { Search } from "lucide-react";
import PhotoAttachment from "../components/PhotoAttachment";
import LaudoStamp from "../components/LaudoStamp";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [result, setResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  
  // Estado para resolver o erro de hidratação (SSR vs Client)
  const [headerData, setHeaderData] = useState({ id: "----", data: "--/--/----" });

  useEffect(() => {
    // Roda apenas no navegador, garantindo que não haverá divergência com o servidor
    setHeaderData({
      id: Math.floor(Math.random() * 10000).toString().padStart(4, '0'),
      data: new Date().toLocaleDateString('pt-BR')
    });
  }, []);

  const handleFileSelected = (file) => {
    setSelectedFile(file);
    // Cria uma URL local para preview da foto tirada/selecionada
    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);
    // Limpa o laudo anterior caso haja um
    setResult(null);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      // Usa a rota proxy do próprio Next.js, que encaminhará para o FastAPI
      const response = await fetch("/api/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.details || "Erro 500: API fora do ar");
      }

      const data = await response.json();
      
      // Atualiza a tela com a foto carimbada pelo YOLO e a contagem
      setPreviewUrl(data.image);
      setResult({ count: data.count });
      
    } catch (error) {
      console.error(error);
      alert(`Falha na análise: ${error.message}`);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <main>
      <div className="inspection-board">
        <header className="header">
          <h1 className="header-title">Ficha de Inspeção</h1>
          <div className="header-meta">
            <span className="mono">ID: {headerData.id}</span>
            <span className="mono">DATA: {headerData.data}</span>
          </div>
        </header>

        {/* Anexo da Armadilha/Ovitrampa */}
        <PhotoAttachment 
          previewUrl={previewUrl} 
          onFileSelected={handleFileSelected} 
        />

        {/* Botão de Ação Principal */}
        <button 
          className="btn" 
          style={{ width: "100%", padding: "1rem" }}
          onClick={handleAnalyze}
          disabled={!selectedFile || isAnalyzing}
        >
          {isAnalyzing ? (
            <>
              <div className="loading-indicator"></div>
              <span>PROCESSANDO...</span>
            </>
          ) : (
            <>
              <Search size={20} />
              <span>ANALISAR OVITRAMPA</span>
            </>
          )}
        </button>

        {/* Carimbo do Laudo */}
        {result && <LaudoStamp count={result.count} />}

      </div>
    </main>
  );
}
