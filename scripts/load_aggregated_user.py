import os, json
from db_utils import get_connection

DATA_DIR = "data/aggregated/user/country/india/state"

def load_aggregated_user():
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
                        users = data.get("data", {}).get("usersByDevice")
                        if not users: continue
                        for user in users:
                            cursor.execute("""
                                INSERT INTO aggregated_user (year, quarter, state, brand, count, percentage)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (
                                int(year), quarter, state,
                                user.get("brand", "Unknown"),
                                user.get("count", 0),
                                user.get("percentage", 0.0)
                            ))
                except Exception as e:
                    print(f"[ERROR] {file_path}: {e}")

    conn.commit(); conn.close()
    print("✅ aggregated_user loaded.")

if __name__ == "__main__":
    load_aggregated_user()
