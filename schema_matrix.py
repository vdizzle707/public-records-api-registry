#!/usr/bin/env python3
import sqlite3

def init():
    conn = sqlite3.connect("public_apis_registry.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS input_indicator_matrix (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input_param TEXT NOT NULL,
        indicator_name TEXT NOT NULL,
        data_source TEXT NOT NULL,
        resolution_type TEXT NOT NULL,
        UNIQUE(input_param, indicator_name)
    );
    """)
    conn.commit()
    conn.close()
    print("[INIT] input_indicator_matrix table initialized.")

if __name__ == "__main__":
    init()
