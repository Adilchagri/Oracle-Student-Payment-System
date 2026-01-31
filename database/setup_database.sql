--------------------------------------------------------------------------------
-- PROJET: SYSTEME DE GESTION DES PAIEMENTS (ORACLE 19c)
-- AUTEURS: Adil CHAGRI & Chouaib JBEL
-- DATE: Janvier 2026
--------------------------------------------------------------------------------

-- 1. NETTOYAGE (Ordre inverse des dépendances)
BEGIN
    EXECUTE IMMEDIATE 'DROP VIEW VIEW_RISK_DASHBOARD';
    EXECUTE IMMEDIATE 'DROP TABLE RISK_ALERTS CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE PAYMENTS CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE INSTALLMENTS CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE STUDENTS CASCADE CONSTRAINTS';
    EXECUTE IMMEDIATE 'DROP TABLE DEPARTMENTS CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

-- 2. CREATION DES TABLES (DDL)

-- Nouvelle table pour les filières
CREATE TABLE DEPARTMENTS (
    dept_id      NUMBER(3)       CONSTRAINT pk_depts PRIMARY KEY,
    dept_name    VARCHAR2(100)   NOT NULL,
    description  VARCHAR2(255)
);

CREATE TABLE STUDENTS (
    student_id      NUMBER(5)       CONSTRAINT pk_students PRIMARY KEY,
    name            VARCHAR2(100)   NOT NULL,
    email           VARCHAR2(100),
    phone           VARCHAR2(20),
    dept_id         NUMBER(3),      -- Lien vers le département
    total_tuition   NUMBER(10,2)    NOT NULL,
    enrollment_date DATE            DEFAULT SYSDATE,
    CONSTRAINT fk_std_dept FOREIGN KEY (dept_id) REFERENCES DEPARTMENTS(dept_id)
);

CREATE TABLE INSTALLMENTS (
    installment_id  NUMBER(8)       CONSTRAINT pk_installments PRIMARY KEY,
    student_id      NUMBER(5),
    amount_due      NUMBER(10,2)    NOT NULL,
    due_date        DATE            NOT NULL,
    status          VARCHAR2(20)    DEFAULT 'PENDING',
    CONSTRAINT ck_status CHECK (status IN ('PENDING', 'PAID', 'PARTIAL', 'OVERDUE')),
    CONSTRAINT fk_inst_student FOREIGN KEY (student_id) REFERENCES STUDENTS(student_id)
);

CREATE TABLE PAYMENTS (
    payment_id      NUMBER(10)      CONSTRAINT pk_payments PRIMARY KEY,
    installment_id  NUMBER(8),
    amount_paid     NUMBER(10,2)    NOT NULL,
    payment_date    DATE            DEFAULT SYSDATE,
    CONSTRAINT fk_pay_installment FOREIGN KEY (installment_id) REFERENCES INSTALLMENTS(installment_id)
);

CREATE TABLE RISK_ALERTS (
    alert_id        NUMBER(10)      CONSTRAINT pk_alerts PRIMARY KEY,
    student_id      NUMBER(5),
    alert_date      DATE            DEFAULT SYSDATE,
    risk_level      VARCHAR2(10),
    message         VARCHAR2(255),
    CONSTRAINT fk_alert_student FOREIGN KEY (student_id) REFERENCES STUDENTS(student_id)
);

-- 3. INSERTIONS INITIALES (Données de test)
INSERT INTO DEPARTMENTS VALUES (1, 'Intelligence Artificielle', 'Parcours Excellence IA');
INSERT INTO DEPARTMENTS VALUES (2, 'Informatique', 'Génie Logiciel et Développement');
INSERT INTO DEPARTMENTS VALUES (3, 'Multimédia', 'Conception Web et Design');

INSERT INTO STUDENTS (student_id, name, email, dept_id, total_tuition) 
VALUES (1, 'Adil Chagri', 'adil.chagri@email.com', 1, 45000);
INSERT INTO STUDENTS (student_id, name, email, dept_id, total_tuition) 
VALUES (2, 'Chouaib Jbel', 'chouaib.jbel@email.com', 1, 45000);

COMMIT;

-- 4. TRIGGER (Gestion Automatique des Paiements)
CREATE OR REPLACE TRIGGER TRG_UPDATE_INSTALLMENT_STATUS
FOR INSERT ON PAYMENTS
COMPOUND TRIGGER
    v_inst_id NUMBER;
    v_total   NUMBER;
    v_due     NUMBER;

    AFTER EACH ROW IS
    BEGIN
        v_inst_id := :NEW.installment_id;
    END AFTER EACH ROW;

    AFTER STATEMENT IS
    BEGIN
        SELECT amount_due INTO v_due FROM INSTALLMENTS WHERE installment_id = v_inst_id;
        SELECT NVL(SUM(amount_paid), 0) INTO v_total FROM PAYMENTS WHERE installment_id = v_inst_id;

        IF v_total >= v_due THEN
            UPDATE INSTALLMENTS SET status = 'PAID' WHERE installment_id = v_inst_id;
        ELSE
            UPDATE INSTALLMENTS SET status = 'PARTIAL' WHERE installment_id = v_inst_id;
        END IF;
    END AFTER STATEMENT;
END TRG_UPDATE_INSTALLMENT_STATUS;
/

-- 5. PROCEDURE (Analyse des Risques)
CREATE OR REPLACE PROCEDURE PROC_DAILY_RISK_ANALYSIS IS
BEGIN
    FOR r IN (
        SELECT installment_id, student_id 
        FROM INSTALLMENTS
        WHERE due_date < SYSDATE AND status NOT IN ('PAID', 'OVERDUE')
    ) LOOP
        UPDATE INSTALLMENTS SET status = 'OVERDUE' WHERE installment_id = r.installment_id;
        
        INSERT INTO RISK_ALERTS (alert_id, student_id, risk_level, message)
        VALUES (
            (SELECT NVL(MAX(alert_id), 0) + 1 FROM RISK_ALERTS), 
            r.student_id, 
            'MEDIUM', 
            'Retard détecté facture #' || r.installment_id
        );
    END LOOP;
    COMMIT;
END;
/

-- 6. SCHEDULER JOB
BEGIN
    DBMS_SCHEDULER.CREATE_JOB (
        job_name        => 'JOB_DAILY_RISK_CHECK',
        job_type        => 'PLSQL_BLOCK',
        job_action      => 'BEGIN PROC_DAILY_RISK_ANALYSIS; END;',
        start_date      => SYSTIMESTAMP,
        repeat_interval => 'FREQ=DAILY; BYHOUR=0; BYMINUTE=0',
        enabled         => TRUE
    );
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

-- 7. VUE DASHBOARD (Mis à jour pour inclure le département)
CREATE OR REPLACE VIEW VIEW_RISK_DASHBOARD AS
SELECT 
    s.student_id,
    s.name AS Student_Name,
    d.dept_name AS Department,
    COUNT(r.alert_id) AS Total_Alerts,
    SUM(CASE WHEN i.status = 'OVERDUE' THEN i.amount_due ELSE 0 END) AS Total_Debt,
    CASE 
        WHEN COUNT(r.alert_id) >= 2 THEN 'CRITICAL'
        WHEN COUNT(r.alert_id) > 0 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS Risk_Profile
FROM STUDENTS s
JOIN DEPARTMENTS d ON s.dept_id = d.dept_id
LEFT JOIN INSTALLMENTS i ON s.student_id = i.student_id
LEFT JOIN RISK_ALERTS r ON s.student_id = r.student_id
GROUP BY s.student_id, s.name, d.dept_name;
