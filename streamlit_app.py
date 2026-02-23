import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- CONFIGURATION GOOGLE SHEETS (TES CLÉS) ---
INFO = {
  "type": "service_account",
  "project_id": "erp-sasu",
  "private_key_id": "8a2d387163fe21237b1989385d37844f019e475d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDWoyzzn7Kib8qt\np75ZxcpwTLnvG9tcpHuNVxKwOSxfpfkBEWHlURxOkn5KP+thCHtJVCjA669+4R9Y\nSdHA0wZ2bTkB6Xk7ve2EyZLWtgEvS4UhZ7DRDNLEykzItBKcgV4CQy8SGKvgBeos\nJ3tI3OqpK8v2upfSIaODGk0vxn20qUf/HRE7hjk3/smfbkcB3Nz7srkBan9PFm8N\nCbWrXPT/JXItMH1OUkxFUWUc7Dlcv/dlooameiZHD5GV0NOqB+WEGyMGfTV0bYZ9\ndz3vQUw0WFsgoX7ZX1qhuQveaYtVG3bAIZt+6Ko/ka+PMM8zaJl8AsHs6H96/DwX\neK12/JGXAgMBAAECggEAFRzW6p3uVeEWOC+0XyNADvzVG0qLsNizGIuUmIX/Medj\nD3JUxVhNpwLs7kPMVO6fJe7j1Vo5mIrvaOFWAxge3h5PSbtcA/7iMrobOgiMJElS\n7p7C+0U+JEJb/DAOVpu5EhLmuep4WaBrUO2PSHMGmB5pQTtIfNB3Q4meRxFIwzDn\neO8Eb5x4w6CYG3Nyn39nbTCC5Oy4NgA96PMytSPuLjOO/Z6+RPAh6swq1+ZxM1fg\nQhQOA7nKQk7ft9+MfxFMxXwX27gvr1JQR5kp+9H/fifZWMcRiQa1IgQ4UUOlYgKW\nU9jigadUTaalemmx44cTrvvjA3uCyebVz+N6TuFSpQKBgQDrU1MU3M5zEfvrM+6Q\nhZvA5Pg2PMJfFkILiJEcOq83iGXXN+wsmIeNjTUOx2UWj+bPv2/mlcrG4iW1GiJt\nvvHc9FGzhgWysE2Goq9V4JjUjB+cqL1xmpqHKaShHQdflJKYh1eqBfxRgFl9Tkud\n7NP90azHESb/b2GDMAqlMJL/5QKBgQDpfo7cUVa5YJdcTbF35vpTuIkRE6h/a+aF\nQ7yywzu8Tpc2C0wkkEnT1B+v8LqUAZoWyyMI6YR3CdmPBB6HVLTx/ocVe71JpA7c\IzyYaqFtEWJIOO6A124R7SKZwSqg6iIzU3yC/lcnAlV6d2mJ8U0tuMSn6AaWXdyd\nb0Vwe8ybywKBgGp9fXZOaZpHBCIukQGThKUouG4K1sai0uZXOZt1rv7JWZSn+NdB\neu4CfYUflE4+dmuCrQfCt02C3x9yISxaoSak5SgBOSjggWSwz/ljtqVQd6mz7m6v\nUMhjft1tvn1xRVmCvZfyN3lGRLjgqnVfy5rrvG0lBOnIpG7yWY7hSVRFAoGAGjJ5\n4tw5Z7kfolqRM8u1gFku/7x95jX7+i28aS4gcKM8sfKYi22o6txc5ceTl3GKkU4f\nUyuoEhcH0tT6e+KUHqaZD17/wNhoVmiZrtwf2nXd2g6RK+F/1wENJcUXfFBon+uZ\nB7Vzn8vSPVhSfgiVyTB22APfYVWMoBlQ6CrrrPsCgYAnmpEeR3u31ZUwe4hN0ThN\nq3/P8LOv+Fsb/pJAldF82wd5f82sFlEuL20y6wd7O5vP9NoXwsd2q+IRWuzoxPuF\n1552gjvkOSUXhtVBjLlJJUWH5DMZP1ixXolszGIK8ei8o/9WDIjBYdgnnQlY4qqb\nppih4bv0jh+Bnx1+wslTlw==\n-----END PRIVATE KEY-----\n",
  "client_email": "admin-sasu@erp-sasu.iam.gserviceaccount.com",
  "client_id": "104273062907143733809",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/admin-sasu%40erp-sasu.iam.gserviceaccount.com"
}

# Connexion sécurisée
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(INFO, scopes=SCOPE)
client = gspread.authorize(creds)

# --- INTERFACE ---
st.set_page_config(page_title="ERP SASU", layout="centered")
st.title("📊 ERP SASU Connecté")

menu = st.sidebar.selectbox("Menu", ["Stock", "Ventes"])

if menu == "Stock":
    st.subheader("📦 Ajouter au Stock")
    with st.form("form_stock"):
        produit = st.text_input("Nom du produit")
        qte = st.number_input("Quantité", min_value=1)
        prix = st.number_input("Prix Achat (€)", min_value=0.0)
        
        if st.form_submit_button("🚀 Enregistrer dans le Cloud"):
            try:
                # Ouvre le fichier Sheets (ASSURE-TOI DE L'AVOIR CRÉÉ ET PARTAGÉ !)
                sheet = client.open("ERP_SASU_Data").sheet1
                date_now = datetime.now().strftime("%d/%m/%Y %H:%M")
                sheet.append_row([date_now, produit, qte, prix])
                st.success(f"✅ {produit} enregistré dans Google Sheets !")
            except Exception as e:
                st.error(f"Erreur de connexion : {e}")
                st.info("Vérifie que ton fichier Google Sheets s'appelle 'ERP_SASU_Data' et qu'il est partagé avec : admin-sasu@erp-sasu.iam.gserviceaccount.com")

elif menu == "Ventes":
    st.subheader("💰 Suivi des Ventes")
    st.write("Espace en cours de développement.")
