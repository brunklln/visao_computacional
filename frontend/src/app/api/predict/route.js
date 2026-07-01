import { NextResponse } from 'next/server';

export async function POST(request) {
  try {
    const formData = await request.formData();
    const file = formData.get("file");
    
    if (!file) {
      return NextResponse.json({ error: "No file found" }, { status: 400 });
    }
    
    // Recria o FormData explicitamente para evitar bugs de serialização (502 Bad Gateway) do Node.js no Vercel
    const backendFormData = new FormData();
    backendFormData.append("file", file);
    
    console.log("Enviando requisição proxy para o FastAPI...");

    const BACKEND_URL = process.env.BACKEND_URL || 'http://127.0.0.1:8000';
    const response = await fetch(`${BACKEND_URL}/api/v1/predict`, {
      method: "POST",
      body: backendFormData,
      headers: {
        "Bypass-Tunnel-Reminder": "true" // Header obrigatório para APIs via localtunnel
      }
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("FastAPI Error:", response.status, errorText);
      return NextResponse.json({ error: "Backend error", details: errorText }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("Proxy Exception:", error);
    return NextResponse.json({ error: "Proxy error", details: error.message }, { status: 500 });
  }
}
