import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("en_IN")

POLICY_PRODUCT_IDS = list(range(1001, 10000))
MAX_POLICIES_PER_CUSTOMER = 3

insurance_prefix = ["LIC", "HDFC", "ICIC", "SBI", "TATA"]

today = datetime.today().date()

def enrollment(NUM_CUSTOMERS = 100):
    records = []
    customer_policy_id_counter = 1

    for customer_id in range(1, NUM_CUSTOMERS + 1):
        num_policies = random.randint(1, MAX_POLICIES_PER_CUSTOMER)
        for _ in range(num_policies):
            product_id = random.choice(POLICY_PRODUCT_IDS)
            enrollment_date = fake.date_between(start_date="-5y", end_date="-30d")

            policy_term_years = random.choice([1, 5, 10, 15])
            policy_start_date = enrollment_date
            policy_end_date = policy_start_date + timedelta(days=365 * policy_term_years)

            renewal_count = max(0, (today.year - policy_start_date.year) // policy_term_years)

            auto_renew = random.random() < 0.6
            renewal_date = policy_end_date if auto_renew else None

            # Policy status logic
            if policy_end_date < today:
                policy_status = random.choices(
                    ["Expired", "Renewed"],
                    weights=[40, 60]
                )[0]
            else:
                policy_status = random.choices(
                    ["Active", "Cancelled"],
                    weights=[85, 15]
                )[0]

            underwriting_status = random.choices(
                ["Approved", "Manual Review", "Rejected"],
                weights=[75, 20, 5]
            )[0]

            policy_number = (
                random.choice(insurance_prefix)
                + "-"
                + str(enrollment_date.year)
                + "-"
                + str(customer_policy_id_counter).zfill(8)
            )

            record = {
                "customer_policy_id": customer_policy_id_counter,
                "policy_number": policy_number,
                "customer_id": customer_id,
                "policy_product_id": product_id,
                "enrollment_date": enrollment_date,
                "policy_start_date": policy_start_date,
                "policy_end_date": policy_end_date,
                "renewal_date": renewal_date,
                "policy_status": policy_status,
                "underwriting_status": underwriting_status,
                "payment_mode_preference": random.choice(
                    ["UPI", "Credit Card", "Debit Card", "Net Banking", "ECS"]
                ),
                "auto_renew_flag": auto_renew,
                "renewal_count": renewal_count,
                "created_at": fake.date_time_between(start_date=enrollment_date, end_date="now")
            }

            records.append(record)
            customer_policy_id_counter += 1

    df_enrollment = pd.DataFrame(records)
    return df_enrollment

    # df_enrollment.to_csv("customer_enrollment_india.csv", index=False)
