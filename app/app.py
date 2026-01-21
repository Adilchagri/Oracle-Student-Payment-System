import streamlit as st
import oracledb
import pandas as pd
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Système Gestion Scolarité", layout="wide")

# --- CONNEXION ORACLE ---
@st.cache_resource
def init_connection():
    try:
        return oracledb.connect(
            user="projet_paiement",
            password="password123",
            dsn="localhost:1521/ORCLCDB",
            disable_oob=True
        )
    except Exception as e:
        st.error(f"Erreur connexion : {e}")
        return None

conn = init_connection()

# --- FONCTIONS UTILES (SQL) ---
def run_query(query, params=None):
    with conn.cursor() as cursor:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()

def get_next_id(table, col):
    # Récupère le prochain ID disponible (MAX + 1)
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT NVL(MAX({col}), 0) + 1 FROM {table}")
        return cursor.fetchone()[0]

# --- NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller vers :", ["📊 Tableau de Bord", "➕ Inscrire Étudiant", "📄 Créer Facture", "💰 Enregistrer Paiement"])

# =========================================================
# PAGE 1 : TABLEAU DE BORD (Visualisation)
# =========================================================
if page == "📊 Tableau de Bord":
    st.title("📊 Tableau de Bord des Risques")
    
    # Bouton pour rafraîchir la Vue et lancer le Batch manuellement
    if st.button("🔄 Lancer l'Analyse de Risque (Batch)"):
        try:
            run_query("BEGIN PROC_DAILY_RISK_ANALYSIS; END;")
            st.toast("Analyse de risque terminée !", icon="✅")
        except Exception as e:
            st.error(f"Erreur batch : {e}")

    # Affichage des données
    if conn:
        df = pd.read_sql("SELECT * FROM VIEW_RISK_DASHBOARD", conn)
        
        # KPI
        col1, col2, col3 = st.columns(3)
        risk_count = len(df[df['RISK_PROFILE'] != 'LOW'])
        total_debt = df['TOTAL_DEBT'].sum()
        
        col1.metric("Étudiants", len(df))
        col2.metric("À Risque", risk_count, delta_color="inverse")
        col3.metric("Dette Totale", f"{total_debt:,.2f} DH")
        
        # Tableau coloré
        st.subheader("Détail par Étudiant")
        def color_risk(val):
            return f'color: {"red" if val == "CRITICAL" else "orange" if val == "MEDIUM" else "green"}; font-weight: bold'
        
        st.dataframe(df.style.map(color_risk, subset=['RISK_PROFILE']), use_container_width=True)

# =========================================================
# PAGE 2 : INSCRIRE UN ÉTUDIANT (ET CRÉER SA FACTURE)
# =========================================================
elif page == "➕ Inscrire Étudiant":
    st.title("➕ Inscription & Facturation")
    
    with st.form("form_student"):
        st.subheader("1. Informations Étudiant")
        name = st.text_input("Nom Complet")
        email = st.text_input("Email")
        phone = st.text_input("Téléphone")
        
        st.subheader("2. Première Facture (Automatique)")
        # On définit par défaut une facture "Trimestre 1"
        col1, col2 = st.columns(2)
        tuition_total = col1.number_input("Scolarité Totale (DH)", value=5000)
        first_payment = col2.number_input("Montant 1ère échéance (DH)", value=1000)
        due_date = st.date_input("Date limite de paiement", datetime.date.today() + datetime.timedelta(days=30))
        
        submitted = st.form_submit_button("Valider Inscription")
        
        if submitted and name:
            try:
                # 1. On génère les IDs
                new_student_id = get_next_id("STUDENTS", "student_id")
                new_inst_id = get_next_id("INSTALLMENTS", "installment_id")
                
                # 2. Requete SQL (Double Insertion)
                # On utilise une transaction pour s'assurer que tout se crée ou rien du tout
                with conn.cursor() as cursor:
                    # A. Création Étudiant
                    sql_student = """
                        INSERT INTO STUDENTS (student_id, name, email, phone, total_tuition) 
                        VALUES (:1, :2, :3, :4, :5)
                    """
                    cursor.execute(sql_student, [new_student_id, name, email, phone, tuition_total])
                    
                    # B. Création Facture Immédiate
                    sql_invoice = """
                        INSERT INTO INSTALLMENTS (installment_id, student_id, amount_due, due_date, status) 
                        VALUES (:1, :2, :3, :4, 'PENDING')
                    """
                    cursor.execute(sql_invoice, [new_inst_id, new_student_id, first_payment, due_date])
                    
                    conn.commit()
                
                st.success(f"✅ Succès ! {name} est inscrit et la facture #{new_inst_id} de {first_payment} DH est générée.")
                st.info("Vous pouvez voir cet étudiant immédiatement dans le Tableau de Bord.")
                
            except Exception as e:
                st.error(f"Erreur lors de l'enregistrement : {e}")
# =========================================================
# PAGE 3 : CRÉER UNE FACTURE (CREATE)
# =========================================================
elif page == "📄 Créer Facture":
    st.title("📄 Nouvelle Échéance")
    
    # Liste déroulante des étudiants
    students = pd.read_sql("SELECT student_id, name FROM STUDENTS ORDER BY name", conn)
    student_dict = dict(zip(students['NAME'] + " (ID: " + students['STUDENT_ID'].astype(str) + ")", students['STUDENT_ID']))
    
    selected_student_label = st.selectbox("Choisir l'étudiant", student_dict.keys())
    selected_student_id = int(student_dict[selected_student_label])
    
    with st.form("form_installment"):
        amount = st.number_input("Montant Dû (DH)", value=1000)
        due_date = st.date_input("Date limite", datetime.date.today() + datetime.timedelta(days=30))
        submitted = st.form_submit_button("Générer Facture")
        
        if submitted:
            try:
                new_inst_id = get_next_id("INSTALLMENTS", "installment_id")
                sql = "INSERT INTO INSTALLMENTS (installment_id, student_id, amount_due, due_date, status) VALUES (:1, :2, :3, :4, 'PENDING')"
                run_query(sql, [new_inst_id, selected_student_id, amount, due_date])
                st.success(f"Facture #{new_inst_id} créée pour {amount} DH !")
            except Exception as e:
                st.error(f"Erreur : {e}")

# =========================================================
# PAGE 4 : ENREGISTRER PAIEMENT (UPDATE VIA TRIGGER)
# =========================================================
elif page == "💰 Enregistrer Paiement":
    st.title("💰 Saisir un Paiement")
    st.info("Le système mettra à jour automatiquement le statut (Trigger PL/SQL).")
    
    # On ne montre que les factures impayées
    sql_inst = """
        SELECT i.installment_id, s.name, i.amount_due, i.status 
        FROM INSTALLMENTS i JOIN STUDENTS s ON i.student_id = s.student_id 
        WHERE i.status != 'PAID'
        ORDER BY i.installment_id
    """
    insts = pd.read_sql(sql_inst, conn)
    
    if not insts.empty:
        inst_options = insts.apply(lambda x: f"Facture #{x['INSTALLMENT_ID']} - {x['NAME']} ({x['AMOUNT_DUE']} DH) [{x['STATUS']}]", axis=1)
        # Création d'un dictionnaire pour retrouver l'ID à partir du texte
        inst_map = dict(zip(inst_options, insts['INSTALLMENT_ID']))
        
        selected_inst_label = st.selectbox("Sélectionner la facture à payer", inst_map.keys())
        selected_inst_id = int(inst_map[selected_inst_label])
        
        with st.form("form_payment"):
            amount_pay = st.number_input("Montant Versé (DH)", min_value=1.0)
            submitted = st.form_submit_button("Valider le Paiement")
            
            if submitted:
                try:
                    new_pay_id = get_next_id("PAYMENTS", "payment_id")
                    sql = "INSERT INTO PAYMENTS (payment_id, installment_id, amount_paid) VALUES (:1, :2, :3)"
                    run_query(sql, [new_pay_id, selected_inst_id, amount_pay])
                    st.success("Paiement enregistré ! Vérifiez le statut dans le tableau de bord.")
                except Exception as e:
                    st.error(f"Erreur : {e}")
    else:
        st.success("Aucune facture en attente ! Tout est payé.")
