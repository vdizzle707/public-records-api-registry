#!/usr/bin/env python3
"""
CHRONOS OS // INPUT PARAMETER MATRIX RESOLVER
Calculates available indicators from supplied parameter sets and prints
an operational dependency table.
"""

import sys
import sqlite3

class MatrixResolver:
    def __init__(self, db_path="public_apis_registry.db"):
        self.db_path = db_path

    def inspect_dependencies(self, available_inputs):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        placeholders = ",".join(["?"] * len(available_inputs))
        query = f"""
            SELECT m.input_param, m.indicator_name, m.data_source, m.resolution_type,
                   COALESCE(i.category, 'General') as category,
                   COALESCE(i.data_type, 'String') as data_type
            FROM input_indicator_matrix m
            LEFT JOIN indicator_master i ON m.indicator_name = i.name
            WHERE m.input_param IN ({placeholders})
            ORDER BY m.input_param, m.indicator_name
        """
        rows = [dict(r) for r in c.execute(query, available_inputs).fetchall()]
        
        # Summary counts
        total_possible = c.execute("SELECT COUNT(DISTINCT indicator_name) FROM input_indicator_matrix").fetchone()[0]
        conn.close()

        unlocked_count = len(set(r["indicator_name"] for r in rows))
        coverage_pct = (unlocked_count / total_possible * 100) if total_possible else 0

        print("=" * 72)
        print("  INPUT PARAMETER -> INDICATOR RESOLUTION MATRIX")
        print("=" * 72)
        print(f"Inputs Provided: {', '.join(available_inputs)}")
        print(f"Coverage:        {unlocked_count} of {total_possible} indicators unlocked ({coverage_pct:.1f}%)\n")

        print(f"{'INPUT KEY':<14} | {'INDICATOR NAME':<30} | {'DATA SOURCE':<22}")
        print("-" * 72)
        for r in rows:
            print(f"{r['input_param']:<14} | {r['indicator_name']:<30} | {r['data_source']:<22}")

        print("\n" + "=" * 72)
        print("MISSING INPUTS CHECK:")
        all_possible_inputs = ["lat_lon", "apn", "fips", "address", "query_isp"]
        missing = [i for i in all_possible_inputs if i not in available_inputs]
        if missing:
            print(f"To achieve 100% resolution, supply: {', '.join(missing)}")
        else:
            print("Full parameter set supplied. Maximum indicator yield active.")
        print("=" * 72)

if __name__ == "__main__":
    inputs = sys.argv[1:] if len(sys.argv) > 1 else ["lat_lon", "apn"]
    resolver = MatrixResolver()
    resolver.inspect_dependencies(inputs)
