import os
import pandas as pd
from sqlalchemy import create_engine

# Create the SQLAlchemy engine to connect to MySQL
db_user = "root"
db_password = ""
db_host = "localhost"
db_name = "sound"

# Format for SQLAlchemy connection string: mysql+mysqlconnector://user:password@host/database
engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}")

# Fetch directory list
dir_list = os.listdir()

# Remove unwanted directories if they exist
unwanted_dirs = ['.git', 'create_database.py']
dir_list = [d for d in dir_list if d not in unwanted_dirs]

# Prepare list to collect all data
data = []

for sound_name in dir_list:
    sub_dir = os.listdir(f'./{sound_name}')
    for phone in sub_dir:
        files = os.listdir(f'./{sound_name}/{phone}')
        for file in files:
            path = f"./{sound_name}/{phone}/{file}"

            # Append the data to the list
            data.append([sound_name, phone, path])

# Convert to pandas DataFrame
df = pd.DataFrame(data, columns=['soundName', 'phoneName', 'soundPath'])

# Display the DataFrame
print(df)

# Insert the DataFrame into MySQL table using SQLAlchemy engine
df.to_sql(name='sound_main', con=engine, if_exists='replace', index=True)
df.to_csv('sound_path.csv')