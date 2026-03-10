import random
from faker import Faker
from datetime import timedelta

fake = Faker("en_IN")

ROOM_TYPES = {
    "General": 1.0,
    "Semi-Private": 1.2,
    "Private": 1.5,
    "ICU": 2.5
}

CLAIM_STATUS_WEIGHTS = {
    "Approved": 65,
    "Partially Approved": 15,
    "Rejected": 15,
    "Under Investigation": 5
}

DIAGNOSIS_LIST = [
    ("I10", "Hypertension"),
    ("E11", "Type 2 Diabetes"),
    ("J18", "Pneumonia"),
    ("N20", "Kidney Stone"),
    ("K35", "Appendicitis"),
    ("I21", "Heart Attack")
]


def _weighted_choice(weight_dict):
    choices = list(weight_dict.keys())
    weights = list(weight_dict.values())
    return random.choices(choices, weights=weights)[0]


def generate_claims_data(
        num_policies,  claim_id_counter,
        num_hospitals: int = 500
):
    """
    Generates synthetic insurance claims data.

    Returns:
        List[Tuple] -> Ready for Postgres bulk insert
    """

    records = []

    for policy_id in range(1, num_policies + 1):
        hospital_id = random.randint(1, num_hospitals)

        claim_date = fake.date_between(start_date="-3y", end_date="today")
        hospitalization_date = claim_date - timedelta(days=random.randint(1, 5))
        discharge_date = hospitalization_date + timedelta(days=random.randint(1, 10))

        diagnosis_code, diagnosis_desc = random.choice(DIAGNOSIS_LIST)
        room_type = random.choice(list(ROOM_TYPES.keys()))

        base_bill = random.uniform(30000, 300000)
        total_bill = round(base_bill * ROOM_TYPES[room_type], 2)

        claimed_amount = total_bill
        status = _weighted_choice(CLAIM_STATUS_WEIGHTS)

        if status == "Approved":
            approved_amount = claimed_amount
            rejected_amount = 0
            rejection_reason = None
            settlement_date = claim_date + timedelta(days=random.randint(3, 15))

        elif status == "Partially Approved":
            approved_amount = round(claimed_amount * random.uniform(0.6, 0.9), 2)
            rejected_amount = round(claimed_amount - approved_amount, 2)
            rejection_reason = "Policy Sub-limit"
            settlement_date = claim_date + timedelta(days=random.randint(5, 20))

        elif status == "Rejected":
            approved_amount = 0
            rejected_amount = claimed_amount
            rejection_reason = random.choice([
                "Pre-existing condition not covered",
                "Waiting period not completed",
                "Policy expired"
            ])
            settlement_date = None

        else:  # Under Investigation
            approved_amount = 0
            rejected_amount = 0
            rejection_reason = None
            settlement_date = None

        processing_days = (
            (settlement_date - claim_date).days
            if settlement_date else random.randint(5, 30)
        )

        created_at = fake.date_time_between(start_date=claim_date, end_date="now")

        record_tuple = (
            claim_id_counter,
            f"CLM-{str(claim_id_counter).zfill(8)}",
            policy_id,
            hospital_id,
            claim_date,
            hospitalization_date,
            discharge_date,
            diagnosis_code,
            diagnosis_desc,
            room_type,
            total_bill,
            claimed_amount,
            approved_amount,
            rejected_amount,
            status,
            rejection_reason,
            settlement_date,
            processing_days,
            created_at
        )

        records.append(record_tuple)
        claim_id_counter += 1

    return records


