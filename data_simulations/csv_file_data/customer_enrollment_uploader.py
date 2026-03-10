from azure.storage.filedatalake import DataLakeServiceClient
from datetime import datetime
import io
import os
from dotenv import load_dotenv

from customer_enrollment import enrollment

# ----------------------------
# CONFIG
# ----------------------------
load_dotenv()
ACCOUNT_NAME = os.getenv("ACCOUNT_NAME")
ACCOUNT_KEY = os.getenv("ACCOUNT_KEY")

FILE_SYSTEM = "bronze"
TABLE_NAME = "customer_enrollment"

# -----------------------
# GENERATE DATA
# -----------------------
df = enrollment(100)

# Convert dataframe to CSV in memory
csv_buffer = io.StringIO()
df.to_csv(csv_buffer, index=False)

data = csv_buffer.getvalue().encode()

# -----------------------
# CONNECT TO ADLS
# -----------------------
account_url = f"https://{ACCOUNT_NAME}.dfs.core.windows.net"

service_client = DataLakeServiceClient(
    account_url=account_url,
    credential=ACCOUNT_KEY
)

file_system_client = service_client.get_file_system_client(FILE_SYSTEM)

# -----------------------
# PARTITION PATH
# -----------------------
today = datetime.today().strftime("%Y-%m-%d")
timestamp = datetime.now().strftime("%H%M%S")

directory_path = f"{TABLE_NAME}/ingestion_date={today}"

directory_client = file_system_client.get_directory_client(directory_path)

try:
    directory_client.create_directory()
except:
    pass

file_name = f"customer_enrollment_{timestamp}.csv"

file_client = directory_client.create_file(file_name)

file_client.append_data(data, offset=0, length=len(data))
file_client.flush_data(len(data))

print("Customer enrollment data uploaded to ADLS Bronze.")