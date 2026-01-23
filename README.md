<div align="center">

# 🎓 Système Intelligent de Suivi des Paiements

### Gestion Automatisée des Paiements Universitaires avec Analyse de Risque

[![Oracle](https://img.shields.io/badge/Oracle-19c-F80000?style=for-the-badge&logo=oracle&logoColor=white)](https://www.oracle.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Latest-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

[📖 Documentation](#-fonctionnalités) • [🚀 Installation](#-installation) • [💻 Utilisation](#-utilisation) • [📊 Captures d'écran](#-captures-décran)

</div>

---

## 📋 Table des Matières

- [À Propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Technologies](#-technologies)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du Projet](#-structure-du-projet)
- [Captures d'Écran](#-captures-décran)
- [Auteurs](#-auteurs)
- [Licence](#-licence)

---

## 🎯 À Propos

Ce projet vise à **informatiser et automatiser** le processus de gestion des paiements de scolarité dans un établissement d'enseignement supérieur. Il remplace les systèmes manuels disparates (Excel) par une solution **centralisée, automatisée et intelligente**.

### 🎓 Contexte Académique

Projet réalisé dans le cadre du **Master Intelligence Artificielle** à l'Université Sultan Moulay Slimane - Faculté des Sciences et Techniques.

### 🔑 Problématique Résolue

Le suivi manuel via tableurs entraîne :
- ❌ Erreurs de saisie
- ❌ Redondance des données
- ❌ Difficulté à consolider les chiffres
- ❌ Incapacité à détecter les retards en temps réel

Notre solution apporte :
- ✅ Centralisation des données
- ✅ Automatisation des calculs
- ✅ Détection proactive des risques
- ✅ Aide à la décision en temps réel

---

## ✨ Fonctionnalités

### 🏦 Gestion des Paiements

- **Inscription Étudiants** : Enregistrement des nouveaux étudiants avec génération automatique de leur échéancier
- **Facturation Automatique** : Création de factures avec contraintes d'intégrité strictes
- **Paiements Partiels** : Support natif des versements échelonnés
- **Mise à Jour Automatique** : Les statuts de paiement sont calculés par triggers PL/SQL

### 📊 Dashboard Analytique

- **KPI en Temps Réel** :
  - Nombre total d'étudiants
  - Étudiants à risque
  - Dette totale de l'établissement
  
- **Classification des Risques** :
  - 🔴 **CRITICAL** : Plus de 2 alertes de retard
  - 🟡 **MEDIUM** : 1 retard détecté
  - 🟢 **LOW** : Paiements à jour

### 🤖 Analyse Automatisée

- **Batch Processing Nocturne** : Analyse quotidienne des retards de paiement
- **Génération d'Alertes** : Notifications automatiques pour les impayés
- **Mise à Jour des Statuts** : Marquage automatique des factures en retard

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Streamlit)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Dashboard   │  │ Inscription  │  │  Paiements   │  │
│  │   Risques    │  │  Étudiant    │  │    Caisse    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │ Python-OracleDB (Thin Client)
                         ▼
┌─────────────────────────────────────────────────────────┐
│              BACKEND (Oracle Database 19c)               │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Tables Principales                   │  │
│  │  • STUDENTS      • INSTALLMENTS                   │  │
│  │  • PAYMENTS      • RISK_ALERTS                    │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │           Logique Métier (PL/SQL)                 │  │
│  │  • Triggers automatiques                          │  │
│  │  • Procédures stockées                            │  │
│  │  • Contraintes d'intégrité                        │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         ▲
                         │ Conteneurisé avec Docker
                         ▼
┌─────────────────────────────────────────────────────────┐
│            INFRASTRUCTURE (Ubuntu 22.04 LTS)             │
│                    VMware + Docker                       │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technologies

### Backend
- **SGBD** : Oracle Database 19c Enterprise Edition
- **Langage** : PL/SQL pour la logique métier
- **Outils** : DBeaver, SQL*Plus

### Frontend
- **Langage** : Python 3.10+
- **Framework** : Streamlit
- **Connecteur** : python-oracledb (Thin Client)
- **Visualisation** : Pandas, Plotly (optionnel)

### Infrastructure
- **OS** : Ubuntu 22.04 LTS
- **Virtualisation** : VMware
- **Conteneurisation** : Docker
- **Orchestration** : Docker Compose (optionnel)

---

## 🚀 Installation

### Prérequis

- Docker & Docker Compose
- Python 3.10 ou supérieur
- Git

### Étape 1 : Cloner le Projet

```bash
git clone https://github.com/votre-username/payment-tracking-system.git
cd payment-tracking-system
```

### Étape 2 : Lancer Oracle Database

```bash
# Démarrer le conteneur Oracle
docker-compose up -d oracle

# Vérifier que la base de données est prête
docker logs -f oracle-db
```

### Étape 3 : Initialiser la Base de Données

```bash
# Se connecter au conteneur
docker exec -it oracle-db sqlplus sys/your_password@//localhost:1521/ORCLPDB1 as sysdba

# Exécuter les scripts DDL
@scripts/01_create_tables.sql
@scripts/02_create_triggers.sql
@scripts/03_create_procedures.sql
@scripts/04_insert_sample_data.sql
```

### Étape 4 : Installer les Dépendances Python

```bash
# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les packages
pip install -r requirements.txt
```

### Étape 5 : Configurer les Variables d'Environnement

```bash
# Créer un fichier .env
cp .env.example .env

# Éditer avec vos credentials
nano .env
```

**Contenu du `.env` :**
```env
ORACLE_USER=system
ORACLE_PASSWORD=your_password
ORACLE_DSN=localhost:1521/ORCLPDB1
```

### Étape 6 : Lancer l'Application

```bash
streamlit run app.py
```

L'application sera accessible sur **http://localhost:8501**

---

## 💻 Utilisation

### 1️⃣ Tableau de Bord des Risques

Accédez à la page d'accueil pour visualiser :
- Les KPI globaux
- La liste des étudiants à risque
- Le code couleur selon le niveau de risque

### 2️⃣ Inscription d'un Étudiant

1. Naviguer vers **"Inscription & Facturation"**
2. Remplir le formulaire avec les informations de l'étudiant
3. Définir le montant et la date d'échéance de la première facture
4. Valider → L'étudiant et sa facture sont créés automatiquement

### 3️⃣ Enregistrer un Paiement

1. Aller sur **"Saisir un Paiement"**
2. Sélectionner l'étudiant dans la liste déroulante
3. Saisir le montant versé
4. Valider → Le trigger met à jour automatiquement le statut

### 4️⃣ Lancer l'Analyse de Risque

Depuis le dashboard, cliquer sur **"Actualiser l'Analyse"** pour :
- Détecter les factures échues
- Générer des alertes
- Mettre à jour les statuts en OVERDUE

---

## 📁 Structure du Projet

```
payment-tracking-system/
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 docker-compose.yml
├── 📄 .env.example
├── 📂 app/
│   ├── 📄 app.py                 # Point d'entrée Streamlit
│   ├── 📂 pages/
│   │   ├── 📄 1_📊_Dashboard.py
│   │   ├── 📄 2_➕_Inscription.py
│   │   └── 📄 3_💰_Paiement.py
│   ├── 📂 database/
│   │   ├── 📄 connection.py
│   │   └── 📄 queries.py
│   └── 📂 utils/
│       ├── 📄 helpers.py
│       └── 📄 config.py
├── 📂 scripts/
│   ├── 📄 01_create_tables.sql
│   ├── 📄 02_create_triggers.sql
│   ├── 📄 03_create_procedures.sql
│   └── 📄 04_insert_sample_data.sql
├── 📂 docs/
│   ├── 📄 Rapport_Projet.pdf
│   └── 📄 Architecture.md
└── 📂 assets/
    └── 📂 images/
        ├── 📄 dashboard.png
        ├── 📄 inscription.png
        └── 📄 paiement.png
```

---

## 📊 Captures d'Écran

### Dashboard des Risques
![Dashboard](assets/images/dashboard.png)
*Vue d'ensemble des KPI et classification des risques par code couleur*

### Module d'Inscription
![Inscription](assets/images/inscription.png)
*Formulaire d'inscription avec génération automatique de facture*

### Module de Paiement
![Paiement](assets/images/paiement.png)
*Interface simplifiée pour les agents de caisse*

---

## 📚 Documentation Technique

### Modèle de Données (ERD)

```sql
STUDENTS (1,n) ──< INSTALLMENTS (1,n) ──< PAYMENTS
                         │
                         └──> RISK_ALERTS (0,n)
```

### Triggers Principaux

#### TRG_UPDATE_INSTALLMENT_STATUS
```sql
-- Se déclenche après chaque INSERT dans PAYMENTS
-- Calcule automatiquement le statut (PAID/PARTIAL)
-- Garantit la cohérence sans intervention humaine
```

### Procédures Stockées

#### PROC_DAILY_RISK_ANALYSIS
```sql
-- Exécution planifiée chaque nuit
-- Scanne les factures échues
-- Génère des alertes pour les impayés
-- Met à jour les statuts en OVERDUE
```

---

## 🔐 Sécurité

- ✅ Contraintes d'intégrité référentielle strictes
- ✅ Validation des données au niveau SGBD
- ✅ Transactions atomiques (COMMIT/ROLLBACK)
- ✅ Isolation des environnements via Docker
- ✅ Credentials stockés dans variables d'environnement

---

## 🚦 Tests

### Tests Unitaires (à venir)
```bash
pytest tests/
```

### Tests d'Intégration
```bash
# Vérifier la connexion à la base
python -m app.database.connection

# Tester les requêtes
python -m tests.test_queries
```

---

## 🗺️ Roadmap

### Version 1.0 (Actuelle)
- [x] CRUD Étudiants
- [x] Gestion des factures
- [x] Enregistrement des paiements
- [x] Dashboard des risques
- [x] Analyse batch nocturne

### Version 2.0 (Prévue)
- [ ] Module de gestion des bourses
- [ ] Interface parent (consultation des paiements)
- [ ] Notifications par email/SMS
- [ ] Exportation PDF des relevés
- [ ] Statistiques avancées (prédictions IA)
- [ ] API REST pour intégration externe

---

## 👥 Auteurs

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/adilchagri.png" width="100px;" alt="Adil CHAGRI"/><br />
      <sub><b>Adil CHAGRI</b></sub><br />
      <a href="https://github.com/adilchagri">GitHub</a>
    </td>
    <td align="center">
      <img src="https://github.com/choua1b.png" width="100px;" alt="Jbel CHOUAIB"/><br />
      <sub><b>Jbel CHOUAIB</b></sub><br />
      <a href="https://github.com/choua1b">GitHub</a>
    </td>
  </tr>
</table>

### 🎓 Encadrement
**M. Youness KHOURDIFI** - Professeur Encadrant

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- Université Sultan Moulay Slimane
- Faculté des Sciences et Techniques
- M. Youness KHOURDIFI pour son encadrement
- La communauté Oracle et Streamlit pour la documentation

---

## 📞 Contact

Pour toute question ou suggestion :

- 📧 Email : adil.chagri@example.com
- 💼 LinkedIn : [Adil CHAGRI](https://linkedin.com/in/adilchagri)
- 🐦 Twitter : [@adilchagri](https://twitter.com/adilchagri)

---

<div align="center">

**⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile ! ⭐**

Made with ❤️ by Adil CHAGRI & Jbel CHOUAIB

</div>
