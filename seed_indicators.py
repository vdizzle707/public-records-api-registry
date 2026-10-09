#!/usr/bin/env python3
"""
CHRONOS OS // MASTER INDICATOR BATCH COMPILER & DOCUMENTATION GENERATOR
Seeds comprehensive canonical indicators across all real estate, distress, legal,
and open government categories with strict duplicate prevention and markdown export.
"""

from indicator_master import IndicatorLibrary
import sqlite3

ALL_INDICATORS = [
    # 1. Real Estate & Spatial Geometrics
    (
        "apn",
        "Real Estate / Spatial",
        "Assessor Parcel Number identifying the land unit with the county tax collector.",
        "Non-static identifier. Subject to parcel splits, combinations, or municipal redistricting. Must be validated against 5-digit county FIPS code.",
        "String",
        ["parcel_id", "parcel_number", "pin", "tax_id", "folio_number"]
    ),
    (
        "fips",
        "Real Estate / Spatial",
        "Federal Information Processing Standard 5-digit county identifier code.",
        "Mandatory for resolving duplicate or overlapping APN formats across disparate US county jurisdictions.",
        "String (5-digit)",
        ["fips_code", "county_fips", "jurisdiction_code"]
    ),
    (
        "lot_size",
        "Real Estate / Spatial",
        "Gross land area recorded on county tax rolls and recorded subdivision maps.",
        "Plat map boundaries take legal precedence over county tax assessor GIS polygon approximations.",
        "Float / Area (Acres/SqFt)",
        ["parcel_area", "lot_sqft", "acreage", "gross_area"]
    ),
    (
        "zoning_code",
        "Real Estate / Municipal",
        "Municipal or county land-use classification regulating physical development and density.",
        "Determines permissible structure types (e.g., R-1 Single Family, AG Agricultural, C-2 Commercial). Overlays (e.g., riparian, wildfire hazard, slope) further restrict development rights.",
        "String",
        ["zoning", "land_use_code", "zoning_district", "use_designation"]
    ),
    (
        "gis_geometry",
        "Real Estate / Spatial",
        "GeoJSON or Esri Shapefile vector polygon boundary coordinates.",
        "GIS boundary shapes are administrative depictions for tax assessment and do not substitute for a licensed boundary survey by a Professional Land Surveyor.",
        "GeoJSON / Well-Known Text (WKT)",
        ["boundary_polygon", "parcel_geom", "spatial_geometry", "shape_coordinates"]
    ),
    (
        "legal_description",
        "Real Estate / Title",
        "Formal written metes-and-bounds, lot/block, or Public Land Survey System (PLSS) description.",
        "The controlling legal definition of real property conveyance in recorded warranty deeds and grant deeds.",
        "Text",
        ["metes_and_bounds", "plss_description", "plat_legal"]
    ),

    # 2. Valuation & Financial Indexes
    (
        "assessed_value",
        "Valuation & Financial",
        "Total statutory ad-valorem tax roll valuation established by the local county assessor.",
        "Governed by statutory formula caps (e.g., CA Proposition 13 limits base-year tax increases to 2% annually until reassessment events). Does not represent current fair market liquidation value.",
        "Currency (USD)",
        ["tax_assessed_value", "assessment_roll", "tax_value", "total_assessed_value"]
    ),
    (
        "land_value",
        "Valuation & Financial",
        "Statutory assessed value attributed exclusively to raw land excluding improvements.",
        "Used to calculate residual value when analyzing tear-down prospects or agricultural viability.",
        "Currency (USD)",
        ["assessed_land", "land_roll_value"]
    ),
    (
        "improvement_value",
        "Valuation & Financial",
        "Statutory assessed value of permanent residential, commercial, or outbuilding structures.",
        "Unpermitted structural modifications or off-grid sheds may not be captured on county tax records.",
        "Currency (USD)",
        ["structure_value", "building_assessed_value", "improvements"]
    ),
    (
        "zestimate_value",
        "Valuation & Financial",
        "Algorithmic computer-generated automated valuation model (AVM) estimate.",
        "Proprietary statistical estimation using recent neighborhood sales comparables. Unofficial estimate; does not constitute a formal appraisal.",
        "Currency (USD)",
        ["avm_estimate", "zestimate", "market_estimate"]
    ),
    (
        "rent_zestimate",
        "Valuation & Financial",
        "Estimated median monthly gross rental revenue for an address.",
        "Modeled metric derived from local multifamily and single-family rental listings. Subject to seasonal rental volatility.",
        "Currency (USD/Month)",
        ["estimated_rent", "rental_avm", "rent_estimate"]
    ),

    # 3. Distress, Pre-Foreclosure & Liens
    (
        "tax_delinquency",
        "Distress & Liens",
        "Cumulative unpaid county property taxes exceeding statutory grace periods.",
        "Triggers statutory redemption periods (typically 3 to 5 years). Uncured delinquency leads to county-administered tax sale public auctions.",
        "Currency (USD)",
        ["delinquent_taxes", "unpaid_tax_balance", "back_taxes", "tax_default"]
    ),
    (
        "tax_delinquent_year",
        "Distress & Liens",
        "The tax year in which property taxes were first declared in default.",
        "Statutory clock for tax sale auctions runs directly from this initial declaration date.",
        "Integer (Year)",
        ["default_year", "delinquency_start_year"]
    ),
    (
        "lis_pendens",
        "Distress & Legal",
        "Recorded notice of pending judicial litigation affecting title to real property.",
        "Constructive legal notice that clouds marketable title. Commonly marks the commencement of judicial mortgage foreclosure or quiet title litigation.",
        "Docket String / Boolean",
        ["suit_pending", "notice_of_action", "lis_pendens_notice", "judicial_notice"]
    ),
    (
        "notice_of_default",
        "Distress & Foreclosure",
        "Public notice filed by a trustee or mortgage servicer declaring borrower non-repayment.",
        "Prerequisite in non-judicial foreclosure states triggering a mandatory statutory reinstatement cure window (typically 90 days) before notice of sale publication.",
        "Document Reference / Date",
        ["nod", "default_filing", "notice_of_foreclosure", "default_notice"]
    ),
    (
        "notice_of_sale",
        "Distress & Foreclosure",
        "Recorded notice specifying the exact auction date, time, and location for trustee or sheriff auction.",
        "Published at least 20 to 21 days before auction across local newspapers and county public bulletin systems.",
        "Document Reference / Date",
        ["not_of_trustee_sale", "nots", "notice_of_trustee_sale", "sheriff_sale_notice"]
    ),
    (
        "auction_date",
        "Distress & Foreclosure",
        "Scheduled date for county trustee sale, sheriff auction, or tax-defaulted land liquidation.",
        "Subject to last-minute postponement via Chapter 13 bankruptcy automatic stays (11 U.S.C. Section 362), beneficiary agreements, or loan modification reviews.",
        "ISO-8601 Timestamp",
        ["sale_date", "foreclosure_date", "trustee_sale_date", "auction_timestamp"]
    ),
    (
        "default_amount",
        "Distress & Foreclosure",
        "Total delinquency balance required to cure default and reinstate loan.",
        "Includes past-due payments, late charges, and legal fees. Does not represent total accelerated mortgage balance.",
        "Currency (USD)",
        ["cure_amount", "reinstatement_amount", "arrearage_balance"]
    ),
    (
        "lien_type",
        "Distress & Liens",
        "Legal classification of encumbrance recorded against title.",
        "Priority generally dictated by recording date ('first in time, first in right') except for statutory super-priority tax liens, HOA assessment liens, and federal tax liens.",
        "String",
        ["encumbrance_type", "claim_type", "lien_classification"]
    ),
    (
        "open_balance",
        "Distress & Encumbrances",
        "Recorded face principal amount of active mortgage deeds of trust or liens.",
        "Reflects original loan face value; actual current balance requires an official beneficiary payoff demand statement.",
        "Currency (USD)",
        ["loan_balance", "mortgage_balance", "lien_balance", "unpaid_principal"]
    ),
    (
        "judgment_amount",
        "Distress & Legal",
        "Liquidated damages awarded by a court recorded as a general judgment lien.",
        "Attaches automatically to all real property owned by debtor in county where abstract of judgment is recorded.",
        "Currency (USD)",
        ["judgment_lien_amount", "court_award", "court_judgment"]
    ),
    (
        "bankruptcy_chapter",
        "Distress & Legal",
        "Federal court bankruptcy jurisdiction filing (Chapter 7, 11, or 13).",
        "Imposes immediate nationwide automatic stay halting all foreclosure, eviction, or collection enforcement actions without relief from stay.",
        "String (Enum: 7, 11, 12, 13)",
        ["bankruptcy_filing", "bkr_chapter", "bankruptcy_type"]
    ),
    (
        "case_number",
        "Distress & Legal",
        "Official court or county clerk tracking docket number.",
        "Mandatory key required to pull direct civil complaint filings, lis pendens abstracts, or probate dockets.",
        "String",
        ["docket_number", "court_case_id", "case_id"]
    ),

    # 4. Chain of Title & Transaction History
    (
        "grantor",
        "Chain of Title",
        "Transferor, seller, or grantor relinquishing legal title in a recorded deed conveyance.",
        "Must verify grantor matches preceding recorded grantee to ensure unbroken marketable chain of title.",
        "String",
        ["seller", "transferor", "prior_owner", "grantor_name"]
    ),
    (
        "grantee",
        "Chain of Title",
        "Transferee, buyer, or grantee acquiring legal title in a recorded deed conveyance.",
        "Must be checked for precise legal entity structure (e.g., LLC, Revocable Living Trust, Joint Tenancy).",
        "String",
        ["buyer", "transferee", "new_owner", "deed_recipient", "owner_name"]
    ),
    (
        "sale_price",
        "Chain of Title",
        "Documentary transfer tax declared consideration paid for property transfer.",
        "In non-disclosure states (e.g., TX, NM, UT), sale price is not disclosed on deed; documentary transfer tax calculations or MLS data must be utilized.",
        "Currency (USD)",
        ["purchase_price", "consideration_amount", "deed_amount", "sales_price"]
    ),
    (
        "recording_date",
        "Chain of Title",
        "Timestamp when deed or document was indexed by the County Recorder.",
        "Establishes statutory legal priority under state recording acts (race-notice or notice jurisdictions).",
        "ISO-8601 Date",
        ["doc_recording_date", "filing_date", "recorded_timestamp"]
    ),
    (
        "document_type",
        "Chain of Title",
        "Legal classification of recorded real estate instrument.",
        "Distinguishes between Grant Deeds (warranting title free of unannounced encumbrances) versus Quitclaim Deeds (conveying solely grantor's current interest without title warranties).",
        "String",
        ["deed_type", "instrument_type", "conveyance_type"]
    ),
    (
        "instrument_number",
        "Chain of Title",
        "Unique county recorder document identifier or book/page reference.",
        "Direct locator needed by title plants and county recorders to pull stamped microfiche or scanned deed copies.",
        "String",
        ["book_page", "doc_number", "recorder_id", "recording_number"]
    ),

    # 5. Entity & Individual Verification (Skip Tracing)
    (
        "corporate_status",
        "Entity Verification",
        "Secretary of State business registration standing (Active, Suspended, Dissolved, Forfeited).",
        "Entities marked 'Suspended' (e.g., by CA Franchise Tax Board) lack legal capacity to contract, convey real property, or defend court actions.",
        "String",
        ["sos_status", "entity_status", "business_standing"]
    ),
    (
        "registered_agent",
        "Entity Verification",
        "Individual or corporate entity authorized to receive service of process on behalf of an entity.",
        "Primary point of contact for legal service of quiet title or pre-litigation settlement demands.",
        "String",
        ["agent_for_service", "resident_agent", "statutory_agent"]
    ),
    (
        "ein",
        "Entity Verification",
        "Federal Employer Identification Number issued by Internal Revenue Service.",
        "Required for business entity verification, commercial debt matching, and corporate tax lien tracking.",
        "String (XX-XXXXXXX)",
        ["fein", "federal_tax_id", "tax_ein"]
    ),
    (
        "ssn_verified",
        "Skip Tracing / Identity",
        "Indicator that Social Security Number passes SSA issuance range and Death Master File checks.",
        "Confirming identity helps prevent false-positive matches on common individual names.",
        "Boolean",
        ["ssn_valid", "ssn_match", "identity_verified"]
    ),
    (
        "phone_carrier",
        "Skip Tracing / Identity",
        "Originating telecommunications provider for telephone contact records.",
        "Identifies active tier-1 mobile carriers versus disposable VoIP/burner numbers to prioritize outreach quality.",
        "String",
        ["telecom_carrier", "carrier_name", "wireless_provider"]
    ),
    (
        "alias_names",
        "Skip Tracing / Identity",
        "Documented legal name variants, prior maiden names, or fictitious business names (DBA).",
        "Critical for cross-referencing judgment liens recorded under alternate name permutations.",
        "Array of Strings",
        ["aka", "fka", "dba_name", "alternate_names"]
    ),
    (
        "deceased_flag",
        "Skip Tracing / Identity",
        "Indicator that entity or owner is indexed on SSA Social Security Death Index (SSDI).",
        "Marks property for immediate probate search and probate administration filings.",
        "Boolean",
        ["is_deceased", "ssdi_match", "death_indicator"]
    ),

    # 6. Open Data & Federal Infrastructure Indicators
    (
        "ckan_package_id",
        "Open Data / Infrastructure",
        "UUID identifier for open datasets indexed on Data.gov / CKAN platforms.",
        "Identifies open datasets for programmatic metadata retrieval and schema monitoring.",
        "UUID String",
        ["dataset_id", "ckan_id", "package_uuid"]
    ),
    (
        "download_url",
        "Open Data / Infrastructure",
        "Direct link to raw machine-readable data feeds (CSV, GeoJSON, Parquet, REST API).",
        "Must verify HTTPS certificates and transport status prior to initiating scheduled automated ingestion.",
        "URI",
        ["resource_url", "data_link", "direct_download"]
    ),
    (
        "update_frequency",
        "Open Data / Infrastructure",
        "Frequency schedule at which source custodian refreshes public data records.",
        "Determines pipeline synchronization cadences. Real estate distress requires weekly cycles, whereas zoning overlays are typically annual.",
        "String (ISO Period)",
        ["refresh_rate", "ingest_frequency", "cadence"]
    ),
    (
        "agency_name",
        "Open Data / Infrastructure",
        "Government body or county agency with custodial responsibility for the record.",
        "Establishes statutory custody and source authenticity for court-admissible audit trails.",
        "String",
        ["custodian", "data_owner", "issuing_agency", "source_agency"]
    )
]

def main():
    lib = IndicatorLibrary()
    print("─────────────────────────────────────────────────────────────")
    print("  SEEDING FULL CANONICAL INDICATOR TAXONOMY                  ")
    print("─────────────────────────────────────────────────────────────")
    
    added_count = 0
    duplicate_count = 0
    
    for name, cat, desc, disc, dtype, aliases in ALL_INDICATORS:
        success, rec, msg = lib.register_indicator(
            name=name,
            category=cat,
            description=desc,
            disclosure=disc,
            data_type=dtype,
            aliases=aliases
        )
        if success:
            added_count += 1
            print(f"[REGISTERED] {rec['name'].ljust(22)} [{rec['category']}]")
        else:
            duplicate_count += 1
            print(f"[DEDUPED]    {name.ljust(22)} -> Matches canonical '{rec['name']}'")

    print("\n" + "─"*65)
    print(f"Summary: {added_count} newly indexed | {duplicate_count} deduplicated | Total: {len(lib.list_all())}")
    print("─"*65)

    # Export formal markdown documentation
    export_markdown(lib)

def export_markdown(lib: IndicatorLibrary):
    """Exports structured reference runbook for Git and developer auditing."""
    indicators = lib.list_all()
    md_content = """# Master Public Record & Municipal Data Indicator Dictionary

An operational index and regulatory disclosure specification of canonical data indicators across real estate, legal distress, encumbrances, and municipal open data APIs.

---

"""
    # Group by category
    by_category = {}
    for ind in indicators:
        cat = ind["category"]
        by_category.setdefault(cat, []).append(ind)

    for cat, items in by_category.items():
        md_content += f"## {cat}\n\n"
        for i in items:
            md_content += f"### `{i['name']}`\n"
            md_content += f"- **Data Type:** `{i['data_type']}`\n"
            md_content += f"- **Aliases / Synonyms:** {i['aliases'] or 'None'}\n"
            md_content += f"- **Description:** {i['description']}\n"
            md_content += f"- **Legal & Operational Disclosure:** {i['disclosure']}\n\n"
        md_content += "---\n\n"

    with open("INDICATOR_DICTIONARY.md", "w") as f:
        f.write(md_content)
    print("[EXPORT SUCCESS] Generated formal documentation: INDICATOR_DICTIONARY.md")

if __name__ == "__main__":
    main()
