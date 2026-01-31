import streamlit as st
import oracledb
import pandas as pd
import datetime
from fpdf import FPDF
import base64

# --- CONFIGURATION & STYLE ---
st.set_page_config(page_title="Système Gestion Scolarité", layout="wide", page_icon="🎓")
st.markdown("""
<style>
    /* Cartes KPI */
    div[data-testid="stMetric"] { background-color: #ffffff; border: 1px solid #e6e6e6; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); text-align: center; }
    /* Titres */
    h1, h2, h3 { color: #2c3e50; font-family: 'Segoe UI', sans-serif; }
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #f8f9fa; }
    /* Boutons */
    .stButton>button { border-radius: 20px; font-weight: bold; }
    /* Onglets Analytics */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 4px 4px 0 0; gap: 1px; padding-top: 10px; padding-bottom: 10px; }
    .stTabs [aria-selected="true"] { background-color: #ffffff; border-bottom: 2px solid #ff4b4b; }
    .warning-box { background-color: #ffeeba; color: #856404; padding: 10px; border-radius: 5px; border: 1px solid #ffeeba; }
</style>
""", unsafe_allow_html=True)

# --- CONNEXION ORACLE (Correction UTF-8 auto) ---
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

# --- FONCTIONS UTILES ---
def run_query(query, params=None):
    with conn.cursor() as cursor:
        if params: cursor.execute(query, params)
        else: cursor.execute(query)
        conn.commit()

def get_next_id(table, col):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT NVL(MAX({col}), 0) + 1 FROM {table}")
        return cursor.fetchone()[0]

def create_receipt_pdf(student_name, amount, payment_id, date):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_fill_color(44, 62, 80)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(190, 20, txt="RECU DE PAIEMENT", ln=1, align='C')
    pdf.ln(20)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Ref Transaction : #{payment_id}", ln=1)
    pdf.cell(200, 10, txt=f"Date : {date}", ln=1)
    pdf.cell(200, 10, txt=f"Etudiant : {student_name}", ln=1)
    pdf.ln(10)
    pdf.set_fill_color(236, 240, 241)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 15, txt=f"Montant Paye : {amount:.2f} DH", ln=1, align='C', fill=True)
    pdf.ln(30)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="Document genere automatiquement par le Systeme Oracle.", ln=1, align='C')
    return pdf.output(dest="S").encode("latin-1", errors="replace")

# --- NAVIGATION INTELLIGENTE ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2995/2995467.png", width=80)
st.sidebar.title("Gestion Scolarité")
st.sidebar.markdown("---")

# 1. Sélection du Module (Catégorie)
module = st.sidebar.selectbox("📂 Module", [
    "📊 Pilotage & Décision",
    "💼 Administration",
    "💰 Finance & Compta",
    "🛠️ Technique"
])

# 2. Sélection de la Page (Sous-menu dynamique)
if module == "📊 Pilotage & Décision":
    page = st.sidebar.radio("Navigation", ["Tableau de Bord", "Analyses Financières"])
elif module == "💼 Administration":
    page = st.sidebar.radio("Navigation", ["Annuaire & Dossiers", "Inscription & Facture", "Gestion Étudiants"])
elif module == "💰 Finance & Compta":
    page = st.sidebar.radio("Navigation", ["Caisse (Paiements)", "Créer Facture"])
elif module == "🛠️ Technique":
    page = st.sidebar.radio("Navigation", ["Schéma BDD"])

st.sidebar.markdown("---")
st.sidebar.caption("Master IA - Projet Oracle")

# =========================================================
# PAGE 1: DASHBOARD
# =========================================================
if page == "Tableau de Bord":
    st.title("📊 Tableau de Bord des Risques")
    st.caption("Surveillance en temps réel des impayés et des statuts étudiants.")
    
    if st.button("🔄 Lancer l'Analyse de Risque (Batch Manuel)"):
        try:
            run_query("BEGIN PROC_DAILY_RISK_ANALYSIS; END;")
            st.toast("Batch exécuté avec succès !", icon="✅")
        except Exception as e: st.error(f"Erreur : {e}")

    if conn:
        df = pd.read_sql("SELECT * FROM VIEW_RISK_DASHBOARD", conn)
        col1, col2, col3, col4 = st.columns(4)
        risk_count = len(df[df['RISK_PROFILE'] != 'LOW'])
        total_debt = df['TOTAL_DEBT'].sum()
        recovery = pd.read_sql("SELECT (SELECT NVL(SUM(amount_paid),0) FROM PAYMENTS) as P, (SELECT NVL(SUM(amount_due),1) FROM INSTALLMENTS) as D FROM DUAL", conn)
        rate = (recovery['P'][0] / recovery['D'][0]) * 100 if recovery['D'][0] > 0 else 0

        col1.metric("Étudiants Inscrits", len(df))
        col2.metric("Étudiants à Risque", risk_count, delta="-Attention", delta_color="inverse")
        col3.metric("Dette Globale", f"{total_debt:,.0f} DH", delta_color="inverse")
        col4.metric("Taux Recouvrement", f"{rate:.1f}%")
        
        st.divider()
        st.subheader("📋 État des Lieux par Étudiant")
        
        def highlight_risk(val):
            color = '#ffcccb' if val == 'CRITICAL' else '#ffe5b4' if val == 'MEDIUM' else '#d4edda'
            return f'background-color: {color}; color: black; font-weight: bold; border-radius: 4px;'
            
        st.dataframe(df.style.map(highlight_risk, subset=['RISK_PROFILE']).format({'TOTAL_DEBT': "{:,.2f} DH"}), use_container_width=True)

# =========================================================
# PAGE 1-BIS: ANALYSES
# =========================================================
elif page == "Analyses Financières":
    st.title("📈 Analyses & Projections")
    st.markdown("Vue détaillée de la répartition financière et académique.")
    
    if conn:
        tab1, tab2 = st.tabs(["💰 Performance", "🎓 Académique"])
        
        with tab1:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("##### 📉 Dette vs Encaissement")
                df_perf = pd.read_sql("""
                    SELECT '1. Attendu' as "Type", SUM(amount_due) as "Montant" FROM INSTALLMENTS 
                    UNION ALL 
                    SELECT '2. Perçu' as "Type", SUM(amount_paid) FROM PAYMENTS
                """, conn)
                st.bar_chart(df_perf.set_index('Type'), color="#27ae60", height=300)
            
            with c2:
                st.markdown("##### 📅 Projection des Rentrées (Factures impayées)")
                df_proj = pd.read_sql("""
                    SELECT TO_CHAR(due_date, 'YYYY-MM') as "Mois", SUM(amount_due) as "Montant Attendu" 
                    FROM INSTALLMENTS WHERE status != 'PAID' 
                    GROUP BY TO_CHAR(due_date, 'YYYY-MM') ORDER BY "Mois"
                """, conn)
                if not df_proj.empty:
                    st.area_chart(df_proj.set_index('Mois'), color="#e67e22", height=300)
                else:
                    st.success("✅ Aucune facture en attente ! Tout est à jour.")

        with tab2:
            st.markdown("##### 📊 Répartition par Département")
            df_dept = pd.read_sql("""
                SELECT d.dept_name as "Département", COUNT(s.student_id) as "Nombre" 
                FROM STUDENTS s 
                JOIN BRANCHES b ON s.branch_id=b.branch_id 
                JOIN DEPARTMENTS d ON b.dept_id=d.dept_id 
                GROUP BY d.dept_name
            """, conn)
            st.bar_chart(df_dept.set_index("Département"), color="#3498db")

# =========================================================
# PAGE 2: INSCRIPTION
# =========================================================
elif page == "Inscription & Facture":
    st.title("➕ Inscription Académique")
    
    depts = pd.read_sql("SELECT * FROM DEPARTMENTS ORDER BY dept_name", conn)
    dept_map = dict(zip(depts['DEPT_NAME'], depts['DEPT_ID']))
    
    st.info("Étape 1 : Choisissez le département pour voir les filières disponibles.")
    sel_dept_name = st.selectbox("Département de rattachement", options=depts['DEPT_NAME'])
    sel_dept_id = dept_map[sel_dept_name]
    
    branches = pd.read_sql(f"SELECT * FROM BRANCHES WHERE dept_id = {sel_dept_id} ORDER BY branch_name", conn)
    
    if not branches.empty:
        branch_map = dict(zip(branches['BRANCH_NAME'], branches['BRANCH_ID']))
        price_map = dict(zip(branches['BRANCH_NAME'], branches['ANNUAL_TUITION']))
        
        with st.form("form_student"):
            st.markdown(f"#### Formulaire d'inscription : {sel_dept_name}")
            
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Nom Complet")
                email = st.text_input("Email")
                phone = st.text_input("Téléphone")
            
            with c2:
                sel_branch = st.selectbox("Filière / Niveau", options=branches['BRANCH_NAME'])
                tuition_val = float(price_map[sel_branch])
                branch_id = branch_map[sel_branch]
                tuition = st.number_input("Scolarité Annuelle (DH)", value=tuition_val)
                st.caption(f"Prix standard : {tuition_val:,.0f} DH")
                
            st.markdown("---")
            st.subheader("Plan de Paiement Initial")
            col_p1, col_p2 = st.columns(2)
            first_pay = col_p1.number_input("Montant 1er Versement", value=5000.0)
            due_date = col_p2.date_input("Date Limite", datetime.date.today() + datetime.timedelta(days=30))
            
            submitted = st.form_submit_button("✅ Valider Inscription", type="primary")
            
            if submitted and name:
                try:
                    nid = get_next_id("STUDENTS", "student_id")
                    niid = get_next_id("INSTALLMENTS", "installment_id")
                    with conn.cursor() as cursor:
                        cursor.execute("INSERT INTO STUDENTS (student_id, name, email, phone, branch_id, total_tuition) VALUES (:1,:2,:3,:4,:5,:6)", [nid, name, email, phone, branch_id, tuition])
                        cursor.execute("INSERT INTO INSTALLMENTS (installment_id, student_id, amount_due, due_date, status) VALUES (:1,:2,:3,:4,'PENDING')", [niid, nid, first_pay, due_date])
                        conn.commit()
                    st.success(f"Inscription réussie ! Facture #{niid} générée.")
                except Exception as e: st.error(f"Erreur technique : {e}")
    else:
        st.warning("Aucune filière n'est disponible pour ce département.")

# =========================================================
# PAGE 2-BIS: GESTION ETUDIANTS
# =========================================================
elif page == "Gestion Étudiants":
    st.title("🛠️ Gestion Administrative")
    st.markdown("Recherchez un étudiant pour **Modifier** ses informations ou le **Supprimer**.")
    
    search_q = st.text_input("🔍 Rechercher un étudiant (Nom ou ID)", placeholder="Ex: Adil ou 102")
    
    if search_q and conn:
        sql_search = f"""
            SELECT s.*, b.branch_name, b.dept_id 
            FROM STUDENTS s
            JOIN BRANCHES b ON s.branch_id = b.branch_id
            WHERE LOWER(s.name) LIKE '%{search_q.lower()}%' OR TO_CHAR(s.student_id) = '{search_q}'
        """
        results = pd.read_sql(sql_search, conn)
        
        if not results.empty:
            student_options = results.apply(lambda x: f"{x['NAME']} (ID: {x['STUDENT_ID']})", axis=1)
            selected_label = st.selectbox("Sélectionnez l'étudiant :", student_options)
            selected_row = results.iloc[student_options[student_options == selected_label].index[0]]
            sid = int(selected_row['STUDENT_ID'])
            
            tab_edit, tab_delete = st.tabs(["✏️ Modifier", "🗑️ Supprimer"])
            
            with tab_edit:
                with st.form("edit_form"):
                    st.subheader(f"Modification : {selected_row['NAME']}")
                    new_name = st.text_input("Nom Complet", value=selected_row['NAME'])
                    new_email = st.text_input("Email", value=selected_row['EMAIL'])
                    new_phone = st.text_input("Téléphone", value=selected_row['PHONE'])
                    
                    st.markdown("**Changement de Filière**")
                    all_branches = pd.read_sql("SELECT * FROM BRANCHES ORDER BY branch_name", conn)
                    branch_opts = list(all_branches['BRANCH_NAME'])
                    curr_branch_idx = branch_opts.index(selected_row['BRANCH_NAME']) if selected_row['BRANCH_NAME'] in branch_opts else 0
                    
                    new_branch_name = st.selectbox("Nouvelle Filière", options=branch_opts, index=curr_branch_idx)
                    new_branch_row = all_branches[all_branches['BRANCH_NAME'] == new_branch_name].iloc[0]
                    new_branch_id = int(new_branch_row['BRANCH_ID'])
                    new_std_price = float(new_branch_row['ANNUAL_TUITION'])
                    
                    update_price = st.checkbox(f"Mettre à jour le tarif ? ({new_std_price:,.0f} DH)", value=True)
                    final_tuition = new_std_price if update_price else float(selected_row['TOTAL_TUITION'])
                    
                    if st.form_submit_button("💾 Enregistrer"):
                        try:
                            with conn.cursor() as cursor:
                                cursor.execute("UPDATE STUDENTS SET name=:1, email=:2, phone=:3, branch_id=:4, total_tuition=:5 WHERE student_id=:6", [new_name, new_email, new_phone, new_branch_id, final_tuition, sid])
                                conn.commit()
                            st.success("✅ Modifications enregistrées !")
                        except Exception as e: st.error(f"Erreur : {e}")

            with tab_delete:
                st.markdown("""<div class="warning-box">⚠️ <b>Attention</b> : La suppression est irréversible et effacera tout l'historique financier de l'étudiant.</div>""", unsafe_allow_html=True)
                st.write("")
                if st.button("🚨 Confirmer la Suppression", type="primary"):
                    try:
                        with conn.cursor() as cursor:
                            cursor.execute("DELETE FROM RISK_ALERTS WHERE student_id = :1", [sid])
                            cursor.execute("DELETE FROM PAYMENTS WHERE installment_id IN (SELECT installment_id FROM INSTALLMENTS WHERE student_id = :1)", [sid])
                            cursor.execute("DELETE FROM INSTALLMENTS WHERE student_id = :1", [sid])
                            cursor.execute("DELETE FROM STUDENTS WHERE student_id = :1", [sid])
                            conn.commit()
                        st.success(f"L'étudiant {selected_row['NAME']} a été supprimé.")
                    except Exception as e: st.error(f"Erreur : {e}")
        else:
            st.warning("Aucun étudiant trouvé.")

# =========================================================
# PAGE 3: CREER FACTURE
# =========================================================
elif page == "Créer Facture":
    st.title("📄 Nouvelle Échéance")
    stds = pd.read_sql("SELECT student_id, name FROM STUDENTS ORDER BY name", conn)
    if not stds.empty:
        smap = dict(zip(stds['NAME'] + " (" + stds['STUDENT_ID'].astype(str) + ")", stds['STUDENT_ID']))
        sel = st.selectbox("Étudiant", smap.keys())
        sid = int(smap[sel])
        with st.form("fi"):
            amt = st.number_input("Montant", value=1000)
            date = st.date_input("Date", datetime.date.today() + datetime.timedelta(days=30))
            if st.form_submit_button("Créer", type="primary"):
                try:
                    nid = get_next_id("INSTALLMENTS", "installment_id")
                    run_query("INSERT INTO INSTALLMENTS (installment_id, student_id, amount_due, due_date) VALUES (:1,:2,:3,:4)", [nid, sid, amt, date])
                    st.success("Facture créée.")
                except Exception as e: st.error(e)

# =========================================================
# PAGE 4: PAIEMENT
# =========================================================
elif page == "Caisse (Paiements)":
    st.title("💰 Caisse")
    insts = pd.read_sql("SELECT i.installment_id, s.name, i.amount_due FROM INSTALLMENTS i JOIN STUDENTS s ON i.student_id=s.student_id WHERE i.status!='PAID'", conn)
    if not insts.empty:
        opts = insts.apply(lambda x: f"#{x['INSTALLMENT_ID']} - {x['NAME']} ({x['AMOUNT_DUE']} DH)", axis=1)
        imap = dict(zip(opts, insts['INSTALLMENT_ID']))
        sel = st.selectbox("Facture", imap.keys())
        iid = int(imap[sel])
        std = sel.split(" - ")[1].split(" (")[0]
        with st.form("pay"):
            mnt = st.number_input("Montant", min_value=1.0)
            if st.form_submit_button("Valider", type="primary"):
                try:
                    pid = get_next_id("PAYMENTS", "payment_id")
                    run_query("INSERT INTO PAYMENTS (payment_id, installment_id, amount_paid) VALUES (:1,:2,:3)", [pid, iid, mnt])
                    st.success("Payé !")
                    pdf = create_receipt_pdf(std, mnt, pid, datetime.date.today())
                    b64 = base64.b64encode(pdf).decode()
                    st.markdown(f'<a href="data:application/octet-stream;base64,{b64}" download="recu.pdf" style="background-color:#2c3e50;color:white;padding:10px;border-radius:5px;text-decoration:none;">📥 Reçu PDF</a>', unsafe_allow_html=True)
                except Exception as e: st.error(e)
    else: st.success("Rien à payer.")

# =========================================================
# PAGE 5: ANNUAIRE
# =========================================================
elif page == "Annuaire & Dossiers":
    st.title("🔍 Annuaire & Dossiers 360°")
    
    with st.expander("🔎 Filtres de Recherche", expanded=True):
        col_f1, col_f2, col_f3 = st.columns(3)
        depts = pd.read_sql("SELECT * FROM DEPARTMENTS ORDER BY dept_name", conn)
        all_depts = ["Tous"] + list(depts['DEPT_NAME'])
        sel_dept = col_f1.selectbox("Département", options=all_depts)
        
        if sel_dept != "Tous":
            dept_id = depts[depts['DEPT_NAME'] == sel_dept].iloc[0]['DEPT_ID']
            branches = pd.read_sql(f"SELECT * FROM BRANCHES WHERE dept_id = {dept_id} ORDER BY branch_name", conn)
        else:
            branches = pd.read_sql("SELECT * FROM BRANCHES ORDER BY branch_name", conn)
            
        all_branches = ["Tous"] + list(branches['BRANCH_NAME'])
        sel_branch = col_f2.selectbox("Filière", options=all_branches)
        search_txt = col_f3.text_input("Recherche Nom/ID", placeholder="Ex: Sarah")

    base_sql = """
        SELECT s.student_id, s.name, s.email, s.phone, b.branch_name, d.dept_name, s.total_tuition
        FROM STUDENTS s 
        JOIN BRANCHES b ON s.branch_id = b.branch_id 
        JOIN DEPARTMENTS d ON b.dept_id = d.dept_id
        WHERE 1=1
    """
    if sel_dept != "Tous": base_sql += f" AND d.dept_name = '{sel_dept}'"
    if sel_branch != "Tous": base_sql += f" AND b.branch_name = '{sel_branch}'"
    if search_txt: base_sql += f" AND (LOWER(s.name) LIKE '%{search_txt.lower()}%' OR TO_CHAR(s.student_id) = '{search_txt}')"
    base_sql += " ORDER BY s.name"
    
    if conn:
        results = pd.read_sql(base_sql, conn)
        st.markdown(f"### 📋 Liste des Étudiants ({len(results)})")
        
        if not results.empty:
            student_list = results.apply(lambda x: f"{x['NAME']} (ID: {x['STUDENT_ID']})", axis=1)
            selected_student_str = st.selectbox("👉 Sélectionnez un étudiant pour voir son dossier complet :", options=student_list)
            st.divider()
            
            if selected_student_str:
                selected_id = int(selected_student_str.split("(ID: ")[1].replace(")", ""))
                info = results[results['STUDENT_ID'] == selected_id].iloc[0]
                
                with st.container(border=True):
                    c1, c2 = st.columns([1, 3])
                    c1.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
                    c2.markdown(f"## {info['NAME']}")
                    c2.info(f"🏛 {info['DEPT_NAME']} | 🎓 {info['BRANCH_NAME']}")
                    c2.text(f"📞 {info['PHONE']} | 📧 {info['EMAIL']}")
                    c2.metric("Scolarité Totale", f"{info['TOTAL_TUITION']:,.2f} DH")
                    
                    st.divider()
                    tab_fact, tab_alert = st.tabs(["📂 Factures & Paiements", "⚠️ Risques & Alertes"])
                    
                    with tab_fact:
                        df_inst = pd.read_sql(f"SELECT installment_id, amount_due, due_date, status FROM INSTALLMENTS WHERE student_id={selected_id} ORDER BY due_date", conn)
                        def color_status(val):
                            color = '#d4edda' if val=='PAID' else '#f8d7da' if val=='OVERDUE' else '#fff3cd'
                            return f'background-color: {color}'
                        st.dataframe(df_inst.style.map(color_status, subset=['STATUS']), use_container_width=True)
                        paid = pd.read_sql(f"SELECT SUM(amount_paid) FROM PAYMENTS p JOIN INSTALLMENTS i ON p.installment_id = i.installment_id WHERE i.student_id={selected_id}", conn).iloc[0,0]
                        st.metric("Total Payé à ce jour", f"{paid if paid else 0:,.2f} DH")

                    with tab_alert:
                        df_alert = pd.read_sql(f"SELECT alert_date, risk_level, message FROM RISK_ALERTS WHERE student_id={selected_id} ORDER BY alert_date DESC", conn)
                        if not df_alert.empty: st.dataframe(df_alert, use_container_width=True)
                        else: st.success("Aucune alerte enregistrée.")
        else:
            st.info("Aucun étudiant ne correspond aux critères.")

# =========================================================
# PAGE 6: SCHEMA
# =========================================================
elif page == "Schéma BDD":
    st.title("🔗 Structure")
    graph = """
    digraph ERD {
        rankdir=LR; node [shape=plaintext];
        DEPT [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"><TR><TD BGCOLOR="#8e44ad"><B><FONT COLOR="white">DEPARTMENTS</FONT></B></TD></TR></TABLE>>];
        BRANCH [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"><TR><TD BGCOLOR="#9b59b6"><B><FONT COLOR="white">BRANCHES</FONT></B></TD></TR></TABLE>>];
        STUD [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"><TR><TD BGCOLOR="#3498db"><B><FONT COLOR="white">STUDENTS</FONT></B></TD></TR></TABLE>>];
        INST [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"><TR><TD BGCOLOR="#95a5a6"><B><FONT COLOR="white">INSTALLMENTS</FONT></B></TD></TR></TABLE>>];
        PAY [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"><TR><TD BGCOLOR="#2ecc71"><B><FONT COLOR="white">PAYMENTS</FONT></B></TD></TR></TABLE>>];
        DEPT -> BRANCH [label="1..N"];
        BRANCH -> STUD [label="1..N"];
        STUD -> INST [label="1..N"];
        INST -> PAY [label="1..N"];
    }
    """
    st.graphviz_chart(graph)
