import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

updates = {
    "None_Type": "None-Type",
    "None-type": "None-Type",
    "none_type": "None-Type",
    "meta_based": "Meta-Based",
    "boolean-based": "Boolean-Based",
    "stackqueries_based": "Stacked-Queries-Based"
}

for old, new in updates.items():
    cursor.execute(
        "UPDATE logs SET attack_type = ? WHERE attack_type = ?",
        (new, old)
    )

conn.commit()
conn.close()

print("Old log labels cleaned successfully.")