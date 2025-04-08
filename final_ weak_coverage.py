import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Cargar los datos
weakcoverage = pd.read_csv('/Users/Propietario/Desktop/TFG/03 Weak Coverage.csv', skiprows=lambda x: x not in [0, 12, 34, 67, 89, 122, 144, 177, 199, 232, 254])
sector = pd.read_csv('/Users/Propietario/Desktop/TFG/03 Weak Coverage.csv', skiprows=lambda x: x not in [0, 23, 45, 56, 78, 100, 111, 133, 155, 166, 188, 210, 221, 243, 265])
vecinas = pd.read_csv('/Users/Propietario/Desktop/TFG/03 Weak Coverage.csv', skiprows=lambda x: x not in [0, 1, 6, 17, 19, 30, 51, 61, 72, 74, 85, 106, 116, 127, 129, 140, 161, 171, 182, 184, 195, 216, 226, 237, 239, 250, 271])

# Indicadores seleccionados
target_indicators = [
    "cellLoad_allUsers_mean",
    "RSRQ_allUsers_p95",
    "RSRP_BadCoverage",
    "cargaSlots"
]

vecinas, sector, weakcoverage = vecinas[target_indicators], sector[target_indicators], weakcoverage[target_indicators]

vecinas_means = vecinas.mean().reset_index().rename(columns={'index': 'Indicador', 0: 'Media'}); vecinas_means['Categoría'] = 'Vecinas'
sector_means = sector.mean().reset_index().rename(columns={'index': 'Indicador', 0: 'Media'}); sector_means['Categoría'] = 'Sector'
weakcoverage_means = weakcoverage.mean().reset_index().rename(columns={'index': 'Indicador', 0: 'Media'}); weakcoverage_means['Categoría'] = 'Problemáticas'

combined = pd.concat([vecinas_means, sector_means, weakcoverage_means])

# Corrección: RSRP_BadCoverage es positivo
indicadores_negativos = ["RSRQ_allUsers_p95"]
indicadores_positivos = [ind for ind in target_indicators if ind not in indicadores_negativos]

# Crear figura 2x2
fig, axes = plt.subplots(2, 2, figsize=(15, 10))  # 2 filas, 2 columnas

# Aplanar el array de ejes para iterar más fácilmente
axes = axes.flatten()

# Graficar cada indicador en su subplot correspondiente
for i, indicador in enumerate(target_indicators):
    data = combined[combined['Indicador'] == indicador]
    ax = axes[i]  # Seleccionar el subplot correspondiente
    
    sns.barplot(
        x='Categoría', y='Media', data=data, 
        palette={'Vecinas': '#66B2FF', 'Sector': '#FF9999', 'Problemáticas': '#99FF99'}, 
        alpha=0.9, edgecolor='black', ax=ax
    )

    # Ajustar los límites del eje Y
    if indicador in indicadores_negativos:
        ax.set_ylim(data['Media'].min() * 1.1, data['Media'].max() * 0.9)  
    else:
        ax.set_ylim(0, data['Media'].max() * 1.1)  

    ax.set_title(f'{indicador}', fontsize=10)
    ax.set_ylabel('Valor Medio', fontsize=9)
    ax.set_xlabel('')

    # Etiquetas sobre las barras
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height:.2f}', 
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom',
                    xytext=(0, 5), textcoords='offset points', 
                    fontsize=8)

    ax.tick_params(axis='x', rotation=30)

# Ajustes de diseño
plt.tight_layout()

plt.subplots_adjust(wspace=0.4, hspace=0.4, bottom=0.2)
plt.show()
