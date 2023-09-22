#Import des bibliotheques nécessaires 
import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

#On definit une fonction get_data()  qui envoie une requête GET à l'API FastAPI 
#pour récupérer les données environnementales. On peut également traiter  les erreurs potentielles.

def get_data():
    try:
        # Remplacez l'adresse IP ci-dessous par l'adresse IP de votre machine hôte
        response = requests.get("http://localhost:8000/api/data")
        data = response.json()
        return data
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de la récupération des données : {e}")
        return []

#On définit une fonction get_unique_regions(data)
#qui prend en entrée les données environnementales et renvoie une liste triée des régions uniques contenues dans les données.

def get_data_by_region(region):
    try:
        # Remplacez l'adresse IP ci-dessous par l'adresse IP de votre machine hôte
        response = requests.get(f"http://localhost:8000/api/data/{region}")
        data = response.json()
        return data
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de la récupération des données : {e}")
        return []

# Fonction pour récupérer la liste unique de toutes les régions depuis les données
def get_unique_regions(data):
    regions = set()
    for item in data:
        if "Region" in item:
            regions.add(item["Region"])
    return sorted(list(regions))

# Page d'accueil de l'application Streamlit
def main():
    st.title("Visualisation de données environnementales")
    # Récupérer les données depuis l'API Flask
    data = get_data()
    if data:
        # Convertir les données en DataFrame pandas
        df = pd.DataFrame(data)
        # Afficher un aperçu des données
        st.write("Aperçu des données :")
        st.write(df)
        # Afficher un graphique à barres pour les émissions de CO2 par année
        st.subheader("Émissions de CO2 par année")
        fig, ax = plt.subplots()
        df_grouped = df.groupby("Year")["CO2 emissions from fuel combustion (MtCO2)"].sum()
        ax.bar(df_grouped.index, df_grouped.values)
        plt.xlabel("Année")
        plt.ylabel("Émissions de CO2 (MtCO2)")
        st.pyplot(fig)
        # Ajoutez d'autres graphiques selon vos besoins
    else:
        st.warning("Aucune donnée n'a été récupérée.")

    # Obtenez la liste unique de toutes les régions
    regions = get_unique_regions(data)

    # Dans votre application Streamlit, vous pouvez ajouter un menu déroulant pour sélectionner la région
    region_input = st.selectbox("Sélectionnez une région :", regions)

    if region_input:
        region_data = get_data_by_region(region_input)
        
        if region_data:
            # Remplacez 'n.a.' par NaN dans les données JSON
            for item in region_data:
                if isinstance(item, dict):  # Vérifiez si l'élément est un dictionnaire
                    for key, value in item.items():
                        if value == 'n.a.':
                            item[key] = float('nan')
            # Créez un DataFrame pandas à partir des données
            df_region = pd.DataFrame(region_data)
            st.write("Données pour la région :", region_input)
            st.write(df_region)
        else:
            st.warning("Aucune donnée n'a été récupérée pour cette région.")

if __name__ == "__main__":
    main()
