import psycopg2
import insurance_agents
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
        host=hostname,
        user=username,
        password=password,
        dbname=database,
        port=port_id
    )

    print("Connection to the database was successful!")

    cur = conn.cursor()

    table_creation_script = '''
    CREATE TABLE IF NOT EXISTS insurance_agents (
        agent_id INT PRIMARY KEY,
        agent_name VARCHAR(100),
        license_number VARCHAR(20) UNIQUE,
        region VARCHAR(20),
        branch_code VARCHAR(10),
        joining_date DATE,
        commission_percentage NUMERIC(5,2),
        performance_rating NUMERIC(3,2),
        active_flag BOOLEAN,
        manager_id INT,
        created_at TIMESTAMP
    );
    '''

    cur.execute(table_creation_script)

    print("Insurance agents table created successfully!")

    cur.execute("SELECT COALESCE(MAX(agent_id),0) FROM insurance_agents;")
    result = cur.fetchone()

    agent_id_counter = result[0] + 1

    agent_records = insurance_agents.generate_agents_data(agent_id_counter)

    start = time.time()

    insert_query = '''
        INSERT INTO insurance_agents (
            agent_id,
            agent_name,
            license_number,
            region,
            branch_code,
            joining_date,
            commission_percentage,
            performance_rating,
            active_flag,
            manager_id,
            created_at
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''

    print("Inserting insurance agent records...")

    cur.executemany(insert_query, agent_records)

    conn.commit()

    end = time.time()

    print(f"{len(agent_records)} agent records inserted successfully in {end - start:.2f} seconds!")

except Exception as e:

    print(f"Error connecting to the database: {e}")

finally:

    if cur is not None:
        cur.close()

    if conn is not None:
        conn.close()

    print("Database connection closed.")