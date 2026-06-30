import { Source_Serif_4, IBM_Plex_Mono } from "next/font/google";
import "./globals.css";

const sourceSerif = Source_Serif_4({ 
  subsets: ["latin"],
  variable: '--font-source-serif',
});

const plexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ['400', '600', '700'],
  variable: '--font-plex-mono',
});

export const metadata = {
  title: "Ficha de Inspeção - Aedes",
  description: "Sistema de Campo para Agentes de Saúde",
};

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <body className={`${sourceSerif.variable} ${plexMono.variable}`}>
        {children}
      </body>
    </html>
  );
}
