import pandas as pd

# Chemin du fichier
file_path = "C:\\Users\\marin\\Downloads\\accidentsVelo.csv"

# Chargement des données
df = pd.read_csv(file_path)

# Affichage des premières lignes
print(df.head())

num_observations = df.shape[0]
num_variables = df.shape[1]
print(f"Nombre d'observations: {num_observations}")
print(f"Nombre de variables: {num_variables}")

num_observations = df.shape[0]
num_variables = df.shape[1]
print(f"Nombre d'observations: {num_observations}")
print(f"Nombre de variables: {num_variables}")


# Description du jeu de données
st.header("Description du jeu de données")
st.write("Origine des données : [Lien vers le jeu de données](https://opendata.paris.fr/explore/dataset/inventaire-des-emissions-de-gaz-a-effet-de-serre-du-territoire/dataviz/)")
st.write(f"Nombre d'années d'observation : {data.shape[0]}")
st.write(f"Nombre de variables : {data.shape[1]-2}") # On parle seulement ici des données collectées sur le site et pas des variables créées
st.write("Types de variables :")
st.write(data.dtypes)
st.write("Nombre de valeurs manquantes par variable :")
st.write(data.isnull().sum())

st.header("Statistiques descriptives")
st.write(df.describe())

# Visualisations
st.header("Visualisations")

# Suppression ou imputation des valeurs manquantes
df = df.dropna()  # Exemple de suppression des lignes avec des valeurs manquantes
# Autres opérations de nettoyage possibles


def safe_int_conversion(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None  # Ou une autre valeur par défaut selon votre logique

# Création de la nouvelle variable en utilisant une conversion sécurisée
df['heure'] = df['hrmn'].apply(lambda x: safe_int_conversion(x.split(':')[0]))
df['minute'] = df['hrmn'].apply(lambda x: safe_int_conversion(x.split(':')[1]))


import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Conversion de l'heure en format datetime pour une meilleure gestion par Matplotlib
df['heure_datetime'] = df['heure'].apply(lambda x: datetime.strptime(str(x), '%H'))

# Affichage dans Streamlit
st.header("Distribution des heures des accidents")

# Filtre interactif pour le mois
selected_month = st.selectbox('Sélectionner un mois', df['mois'].unique())

# Création de l'histogramme avec filtrage par mois
filtered_data = df[df['mois'] == selected_month]
fig, ax = plt.subplots()
sns.histplot(filtered_data['heure_datetime'], bins=24, kde=True, ax=ax)
ax.set_xlabel('Heure de l\'accident')
ax.set_ylabel('Nombre d\'accidents')
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))  # Format de l'axe des abscisses
st.pyplot(fig)


import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static  # Module pour intégrer Folium avec Streamlit

# Chargement des données
file_path = "C:\\Users\\marin\\Downloads\\accidentsVelo.csv"
df = pd.read_csv(file_path)

# Conversion des colonnes lat et long en numérique et gestion des NaN
df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
df['long'] = pd.to_numeric(df['long'], errors='coerce')

# Suppression des lignes avec des NaN dans lat et long
df.dropna(subset=['lat', 'long'], inplace=True)

# Interface Streamlit
st.header("Carte des Lieux d'Accidents")

# Filtre interactif pour le département
selected_department = st.selectbox('Sélectionner un département', df['dep'].unique())

# Filtrage des données par département
filtered_data = df[df['dep'] == selected_department]

# Création de la carte avec Folium
if not filtered_data.empty:
    # Calcul du centre de la carte
    map_center = filtered_data[['lat', 'long']].mean().values.tolist()

    # Création de la carte Folium
    my_map = folium.Map(location=map_center, zoom_start=10)

    # Ajout des marqueurs pour chaque point d'accident
    for index, row in filtered_data.iterrows():
        folium.Marker([row['lat'], row['long']]).add_to(my_map)

    # Affichage de la carte dans Streamlit
    folium_static(my_map)
else:
    st.warning("Aucune donnée disponible pour afficher la carte.")


import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.header("Types d'Accidents")

# Slider interactif pour la gravité
selected_gravity = st.slider('Sélectionner la gravité', min_value=1, max_value=4, value=1)

# Création du diagramme à barres avec filtrage par gravité
filtered_data = df[df['grav'] == selected_gravity]
accident_types = filtered_data['agg'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=accident_types.index, y=accident_types.values, ax=ax)
ax.set_xlabel('Type d\'accident')
ax.set_ylabel('Nombre d\'accidents')
st.pyplot(fig)


st.write("### Nombre d'accidents par jour de la semaine")
accidents_by_day = df['jour'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
sns.barplot(x=accidents_by_day.index, y=accidents_by_day.values)
plt.xlabel('Jour de la semaine')
plt.ylabel('Nombre d\'accidents')
st.pyplot()


st.write("### Répartition des accidents par sexe")
accidents_by_sex = df['sexe'].value_counts()
plt.figure(figsize=(8, 5))
plt.pie(accidents_by_sex, labels=['Hommes', 'Femmes'], autopct='%1.1f%%', startangle=140)
plt.axis('equal')
st.pyplot()


st.write("### Répartition des accidents par condition atmosphérique")
accidents_by_weather = df['atm'].value_counts()
plt.figure(figsize=(10, 6))
sns.barplot(x=accidents_by_weather.index, y=accidents_by_weather.values)
plt.xlabel('Condition atmosphérique')
plt.ylabel('Nombre d\'accidents')
st.pyplot()


# Mapping des codes ATM aux descriptions
atm_mapping = {
    -1: "Non renseigné",
    1: "Normale",
    2: "Pluie légère",
    3: "Pluie forte",
    4: "Neige - grêle",
    5: "Brouillard - fumée",
    6: "Vent fort - tempête",
    7: "Temps éblouissant",
    8: "Temps couvert",
    9: "Autre"
}

# Ajout d'une colonne 'atm_description' au DataFrame
df['atm_description'] = df['atm'].map(atm_mapping)


from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Concaténation des descriptions ATM en une seule chaîne
text = ' '.join(df['atm_description'].dropna())

# Création du WordCloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Affichage du WordCloud
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('WordCloud des Conditions Atmosphériques')
st.pyplot()
