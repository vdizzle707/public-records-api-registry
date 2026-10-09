#!/usr/bin/env python3
"""
CHRONOS OS // ENTERPRISE INDICATOR TAXON EXPANSION (100+ INDICATORS)
Expands the master repository across environmental, mortgage/securitization, tax roll,
probate, municipal code enforcement, and UCC/corporate assets.
"""

from indicator_master import IndicatorLibrary
import sqlite3

EXPANDED_TAXONOMY = [
    # ── 1. ENVIRONMENTAL, TOPOGRAPHY & NATURAL HAZARDS ──
    ("flood_zone", "Environmental / Hazard", "FEMA Special Flood Hazard Area (SFHA) designation (e.g., Zone A, AE, V, X).", "Determines mandatory federal flood insurance purchase requirements under NFIP. Affects debt service and insurability.", "String", ["fema_zone", "flood_hazard_zone", "floodplain"]),
    ("base_flood_elevation", "Environmental / Hazard", "FEMA modeled water surface elevation of a 100-year flood event.", "Critical for building pad permits and elevation certificate compliance.", "Float (Feet)", ["bfe", "flood_elevation"]),
    ("wildfire_hazard_severity", "Environmental / Hazard", "CAL FIRE / State Fire Marshal hazard classification (LRA/SRA: Moderate, High, Very High).", "Very High Fire Hazard Severity Zones (VHFHSZ) trigger mandatory defensible space and strict home-hardening building codes.", "String (Enum)", ["fire_zone", "vhfhsz", "wildfire_risk"]),
    ("wetlands_flag", "Environmental / Conservation", "USFWS National Wetlands Inventory (NWI) jurisdictional wetlands indicator.", "Triggers Clean Water Act Section 404 Army Corps of Engineers permitting; severely limits physical land disturbance.", "Boolean", ["nwi_wetland", "jurisdictional_wetland"]),
    ("earthquake_fault_zone", "Environmental / Seismic", "State geological survey designated active fault rupture hazard zone (e.g., Alquist-Priolo).", "Prohibits human-occupancy structures directly astride active fault traces; requires licensed geologic fault investigation.", "Boolean", ["alquist_priolo", "fault_zone", "seismic_fault"]),
    ("liquefaction_susceptibility", "Environmental / Seismic", "Susceptibility of saturated granular soil to strength loss during ground shaking.", "Requires deep foundation engineering, pile driving, or soil densification mitigation.", "String (Enum: Low/Med/High)", ["liquefaction_zone", "soil_liquefaction"]),
    ("slope_percentage", "Topography & Engineering", "Degrees of inclination or percent slope across parcel topography.", "Municipal grading ordinances prohibit or heavily restrict building pads on slopes exceeding 15-20%.", "Float (Percentage)", ["grade_slope", "topographic_slope", "incline"]),
    ("soil_classification", "Topography & Agriculture", "USDA NRCS soil survey taxonomy and prime farmland rating.", "Governs agricultural yield, septic drainfield absorption viability, and structural foundation expansive clay risks.", "String", ["usda_soil", "soil_type", "soil_map_unit"]),
    ("sea_level_rise_exposure", "Environmental / Climate", "NOAA projected coastal inundation under progressive 1-6 foot sea rise models.", "Governs coastal development permits (CDP) under state Coastal Commissions.", "Float (Feet)", ["slr_risk", "coastal_inundation"]),
    ("superfund_npl_proximity", "Environmental / Contamination", "Proximity distance to EPA Comprehensive Environmental Response (CERCLA) Superfund site.", "Creates potential joint and strict liability under federal CERCLA without bona fide prospective purchaser status.", "Float (Miles)", ["cercla_site", "epa_superfund", "toxic_proximity"]),

    # ── 2. MORTGAGE, NOTE & SECURITIZATION TELEMETRY ──
    ("original_loan_amount", "Mortgage & Securitization", "Original face value of promissory note secured by deed of trust.", "Does not reflect amortization; baseline used for calculating original loan-to-value (LTV).", "Currency (USD)", ["note_amount", "original_principal", "face_value_loan"]),
    ("interest_rate_type", "Mortgage & Securitization", "Interest rate classification: Fixed Rate (FRM), Adjustable (ARM), or Variable.", "ARM notes in high-interest environments signal imminent debt-service reset shocks.", "String (Enum: Fixed, ARM)", ["rate_type", "loan_type_rate", "rate_structure"]),
    ("current_interest_rate", "Mortgage & Securitization", "Effective nominal interest rate recorded on promissory note or modification agreement.", "Critical for debt-service coverage ratio (DSCR) underwriting.", "Float (Percentage)", ["nominal_rate", "note_rate", "mortgage_rate"]),
    ("loan_maturity_date", "Mortgage & Securitization", "Stated legal maturity date of promissory note.", "Matured loans with unpaid principal balloons represent high-priority recapitalization or distress opportunities.", "ISO-8601 Date", ["maturity_date", "note_expiration", "balloon_date"]),
    ("lender_name", "Mortgage & Securitization", "Original beneficiary or lending institution named on deed of trust.", "Distinguishes between GSE-backed loans (Fannie/Freddie), private money hard-money lenders, and seller-carry notes.", "String", ["beneficiary", "mortgagee", "original_lender"]),
    ("servicer_name", "Mortgage & Securitization", "Mortgage loan servicing entity collecting debt payments and managing escrow.", "Points of contact for payoff demand letters, short sale packages, and loss mitigation.", "String", ["loan_servicer", "note_servicer", "current_servicer"]),
    ("mers_min_number", "Mortgage & Securitization", "Mortgage Electronic Registration Systems (MERS) 18-digit identification number.", "Enables tracking of unrecorded electronic mortgage assignment transfers across secondary markets.", "String (18-digit)", ["mers_id", "min_number", "mers_tracking"]),
    ("prepayment_penalty_flag", "Mortgage & Securitization", "Clause imposing financial penalty for early principal payoff within statutory window.", "Critical for calculating refinancing friction or accelerated acquisition costs.", "Boolean", ["prepay_penalty", "prepayment_clause"]),
    ("subordination_status", "Mortgage & Securitization", "Lien seniority rank: 1st Trust Deed, 2nd Home Equity Line (HELOC), Mezzanine, or Junior.", "Junior liens are wiped out in senior foreclosure sales unless surplus equity exists.", "String (Enum: 1st, 2nd, Junior)", ["lien_priority", "seniority_rank", "mortgage_position"]),
    ("heloc_draw_limit", "Mortgage & Securitization", "Maximum credit line capacity established on revolving Home Equity Line of Credit.", "Unused credit capacity impacts borrower total debt capacity.", "Currency (USD)", ["credit_line_cap", "heloc_limit", "revolving_cap"]),

    # ── 3. EXTENDED MUNICIPAL CODE ENFORCEMENT & STRUCTURE ──
    ("code_violation_count", "Municipal / Enforcement", "Active municipal code citations, blight complaints, or health department notices.", "High violation velocity signals absentee owner neglect or deferred structural maintenance.", "Integer", ["code_violations", "blight_citations", "municipal_citations"]),
    ("red_tag_status", "Municipal / Enforcement", "Municipal building department order declaring structure unsafe for human occupancy.", "Immediate prohibition on tenancy; requires building permits and structural certification to clear.", "Boolean", ["condemned_flag", "unsafe_occupancy", "red_tagged"]),
    ("unpermitted_work_flag", "Municipal / Enforcement", "Assessor or planning flag indicating construction completed without building permits.", "Buyer inherits legal liability to bring unpermitted square footage to code or demolish it.", "Boolean", ["unpermitted_addition", "bootleg_structure", "illegal_construction"]),
    ("demolition_order_pending", "Municipal / Enforcement", "Recorded administrative notice of intent to demolish nuisance structure.", "Property risks direct municipal demolition assessment liens if nuisance is not abated.", "Boolean", ["demo_order", "razing_order", "abatement_demolition"]),
    ("lead_paint_risk_indicator", "Municipal & Structure", "Binary indicator based on structure pre-dating federal 1978 residential ban.", "Mandates federal EPA Title X lead-based paint disclosure prior to leasing or conveyance.", "Boolean", ["lead_hazard", "pre_1978_lead"]),
    ("asbestos_hazard_indicator", "Municipal & Structure", "Indicator derived from construction pre-dating 1989 EPA ban on asbestos-containing materials.", "Requires formal asbestos survey before demolition or renovation under NESHAP regulations.", "Boolean", ["acm_hazard", "asbestos_flag"]),
    ("year_built", "Structure & Physical", "Recorded year of primary structure construction completion.", "Baseline indicator for effective mechanical age, structural framing methods, and plumbing standards.", "Integer (Year)", ["construction_year", "built_year", "vintage"]),
    ("effective_age", "Structure & Physical", "Appraiser-calculated physical age reflecting improvements, renovations, or neglect.", "Calculates remaining economic life of commercial and residential improvements.", "Integer (Years)", ["adjusted_age", "economic_age"]),
    ("hvac_type", "Structure & Utilities", "Primary heating, ventilation, and air conditioning system installed.", "Critical utility parameter for energy efficiency and replacement reserves.", "String", ["heating_system", "cooling_system", "climate_control"]),
    ("foundation_type", "Structure & Physical", "Structural foundation design (Raised Pier & Beam, Slab-on-Grade, Stem Wall, Basement).", "Directly correlates with seismic retrofitting complexity and flood inundation vulnerability.", "String", ["foundation_style", "substructure"]),

    # ── 4. UTILITIES & INFRASTRUCTURE CONNECTIVITY ──
    ("water_source", "Utilities & Off-Grid", "Primary potable water supply: Municipal City Water, Private Water Well, Shared Mutual.", "Private wells require casing yield verification (GPM) and certified chemical potability tests.", "String", ["potable_water", "water_service", "well_water"]),
    ("sewer_type", "Utilities & Off-Grid", "Waste disposal infrastructure: Municipal Public Sewer, On-Site Septic System, Cesspool.", "Septic systems require percolation rate testing and county health clearance for transfer.", "String", ["septic_system", "wastewater", "sewer_service"]),
    ("electric_service_provider", "Utilities & Off-Grid", "Regulated electric utility grid operator (e.g., PG&E, ConEd, Southern Company).", "Determines interconnect tariffs, net energy metering (NEM 3.0) policies, and base rate structures.", "String", ["electric_utility", "power_provider", "grid_operator"]),
    ("grid_interconnection_status", "Utilities & Off-Grid", "Status of electrical utility meter hookup: Grid-Tied, Off-Grid Solar/Battery, De-energized.", "De-energized meters exceeding 12 months often require comprehensive municipal safety reinspections.", "String (Enum)", ["meter_status", "power_connected", "grid_status"]),
    ("natural_gas_connected", "Utilities & Off-Grid", "Availability of direct piped natural gas versus bulk on-site propane tank (LPG).", "Propane heating requires bulk tank lease/ownership verification and ongoing delivery logistics.", "Boolean", ["gas_service", "piped_gas", "propane_flag"]),
    ("broadband_carrier_availability", "Utilities & Infrastructure", "Terrestrial broadband connectivity (Fiber, Coaxial Cable, Fixed Wireless, Satellite Only).", "Significant driver of valuation for remote residential and commercial flex properties.", "String", ["internet_carrier", "fiber_available", "broadband_type"]),

    # ── 5. PROBATE, ESTATE & SURVIVORSHIP INDICATORS ──
    ("probate_case_number", "Probate & Estate", "Superior court probate docket tracking decedent estate administration.", "Requires probate court approval or Letters of Administration before executing valid conveyance deed.", "String", ["estate_docket", "probate_id", "probate_filing"]),
    ("letters_testamentary_issued", "Probate & Estate", "Judicial order appointing personal representative or executor with power of sale.", "Confirms legal authority of executor to enter into binding purchase agreements under IAEA.", "Boolean", ["letters_issued", "executor_authority", "probate_authority"]),
    ("iaea_full_authority_flag", "Probate & Estate", "Independent Administration of Estates Act full authority indicator.", "Permits executor to sell real property without mandatory court overbid auction procedures.", "Boolean", ["iaea_full", "iaea_powers"]),
    ("estate_tax_lien_flag", "Probate & Estate", "Statutory federal estate tax lien (IRC Section 6324) attaching to gross estate assets.", "Clouds title for 10 years post-decedent death unless formal Certificate of Discharge is obtained.", "Boolean", ["form_706_lien", "federal_estate_lien"]),
    ("survivorship_rights_flag", "Probate & Title", "Vesting type establishing automatic right of survivorship (Joint Tenancy, Community Property).", "Allows title to vest automatically in surviving co-owner by recording Affidavit of Death without probate.", "Boolean", ["joint_tenancy_right", "right_of_survivorship"]),

    # ── 6. UCC, COMMERCIAL & CORPORATE ASSET ENCUMBRANCES ──
    ("ucc_1_filing_number", "Commercial & Debt", "Uniform Commercial Code fixture filing index with the Secretary of State.", "Attaches security interest to property fixtures (HVAC units, commercial solar panels, heavy equipment).", "String", ["ucc_filing", "fixture_filing", "ucc_id"]),
    ("commercial_solar_ppa_flag", "Commercial & Encumbrance", "Recorded Solar Power Purchase Agreement or fixture UCC lien.", "Obligates buyer to assume long-term energy purchase contracts or negotiate costly buyout terms.", "Boolean", ["solar_ppa", "solar_lease_lien"]),
    ("pace_financing_lien", "Commercial & Tax Roll", "Property Assessed Clean Energy (PACE) special tax assessment recorded on property.", "Senior lien collecting repayment through county property tax bills; must be subordinated or paid off.", "Currency (USD)", ["pace_lien", "heroe_assessment", "clean_energy_lien"]),
    ("mechanics_lien_amount", "Commercial & Debt", "Statutory mechanic's lien filed by unpaid general contractors or material suppliers.", "Must be perfected via lawsuit within statutory deadlines (e.g., 90 days in CA) or become unenforceable.", "Currency (USD)", ["contractor_lien", "mechanic_claim", "construction_lien"]),
    ("hoa_delinquency_amount", "Distress & Encumbrance", "Past-due homeowners association dues and assessment liens.", "In super-priority lien states, HOA liens can extinguish first-position mortgages if foreclosed.", "Currency (USD)", ["hoa_arrears", "past_due_hoa", "condo_assessment_lien"])
]

def main():
    lib = IndicatorLibrary()
    print("─────────────────────────────────────────────────────────────")
    print("  EXECUTING EXPANDED INDICATOR COMPILER                      ")
    print("─────────────────────────────────────────────────────────────")

    added = 0
    deduped = 0

    for name, cat, desc, disc, dtype, aliases in EXPANDED_TAXONOMY:
        success, rec, msg = lib.register_indicator(
            name=name, category=cat, description=desc, disclosure=disc, data_type=dtype, aliases=aliases
        )
        if success:
            added += 1
            print(f"[REGISTERED] {rec['name'].ljust(26)} [{rec['category']}]")
        else:
            deduped += 1
            print(f"[DEDUPED]    {name.ljust(26)} -> Canonical: '{rec['name']}'")

    total_records = len(lib.list_all())
    print("\n" + "─"*65)
    print(f"Compilation Results: {added} new | {deduped} deduplicated | Total Master Library: {total_records}")
    print("─"*65)

    # Regenerate INDICATOR_DICTIONARY.md with full updated catalog
    regenerate_dictionary(lib)

def regenerate_dictionary(lib: IndicatorLibrary):
    indicators = lib.list_all()
    md = """# Master Public Record & Municipal Data Indicator Dictionary
**Enterprise Governance Notice:** Operational taxonomy and statutory regulatory disclosures across public record APIs, spatial GIS layers, encumbrance feeds, and municipal open data.

---

"""
    by_category = {}
    for ind in indicators:
        by_category.setdefault(ind["category"], []).append(ind)

    for cat in sorted(by_category.keys()):
        md += f"## {cat}\n\n"
        for i in by_category[cat]:
            md += f"### `{i['name']}`\n"
            md += f"- **Data Type:** `{i['data_type']}`\n"
            md += f"- **Aliases / Synonyms:** {i['aliases'] or 'None'}\n"
            md += f"- **Description:** {i['description']}\n"
            md += f"- **Legal & Operational Disclosure:** {i['disclosure']}\n\n"
        md += "---\n\n"

    with open("INDICATOR_DICTIONARY.md", "w") as f:
        f.write(md)
    print("[RUNBOOK EXPORT SUCCESS] Updated: INDICATOR_DICTIONARY.md")

if __name__ == "__main__":
    main()
