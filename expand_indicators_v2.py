#!/usr/bin/env python3
from indicator_master import IndicatorLibrary

SPECIALTY_TAXONOMY = [
    ("mineral_rights_severed_flag", "Subsurface & Resources", "Mineral rights severed from surface estate.", "Severed estate allows surface access for extraction.", "Boolean", ["severed_minerals", "mineral_reservation"]),
    ("water_rights_classification", "Subsurface & Resources", "Legal doctrine governing extraction (Riparian, Appropriative).", "Prior appropriation gives senior holders full priority.", "String", ["water_doctrine", "water_right_type"]),
    ("adjudicated_basin_flag", "Subsurface & Resources", "Groundwater extraction capped by court decree or SGMA.", "Imposes strict metered allocations and drilling moratoriums.", "Boolean", ["groundwater_adjudication", "sgma_cap"]),
    ("well_casing_depth", "Subsurface & Water", "Total vertical depth of groundwater well casing in feet.", "Assesses aquifer stability and deepening costs.", "Float", ["well_depth", "casing_depth"]),
    ("well_flow_rate_gpm", "Subsurface & Water", "Sustained yield of well in Gallons Per Minute.", "Mandatory 3 to 5 GPM minimum for certificate of occupancy.", "Float", ["well_yield", "gpm_flow"]),
    ("timber_production_zone_flag", "Subsurface & Resources", "Tax overlay restricting land strictly to timber harvesting.", "Mandatory 10-year phase-out; severe tax recapture if breached.", "Boolean", ["tpz_flag", "timber_preserve"]),
    ("landlocked_indicator", "Access & Easements", "Parcel lacks frontage on dedicated public rights-of-way.", "Requires recorded easement or quiet title easement by necessity.", "Boolean", ["landlocked_flag", "no_public_access"]),
    ("appurtenant_access_easement", "Access & Easements", "Recorded deeded right-of-way across neighboring parcel.", "Must verify maintenance terms and exclusivity.", "Document", ["deeded_easement", "access_easement"]),
    ("utility_easement_sqft", "Access & Easements", "Surface land area dedicated to utility corridors.", "Permanent structures prohibited in utility rights-of-way.", "Float", ["utility_corridor", "pue_area"]),
    ("conservation_easement_flag", "Access & Easements", "Restriction deeded to land trust permanently barring development.", "Runs with title perpetually; extinguishes build rights.", "Boolean", ["land_trust_easement", "conservation_easement"]),
    ("prescriptive_easement_claim", "Access & Easements", "Hostile, open third-party access claim via continuous use.", "Clouds title; risks loss of exclusive access.", "Boolean", ["hostile_access", "prescriptive_claim"])
]
SPECIALTY_TAXONOMY += [
    ("williamson_act_contract_flag", "Agricultural & Abatement", "California Land Conservation Act agricultural preserve contract.", "Lowers assessed value by 20 to 75 percent based on crop yield.", "Boolean", ["williamson_act", "clca_contract"]),
    ("williamson_non_renewal_status", "Agricultural & Abatement", "Notice of non-renewal served on agricultural contract.", "Initiates 9-year transition returning taxes to market level.", "Boolean", ["non_renewal_filed", "clca_exit"]),
    ("rollback_tax_liability", "Agricultural & Abatement", "Statutory penalty assessed upon cancellation of ag abatement.", "Can equal 12.5 percent or more of full unrestricted market value.", "Currency", ["cancellation_penalty", "ag_rollback_tax"]),
    ("mello_roos_annual_tax", "Special Taxes & CFD", "Annual special tax levied under Community Facilities District.", "Senior assessment collected on county tax roll.", "Currency", ["cfd_tax", "mello_roos"]),
    ("mello_roos_bond_maturity_year", "Special Taxes & CFD", "Year CFD municipal infrastructure bond matures.", "Expiration lowers property tax burden and improves net income.", "Integer", ["cfd_maturity", "special_tax_expiration"]),
    ("improvement_bond_1915_act", "Special Taxes & CFD", "Special assessment lien authorized under 1915 Bond Act.", "Direct parcel lien; unpaid balance accelerates foreclosure.", "Currency", ["1915_act_lien", "assessment_bond_balance"]),
    ("usda_rural_eligible_flag", "Government Lending", "Parcel falls within USDA Rural Development boundary lines.", "Confirms eligibility for 0 percent down USDA single-close loans.", "Boolean", ["usda_boundary", "rural_dev_eligible"]),
    ("hud_opportunity_zone_flag", "Government Lending & Tax", "Qualified Opportunity Zone census tract designation.", "Permits tax elimination on capital gains held over 10 years.", "Boolean", ["qoz_flag", "opportunity_zone"]),
    ("fema_disaster_declaration_flag", "Government Lending & Hazard", "Active Presidential or FEMA disaster declaration in county.", "Unlocks SBA disaster loans and temporary foreclosure freezes.", "Boolean", ["major_disaster_area", "fema_declared"]),
    ("hud_fair_market_rent_40th", "Government Lending & Housing", "HUD 40th percentile Fair Market Rent for zip code.", "Benchmark cap for Section 8 Housing Choice Voucher payouts.", "Currency", ["hud_fmr", "section_8_rent_limit"]),
    ("historic_district_register_flag", "Historic & Preservation", "National Register of Historic Places or municipal overlay.", "Alterations require historic board review; demolitions blocked.", "Boolean", ["historic_overlay", "historic_landmark"])
]
SPECIALTY_TAXONOMY += [
    ("soil_percolation_rate_mpi", "Geotechnical & Septic", "Soil absorption time in Minutes Per Inch via perc test.", "Rates slower than 60 MPI require engineered septic systems.", "Float", ["perc_rate", "soil_absorption_rate"]),
    ("depth_to_bedrock", "Geotechnical & Foundation", "Vertical distance from ground surface to impermeable rock.", "Shallow bedrock under 5 feet drastically increases excavation costs.", "Float", ["bedrock_depth", "refusal_depth"]),
    ("water_table_depth", "Geotechnical & Foundation", "Minimum static distance to seasonal high groundwater table.", "High water table under 4 feet impairs septic drainfields.", "Float", ["groundwater_depth", "static_water_level"]),
    ("expansive_soil_expansion_index", "Geotechnical & Foundation", "ASTM D4829 Expansion Index quantifying soil shrink and swell.", "Index over 90 causes severe foundation cracking.", "Integer", ["expansion_index", "expansive_clay_score"]),
    ("coastal_zone_jurisdiction_flag", "Municipal & Environmental", "Parcel lies within statutory Coastal Zone boundary.", "Mandates Coastal Development Permits and public access rules.", "Boolean", ["coastal_commission", "coastal_zone"])
]

def main():
    lib = IndicatorLibrary()
    added, deduped = 0, 0
    for name, cat, desc, disc, dtype, aliases in SPECIALTY_TAXONOMY:
        success, rec, msg = lib.register_indicator(name=name, category=cat, description=desc, disclosure=disc, data_type=dtype, aliases=aliases)
        if success:
            added += 1
            print(f"[REGISTERED] {rec['name'].ljust(30)} [{rec['category']}]")
        else:
            deduped += 1
            print(f"[DEDUPED]    {name.ljust(30)} -> Canonical: {rec['name']}")
    print(f"\nCompleted: {added} registered | {deduped} deduplicated | Total in DB: {len(lib.list_all())}")

if __name__ == "__main__":
    main()
