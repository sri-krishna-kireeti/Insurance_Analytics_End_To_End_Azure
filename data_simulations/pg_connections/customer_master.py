import random
import uuid
from faker import Faker
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

fake = Faker("en_IN")

MAX_AGENT_ID = 200

# --------------------------
# Static Reference Data
# --------------------------

genders = ["Male", "Female", "Other"]
marital_statuses = ["Single", "Married", "Divorced", "Widowed"]
employment_types = ["Salaried", "Self-Employed", "Unemployed"]
physical_levels = ["low", "moderate", "high"]
alcohol_levels = ["none", "low", "moderate", "high"]

occupations = [ "IT", "Healthcare", "Non-IT", "Business", "Government", "Other"]

medical_conditions = ["Diabetes", "Hypertension", "Asthma", "Heart Disease", "Thyroid", "Other", "None"]

states = [
    "Andhra Pradesh", "Telangana", "Karnataka",
    "Tamil Nadu", "Maharashtra", "Delhi"
]

cities = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada"],
    "Telangana": ["Hyderabad", "Warangal"],
    "Karnataka": ["Bengaluru", "Mysuru"],
    "Tamil Nadu": ["Chennai", "Coimbatore"],
    "Maharashtra": ["Mumbai", "Pune"],
    "Delhi": ["New Delhi"]
}

# --------------------------
# Helper Functions
# --------------------------

def generate_income():
    band = random.choices(
        ["low", "mid", "upper_mid", "high", "ultra"],
        weights=[30, 30, 25, 12, 3]
    )[0]

    if band == "low":
        return round(random.uniform(200000, 500000), 2)
    elif band == "mid":
        return round(random.uniform(500000, 1000000), 2)
    elif band == "upper_mid":
        return round(random.uniform(1000000, 2500000), 2)
    elif band == "high":
        return round(random.uniform(2500000, 10000000), 2)
    else:
        return round(random.uniform(10000000, 30000000), 2)


def generate_credit_score(income):
    base = random.randint(650, 750)

    if income > 2500000:
        base += random.randint(20, 80)
    elif income < 500000:
        base -= random.randint(20, 80)

    return max(300, min(830, base))

def generate_custom_email(first_name, last_name, domain="example.com"):
    return f"{first_name}.{last_name}@{domain}"

def generate_health(age):
    height = round(random.uniform(150, 185), 2)
    weight = round(random.uniform(50, 100), 2)
    smoker = random.random() < 0.25
    chronic = age > 45 and random.random() < 0.4
    family_history = random.random() < 0.35
    stress = random.randint(1, 10)
    sleep = round(random.uniform(5.0, 8.5), 1)
    condition = random.choice(medical_conditions)
    return height, weight, smoker, chronic, family_history, stress, sleep, condition


# --------------------------
# Main Data Generation
# --------------------------

def customer_data(NUM_RECORDS, start_id):
    records = []

    for i in range(start_id, start_id +NUM_RECORDS + 1):

        gender = random.choice(genders)
        first_name = fake.first_name_male() if gender == "Male" else fake.first_name_female()
        last_name = fake.last_name_male()
        middle_name = random.choice([fake.first_name(), None])

        dob = fake.date_of_birth(minimum_age=18, maximum_age=75)
        age = datetime.now().year - dob.year

        state = random.choice(states)
        city = random.choice(cities[state])

        income = generate_income()
        credit_score = generate_credit_score(income)

        (
            height,
            weight,
            smoker,
            chronic,
            family_history,
            stress,
            sleep,
            condition
        ) = generate_health(age)

        created = fake.date_time_between(start_date="-3y", end_date="now")
        updated = datetime.now()

        record = (
            i,  # customer_id
            str(uuid.uuid4()),  # customer_external_ref
            random.randint(1, MAX_AGENT_ID),  # agent_id
            first_name,
            middle_name,
            last_name,
            dob,
            gender,
            random.choice(marital_statuses),
            generate_custom_email(first_name, last_name),
            "+91" + str(random.randint(6000000000, 9999999999)),
            fake.street_address(),
            city,
            state,
            str(random.randint(100000, 999999)),
            "India",
            random.choice(occupations),
            random.choice(employment_types),
            income,
            credit_score,
            height,
            weight,
            smoker,
            random.choice(alcohol_levels),
            random.choice(physical_levels),
            condition,
            chronic,
            family_history,
            stress,
            sleep,
            created,
            updated,
            "CRM_CORE",
            1  # record_version
        )

        records.append(record)
    return records
    # df = pd.DataFrame(records)

    # Save outputs
    # df.to_csv("crm_customers_india.csv", index=False)
    # df.to_json("crm_customers_india.json", orient="records", date_format="iso")

    # print("Data generation completed.")