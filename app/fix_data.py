import oracledb

# Configuration de la connexion
# Le mode 'disable_oob=True' est crucial pour Docker/Linux
try:
    conn = oracledb.connect(
        user="projet_paiement",
        password="password123",
        dsn="localhost:1521/ORCLCDB",
        disable_oob=True
    )
    cursor = conn.cursor()
    print("✅ Connexion réussie.")

    # Liste des corrections SQL à appliquer pour réparer les '??'
    updates = [
        # Correction des Départements
        "UPDATE DEPARTMENTS SET dept_name = 'Département Mathématiques & Informatique' WHERE dept_id = 10",
        "UPDATE DEPARTMENTS SET dept_name = 'Département Économie & Gestion' WHERE dept_id = 20",
        "UPDATE DEPARTMENTS SET dept_name = 'Département Sciences Physiques' WHERE dept_id = 30",
        
        # Correction des Filières (Branches)
        "UPDATE BRANCHES SET branch_name = 'Licence 3 - Génie Logiciel' WHERE branch_id = 101",
        "UPDATE BRANCHES SET branch_name = 'Master 1 - Intelligence Artificielle' WHERE branch_id = 102",
        "UPDATE BRANCHES SET branch_name = 'Master 2 - Intelligence Artificielle' WHERE branch_id = 103",
        "UPDATE BRANCHES SET branch_name = 'Cycle Ingénieur 1 - Cloud Computing' WHERE branch_id = 104",
        "UPDATE BRANCHES SET branch_name = 'Licence Fondamentale - Gestion' WHERE branch_id = 201",
        "UPDATE BRANCHES SET branch_name = 'Master - Audit & Contrôle' WHERE branch_id = 202",
        "UPDATE BRANCHES SET branch_name = 'Master - Finance de Marché' WHERE branch_id = 203"
    ]

    # Exécution des mises à jour
    for sql in updates:
        cursor.execute(sql)
    
    conn.commit()
    print("✅ Tous les noms ont été corrigés avec les bons accents (UTF-8) !")

except Exception as e:
    print(f"❌ Erreur : {e}")

finally:
    # Fermeture propre de la connexion
    if 'conn' in locals() and conn:
        conn.close()
