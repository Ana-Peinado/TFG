import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datos de massive users y los archivos adicionales
massive_users = pd.read_csv('/Users/Propietario/Desktop/TFG/04 Massive Users.csv', skiprows=lambda x: x not in [0, 12, 23, 34, 45, 56, 67, 78, 89, 100, 111, 122, 133, 144, 155, 166, 177, 188, 199, 210, 221, 232, 243, 254, 265])
normal = pd.read_csv('/Users/Propietario/Desktop/TFG/01 Normal.csv', skiprows=lambda x: x not in [0, 12, 23, 34, 45, 56, 67, 78, 89, 100, 111, 122, 133, 144, 155, 166, 177, 188, 199, 210, 221, 232, 243, 254, 265], engine='python')
weakcoverage = pd.read_csv('/Users/Propietario/Desktop/TFG/03 Weak Coverage.csv', skiprows=lambda x: x not in [0, 12, 23, 34, 45, 56, 67, 78, 89, 100, 111, 122, 133, 144, 155, 166, 177, 188, 199, 210, 221, 232, 243, 254, 265])

target_indicators = [
    "cargaSlots",
    "RSRP_BadCoverage",
    "Distance_allUsers_mean",
    "Throughput_allUsers_p95" #bajo
]

# Filtrar solo las columnas de interés
massive_users = massive_users[target_indicators]
normal = normal[target_indicators]
weakcoverage = weakcoverage[target_indicators]

# Calcular medias
massive_users_means = massive_users.mean().reset_index().rename(columns={'index': 'Indicador', 0: 'Media'}); massive_users_means['Categoría'] = 'MU'
normal_means = normal.mean().reset_index().rename(columns={'index': 'Indicador', 0: 'Media'}); normal_means['Categoría'] = 'Normal'
weakcoverage_means = weakcoverage.mean().reset_index().rename(columns={'index': 'Indicador', 0: 'Media'}); weakcoverage_means['Categoría'] = 'WC'

# Combinar datos
combined = pd.concat([massive_users_means, normal_means, weakcoverage_means])

# Crear subplots
fig, axes = plt.subplots(1, len(target_indicators), figsize=(15, 6))


# Diccionario de colores para las categorías
color_dict = {'MU': '#66B2FF', 'Normal': '#FF9999', 'WC': '#99FF99'}

# Crear un gráfico para cada indicador
for i, indicator in enumerate(target_indicators):
    sns.barplot(x='Categoría', y='Media', 
                data=combined[combined['Indicador'] == indicator], 
                palette=color_dict,
                alpha=0.9,
                edgecolor='black',
                ax=axes[i])
    axes[i].set_title(indicator, fontsize=9)
    axes[i].set_xlabel('')
    axes[i].tick_params(axis='x')
    
    # Añadir anotaciones
    for p in axes[i].patches:
        height = p.get_height()
        axes[i].annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                         ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.show()
