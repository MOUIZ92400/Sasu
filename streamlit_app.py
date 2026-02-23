import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- 1. TES ACCÈS GOOGLE (À remplir avec tes clés) ---
INFO = {
  "type": "service_account",
  "project_id": "TON_PROJECT_ID",
  "private_key_id": "TON_KEY_ID",
  "private_key": "-----BEGIN PRIVATE KEY-----\nTON_CODE_SECRET\n-----END PRIVATE KEY-----\n",
  "client_email": "TON_EMAIL_SERVICE_ACCOUNT",
  "client_id": "TON_CLIENT_ID",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "TON_CERT_URL"
}

# Connexion sécurisée
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(INFO, scopes=SCOPE)
client = gspread.authorize(creds)

# --- 2. L'INTERFACE ---
st.title("📊 ERP SASU Connecté")

with st.form("ajout_stock"):
    produit = st.text_input("Nom du produit")
    qte = st.number_input("Quantité", min_value=1)
    prix = st.number_input("Prix (€)", min_value=0.0)
    
    if st.form_submit_button("🚀 Enregistrer"):
        try:
            # Ouvrir le fichier Sheets
            sheet = client.open("ERP_SASU_Data").sheet1
            # Ajouter la ligne
            sheet.append_row([str(datetime.now()), produit, qte, prix])
            st.success(f"Bravo Monsieur le Président ! {produit} est dans le tableau.")
        except Exception as e:
            st.error(f"Erreur : {e}")
            
