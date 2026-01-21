🎓 Système Intelligent de Suivi des Paiements & Analyse de Risque

Une solution complète de gestion de scolarité capable de détecter automatiquement les étudiants en situation d'impayé grâce à des procédures stockées Oracle et une interface moderne en Python.

🚀 Fonctionnalités Clés

Gestion des Étudiants : Inscription avec génération automatique de facture (Transaction Atomique).

Suivi des Paiements : Mise à jour automatique des soldes via Triggers PL/SQL (détection Paiement Partiel vs Total).

Détection des Risques : Batch de nuit (Oracle Scheduler) pour identifier les retards et générer des alertes.

Dashboard Décisionnel : Interface Web interactive pour visualiser les KPI financiers en temps réel.

🛠️ Architecture Technique

Ce projet repose sur une architecture conteneurisée :

Composant

Technologie

Rôle

Database

Oracle 19c (Docker)

Stockage, Triggers, Procédures stockées

Backend Logic

PL/SQL

Automatisation métier (Business Logic)

Frontend

Python (Streamlit)

Interface utilisateur et Dashboards

Driver

python-oracledb

Connectivité (Thin Client)

📦 Installation & Démarrage

1. Prérequis

Docker Desktop ou Engine

Python 3.8+

2. Démarrer la Base de Données

docker run -d -p 1521:1521 --name oracle19c -e ORACLE_PWD=password123 doctorkirk/oracle-19c


3. Initialiser les Tables

Connectez-vous à la base (via SQL*Plus ou DBeaver) et exécutez le script situé dans database/setup_database.sql.

4. Lancer l'Application

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
streamlit run app/app.py


L'application sera accessible sur http://localhost:8501.

📂 Structure du Projet

Projet_Oracle_Paiement/
├── app/
│   └── app.py              # Interface Streamlit
├── database/
│   └── setup_database.sql  # Script SQL complet (DDL + PL/SQL)
├── docs/
│   └── Rapport_Projet.pdf  # Documentation technique
├── requirements.txt        # Dépendances Python
└── README.md               # Documentation du dépôt


👥 Auteurs

Ce projet a été réalisé dans le cadre du Master IA (Université Sultan Moulay Slimane).

Adil CHAGRI (@Adilchagri)

Jbel CHOUAIB

Encadrant : M. Youness KHOURDIFI
