"use client";

export default function LaudoStamp({ count }) {
  if (count === null || count === undefined) return null;

  const isAlert = count > 0;
  const stampClass = isAlert ? "alert" : "clean";
  const statusText = isAlert ? "FOCOS DETECTADOS" : "LIMPO / NEGATIVO";

  return (
    <div className="stamp-container">
      <div className={`stamp ${stampClass}`}>
        <div className="stamp-title">{statusText}</div>
        <div className="stamp-value">
          {count} {count === 1 ? "LARVA" : "LARVAS"}
        </div>
      </div>
    </div>
  );
}
