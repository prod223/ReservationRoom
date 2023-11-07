# Importe le module firebase_admin nécessaire pour l'initialisation de Firebase
import firebase_admin

from firebase_admin import credentials

import pyrebase

from configs.firebase_config import firebase_config

if not firebase_admin._apps:

    # Charge les informations d'authentification
    cred = credentials.Certificate("configs/key_config.json")

    # Initialise l'application Firebase 
    firebase_admin.initialize_app(cred)

# Initialise l'application Firebase
firebase = pyrebase.initialize_app(firebase_config)

# Crée une instance de la base de données Firebase
db = firebase.database()
authStudent = firebase.auth()
