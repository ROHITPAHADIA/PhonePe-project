import os, json
from db_utils import get_connection

DATA_DIR = "data/map/user/hover/country/india/state"

def load_map_user():
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
                        districts = data.get("data", {}).get("hoverData", {})
                        for district, stats in districts.items():
                            cursor.execute("""
                                INSERT INTO map_user (year, quarter, state, district, registered_users, app_opens)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (
                                int(year), quarter, state, district,
                                stats.get("registeredUsers", 0),
                                stats.get("appOpens", 0)
                            ))
                except Exception as e:
                    print(f"[ERROR] {file_path}: {e}")

    conn.commit(); conn.close()
    print("✅ map_user loaded.")

if __name__ == "__main__":
    load_map_user()
