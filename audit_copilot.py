#!/usr/bin/env python3
import sys
import json
import re
from typing import Dict, Any, List

from engine_nlp import ConversationalEngine
from router import UnifiedRouter
from indicator_master import IndicatorLibrary
from lead_pipeline import DistressLeadEngine

INDICATOR_TAXONOMY = {
    "apn": "Assessor Parcel Number identifying the land unit with county tax collector.",
    "fips": "Federal Information Processing Standard 5-digit county identifier code.",
    "assessed_value": "Current statutory ad-valorem tax roll valuation (Land + Improvements).",
    "tax_delinquency": "Unpaid county property tax balance past statutory grace periods.",
    "lot_size": "Gross parcel square footage or acreage recorded on county plat maps.",
    "zoning_code": "Municipal land-use designation determining permitted physical development.",
    "gis_geometry": "Polygon coordinates for boundary verification and spatial intersections.",
    "grantor": "Transferor or seller relinquishing legal title in recorded deed conveyance.",
    "grantee": "Transferee or buyer acquiring legal title in recorded deed conveyance.",
    "sale_price": "Documentary transfer tax declared consideration paid for property.",
    "recording_date": "Timestamp when deed was stamped and indexed by County Recorder.",
    "document_type": "Instrument legal classification (Grant Deed, Quitclaim, Warranty).",
    "lis_pendens": "Formal recorded notice of pending judicial litigation against real property.",
    "notice_of_default": "Statutory pre-foreclosure notice filed by lender or trustee.",
    "auction_date": "Scheduled county trustee or sheriff sale date for auction.",
    "default_amount": "Arrearage balance required to cure default and reinstate loan.",
    "case_number": "Civil court or recorder docket tracking identifier.",
    "lien_type": "Classification of claim (IRS Federal Tax, Mechanic's, Judgment).",
    "open_balance": "Principal balance remaining on recorded voluntary/involuntary liens.",
    "judgment_amount": "Liquidated damages awarded by court attached as statutory lien.",
    "bankruptcy_chapter": "Federal bankruptcy jurisdiction (Chapter 7, 11, or 13).",
    "corporate_status": "Secretary of State standing (Active, Suspended, Dissolved).",
    "registered_agent": "Designated individual or entity authorized to receive legal service.",
    "ein": "Federal Employer Identification Number for business identity verification.",
    "ssn_verified": "Social Security Number cryptographic issuance verification flag.",
    "phone_carrier": "Originating telecommunications provider for skip-trace verification.",
    "alias_names": "Documented DBAs, maiden names, or known legal aliases."
}

class AuditCopilot:
    def __init__(self):
        self.nlp = ConversationalEngine()
        self.router = UnifiedRouter()
        self.indicator_lib = IndicatorLibrary()
        self.lead_engine = DistressLeadEngine()

    def audit_and_synthesize(self, prompt: str) -> Dict[str, Any]:
        analysis = self.nlp.parse_query(prompt)
        target_indicators = set(analysis.get("target_indicators", []))
        detected_params = analysis.get("detected_params", {})

        lower = prompt.lower()
        if any(w in lower for w in ["lead", "pipeline", "scoring", "export"]):
            target_indicators.update(["apn", "assessed_value", "tax_delinquency", "default_amount", "open_balance"])
        if any(w in lower for w in ["foreclose", "distress", "auction", "default", "trouble"]):
            target_indicators.update(["lis_pendens", "notice_of_default", "auction_date", "default_amount", "tax_delinquency", "case_number"])
        if any(w in lower for w in ["owner", "title", "buy", "sell", "deed", "transfer"]):
            target_indicators.update(["grantor", "grantee", "sale_price", "recording_date", "document_type", "corporate_status"])
        if any(w in lower for w in ["lien", "debt", "owe", "judgment", "irs", "court"]):
            target_indicators.update(["lien_type", "open_balance", "judgment_amount", "bankruptcy_chapter"])
        if any(w in lower for w in ["parcel", "apn", "lot", "land", "build", "zoning"]):
            target_indicators.update(["apn", "fips", "lot_size", "zoning_code", "assessed_value"])
        if any(w in lower for w in ["business", "company", "llc", "corp"]):
            target_indicators.update(["corporate_status", "registered_agent", "ein"])

        defined_indicators = {}
        for ind_name in sorted(target_indicators):
            matched = self.indicator_lib.get_indicator(ind_name)
            if matched:
                defined_indicators[matched["name"]] = f"{matched['description']} [DISCLOSURE: {matched['disclosure']}]"
            else:
                success, rec, _ = self.indicator_lib.register_indicator(
                    name=ind_name,
                    category="Discovered",
                    description=f"Auto-generated indicator for {ind_name}",
                    disclosure="Automated extraction. Requires county verification.",
                    data_type="Text"
                )
                defined_indicators[rec["name"]] = f"{rec['description']} [DISCLOSURE: {rec['disclosure']}]"

        execution_plan = []
        routes = analysis.get("suggested_routes", [])

        if routes:
            for step_idx, r in enumerate(routes, start=1):
                execution_plan.append({
                    "step": step_idx,
                    "action": f"Query {r['provider']} via {r['method']} {r['path']}",
                    "provider": r["provider"],
                    "endpoint": r["endpoint"],
                    "required_params": r["required_params"],
                    "harvests_indicators": [i for i in r["matched_indicators"] if i in target_indicators]
                })
        else:
            execution_plan.append({
                "step": 1,
                "action": "Broad FTS5 Registry Discovery",
                "provider": "DataGov / Registry FTS",
                "endpoint": "Federated Search",
                "required_params": ["query_term"],
                "harvests_indicators": list(target_indicators)
            })

        return {
            "prompt": prompt,
            "detected_params": detected_params,
            "indicators": defined_indicators,
            "plan": execution_plan
        }

    def execute_plan(self, plan_data: Dict[str, Any]):
        print("\n" + "="*65)
        print("  EXECUTING APPROVED PLAN // LIVE AUDIT RUNTIME")
        print("="*65)

        params = plan_data["detected_params"]
        for s in plan_data["plan"]:
            print(f"\n[RUNNING STEP {s['step']}] -> {s['action']}")
            provider = s["provider"].lower()

            if "propmix" in provider:
                apn = params.get("apn", "014-220-03")
                state = params.get("state", "CA")
                res = self.router.dispatch("propmix", "get_assessment", apn=apn, state=state, county="Mendocino")
            elif "data" in provider:
                term = params.get("apn") or "parcel"
                res = self.router.dispatch("datagov", "search_datasets", query_term=term, rows=1)
            elif "tracers" in provider:
                res = self.router.dispatch("tracers", "search_person", name="Target Entity", state=params.get("state", "CA"))
            else:
                res = {"success": False, "error": f"No client adapter for provider '{provider}'"}

            status = "SUCCESS" if res.get("success") else "HALTED / FAIL-CLOSED"
            print(f"  Status:       {status}")
            print(f"  Live Audited: {res.get('is_live_verified', False)}")
            if res.get("error"):
                print(f"  Notice:       {res['error']}")
            if res.get("data"):
                snippet = json.dumps(res['data'])[:120] + "..."
                print(f"  Payload:      {snippet}")

        print("\n[PLAN COMPLETE] Execution finished.")

    def run_interactive(self):
        print("─────────────────────────────────────────────────────────────")
        print("  CHRONOS AUDIT COPILOT // GOAL & INDICATOR SYNTHESIS        ")
        print("─────────────────────────────────────────────────────────────")
        while True:
            try:
                prompt = input("\n[ENTER GOAL / PROMPT] > ").strip()
                if not prompt:
                    continue
                if prompt.lower() in ("exit", "quit", "q"):
                    print("Copilot offline.")
                    break

                result = self.audit_and_synthesize(prompt)
                print("\n" + "─"*65)
                print(f"Goal: {result['prompt']}")
                print(f"Extracted Params: {result['detected_params'] or 'None (using defaults)'}\n")
                print(f"Synthesized Indicators ({len(result['indicators'])} Total):")
                for ind, desc in result["indicators"].items():
                    print(f"  • {ind.ljust(20)} : {desc}")

                print("\nProposed Step-by-Step Execution Plan:")
                for step in result["plan"]:
                    print(f"  [Step {step['step']}] {step['action']}")
                    print(f"           Params:  {step['required_params']}")
                    print(f"           Targets: {', '.join(step['harvests_indicators']) or 'All'}")

                print("\n" + "─"*65)
                approval = input("[APPROVAL REQUIRED] Authorize execution of this plan? (Y/N): ").strip().lower()
                print("─"*65)

                if approval in ("y", "yes"):
                    self.execute_plan(result)
                else:
                    print("[ABORTED] Plan rejected by operator. Standby.")

            except (KeyboardInterrupt, EOFError):
                print("\nSession ended.")
                break

if __name__ == "__main__":
    copilot = AuditCopilot()
    copilot.run_interactive()
