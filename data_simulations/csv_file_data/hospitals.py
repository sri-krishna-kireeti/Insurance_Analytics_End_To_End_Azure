import random
import pandas as pd
from faker import Faker

fake = Faker("en_IN")

hospital_types = [
    "Government",
    "Private",
    "Multi-Specialty",
    "Super-Specialty",
    "Clinic"
]

regions = {
    "South": ["Hyderabad", "Bengaluru", "Chennai", "Coimbatore"],
    "North": ["Delhi", "Jaipur", "Lucknow"],
    "East": ["Kolkata", "Patna"],
    "West": ["Mumbai", "Pune", "Ahmedabad"],
    "Central": ["Bhopal", "Indore"]
}

tier1_cities = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Hyderabad"]


def generate_bed_capacity(h_type):
    if h_type == "Clinic":
        return random.randint(10, 40)
    elif h_type == "Government":
        return random.randint(100, 500)
    elif h_type == "Private":
        return random.randint(50, 300)
    elif h_type == "Multi-Specialty":
        return random.randint(200, 600)
    else:
        return random.randint(300, 1000)


def generate_avg_claim_cost(h_type, city):

    if h_type == "Clinic":
        base = random.uniform(15000, 40000)
    elif h_type == "Government":
        base = random.uniform(20000, 80000)
    elif h_type == "Private":
        base = random.uniform(50000, 200000)
    elif h_type == "Multi-Specialty":
        base = random.uniform(100000, 400000)
    else:
        base = random.uniform(200000, 800000)

    if city in tier1_cities:
        base *= 1.3

    return round(base, 2)


def generate_hospitals(NUM_HOSPITALS=500):

    records = []
    hospital_id_counter = 1

    for region, cities in regions.items():

        for _ in range(NUM_HOSPITALS // len(regions)):

            city = random.choice(cities)
            h_type = random.choice(hospital_types)

            network = random.random() < 0.7

            rating = round(
                min(5.0, max(2.5, random.gauss(4.0 if network else 3.5, 0.4))),
                2
            )

            record = {
                "hospital_id": hospital_id_counter,
                "hospital_name": fake.company() + " Hospital",
                "hospital_type": h_type,
                "network_flag": network,
                "empanelment_date": fake.date_between(start_date="-10y", end_date="-1y") if network else None,
                "city": city,
                "state": fake.state(),
                "region": region,
                "bed_capacity": generate_bed_capacity(h_type),
                "rating": rating,
                "average_claim_cost": generate_avg_claim_cost(h_type, city)
            }

            records.append(record)
            hospital_id_counter += 1

    df_hospitals = pd.DataFrame(records)

    return df_hospitals