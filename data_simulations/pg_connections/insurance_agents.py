import random
from faker import Faker

fake = Faker("en_IN")

NUM_AGENTS = 200

regions = ["South", "North", "East", "West", "Central"]

branch_codes = {
    "South": ["HYD01", "BLR01", "CHE01"],
    "North": ["DEL01", "LKO01", "JAI01"],
    "East": ["KOL01", "PAT01"],
    "West": ["MUM01", "PUN01", "AHM01"],
    "Central": ["BPL01", "IND01"]
}

regional_heads = range(1, 6)
branch_managers = range(6, 31)
field_agents = range(31, 201)


def generate_agents_data(agent_id_counter):

    records = []

    for agent_id in range(agent_id_counter, agent_id_counter + NUM_AGENTS):

        region = random.choice(regions)
        branch = random.choice(branch_codes[region])

        joining_date = fake.date_between(start_date="-15y", end_date="-6m")

        performance = round(
            min(5.0, max(1.0, random.gauss(3.8, 0.6))), 2
        )

        if agent_id in regional_heads:
            commission = round(random.uniform(18, 25), 2)
            manager_id = None

        elif agent_id in branch_managers:
            commission = round(random.uniform(12, 20), 2)
            manager_id = int(random.choice(list(regional_heads)))

        else:
            commission = round(random.uniform(5, 15), 2)
            manager_id = int(random.choice(list(branch_managers)))

        active_flag = random.random() > 0.1

        created_at = fake.date_time_between(start_date="-15y", end_date="now")

        record_tuple = (
            agent_id,
            fake.name(),
            "IRDAI-" + str(random.randint(100000, 999999)),
            region,
            branch,
            joining_date,
            commission,
            performance,
            active_flag,
            manager_id,
            created_at
        )

        records.append(record_tuple)

    return records