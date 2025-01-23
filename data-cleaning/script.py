import sqlite3
import pandas as pd
import os
import logging
import numpy as np

# This is the main script that handles data cleaning, loading, querying, and saving results

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Absolute paths based on script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  
RAW_DATA_PATH = os.path.join(SCRIPT_DIR, "../raw-data")  
CLEANED_DATA_PATH = os.path.join(SCRIPT_DIR, "clean_data")  
QUERY_PATH = os.path.join(SCRIPT_DIR, "../sql-queries")  
QUERY_RESULTS_PATH = os.path.join(SCRIPT_DIR, "query_results")

# Database file name
DB_NAME = os.path.join(SCRIPT_DIR, "fetch_data.db") 

# Data file paths for CSV files in raw data folder
CSV_FILES = {
    "users": os.path.join(RAW_DATA_PATH, "USER_TAKEHOME.csv"),
    "transactions": os.path.join(RAW_DATA_PATH, "TRANSACTION_TAKEHOME.csv"),
    "products": os.path.join(RAW_DATA_PATH, "PRODUCTS_TAKEHOME.csv")
}

# Create the SQLite database that we will use to query the data
def create_database():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        logging.info(f"Existing database '{DB_NAME}' deleted.")
    
    conn = sqlite3.connect(DB_NAME)
    logging.info(f"Database '{DB_NAME}' created successfully.")
    conn.close()

# Clean data before loading into the database and querying it
def clean_data(df, table_name):
    try:
        # Remove extra spaces from column names
        df.columns = df.columns.str.strip()
        
        # Remove leading/trailing spaces from all string values in the dataframe
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        
        # Convert all columns containing 'DATE' in their name to timezone-aware datetime (UTC)
        date_columns = [col for col in df.columns if 'DATE' in col.upper()]
        df[date_columns] = df[date_columns].apply(lambda x: pd.to_datetime(x, errors='coerce', utc=True))

        # Handling barcode column here since it is a field in both Transactions and Products tables
        if 'BARCODE' in df.columns:
            df['BARCODE'] = pd.to_numeric(df['BARCODE'], errors='coerce')
            df['BARCODE'] = df['BARCODE'].fillna(0).astype('Int64') 
        
        # Handle users table
        if table_name == "users": 
            df["STATE"] = df["STATE"].replace("", "UNKNOWN").str.upper()
            df["GENDER"] = df["GENDER"].fillna("unknown")
            df["LANGUAGE"] = df["LANGUAGE"].replace("", "unknown")
        
        # Handle transactions table
        elif table_name == "transactions":
            if 'FINAL_SALE' in df.columns:
                df['FINAL_SALE'] = pd.to_numeric(df['FINAL_SALE'], errors='coerce').fillna(0.0)
                df.rename(columns={"FINAL_SALE": "SALE"}, inplace=True)
            if 'FINAL_QUANTITY' in df.columns:
                df['FINAL_QUANTITY'] = pd.to_numeric(df['FINAL_QUANTITY'], errors='coerce').fillna(0)
                df.rename(columns={"FINAL_QUANTITY": "QUANTITY"}, inplace=True)
            df.dropna(subset=["USER_ID", "BARCODE"], inplace=True)
        
        # Handle products table
        elif table_name == "products":
            df["CATEGORY_1"] = df["CATEGORY_1"].fillna("UNKNOWN")
        
        return df

    except Exception as e:
        logging.error(f"Error cleaning data for table {table_name}: {e}")
        return pd.DataFrame()

# For saving cleaned data to the cleaned_data folder
def save_cleaned_data(df, table_name):
    if not os.path.exists(CLEANED_DATA_PATH):
        os.makedirs(CLEANED_DATA_PATH)
    cleaned_file_path = os.path.join(CLEANED_DATA_PATH, f"{table_name}_cleaned.csv")
    df.to_csv(cleaned_file_path, index=False)
    logging.info(f"Cleaned data saved to '{cleaned_file_path}'")

# Clean, save, and load CSV files into the database as tables
def load_csv_to_db():
    conn = sqlite3.connect(DB_NAME)

    for table_name, file_path in CSV_FILES.items():
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path, dtype=str).fillna("")  # Read CSV as strings
                df = clean_data(df, table_name)  # Clean the data
                if df.empty:
                    logging.warning(f"Skipping empty cleaned data for table '{table_name}'.")
                    continue
                save_cleaned_data(df, table_name)  # Save cleaned data to folder
                df.to_sql(table_name, conn, if_exists="replace", index=False)
                logging.info(f"Loaded '{file_path}' into '{table_name}' table.")
            except Exception as e:
                logging.error(f"Error loading CSV '{file_path}' into table '{table_name}': {e}")
        else:
            logging.warning(f"File '{file_path}' not found. Skipping...")

    conn.close()

# Read SQL queries from files
def read_sql_file(file_name):
    query_file_path = os.path.join(QUERY_PATH, file_name)
    try:
        if os.path.exists(query_file_path):
            with open(query_file_path, 'r') as file:
                return file.read()
        else:
            logging.warning(f"SQL file '{file_name}' not found.")
            return None
    except Exception as e:
        logging.error(f"Error reading SQL file '{file_name}': {e}")
        return None

# Run SQL query and save result as Pandas DataFrame
def run_query(query):
    try:
        conn = sqlite3.connect(DB_NAME)
        result = pd.read_sql_query(query, conn)
        conn.close()
        return result
    except Exception as e:
        logging.error(f"Error running SQL query: {e}")
        return pd.DataFrame()

# Save query results to CSV file in query_results folder
def save_query_results(df, query_name):
    if not os.path.exists(QUERY_RESULTS_PATH):
        os.makedirs(QUERY_RESULTS_PATH)
    result_file_path = os.path.join(QUERY_RESULTS_PATH, f"{query_name}.csv")
    df.to_csv(result_file_path, index=False)
    logging.info(f"Query results saved to '{result_file_path}'")

# This is the main function that orchestrates the entire process
def main():
    # Step 1: Create database
    create_database()
    
    # Step 2: Load cleaned CSVs into database
    load_csv_to_db()
    
    # Step 3: Run SQL queries from files and save results
    query_files = [
        "fetch-growth-by-year.sql",
        "top-brands-established-users.sql",
        "top-brands-over-21.sql"
    ]

    for query_file in query_files:
        logging.info(f"\nRunning query from file: {query_file}")
        sql = read_sql_file(query_file)
        if sql:
            result_df = run_query(sql)
            if not result_df.empty:
                save_query_results(result_df, query_file.split('.')[0])
            else:
                logging.warning(f"No results returned for query '{query_file}'.")

if __name__ == "__main__":
    main()

