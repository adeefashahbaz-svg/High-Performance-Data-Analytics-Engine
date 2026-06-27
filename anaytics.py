import csv
import os

# ==========================================
# 1. BLUEPRINT CLASS (Data Structure)
# ==========================================
class SalesRecord:
    def __init__(self, row_id, order_id, order_date, customer_name, country, city):
        self.row_id = row_id
        self.order_id = order_id
        self.order_date = order_date
        self.customer_name = customer_name
        self.country = country
        self.city = city

    def display_summary(self):
        print(f"Order ID: {self.order_id} | Customer: {self.customer_name} | Location: {self.city}, {self.country}")


# ==========================================
# 2. INGESTOR CLASS (The Machine)
# ==========================================
class DataIngestor:
    def __init__(self, file_path):
        self.file_path = file_path   
        self.records = []            

    def load_data(self):
        if not os.path.exists(self.file_path):
            print(f"Error: Aapki file '{self.file_path}' is folder mein nahi mili!")
            print(f"Solution: Check karein ke 'train.csv' aur 'analytics.py' dono ek hi folder mein hain.")
            return

        print("Data read hona shuru ho raha hai...")
        
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader) 
                
                for count, row in enumerate(csv_reader):
                    if count >= 5: 
                        break
                    
                    record = SalesRecord(
                        row_id=row[0],          
                        order_id=row[1],        
                        order_date=row[2],      
                        customer_name=row[6],   
                        country=row[8],         
                        city=row[9]             
                    )
                    self.records.append(record)
                    
            print(f"Successfully loaded {len(self.records)} records into Memory!\n")
            
        except Exception as e:
            print(f"Kuch galat hua: {e}")

    def show_records(self):
        print("--- SHOWING RECORDS FROM RAM ---")
        for record in self.records:
            record.display_summary()
        print("--------------------------------")


# ==========================================
# 3. ENGINE EXECUTION (The Start Button)
# ==========================================
if __name__ == "__main__":
    ingestor = DataIngestor("train.csv")
    ingestor.load_data()
    ingestor.show_records()          
