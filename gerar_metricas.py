# gerar_metricas.py
import os, pandas as pd

CSV = os.path.join('resultados_modelo', 'results.csv')
if not os.path.exists(CSV):
    print('Execute train_v2.py primeiro.')
    exit(1)

df = pd.read_csv(CSV)
df.columns = df.columns.str.strip()

# Melhor época (maior mAP50)
best = df.loc[df['metrics/mAP50(B)'].idxmax()]

print('=== MÉTRICAS DO MELHOR MODELO ===')
print(f'Época: {int(best["epoch"])}')
print(f'Precision: {best["metrics/precision(B)"]:.3f}')
print(f'Recall: {best["metrics/recall(B)"]:.3f}')
print(f'mAP50: {best["metrics/mAP50(B)"]:.3f}')
print(f'mAP50-95: {best["metrics/mAP50-95(B)"]:.3f}')
print()
print('Imagens de curva salvas em resultados_modelo/')
