import os, json
from db_utils import get_connection

DATA_DIR = "data/aggregated/transaction/country/india/state"

def load_aggregated_transaction():
    conn = get_connection()
    cursor = conn.cursor()

    for state in os.listdir(DATA_DIR):
        state_path = os.path.join(DATA_DIR, state)
        if not os.path.isdir(state_path): continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file in os.listdir(year_path):
                if not file.endswith(".json"): continue
                quarter = int(file.replace(".json", ""))
                file_path = os.path.join(year_path, file)
                try:
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        txns = data.get("data", {}).get("transactionData")
                        if not txns: continue
                        for txn in txns:
                            cursor.execute("""
                                INSERT INTO aggregated_transaction (year, quarter, state, transaction_type, count, amount)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (
                                int(year), quarter, state,
                                txn["name"],
                                txn["paymentInstruments"][0]["count"],
                                txn["paymentInstruments"][0]["amount"]
                            ))
                except Exception as e:
                    print(f"[ERROR] {file_path}: {e}")

    conn.commit(); conn.close()
    print("✅ aggregated_transaction loaded.")

if __name__ == "__main__":
    load_aggregated_transaction()
