# Importation des modules nécessaires
import streamlit as st
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import streamlit_antd_components as sac
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument('--headless')

import pandas as pd
import undetected_chromedriver as uc
import time
import function

#from selenium.webdriver import FirefoxOptions
#opts = FirefoxOptions()
#opts.add_argument("--headless")
#opts.add_argument("--disable-notifications")
#opts.add_argument("--disable-popup-blocking")
driver =webdriver.Firefox(options=opts,service=service)#driver_executable_path="./chromedriver.exe",

@st.cache_resource
def get_driver():
    return webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=chrome_options)

st.set_page_config(page_title="SmartSMS",layout="wide", initial_sidebar_state="auto", page_icon="logo_SmartSMS.png")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#service = Service(GeckoDriverManager().install())




st.header("SMARTSMS: PERSONNALISEZ ET ENVOYEZ DES SMS EN MASSE FACILEMENT")
function.load_styles()
segment =sac.segmented(
    items=[
        sac.SegmentedItem(label='SmartSMS'),
        sac.SegmentedItem(label="Guide d\'utilisation"),
        sac.SegmentedItem(label='Contactez-nous'),
    ], format_func='title', align='center'
)

if segment=="SmartSMS":

    z1, z2 = st.columns((11,4))
    with z1:
        st.title(":blue[Choisissez votre fichier de contacts :]")
    with z2:
        contacts = st.file_uploader("", type=["xls", "xlsx"])

    col1=col2=col3=col4=COL1=COL2=COL3=COL4=sim=""
    if contacts is not None:
        #read upload file and creer list from columns
        df = pd.read_excel(contacts)
        columns = set(df.columns)

        b1, b2,b3 = st.columns(3)
        with b1:
            numero = st.selectbox('Sélectionner la colonne des numéros de téléphone:',columns,index=None)
        with b2:
            une_puce = st.selectbox("J'ai uniquement une SIM dans mon smartphone:",["OUI","NON"],index=None)
        if une_puce=="NON":
            with b3:
                sim = st.selectbox('Veuillez sélectionner la carte SIM à utiliser:',["SIM 1","SIM 2"],index=None)

        a1, a2, a3, a4 = st.columns(4)
        #on crée plusieurs colonnes pour 
        with a1:
            col1 = st.selectbox('1ère info personnelle:',columns,index=None)

        with a2:
            if col1 is not None and col1 != '':
                col2 = st.selectbox('2nd info personnelle:',columns,index=None)

        with a3:
            if col2 is not None and col2 != '':
                col3 = st.selectbox('3eme info personnelle:',columns,index=None)

        with a4:
            if col3 is not None and col3 != '':
                col4 = st.selectbox('4eme info personnelle:',columns,index=None)

        #msg texte
        msg = st.text_area('Entrez votre message')
        validate_msg =st.button("Envoyez les messages")
        messages = []

        if validate_msg:
            #verification de la colonne numero
            if numero not in columns:
                st.warning("Erreur : Veuillez sélectionner la colonne contenant les contacts avant de continuer. Assurez-vous de sélectionner la bonne colonne pour garantir une saisie correcte des informations.", icon="⚠️")

            elif function.verifier_numeros_telephone(df,numero)!=True:
                error = function.verifier_numeros_telephone(df,numero)
                st.warning(f"{error}.", icon="⚠️")

            elif une_puce not in ["OUI","NON"]:
                st.warning("Erreur : Aucune option sélectionnée. Veuillez nous informer si vous avez uniquement une carte SIM ou non.", icon="⚠️")
            elif (une_puce == "NON") and (sim not in ["SIM 1","SIM 2"]):
                st.warning("Erreur : Aucune carte SIM sélectionnée. Veuillez choisir une carte SIM et réessayer. Assurez-vous de sélectionner la carte SIM que vous souhaitez utiliser pour l'envoi des SMS.", icon="⚠️")
             
            elif len(msg)==0:
                st.warning("Erreur : Aucun message saisi. Veuillez écrire votre message avant de réessayer", icon="⚠️")

            else:
                sim_number = function.return_sim_number(sim)
                NUMEROS = df[numero]
                resultat = function.corriger_msg(msg, col1, col2, col3, col4)
                msg_corrige = resultat[0]

                if len(resultat[1])==0:
                    message = msg_corrige.replace('{}','')
                    for i in range(len(df)):
                        messages.append(message)

                if len(resultat[1])==1:
                    for i in range(len(df)):
                        COL1 = df.loc[i,col1]
                        message = msg_corrige.format(COL1)
                        messages.append(message)

                if len(resultat[1])==2:
                    for i in range(len(df)):
                        COL1, COL2 = df.loc[i,col1], df.loc[i,col2]
                        message = msg_corrige.format(*[COL1, COL2])
                        messages.append(message)

                if len(resultat[1])==3:
                    for i in range(len(df)):
                        COL1, COL2,COL3 = df.loc[i,col1], df.loc[i,col2], df.loc[i,col3]
                        message = msg_corrige.format(*[COL1, COL2, COL3])
                        messages.append(message)

                if len(resultat[1])==4:
                    for i in range(len(df)):
                        COL1, COL2,COL3, COL4 = df.loc[i,col1], df.loc[i,col2], df.loc[i,col3], df.loc[i,col4]
                        message = msg_corrige.format(*[COL1, COL2, COL3, COL4])
                        messages.append(message)

                #lancement du navigateur
                driver =get_driver()
                #driver =uc.Chrome(options=chrome_options)
                #driver =webdriver.Firefox(options=opts,service=service)#driver_executable_path="./chromedriver.exe",
                driver.set_window_size(650,750)
                driver.get("https://messages.google.com/web/authentication")

                #attendre que le qrcode soit disponble
                wait_element = WebDriverWait(driver, 120)
                wait_element.until(EC.presence_of_element_located((By.XPATH, '//mw-qr-code/img')))

                image_placeholder = st.empty()
                texte_placeholder = st.empty()

                #recuperation et affichage du code QR de manière actualise en standant le scan
                try:
                    while True:
                        # Récupération du QR code
                        qrcode = driver.find_element(By.XPATH, '//mw-qr-code/img')
                        lien_image = qrcode.get_attribute('src')

                        texte_placeholder.write(
                            """
                            ### :black[SCANNER LE QR CODE]
                            """
                            )
                        # Afficher l'image dans Streamlit
                        image_placeholder.image(lien_image, width=50, use_column_width='auto')

                        # Attendre 2 secondes avant de mettre à jour le QR code
                        time.sleep(2)

                #une fois le code QR scanné
                except:
                    with image_placeholder:
                        st.write('')
                    with texte_placeholder:
                        st.write('')

                time.sleep(2)
                # Boucle à travers les contacts
                for i in range(len(df)):
                    # Clique sur le bouton pour commencer une nouvelle conversation
                    try:
                        new_conversation = wait_element.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Démarrer")))
                    except:
                        new_conversation = wait_element.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Start")))
                    new_conversation.click()

                   # Saisie du numéro de téléphone
                    wait_element.until(EC.presence_of_element_located((By.CLASS_NAME, "input")))
                    zone_number = driver.find_element(By.CLASS_NAME, "input")
                    zone_number.send_keys(str(NUMEROS[i]))

                    # Confirme le numéro de téléphone
                    wait_element.until(EC.presence_of_element_located((By.CLASS_NAME, "button")))
                    confirm_number = driver.find_element(By.CLASS_NAME, "button")
                    confirm_number.click()

                    if une_puce == "NON":
                        # Clique sur le bouton de changement de carte SIM
                        change_sim_button = wait_element.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sim-info-picker-button')))
                        change_sim_button.click()

                        #on recuperer le cadrant contenant les sim dans le but d'extraire les noms des sims
                        cadrant_sim = wait_element.until(EC.presence_of_element_located((By.XPATH ,'//div[@role="menu"]')))
                        
                        #on selectionne la bonne sim
                        wait_sim = WebDriverWait(cadrant_sim, 120)
                        wait_sim.until(EC.presence_of_element_located((By.TAG_NAME,'button')))
                        good_sim =cadrant_sim.find_elements(By.TAG_NAME,'button')[sim_number]
                        good_sim.click()

                    # Saisie du message dans la zone de texte
                    zone_text = wait_element.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
                    zone_text.send_keys(messages[i])

                    # Envoi du SMS
                    send_sms = wait_element.until(EC.element_to_be_clickable((By.CLASS_NAME, 'inline-send-button')))
                    time.sleep(1)
                    send_sms.click()

                driver.quit()
                st.success("Vos messages ont été envoyées avec succès", icon="✅")



    else:
        st.info("Bienvenue dans notre application SmartSMS ! Vous pouvez envoyer des SMS personnalisés en masse. Avant de commencer, veuillez charger un fichier de contacts.", icon="ℹ️")

if segment=="Guide d\'utilisation":
    st.title(":blue[:one:. Choisissez votre fichier de contacts]")
    st.info(":file_folder: Sur la première page de l'application, vous serez invité à télécharger votre fichier de contacts au format Excel (xlsx ou xls). Assurez-vous que votre fichier contient une colonne de numéros de téléphone aux formats suivants: '+225 XX XX XX XX XX', '225 XX XX XX XX XX' ou 'XX XX XX XX XX'.")

    st.title(":blue[:two:. Configuration des informations de bases]")
    st.info(":wrench: Après avoir téléchargé votre fichier de contacts, vous devrez spécifier les informations obligatoires pour faire fonctionner le programme. Sélectionnez les colonnes correspondantes pour le numéro de téléphone et la carte SIM à utiliser.")

    st.title(":blue[:three:. Configuration des informations personnelles]")
    st.info(":wrench: Après avoir téléchargé votre fichier de contacts, vous devrez spécifier les informations personnelles à inclure dans vos messages. Sélectionnez les colonnes correspondantes, comme par exemple le nom et prénoms.")

    st.title(":blue[:four:. Rédigez votre message]")
    st.info(":memo: Utilisez la zone de texte prévue pour saisir le message que vous souhaitez envoyer. Vous devez utiliser le caractère de substitution '@' pour personnaliser votre message avec les informations de chaque contact. le caractere @ est utilisé a chaque fois qu'on souhaite inclures des informations personnelles, par exemple si on veut avoir le resultat suivant: 'Bonjour monsieur Amany votre matricule est XX001' on devra saisir le texte 'Bonjour monsieur @ votre matricule est @', avec pour colonne selectionnées dans l'odre 'NOM ET PRENOMS' ET 'MATRICULE'")
    st.title(":blue[:five:. Vérifications avant l'envoi]")
    st.info("✅ Avant d'appuyer sur le bouton 'Envoyez les messages', assurez-vous que toutes les étapes précédentes sont correctement configurées. Vérifiez que le numéro de téléphone, la carte SIM, et le message sont corrects.")

    st.title(":blue[:six:. Scannez le code QR]")
    st.info(":old_key: Une fois que vous avez confirmé les détails, cliquez sur le bouton 'Envoyez les messages'. Cela ouvrira une fenêtre avec un code QR que vous devrez scanner à l'aide de l'application Messages de Google sur votre téléphone.")

    st.title(":blue[:seven:. Envoi des SMS]")
    st.info(":arrow_up: Après avoir scanné le code QR, l'application commencera à envoyer les SMS automatiquement. Assurez-vous que votre navigateur reste ouvert pendant tout le processus d'envoi.")

    st.title(":blue[:seven:. Fin de l'opération]")
    st.info(":end: Une fois que tous les messages ont été envoyés avec succès, l'application affichera un message de réussite. Vous pouvez maintenant fermer l'application.")



footer="""<style>
    a:link , a:visited{
    color: blue;
    background-color: transparent;
    text-decoration: underline;
    }

    a:hover,  a:active {
    color: red;
    background-color: transparent;
    text-decoration: underline;
    }

    .footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: transparent;
    color: black;
    text-align: center;
    }
</style>
<div class="footer">
    <p>Developed by <a style='display: block; text-align: center;' href="https://www.linkedin.com/in/nsi%C3%A9ni-kouadio-eli%C3%A9zer-amany-613681185" target="_blank">Nsiéni Amany Kouadio</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)