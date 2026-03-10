import random
import pandas as pd
from faker import Faker

fake = Faker("en_IN")

START_ID = 1001
END_ID = 1050

categories = [
    "Health Insurance",
    "Term Life",
    "Family Floater",
    "Senior Citizen",
    "Critical Illness",
    "ULIP Hybrid"
]

plan_types = ["Individual", "Family", "Group"]
coverage_types = ["Basic", "Comprehensive", "Premium"]
premium_frequencies = ["Monthly", "Quarterly", "Half-Yearly", "Yearly"]
product_statuses = ["Active", "Inactive"]


def generate_coverage(category):

    if category == "Senior Citizen":
        return random.choice([300000, 500000, 1000000])

    elif category == "Critical Illness":
        return random.choice([500000, 1000000, 2500000])

    else:
        return random.choice([500000, 1000000, 2000000, 5000000, 10000000])


def generate_base_premium(coverage):

    return round(coverage * random.uniform(0.01, 0.04), 2)


def generate_policy_products():

    records = []

    for pid in range(START_ID, END_ID + 1):

        category = random.choice(categories)
        coverage_amount = generate_coverage(category)
        base_premium = generate_base_premium(coverage_amount)

        deductible = random.choice([0, 10000, 25000, 50000])
        co_pay = random.choice([0, 10, 20, 30])
        no_claim_bonus = random.choice([5, 10, 20, 25])

        smoker_loading = random.choice([10, 15, 20, 30])
        bmi_threshold = random.choice([25, 27, 30])
        bmi_loading = random.choice([5, 10, 15])
        pre_existing_loading = random.choice([20, 30, 40, 50])
        waiting_period = random.choice([12, 24, 36, 48])

        record = {
            "policy_product_id": pid,
            "policy_code": f"POL{pid}",
            "product_name": f"{category} Plan {pid - 1000}",
            "product_category": category,
            "plan_type": random.choice(plan_types),
            "coverage_type": random.choice(coverage_types),
            "policy_term_years": random.choice([1, 5, 10, 15, 20]),

            "minimum_age": random.choice([18, 21, 25]),
            "maximum_age": random.choice([60, 65, 70, 75]),

            "base_premium_amount": base_premium,
            "premium_frequency": random.choice(premium_frequencies),
            "coverage_amount": coverage_amount,
            "deductible_amount": deductible,
            "co_payment_percentage": co_pay,
            "no_claim_bonus_percentage": no_claim_bonus,
            "max_claim_limit_per_year": coverage_amount,
            "lifetime_claim_limit": coverage_amount * random.choice([2, 3, 5]),

            "smoker_loading_percentage": smoker_loading,
            "bmi_loading_threshold": bmi_threshold,
            "bmi_loading_percentage": bmi_loading,
            "pre_existing_loading_percentage": pre_existing_loading,
            "pre_existing_waiting_period_months": waiting_period,

            "maternity_cover_flag": random.random() > 0.6,
            "critical_illness_cover_flag": category in ["Critical Illness", "Comprehensive"],

            "product_launch_date": fake.date_between(start_date="-10y", end_date="-1y"),
            "product_status": random.choices(product_statuses, weights=[85, 15])[0],
            "underwriting_required_flag": random.random() > 0.4,

            "created_at": fake.date_time_between(start_date="-10y", end_date="now")
        }

        records.append(record)

    df_products = pd.DataFrame(records)

    return df_products