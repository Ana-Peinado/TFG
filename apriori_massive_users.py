import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


low_quantile = 0.30 # no he puesto 33 y 66 porque sino no me salian reglas fuertes
high_quantile = 0.60

df = pd.read_csv('/Users/Propietario/Desktop/TFG/04 Massive Users.csv')

to_drop = [col for col in df.columns if 'masterUsers' in col]
df.drop(columns=to_drop, inplace=True)

quantiles = df.quantile([low_quantile, high_quantile])

dff = pd.read_csv('/Users/Propietario/Desktop/TFG/04 Massive Users.csv',  
                  skiprows=lambda x: x not in [0, 12, 23, 34, 45, 56, 67, 78, 89, 100, 111, 122, 133, 144, 155, 166, 177, 188, 199, 210, 221, 232, 243, 254, 265])
dff.drop(columns=to_drop, inplace=True)

binary_df = pd.DataFrame(index=dff.index)
for col in dff.columns:
    low_threshold = quantiles.loc[low_quantile, col]
    high_threshold = quantiles.loc[high_quantile, col]
    binary_df[col + '_bajo'] = (dff[col] < low_threshold).astype(int)
    binary_df[col + '_alto'] = (dff[col] > high_threshold).astype(int)

frequent_itemsets = apriori(binary_df, min_support=0.5, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.75)

strong_rules = rules[(rules['lift'] > 1.2) & (rules['confidence'] > 0.8)]
print("\nReglas fuertes (antecedente, consecuente, confianza, soporte, lift) ordenadas por lift:")
print(strong_rules[['antecedents', 'consequents', 'confidence', 'support', 'lift']].sort_values('lift', ascending=False))

print("\nNúmero total de reglas:", len(rules))
print("Número de reglas fuertes:", len(strong_rules))

