import psycopg2
import customer_master
import time
import os
from dotenv import load_dotenv

load_dotenv()
hostname = os.getenv("HOSTNAME")
username = os.getenv("POSTGRES_USERNAME")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")
port_id = os.getenv("PORT_ID")

conn, cur = None, None

try:
    conn = psycopg2.connect(
        host = hostname,
        user = username,
        password = password,
        dbname = database,
        port = port_id
    )
    print("Connection to the database was successful!")

    cur = conn.cursor()
    start = time.time()
    table_creation_script = '''
    CREATE TABLE IF NOT EXISTS customer_master (
        customer_id                BIGINT PRIMARY KEY,
        customer_external_ref      UUID NOT NULL UNIQUE,
        agent_id                   INTEGER NOT NULL,
        first_name                 VARCHAR(100) NOT NULL,
        middle_name                VARCHAR(100),
        last_name                  VARCHAR(100) NOT NULL,
        date_of_birth              DATE NOT NULL,
        gender                     VARCHAR(20) CHECK (gender IN ('Male','Female','Other')),
        marital_status             VARCHAR(20),
        email                      VARCHAR(255),
        phone_number               VARCHAR(15),
        address                    TEXT,
        city                       VARCHAR(100),
        state                      VARCHAR(100),
        pincode                    VARCHAR(10),
        country                    VARCHAR(50) DEFAULT 'India',
        occupation                 VARCHAR(100),
        employment_type            VARCHAR(50),
        annual_income              NUMERIC(15,2),
        credit_score               INTEGER CHECK (credit_score BETWEEN 300 AND 860),
        height_cm                  NUMERIC(5,2),
        weight_kg                  NUMERIC(5,2),
        smoker_flag                BOOLEAN,
        alcohol_consumption_level  VARCHAR(20),
        physical_activity_level    VARCHAR(20),
        pre_existing_conditions    VARCHAR(100),
        chronic_disease_flag       BOOLEAN,
        family_medical_history_flag BOOLEAN,
        stress_level_index         INTEGER CHECK (stress_level_index BETWEEN 1 AND 10),
        sleep_hours_avg            NUMERIC(4,1),
        created_at                 TIMESTAMP NOT NULL,
        updated_at                 TIMESTAMP NOT NULL,
        source_system              VARCHAR(50),
        record_version             INTEGER DEFAULT 1,
        CONSTRAINT chk_updated_after_created
            CHECK (updated_at >= created_at)
        )
    '''
    print("Creating customer_master table...")
    cur.execute(table_creation_script)
    print("customer_master table created successfully!")

    cur.execute("SELECT COALESCE(MAX(customer_id), 0) FROM customer_master;")
    result = cur.fetchone()
    customer_id_counter = result[0] + 1
    data = customer_master.customer_data(NUM_RECORDS=100, start_id=customer_id_counter)
    
    insert_query='''
    INSERT INTO customer_master (
        customer_id,
        customer_external_ref,
        agent_id,
        first_name,
        middle_name,
        last_name,
        date_of_birth,
        gender,
        marital_status,
        email,
        phone_number,
        address,
        city,
        state,
        pincode,
        country,
        occupation,
        employment_type,
        annual_income,
        credit_score,
        height_cm,
        weight_kg,
        smoker_flag,
        alcohol_consumption_level,
        physical_activity_level,
        pre_existing_conditions,
        chronic_disease_flag,
        family_medical_history_flag,
        stress_level_index,
        sleep_hours_avg,
        created_at,
        updated_at,
        source_system,
        record_version
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
    '''
    print("Inserting customer records into the database...")

    cur.executemany(insert_query, data)
    conn.commit()
    end = time.time()
    print(f"{len(data)} customer records inserted successfully in {end - start:.2f} seconds!")
    print(f"{len(data)} customer records inserted successfully!")
except Exception as e:
    print(f"Error connecting to the database: {e}")
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
    print("Database connection closed.")