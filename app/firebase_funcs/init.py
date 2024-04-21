import firebase_admin
from firebase_admin import credentials, firestore


def initialize_app():
    cred = credentials.Certificate("./googleCreds.json")
    firebase_app = firebase_admin.initialize_app(cred)
    return firestore.client()


db = initialize_app()
