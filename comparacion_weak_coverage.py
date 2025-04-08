import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer los datos
file_paths = {
    "Weak Coverage": "/Users/Propietario/Desktop/TFG/03 Weak Coverage.csv",
    "Normal": "/Users/Propietario/Desktop/TFG/01 Normal.csv",
    "Massive Users": "/Users/Propietario/Desktop/TFG/04 Massive Users.csv"
}

selected_rows = [0, 12, 23, 34, 45, 56, 67, 78, 89, 100, 111, 122, 133, 144, 155, 166, 177, 188, 199, 210, 221, 232, 243, 254, 265]

# Indicadores de interés
target_indicators = [
  "cellLoad_allUsers_mean",
"RSRQ_allUsers_p95",
"RSRP_BadCoverage", #bajo
"cargaSlots" #bajo
    
]

# Cargar y procesar datos
data_frames = []
for category, path in file_paths.items():
    df = pd.read_csv(path, skiprows=lambda x: x not in selected_rows)  # Leer solo filas seleccionadas
    df = df[target_indicators].dropna()  # Asegurar que no haya NaN
    means = df.mean().reset_index().rename(columns={'index': 'Indicador', 0: 'Media'})
    means['Categoría'] = category
    data_frames.append(means)

# Combinar los datos de todas las categorías
combined = pd.concat(data_frames)

# Crear subplots en una cuadrícula adecuada (8 indicadores → 4x2)
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()  # Aplanar la matriz de ejes para iterar fácilmente

# Diccionario de colores para las categorías
color_dict = {"Massive Users": '#66B2FF', "Normal": '#FF9999', "Weak Coverage": '#99FF99'}

# Crear gráficos de barras para cada KPI
for i, indicator in enumerate(target_indicators):
    ax = axes[i]
    sns.barplot(x='Categoría', y='Media', 
                data=combined[combined['Indicador'] == indicator], 
                palette=color_dict, 
                alpha=0.9, edgecolor='black', ax=ax)
    
    ax.set_title(indicator, fontsize=12)
    ax.set_ylabel('Valor Medio', fontsize=10)
    ax.set_xlabel('')
    
    # Añadir etiquetas en las barras
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom', fontsize=8)

# Ajustar diseño
plt.tight_layout(pad=4)
plt.show()
