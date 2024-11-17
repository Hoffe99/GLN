# Importieren der notwendigen Bibliotheken
import pandas as pd
import matplotlib.pyplot as plt

# Erstellung eines Beispiel-Datensatzes
data = {
    'Monat': ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni'],
    'Verkauf': [100, 120, 150, 180, 200, 220]
}

# Erstellung eines Pandas-DataFrames
df = pd.DataFrame(data)

# Ausgabe des DataFrames
print(df)

# Berechnung der Gesamtsumme der Verkäufe
gesamtsumme = df['Verkauf'].sum()
print("Gesamtsumme der Verkäufe:", gesamtsumme)

# Berechnung des Durchschnittsverkaufs pro Monat
durchschnittsverkauf = df['Verkauf'].mean()
print("Durchschnittsverkauf pro Monat:", durchschnittsverkauf)

# Erstellung eines Diagramms für die Verkaufsdaten
plt.figure(figsize=(10, 6))
plt.plot(df['Monat'], df['Verkauf'], marker='o')
plt.title('Verkaufsdaten')
plt.xlabel('Monat')
plt.ylabel('Verkauf')
plt.grid(True)
plt.show()