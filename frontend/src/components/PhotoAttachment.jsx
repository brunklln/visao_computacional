"use client";

import { Camera, ImagePlus } from "lucide-react";

export default function PhotoAttachment({ previewUrl, onFileSelected }) {
  const handleFileChange = (e) => {
    try {
      const file = e.target.files[0];
      if (file) {
        onFileSelected(file);
      }
      e.target.value = null; // reseta para permitir a mesma foto
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className={`photo-attachment ${previewUrl ? "has-photo" : ""}`}>
      {previewUrl ? (
        <img src={previewUrl} alt="Visualização da foto" className="photo-preview" />
      ) : (
        <>
          <div className="photo-label">NENHUMA FOTO ANEXADA</div>
          <p style={{ fontSize: "0.85rem", color: "#666", marginBottom: "1.5rem" }}>
            Selecione uma foto da armadilha para análise.
          </p>
        </>
      )}

      {/* Técnica Overlay 2.0: O Safari exige que você toque no próprio input visível, 
          então o input fica cobrindo todo o botão com 1% de opacidade. */}
      <div className="action-grid">
        <div className="btn btn-outline file-btn-wrapper" style={{ margin: 0 }}>
          <Camera size={18} /> CÂMERA
          <input
            type="file"
            accept="image/*"
            capture="environment"
            className="overlay-input"
            onChange={handleFileChange}
          />
        </div>
        
        <div className="divider"></div>
        
        <div className="btn btn-outline file-btn-wrapper" style={{ margin: 0 }}>
          <ImagePlus size={18} /> GALERIA
          <input
            type="file"
            accept="image/*"
            className="overlay-input"
            onChange={handleFileChange}
          />
        </div>
      </div>
    </div>
  );
}
