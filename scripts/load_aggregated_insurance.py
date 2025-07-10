import os, json
from db_utils import get_connection

DATA_DIR = "data/aggregated/insurance/country/india/state"

def load_aggregated_insurance():
    conn = get_connection()
    cursor = conn.cursor()

    for state in os.listdir(DATA_DIR):
        state_dir = os.path.join(DATA_DIR, state)
        if not os.path.isdir(state_dir): continue
        for year in os.listdir(state_dir):
            year_dir = os.path.join(state_dir, year)
            for file in os.listdir(year_dir):
                if not file.endswith(".json"): continue
                quarter = int(file.replace(".json", ""))
                file_path = os.path.join(year_dir, file)
                try:
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        txns = data.get("data", {}).get("transactionData", [])
                        for txn in txns:
                            if txn.get("name") != "Insurance":
                                continue
                            instruments = txn.get("paymentInstruments", [])
                            for instrument in instruments:
                                count = instrument.get("count", 0)
                                amount = instrument.get("amount", 0.0)
                                cursor.execute("""
                                    INSERT INTO aggregated_insurance (year, quarter, state, count, amount)
                                    VALUES (?, ?, ?, ?, ?)
                                """, (int(year), quarter, state, count, amount))
                except Exception as e:
                    print(f"[ERROR] {file_path}: {e}")

    conn.commit(); conn.close()
    print("✅ aggregated_insurance loaded.")

if __name__ == "__main__":
    load_aggregated_insurance()
