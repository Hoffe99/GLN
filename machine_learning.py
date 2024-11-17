# Importiere notwendige Bibliotheken
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Erstelle ein einfaches Beispiel für Eingabedaten (X) und Zielvariablen (y)
# X Anzahl der Lernstunden
# Y Anzahl der erreichten Punkten
X = np.array([[1], [2], [3], [4], [5]])  
y = np.array([5, 2, 7, 12, 8])     

# Initialisiere das Modell für lineare Regression
model = LinearRegression()

# Trainiere das Modell mit den Eingabedaten (X) und Zielvariablen (y)
model.fit(X, y)

predicted_score = model.predict([[6]]) # Vorhersage für 6 Stunden lernen

print(f"Vorhergesagte Punktzahl für 6 Stunden Lernen: {predicted_score[0]:.2f}")

# Visualisiere die Daten und die lineare Regression
plt.scatter(X, y, color='blue') 
plt.plot(X, model.predict(X), color='red')  
plt.title('Lineare Regression: Lernstunden vs. Punktzahl')
plt.xlabel('Anzahl der Lernstunden')
plt.ylabel('Punktzahl')
plt.show()
