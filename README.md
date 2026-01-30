🎓 Système Intelligent de Suivi des Paiements & Analyse de Risque

Une solution complète de gestion de scolarité (ERP) capable de gérer le cycle de vie étudiant, d'automatiser la comptabilité et de détecter proactivement les risques d'impayés grâce à un moteur PL/SQL puissant.

🚀 Fonctionnalités Clés

1. Gestion Administrative Avancée

Structure Académique : Gestion hiérarchique (Départements ➝ Filières ➝ Étudiants).

Inscription Intelligente : Formulaire dynamique avec filtrage automatique des filières par département.

Transaction Atomique : Création simultanée de l'étudiant et de son échéancier financier (garantie d'intégrité).

2. Automatisation Financière (PL/SQL)

Suivi Temps Réel : Mise à jour automatique des statuts des factures (PENDING → PARTIAL → PAID) via des Triggers Composés.

Sécurité Comptable : L'agent de saisie n'a aucun accès manuel aux statuts, éliminant les erreurs humaines.

Reçus PDF : Génération automatique de reçus de paiement téléchargeables.

3. Intelligence Artificielle & Risques

Batch Nocturne : Un job planifié (Oracle Scheduler) scanne la base chaque nuit pour détecter les retards.

Alerting : Génération automatique d'alertes de risque dans une table d'audit.

Score de Risque : Classification automatique des étudiants (CRITICAL / MEDIUM / LOW).

4. Business Intelligence (Dashboard)

KPI Financiers : Taux de recouvrement, dette globale, projections de rentrées.

Visualisation : Graphiques interactifs par département et par statut.

Dossier 360° : Vue complète de l'historique d'un étudiant (Paiements, Factures, Alertes).

🛠️ Architecture Technique

Ce projet repose sur une architecture conteneurisée moderne :

Composant

Technologie

Rôle

Database

Oracle 19c (Enterprise)

Hébergement des données, PL/SQL, Jobs

Conteneur

Docker

Virtualisation et isolation de l'environnement

Backend Logic

PL/SQL

Triggers, Procédures Stockées, Vues Matérialisées

Frontend

Python (Streamlit)

Interface Utilisateur, Graphiques, Génération PDF

Driver

python-oracledb

Connectivité optimisée (Mode Thin UTF-8)

📦 Installation & Démarrage

1. Prérequis

Docker Desktop ou Engine installé.

Python 3.8+ installé.

2. Démarrer le Serveur de Base de Données

docker run -d -p 1521:1521 --name oracle19c -e ORACLE_PWD=password123 doctorkirk/oracle-19c


3. Initialiser la Base de Données

Connectez-vous (via SQL*Plus ou DBeaver) et exécutez le script d'initialisation complet :

@database/setup_database.sql


(Ce script crée les tables, triggers, procédures, jobs et insère les données de référence).

4. Lancer l'Application Web

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur Streamlit
streamlit run app/app.py


📍 Accès : L'application sera disponible sur http://localhost:8501.

📂 Structure du Projet

Projet_Oracle_Paiement/
├── app/
│   ├── app.py              # Application Streamlit (Interface Principale)
│   └── fix_data.py         # Script utilitaire de correction d'encodage
├── database/
│   └── setup_database.sql  # Script SQL Master (DDL + PL/SQL + Data)
├── docs/
│   └── Rapport_Projet.pdf  # Documentation technique et fonctionnelle
├── requirements.txt        # Liste des dépendances Python
└── README.md               # Documentation du dépôt


👥 Auteurs

Ce projet a été réalisé dans le cadre du Master IA (Université Sultan Moulay Slimane).

Adil CHAGRI (@Adilchagri)

Jbel CHOUAIB

Encadrant : M. Youness KHOURDIFI

"L'automatisation est la clé de la fiabilité financière."
