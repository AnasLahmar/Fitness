# Importations (supprimer celles qui ne sont pas utilisées)
import sqlite3
import hashlib
import os
import pandas as pd
import streamlit as st
# Fonction pour créer une table utilisateur dans la base de données
class DatabaseManager:
    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()

# Fonction pour créer une table utilisateur dans la base de données
def create_tables():
    with DatabaseManager() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        ''')

# ... (le reste du code utilise également le gestionnaire de contexte)

# Création de la table des utilisateurs au démarrage de l'application
create_tables()

# Fonction pour ajouter un utilisateur à la base de données
def add_user(first_name, last_name, email, password):
    with DatabaseManager() as cursor:
        # Vérifier si l'e-mail existe déjà
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            st.warning("Cet e-mail est déjà enregistré. Veuillez utiliser un autre e-mail.")
            return

        # Hash du mot de passe avant de le stocker
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Insertion dans la base de données
        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, password_hash)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, email, password_hash))

        st.success("Inscription réussie!")

# Fonction pour obtenir l'ID de l'utilisateur par e-mail
def get_user_id(email):
    with DatabaseManager() as cursor:
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        user_id = cursor.fetchone()

    return user_id[0] if user_id else None


# Fonction pour obtenir le prénom de l'utilisateur par ID
def get_user_first_name(user_id):
    with DatabaseManager() as cursor:
        cursor.execute('SELECT first_name FROM users WHERE id = ?', (user_id,))
        first_name = cursor.fetchone()

    return first_name[0] if first_name else None


# Fonction pour récupérer tous les utilisateurs depuis la base de données
def get_all_users():
    with DatabaseManager() as cursor:
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()

    return users

def create_file(user_id):
    # Définir le chemin du fichier excel en fonction de l'identifiant utilisateur
    file_path = f"data/donnees_alimentaires_{user_id}.xlsx"

    # Vérifier si le fichier existe déjà
    if not os.path.exists(file_path):
        # Créer un DataFrame vide et le sauvegarder dans le fichier excel
        pd.DataFrame().to_excel(file_path, index=False)

