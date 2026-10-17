import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

print("Starting the Netflix Churn Data Pipeline...")
# 1. Load your specific Netflix Churn CSV file
try:
    df = pd.read_csv("netflix_customer_churn.csv")
    print(" Successfully read netflix_customer_churn.csv")
except FileNotFoundError:
    print("Error: Could not find 'netflix_customer_churn.csv' in this folder!")
    print("Please make sure the file name matches exactly (all lowercase, with underscores).")
    exit()

# 2. General Data Cleaning using Pandas
# Convert all column names to lowercase with underscores to make SQL querying much easier
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Handle any missing values generally across the dataset
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].fillna('Unknown')
    else:
        # If numeric, fill missing numbers with 0 or the median
        df[col] = df[col].fillna(0)

print(f"Data cleaning complete. Columns found: {list(df.columns)}")

# 3. Create an SQLite Database connection (No Passwords Required!)
engine = create_engine('sqlite:///netflix_analytics_data.db')

# 4. Push data directly into the database table 'netflix_churn'
try:
    print(" Pushing cleaned churn data to the SQL database...")
    df.to_sql('netflix_churn', engine, if_exists='replace', index=False)
    print(" SUCCESS! Data successfully loaded into 'netflix_data.db' under table 'netflix_churn'!")
except Exception as e:
    print(f" Database Error: {e}")

try:
    print(" Deploying SQL Analytics View for Tableau...")
    with engine.connect() as conn:
        # Drop the view if it exists so the script never crashes on repeat runs
        conn.execute(sqlalchemy.text("DROP VIEW IF EXISTS v_tableau_netflix_analytics;"))
        
        # Write your exact analytical query as a permanent database view
        view_query = """
        CREATE VIEW v_tableau_netflix_analytics AS
        SELECT 
            user_id, gender, age, country, join_date,
            subscription_type, monthly_fee, device,
            watch_hours, avg_watch_time_per_day, favorite_genre,
            churned,
            CASE WHEN churned = 1 THEN 'Churned' ELSE 'Retained' END AS retention_status
        FROM netflix_churn
        WHERE subscription_type IS NOT NULL AND watch_hours >= 0;
        """
        conn.execute(sqlalchemy.text(view_query))
        print("SUCCESS! Database View 'v_tableau_netflix_analytics' is live!")
except Exception as e:
    print(f"View Creation Error: {e}")
    # 5. Automatically create the Tableau BI Semantic Layer View
# 5. Automatically create the Tableau BI Semantic Layer View
# 5. Automatically create the Tableau BI Semantic Layer View
try:
    print("[INFO] Deploying SQL Analytics View for Tableau...")
    with engine.connect() as conn:
        # Drop the view if it exists so the script never crashes on repeat runs
        conn.execute(sqlalchemy.text("DROP VIEW IF EXISTS v_tableau_netflix_analytics;"))
        
        # Updated query using customer_id and region to match your database columns
        view_query = """
        CREATE VIEW v_tableau_netflix_analytics AS
        SELECT 
            customer_id, gender, age, region, join_date, subscription_type, 
            monthly_fee, device, watch_hours, avg_watch_time_per_day, 
            favorite_genre, churned,
            CASE 
                WHEN churned = 1 THEN 'Churned' 
                ELSE 'Retained' 
            END AS retention_status
        FROM netflix_churn
        WHERE subscription_type IS NOT NULL AND watch_hours >= 0;
        """
        conn.execute(sqlalchemy.text(view_query))
        print("[SUCCESS] Database View 'v_tableau_netflix_analytics' is live!")
except Exception as e:
    print(f"[ERROR] View Creation Error: {e}")
    # 5. Automatically create the Tableau BI Semantic Layer View
try:
    print("[INFO] Deploying SQL Analytics View for Tableau...")
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("DROP VIEW IF EXISTS v_netflix_final_analytics;"))
        
        view_query = """
        CREATE VIEW v_netflix_final_analytics AS
        SELECT 
            customer_id, gender, age, region, subscription_type, 
            monthly_fee, device, watch_hours, avg_watch_time_per_day, 
            favorite_genre, churned,
            CASE 
                WHEN churned = 1 THEN 'Churned' 
                ELSE 'Retained' 
            END AS retention_status
        FROM netflix_churn
        WHERE subscription_type IS NOT NULL AND watch_hours >= 0;
        """
        conn.execute(sqlalchemy.text(view_query))
        print("[SUCCESS] New Database View is live!")
except Exception as e:
    print(f"[ERROR] View Creation Error: {e}")

