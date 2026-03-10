import psycopg2
import claims_data
import time
import os
from dotenv import load_dotenv

load_dotenv()
hostname = os.getenv("HOSTNAME")
username = os.getenv("POSTGRES_USERNAME")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")
port_id = os.getenv("PORT_ID")

# print(f"Connecting to database with hostname: {hostname}, username: {username}, password: {password}, database: {database}, port: {port_id}")

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

    table_creation_script = '''
    CREATE TABLE IF NOT EXISTS claims (
        claim_id INT PRIMARY KEY,
        claim_number VARCHAR(20) UNIQUE,
        customer_policy_id INT,
        hospital_id INT,
        claim_date DATE,
        hospitalization_date DATE,
        discharge_date DATE,
        diagnosis_code VARCHAR(10),
        diagnosis_description TEXT,
        room_type VARCHAR(20),
        total_bill_amount NUMERIC(12, 2),
        claimed_amount NUMERIC(12, 2),
        approved_amount NUMERIC(12, 2),
        rejected_amount NUMERIC(12, 2),
        claim_status VARCHAR(20),
        rejection_reason TEXT,
        settlement_date DATE,
        processing_days INT,
        created_at TIMESTAMP
    );
    '''

    cur.execute(table_creation_script)
    print("Claims table created successfully!")

    cur.execute("SELECT COALESCE(MAX(claim_id), 0) FROM claims;")
    result = cur.fetchone()
    claim_id_counter = result[0] + 1
    claim_records = claims_data.generate_claims_data(num_policies=10, claim_id_counter=claim_id_counter)

    start = time.time()
    insert_query = '''
        INSERT INTO claims (
        claim_id,
        claim_number,
        customer_policy_id,
        hospital_id,
        claim_date,
        hospitalization_date,
        discharge_date,
        diagnosis_code,
        diagnosis_description,
        room_type,
        total_bill_amount,
        claimed_amount,
        approved_amount,
        rejected_amount,
        claim_status,
        rejection_reason,
        settlement_date,
        processing_days,
        created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    print("Inserting claim records into the database...")

    cur.executemany(insert_query, claim_records)
    conn.commit()
    end = time.time()
    print(f"{len(claim_records)} claim records inserted successfully in {end - start:.2f} seconds!")
    print(f"{len(claim_records)} claim records inserted successfully!")
    
except Exception as e:
    print(f"Error connecting to the database: {e}")
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
    print("Database connection closed.")