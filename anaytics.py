import csv
import os
import psycopg2  # Used to connect Python to the PostgreSQL database

# ==========================================================
# 1. BLUEPRINT CLASS (Data Structure)
# ==========================================================
class SalesRecord:
    def __init__(self, row_id, order_id, order_date, customer_name, country, city):
        self.row_id = row_id
        self.order_id = order_id
        self.order_date = order_date
        self.customer_name = customer_name
        self.country = country
        self.city = city


# ==========================================================
# 2. INGESTOR CLASS (Data Processing Engine)
# ==========================================================
class DataIngestor:
    def __init__(self, file_path):
        self.file_path = file_path   
        self.records = []            

    def load_data(self):
        """Opens the CSV file and reads the first 5 records into memory."""
        if not os.path.exists(self.file_path):
            print(f"Error: File '{self.file_path}' not found!")
            return

        print("Starting to read data from CSV file...")
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)  # Skip the header row
                
                for count, row in enumerate(csv_reader):
                    if count >= 5:  # Load only the first 5 records for testing
                        break
                    
                    raw_date = row[2]
                    
                    # Mapping CSV columns to our SalesRecord object properties
                    record = SalesRecord(
                        row_id=int(row[0]),          
                        order_id=row[1],        
                        order_date=raw_date,      
                        customer_name=row[6],   
                        country=row[8],         
                        city=row[9]             
                    )
                    self.records.append(record)
            print(f"Successfully loaded {len(self.records)} records into Memory!")
        except Exception as e:
            print(f"Error while reading the file: {e}")

    def save_to_database(self):
        """Connects to the database and inserts the records from memory."""
        print("Connecting to the PostgreSQL database...")
        try:
            # ⚠️ CHANGE YOUR PASSWORD HERE
            conn = psycopg2.connect(
                host="localhost",
                database="analytics_db",
                user="postgres",
                password="sasaaa"  # <-- Enter your database password here
            )
            cursor = conn.cursor()
            print("Database connection successful!")

            # Inserting records one by one into the table
            for record in self.records:
                insert_query = """
                INSERT INTO sales_records (row_id, order_id, order_date, customer_name, country, city)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (row_id) DO NOTHING;
                """
                # ON CONFLICT prevents crashing if the data is already inserted
                
                cursor.execute(insert_query, (
                    record.row_id, 
                    record.order_id, 
                    record.order_date, 
                    record.customer_name, 
                    record.country, 
                    record.city
                ))
            
            # Commit changes permanently to the database
            conn.commit()
            print("All records have been successfully saved to PostgreSQL!")
            
            # Close the connection pipes safely
            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Error while saving to the database: {e}")


# ==========================================================
# 3. ENGINE EXECUTION (Main Start Switch)
# ==========================================================
if __name__ == "__main__":
    ingestor = DataIngestor("train.csv")
    ingestor.load_data()          # Step 1: Bring data from CSV to RAM
    ingestor.save_to_database()   # Step 2: Push data from RAM to Database