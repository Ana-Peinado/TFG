import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

problematicas = pd.read_csv('/Users/Propietario/Desktop/TFG/04 Massive Users.csv',  
                            skiprows=lambda x: x not in [0, 12, 34, 67, 89, 122, 144, 177, 199, 232, 254])
sector = pd.read_csv('/Users/Propietario/Desktop/TFG/04 Massive Users.csv', 
                     skiprows=lambda x: x not in [0, 23, 45, 56, 78, 100, 111, 133, 155, 166, 188, 210, 221, 243, 265])
vecinas = pd.read_csv('/Users/Propietario/Desktop/TFG/04 Massive Users.csv', 
                      skiprows=lambda x: x not in [0, 1, 6, 17, 19, 30, 51, 61, 72, 74, 85, 106, 116, 127, 129, 140, 161, 171, 182, 184, 195, 216, 226, 237, 239, 250, 271])

target_indicators = [
    "cargaSlots",
    "RSRP_BadCoverage",
    "Distance_allUsers_mean",
    "Throughput_allUsers_p95"
]

vecinas = vecinas[target_indicators]
sector = sector[target_indicators]
problematicas = problematicas[target_indicators]

# Calcular medias
vecinas_means = vecinas.mean().reset_index().rename(columns={'index': 'Indicador', 0: 'Media'})
vecinas_means['Categoría'] = 'Vecinas'

sector_means = sector.mean().reset_index().rename(columns={'index': 'Indicador', 0: 'Media'})
sector_means['Categoría'] = 'Sector'

problematicas_means = problematicas.mean().reset_index().rename(columns={'index': 'Indicador', 0: 'Media'})
problematicas_means['Categoría'] = 'Problemáticas'

combined = pd.concat([vecinas_means, sector_means, problematicas_means])

# Crear el gráfico con subgráficos
fig, axes = plt.subplots(2, 2, figsize=(35, 10))  # Aumentamos el tamaño de la figura
plt.subplots_adjust(wspace=0.7, hspace=0.5)  # Aumentamos el espacio entre gráficos

color_dict = {'Vecinas': '#66B2FF', 'Sector': '#FF9999', 'Problemáticas': '#99FF99'}

for i, indicator in enumerate(target_indicators):
    ax = axes[i//2, i%2]  # Acceso adecuado para 2D array de subgráficos
    sns.barplot(x='Categoría', y='Media', 
                data=combined[combined['Indicador'] == indicator], 
                palette=color_dict, 
                alpha=0.9, edgecolor='black', ax=ax)
    
    ax.set_title(indicator, fontsize=12)  # Título más grande
    ax.set_xlabel('')
   
    ax.tick_params(axis='y', labelsize=9) 
    ax.tick_params(axis='x', labelsize=9, rotation=30)

    # Agregar anotaciones en las barras
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom', fontsize=10)

    # Eliminar la línea horizontal superior y derecha
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.show()
