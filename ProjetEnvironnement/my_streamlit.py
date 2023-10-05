import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

# On definit une fonction get_data()  qui envoie une requête GET à l'API FastAPI a l'adresse 
# http://localhost:8000/api/data pour récupérer les données environnementales. 
 #On peut également traiter  les erreurs potentielles.

def get_data():
    try:
        response = requests.get("http://localhost:8000/api/data")
        data = response.json()
        return data
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de la récupération des données : {e}")
        return []


# Cette fonction prend en entrée une région et envoie une requête GET à l'API FastAPI 
# avec la région spécifiée dans l'URL pour récupérer les données environnementales spécifiques à cette région.
# Elle renvoie les données sous forme de liste de dictionnaires si la requête est réussie, sinon une liste vide


def get_data_by_region(region):
    try:
        response = requests.get(f"http://localhost:8000/api/data/{region}")
        data = response.json()
        return data
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de la récupération des données : {e}")
        return []



# On définit ici une fonction get_unique_regions(data)
# qui prend en entrée les données environnementales et 
# renvoie une liste triée des régions uniques contenues dans les données.

def get_unique_regions(data):
    regions = set()
    for item in data:
        if "Region" in item:
            regions.add(item["Region"])
    return sorted(list(regions))

# Page d'accueil de l'application Streamlit
def main():
    st.title("Visualisation de données environnementales")
    # Récupérer les données depuis l'API 
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

    else:
        st.warning("Aucune donnée n'a été récupérée.")

    #liste unique de toutes les régions
    regions = get_unique_regions(data)

    # Dans Streamlit, on ajouteé un menu déroulant pour sélectionner la région
    region_input = st.selectbox("Sélectionnez une région :", regions)

    if region_input:
        region_data = get_data_by_region(region_input)
        
        if region_data:
            for item in region_data:
                if isinstance(item, dict):  # Vérification de  si l'élément est un dictionnaire ou non
                    for key, value in item.items():
                        if value == 'n.a.':
                            item[key] = float('nan')
            # DataFrame pandas créé à partir des données
            df_region = pd.DataFrame(region_data)
            st.write("Données pour la région :", region_input)
            st.write(df_region)
        else:
            st.warning("Aucune donnée n'a été récupérée pour cette région.")

if __name__ == "__main__":
    main()
