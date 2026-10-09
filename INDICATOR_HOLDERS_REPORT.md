# Chronos OS // Indicator Compilation & Entity Holder Report
**Generated:** Automated Audit & Compliance Engine  
**Database:** `public_apis_registry.db`  

---

## Executive Summary
This report compiles all master indicators and maps which addresses, parcels, and people hold or are associated with each operational indicator across county assessment rolls, distress ledgers, and audit dossiers.

---

## Indicator: `appurtenant_access_easement`
- **Category:** Access & Easements
- **Data Type:** `Document`
- **Description:** Recorded deeded right-of-way across neighboring parcel.
- **Legal Disclosure:** Must verify maintenance terms and exclusivity.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `conservation_easement_flag`
- **Category:** Access & Easements
- **Data Type:** `Boolean`
- **Description:** Restriction deeded to land trust permanently barring development.
- **Legal Disclosure:** Runs with title perpetually; extinguishes build rights.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `landlocked_indicator`
- **Category:** Access & Easements
- **Data Type:** `Boolean`
- **Description:** Parcel lacks frontage on dedicated public rights-of-way.
- **Legal Disclosure:** Requires recorded easement or quiet title easement by necessity.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `prescriptive_easement_claim`
- **Category:** Access & Easements
- **Data Type:** `Boolean`
- **Description:** Hostile, open third-party access claim via continuous use.
- **Legal Disclosure:** Clouds title; risks loss of exclusive access.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `utility_easement_sqft`
- **Category:** Access & Easements
- **Data Type:** `Float`
- **Description:** Surface land area dedicated to utility corridors.
- **Legal Disclosure:** Permanent structures prohibited in utility rights-of-way.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `rollback_tax_liability`
- **Category:** Agricultural & Abatement
- **Data Type:** `Currency`
- **Description:** Statutory penalty assessed upon cancellation of ag abatement.
- **Legal Disclosure:** Can equal 12.5 percent or more of full unrestricted market value.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `williamson_act_contract_flag`
- **Category:** Agricultural & Abatement
- **Data Type:** `Boolean`
- **Description:** California Land Conservation Act agricultural preserve contract.
- **Legal Disclosure:** Lowers assessed value by 20 to 75 percent based on crop yield.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `williamson_non_renewal_status`
- **Category:** Agricultural & Abatement
- **Data Type:** `Boolean`
- **Description:** Notice of non-renewal served on agricultural contract.
- **Legal Disclosure:** Initiates 9-year transition returning taxes to market level.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `document_type`
- **Category:** Chain of Title
- **Data Type:** `String`
- **Description:** Legal classification of recorded real estate instrument.
- **Legal Disclosure:** Distinguishes between Grant Deeds (warranting title free of unannounced encumbrances) versus Quitclaim Deeds (conveying solely grantor's current interest without title warranties).
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `grantor`
- **Category:** Chain of Title
- **Data Type:** `String`
- **Description:** Transferor, seller, or grantor relinquishing legal title in a recorded deed conveyance.
- **Legal Disclosure:** Must verify grantor matches preceding recorded grantee to ensure unbroken marketable chain of title.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `instrument_number`
- **Category:** Chain of Title
- **Data Type:** `String`
- **Description:** Unique county recorder document identifier or book/page reference.
- **Legal Disclosure:** Direct locator needed by title plants and county recorders to pull stamped microfiche or scanned deed copies.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `recording_date`
- **Category:** Chain of Title
- **Data Type:** `ISO-8601 Date`
- **Description:** Timestamp when deed or document was indexed by the County Recorder.
- **Legal Disclosure:** Establishes statutory legal priority under state recording acts (race-notice or notice jurisdictions).
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `sale_price`
- **Category:** Chain of Title
- **Data Type:** `Currency (USD)`
- **Description:** Documentary transfer tax declared consideration paid for property transfer.
- **Legal Disclosure:** In non-disclosure states (e.g., TX, NM, UT), sale price is not disclosed on deed; documentary transfer tax calculations or MLS data must be utilized.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `mechanics_lien_amount`
- **Category:** Commercial & Debt
- **Data Type:** `Currency (USD)`
- **Description:** Statutory mechanic's lien filed by unpaid general contractors or material suppliers.
- **Legal Disclosure:** Must be perfected via lawsuit within statutory deadlines (e.g., 90 days in CA) or become unenforceable.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `ucc_1_filing_number`
- **Category:** Commercial & Debt
- **Data Type:** `String`
- **Description:** Uniform Commercial Code fixture filing index with the Secretary of State.
- **Legal Disclosure:** Attaches security interest to property fixtures (HVAC units, commercial solar panels, heavy equipment).
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `commercial_solar_ppa_flag`
- **Category:** Commercial & Encumbrance
- **Data Type:** `Boolean`
- **Description:** Recorded Solar Power Purchase Agreement or fixture UCC lien.
- **Legal Disclosure:** Obligates buyer to assume long-term energy purchase contracts or negotiate costly buyout terms.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `pace_financing_lien`
- **Category:** Commercial & Tax Roll
- **Data Type:** `Currency (USD)`
- **Description:** Property Assessed Clean Energy (PACE) special tax assessment recorded on property.
- **Legal Disclosure:** Senior lien collecting repayment through county property tax bills; must be subordinated or paid off.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `open_balance`
- **Category:** Debt
- **Data Type:** `Currency`
- **Description:** Principal balance on mortgage or judgment liens.
- **Legal Disclosure:** Payoff demand statement required for per-diem balance.
- **Linked Holders Count:** 4

### Associated Addresses & People

| # | Person / Entity | Address / APN | Indicator Value / Detail | Source Dataset |
|---|---|---|---|---|
| 1 | Pacific Coast Land Holdings LLC | APN 014-220-03 (State: CA, FIPS: 06045) | Open Liens Balance: $180,000.00 | distress_leads |
| 2 | Redwood Trust | APN 028-110-14 (State: CA, FIPS: 06045) | Open Liens Balance: $680,000.00 | distress_leads |
| 3 | Mendocino Heritage Corp | APN 005-090-22 (State: CA, FIPS: 06045) | Open Liens Balance: $50,000.00 | distress_leads |
| 4 | Vested Owner of Record | APN 003-360-15 (State: CA, FIPS: 06045) | Open Liens Balance: $265,000.00 | distress_leads |

---

## Indicator: `auction_date`
- **Category:** Distress
- **Data Type:** `Timestamp`
- **Description:** Scheduled trustee or tax default auction date.
- **Legal Disclosure:** Subject to bankruptcy automatic stays.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `lis_pendens`
- **Category:** Distress
- **Data Type:** `Docket`
- **Description:** Recorded public notice of pending judicial litigation.
- **Legal Disclosure:** Constructive legal notice of foreclosure.
- **Linked Holders Count:** 1

### Associated Addresses & People

| # | Person / Entity | Address / APN | Indicator Value / Detail | Source Dataset |
|---|---|---|---|---|
| 1 | Redwood Trust | APN 028-110-14 (State: CA, FIPS: 06045) | Trigger Match: tax_delinquency($3,400.00),notice_of_default,lis_pendens | distress_leads |

---

## Indicator: `notice_of_default`
- **Category:** Distress
- **Data Type:** `Document`
- **Description:** Public notice filed by trustee declaring default.
- **Legal Disclosure:** Triggers statutory 90-day cure window.
- **Linked Holders Count:** 2

### Associated Addresses & People

| # | Person / Entity | Address / APN | Indicator Value / Detail | Source Dataset |
|---|---|---|---|---|
| 1 | Pacific Coast Land Holdings LLC | APN 014-220-03 (State: CA, FIPS: 06045) | Default Amount: $18,900.00 | distress_leads |
| 2 | Redwood Trust | APN 028-110-14 (State: CA, FIPS: 06045) | Default Amount: $42,000.00 | distress_leads |

---

## Indicator: `tax_delinquency`
- **Category:** Distress
- **Data Type:** `Currency`
- **Description:** Unpaid property tax balance past grace period.
- **Legal Disclosure:** Triggers statutory tax sale if uncured.
- **Linked Holders Count:** 3

### Associated Addresses & People

| # | Person / Entity | Address / APN | Indicator Value / Detail | Source Dataset |
|---|---|---|---|---|
| 1 | Pacific Coast Land Holdings LLC | APN 014-220-03 (State: CA, FIPS: 06045) | Tax Delinquency: $12,450.00 | distress_leads |
| 2 | Redwood Trust | APN 028-110-14 (State: CA, FIPS: 06045) | Tax Delinquency: $3,400.00 | distress_leads |
| 3 | Mendocino Heritage Corp | APN 005-090-22 (State: CA, FIPS: 06045) | Tax Delinquency: $8,200.00 | distress_leads |

---

## Indicator: `hoa_delinquency_amount`
- **Category:** Distress & Encumbrance
- **Data Type:** `Currency (USD)`
- **Description:** Past-due homeowners association dues and assessment liens.
- **Legal Disclosure:** In super-priority lien states, HOA liens can extinguish first-position mortgages if foreclosed.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `default_amount`
- **Category:** Distress & Foreclosure
- **Data Type:** `Currency (USD)`
- **Description:** Total delinquency balance required to cure default and reinstate loan.
- **Legal Disclosure:** Includes past-due payments, late charges, and legal fees. Does not represent total accelerated mortgage balance.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `notice_of_sale`
- **Category:** Distress & Foreclosure
- **Data Type:** `Document Reference / Date`
- **Description:** Recorded notice specifying the exact auction date, time, and location for trustee or sheriff auction.
- **Legal Disclosure:** Published at least 20 to 21 days before auction across local newspapers and county public bulletin systems.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `bankruptcy_chapter`
- **Category:** Distress & Legal
- **Data Type:** `String (Enum: 7, 11, 12, 13)`
- **Description:** Federal court bankruptcy jurisdiction filing (Chapter 7, 11, or 13).
- **Legal Disclosure:** Imposes immediate nationwide automatic stay halting all foreclosure, eviction, or collection enforcement actions without relief from stay.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `case_number`
- **Category:** Distress & Legal
- **Data Type:** `String`
- **Description:** Official court or county clerk tracking docket number.
- **Legal Disclosure:** Mandatory key required to pull direct civil complaint filings, lis pendens abstracts, or probate dockets.
- **Linked Holders Count:** 1

### Associated Addresses & People

| # | Person / Entity | Address / APN | Indicator Value / Detail | Source Dataset |
|---|---|---|---|---|
| 1 | DISCLOSED SUBJECT | Christina Morgan Simmons | 24-1590 | audit_dossiers (ID #4) |

---

## Indicator: `judgment_amount`
- **Category:** Distress & Legal
- **Data Type:** `Currency (USD)`
- **Description:** Liquidated damages awarded by a court recorded as a general judgment lien.
- **Legal Disclosure:** Attaches automatically to all real property owned by debtor in county where abstract of judgment is recorded.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `lien_type`
- **Category:** Distress & Liens
- **Data Type:** `String`
- **Description:** Legal classification of encumbrance recorded against title.
- **Legal Disclosure:** Priority generally dictated by recording date ('first in time, first in right') except for statutory super-priority tax liens, HOA assessment liens, and federal tax liens.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `tax_delinquent_year`
- **Category:** Distress & Liens
- **Data Type:** `Integer (Year)`
- **Description:** The tax year in which property taxes were first declared in default.
- **Legal Disclosure:** Statutory clock for tax sale auctions runs directly from this initial declaration date.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `corporate_status`
- **Category:** Entity Verification
- **Data Type:** `String`
- **Description:** Secretary of State business registration standing (Active, Suspended, Dissolved, Forfeited).
- **Legal Disclosure:** Entities marked 'Suspended' (e.g., by CA Franchise Tax Board) lack legal capacity to contract, convey real property, or defend court actions.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `ein`
- **Category:** Entity Verification
- **Data Type:** `String (XX-XXXXXXX)`
- **Description:** Federal Employer Identification Number issued by Internal Revenue Service.
- **Legal Disclosure:** Required for business entity verification, commercial debt matching, and corporate tax lien tracking.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `registered_agent`
- **Category:** Entity Verification
- **Data Type:** `String`
- **Description:** Individual or corporate entity authorized to receive service of process on behalf of an entity.
- **Legal Disclosure:** Primary point of contact for legal service of quiet title or pre-litigation settlement demands.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `sea_level_rise_exposure`
- **Category:** Environmental / Climate
- **Data Type:** `Float (Feet)`
- **Description:** NOAA projected coastal inundation under progressive 1-6 foot sea rise models.
- **Legal Disclosure:** Governs coastal development permits (CDP) under state Coastal Commissions.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `wetlands_flag`
- **Category:** Environmental / Conservation
- **Data Type:** `Boolean`
- **Description:** USFWS National Wetlands Inventory (NWI) jurisdictional wetlands indicator.
- **Legal Disclosure:** Triggers Clean Water Act Section 404 Army Corps of Engineers permitting; severely limits physical land disturbance.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `superfund_npl_proximity`
- **Category:** Environmental / Contamination
- **Data Type:** `Float (Miles)`
- **Description:** Proximity distance to EPA Comprehensive Environmental Response (CERCLA) Superfund site.
- **Legal Disclosure:** Creates potential joint and strict liability under federal CERCLA without bona fide prospective purchaser status.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `base_flood_elevation`
- **Category:** Environmental / Hazard
- **Data Type:** `Float (Feet)`
- **Description:** FEMA modeled water surface elevation of a 100-year flood event.
- **Legal Disclosure:** Critical for building pad permits and elevation certificate compliance.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `flood_zone`
- **Category:** Environmental / Hazard
- **Data Type:** `String`
- **Description:** FEMA Special Flood Hazard Area (SFHA) designation (e.g., Zone A, AE, V, X).
- **Legal Disclosure:** Determines mandatory federal flood insurance purchase requirements under NFIP. Affects debt service and insurability.
- **Linked Holders Count:** 1

### Associated Addresses & People

| # | Person / Entity | Address / APN | Indicator Value / Detail | Source Dataset |
|---|---|---|---|---|
| 1 | DISCLOSED SUBJECT | 431 Chablis Dr, Ukiah, CA 95482 | APN: 170-132-21-00; Elev: 632.4 ft; FEMA Flood Zone X; CalFire LRA Non-VHFHSZ; FIPS 06045; Ukiah Municipal Water/Sewer. | audit_dossiers (ID #1) |

---

## Indicator: `wildfire_hazard_severity`
- **Category:** Environmental / Hazard
- **Data Type:** `String (Enum)`
- **Description:** CAL FIRE / State Fire Marshal hazard classification (LRA/SRA: Moderate, High, Very High).
- **Legal Disclosure:** Very High Fire Hazard Severity Zones (VHFHSZ) trigger mandatory defensible space and strict home-hardening building codes.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `earthquake_fault_zone`
- **Category:** Environmental / Seismic
- **Data Type:** `Boolean`
- **Description:** State geological survey designated active fault rupture hazard zone (e.g., Alquist-Priolo).
- **Legal Disclosure:** Prohibits human-occupancy structures directly astride active fault traces; requires licensed geologic fault investigation.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `liquefaction_susceptibility`
- **Category:** Environmental / Seismic
- **Data Type:** `String (Enum: Low/Med/High)`
- **Description:** Susceptibility of saturated granular soil to strength loss during ground shaking.
- **Legal Disclosure:** Requires deep foundation engineering, pile driving, or soil densification mitigation.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `depth_to_bedrock`
- **Category:** Geotechnical & Foundation
- **Data Type:** `Float`
- **Description:** Vertical distance from ground surface to impermeable rock.
- **Legal Disclosure:** Shallow bedrock under 5 feet drastically increases excavation costs.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `expansive_soil_expansion_index`
- **Category:** Geotechnical & Foundation
- **Data Type:** `Integer`
- **Description:** ASTM D4829 Expansion Index quantifying soil shrink and swell.
- **Legal Disclosure:** Index over 90 causes severe foundation cracking.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `water_table_depth`
- **Category:** Geotechnical & Foundation
- **Data Type:** `Float`
- **Description:** Minimum static distance to seasonal high groundwater table.
- **Legal Disclosure:** High water table under 4 feet impairs septic drainfields.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `soil_percolation_rate_mpi`
- **Category:** Geotechnical & Septic
- **Data Type:** `Float`
- **Description:** Soil absorption time in Minutes Per Inch via perc test.
- **Legal Disclosure:** Rates slower than 60 MPI require engineered septic systems.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `usda_rural_eligible_flag`
- **Category:** Government Lending
- **Data Type:** `Boolean`
- **Description:** Parcel falls within USDA Rural Development boundary lines.
- **Legal Disclosure:** Confirms eligibility for 0 percent down USDA single-close loans.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `fema_disaster_declaration_flag`
- **Category:** Government Lending & Hazard
- **Data Type:** `Boolean`
- **Description:** Active Presidential or FEMA disaster declaration in county.
- **Legal Disclosure:** Unlocks SBA disaster loans and temporary foreclosure freezes.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `hud_fair_market_rent_40th`
- **Category:** Government Lending & Housing
- **Data Type:** `Currency`
- **Description:** HUD 40th percentile Fair Market Rent for zip code.
- **Legal Disclosure:** Benchmark cap for Section 8 Housing Choice Voucher payouts.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `hud_opportunity_zone_flag`
- **Category:** Government Lending & Tax
- **Data Type:** `Boolean`
- **Description:** Qualified Opportunity Zone census tract designation.
- **Legal Disclosure:** Permits tax elimination on capital gains held over 10 years.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `historic_district_register_flag`
- **Category:** Historic & Preservation
- **Data Type:** `Boolean`
- **Description:** National Register of Historic Places or municipal overlay.
- **Legal Disclosure:** Alterations require historic board review; demolitions blocked.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `current_interest_rate`
- **Category:** Mortgage & Securitization
- **Data Type:** `Float (Percentage)`
- **Description:** Effective nominal interest rate recorded on promissory note or modification agreement.
- **Legal Disclosure:** Critical for debt-service coverage ratio (DSCR) underwriting.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `heloc_draw_limit`
- **Category:** Mortgage & Securitization
- **Data Type:** `Currency (USD)`
- **Description:** Maximum credit line capacity established on revolving Home Equity Line of Credit.
- **Legal Disclosure:** Unused credit capacity impacts borrower total debt capacity.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `interest_rate_type`
- **Category:** Mortgage & Securitization
- **Data Type:** `String (Enum: Fixed, ARM)`
- **Description:** Interest rate classification: Fixed Rate (FRM), Adjustable (ARM), or Variable.
- **Legal Disclosure:** ARM notes in high-interest environments signal imminent debt-service reset shocks.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `lender_name`
- **Category:** Mortgage & Securitization
- **Data Type:** `String`
- **Description:** Original beneficiary or lending institution named on deed of trust.
- **Legal Disclosure:** Distinguishes between GSE-backed loans (Fannie/Freddie), private money hard-money lenders, and seller-carry notes.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `loan_maturity_date`
- **Category:** Mortgage & Securitization
- **Data Type:** `ISO-8601 Date`
- **Description:** Stated legal maturity date of promissory note.
- **Legal Disclosure:** Matured loans with unpaid principal balloons represent high-priority recapitalization or distress opportunities.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `mers_min_number`
- **Category:** Mortgage & Securitization
- **Data Type:** `String (18-digit)`
- **Description:** Mortgage Electronic Registration Systems (MERS) 18-digit identification number.
- **Legal Disclosure:** Enables tracking of unrecorded electronic mortgage assignment transfers across secondary markets.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `original_loan_amount`
- **Category:** Mortgage & Securitization
- **Data Type:** `Currency (USD)`
- **Description:** Original face value of promissory note secured by deed of trust.
- **Legal Disclosure:** Does not reflect amortization; baseline used for calculating original loan-to-value (LTV).
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `prepayment_penalty_flag`
- **Category:** Mortgage & Securitization
- **Data Type:** `Boolean`
- **Description:** Clause imposing financial penalty for early principal payoff within statutory window.
- **Legal Disclosure:** Critical for calculating refinancing friction or accelerated acquisition costs.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `servicer_name`
- **Category:** Mortgage & Securitization
- **Data Type:** `String`
- **Description:** Mortgage loan servicing entity collecting debt payments and managing escrow.
- **Legal Disclosure:** Points of contact for payoff demand letters, short sale packages, and loss mitigation.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `subordination_status`
- **Category:** Mortgage & Securitization
- **Data Type:** `String (Enum: 1st, 2nd, Junior)`
- **Description:** Lien seniority rank: 1st Trust Deed, 2nd Home Equity Line (HELOC), Mezzanine, or Junior.
- **Legal Disclosure:** Junior liens are wiped out in senior foreclosure sales unless surplus equity exists.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `coastal_zone_jurisdiction_flag`
- **Category:** Municipal & Environmental
- **Data Type:** `Boolean`
- **Description:** Parcel lies within statutory Coastal Zone boundary.
- **Legal Disclosure:** Mandates Coastal Development Permits and public access rules.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `asbestos_hazard_indicator`
- **Category:** Municipal & Structure
- **Data Type:** `Boolean`
- **Description:** Indicator derived from construction pre-dating 1989 EPA ban on asbestos-containing materials.
- **Legal Disclosure:** Requires formal asbestos survey before demolition or renovation under NESHAP regulations.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `lead_paint_risk_indicator`
- **Category:** Municipal & Structure
- **Data Type:** `Boolean`
- **Description:** Binary indicator based on structure pre-dating federal 1978 residential ban.
- **Legal Disclosure:** Mandates federal EPA Title X lead-based paint disclosure prior to leasing or conveyance.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `code_violation_count`
- **Category:** Municipal / Enforcement
- **Data Type:** `Integer`
- **Description:** Active municipal code citations, blight complaints, or health department notices.
- **Legal Disclosure:** High violation velocity signals absentee owner neglect or deferred structural maintenance.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `demolition_order_pending`
- **Category:** Municipal / Enforcement
- **Data Type:** `Boolean`
- **Description:** Recorded administrative notice of intent to demolish nuisance structure.
- **Legal Disclosure:** Property risks direct municipal demolition assessment liens if nuisance is not abated.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `red_tag_status`
- **Category:** Municipal / Enforcement
- **Data Type:** `Boolean`
- **Description:** Municipal building department order declaring structure unsafe for human occupancy.
- **Legal Disclosure:** Immediate prohibition on tenancy; requires building permits and structural certification to clear.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `unpermitted_work_flag`
- **Category:** Municipal / Enforcement
- **Data Type:** `Boolean`
- **Description:** Assessor or planning flag indicating construction completed without building permits.
- **Legal Disclosure:** Buyer inherits legal liability to bring unpermitted square footage to code or demolish it.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `agency_name`
- **Category:** Open Data / Infrastructure
- **Data Type:** `String`
- **Description:** Government body or county agency with custodial responsibility for the record.
- **Legal Disclosure:** Establishes statutory custody and source authenticity for court-admissible audit trails.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `ckan_package_id`
- **Category:** Open Data / Infrastructure
- **Data Type:** `UUID String`
- **Description:** UUID identifier for open datasets indexed on Data.gov / CKAN platforms.
- **Legal Disclosure:** Identifies open datasets for programmatic metadata retrieval and schema monitoring.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `download_url`
- **Category:** Open Data / Infrastructure
- **Data Type:** `URI`
- **Description:** Direct link to raw machine-readable data feeds (CSV, GeoJSON, Parquet, REST API).
- **Legal Disclosure:** Must verify HTTPS certificates and transport status prior to initiating scheduled automated ingestion.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `update_frequency`
- **Category:** Open Data / Infrastructure
- **Data Type:** `String (ISO Period)`
- **Description:** Frequency schedule at which source custodian refreshes public data records.
- **Legal Disclosure:** Determines pipeline synchronization cadences. Real estate distress requires weekly cycles, whereas zoning overlays are typically annual.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `apn`
- **Category:** Parcel
- **Data Type:** `String`
- **Description:** Assessor Parcel Number identifying county tax unit.
- **Legal Disclosure:** Must verify against county FIPS.
- **Linked Holders Count:** 5

### Associated Addresses & People

| # | Person / Entity | Address / APN | Indicator Value / Detail | Source Dataset |
|---|---|---|---|---|
| 1 | Pacific Coast Land Holdings LLC | APN 014-220-03 (State: CA, FIPS: 06045) | APN: 014-220-03 | distress_leads |
| 2 | Redwood Trust | APN 028-110-14 (State: CA, FIPS: 06045) | APN: 028-110-14 | distress_leads |
| 3 | Mendocino Heritage Corp | APN 005-090-22 (State: CA, FIPS: 06045) | APN: 005-090-22 | distress_leads |
| 4 | Vested Owner of Record | APN 003-360-15 (State: CA, FIPS: 06045) | APN: 003-360-15 | distress_leads |
| 5 | DISCLOSED SUBJECT | 431 Chablis Dr, Ukiah, CA 95482 | 170-132-21-00 | audit_dossiers (ID #1) |

---

## Indicator: `estate_tax_lien_flag`
- **Category:** Probate & Estate
- **Data Type:** `Boolean`
- **Description:** Statutory federal estate tax lien (IRC Section 6324) attaching to gross estate assets.
- **Legal Disclosure:** Clouds title for 10 years post-decedent death unless formal Certificate of Discharge is obtained.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `iaea_full_authority_flag`
- **Category:** Probate & Estate
- **Data Type:** `Boolean`
- **Description:** Independent Administration of Estates Act full authority indicator.
- **Legal Disclosure:** Permits executor to sell real property without mandatory court overbid auction procedures.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `letters_testamentary_issued`
- **Category:** Probate & Estate
- **Data Type:** `Boolean`
- **Description:** Judicial order appointing personal representative or executor with power of sale.
- **Legal Disclosure:** Confirms legal authority of executor to enter into binding purchase agreements under IAEA.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `probate_case_number`
- **Category:** Probate & Estate
- **Data Type:** `String`
- **Description:** Superior court probate docket tracking decedent estate administration.
- **Legal Disclosure:** Requires probate court approval or Letters of Administration before executing valid conveyance deed.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `survivorship_rights_flag`
- **Category:** Probate & Title
- **Data Type:** `Boolean`
- **Description:** Vesting type establishing automatic right of survivorship (Joint Tenancy, Community Property).
- **Legal Disclosure:** Allows title to vest automatically in surviving co-owner by recording Affidavit of Death without probate.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `zoning_code`
- **Category:** Real Estate / Municipal
- **Data Type:** `String`
- **Description:** Municipal or county land-use classification regulating physical development and density.
- **Legal Disclosure:** Determines permissible structure types (e.g., R-1 Single Family, AG Agricultural, C-2 Commercial). Overlays (e.g., riparian, wildfire hazard, slope) further restrict development rights.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `fips`
- **Category:** Real Estate / Spatial
- **Data Type:** `String (5-digit)`
- **Description:** Federal Information Processing Standard 5-digit county identifier code.
- **Legal Disclosure:** Mandatory for resolving duplicate or overlapping APN formats across disparate US county jurisdictions.
- **Linked Holders Count:** 5

### Associated Addresses & People

| # | Person / Entity | Address / APN | Indicator Value / Detail | Source Dataset |
|---|---|---|---|---|
| 1 | Pacific Coast Land Holdings LLC | APN 014-220-03 (State: CA, FIPS: 06045) | FIPS: 06045 | distress_leads |
| 2 | Redwood Trust | APN 028-110-14 (State: CA, FIPS: 06045) | FIPS: 06045 | distress_leads |
| 3 | Mendocino Heritage Corp | APN 005-090-22 (State: CA, FIPS: 06045) | FIPS: 06045 | distress_leads |
| 4 | Vested Owner of Record | APN 003-360-15 (State: CA, FIPS: 06045) | FIPS: 06045 | distress_leads |
| 5 | DISCLOSED SUBJECT | 431 Chablis Dr, Ukiah, CA 95482 | 06045 | audit_dossiers (ID #1) |

---

## Indicator: `gis_geometry`
- **Category:** Real Estate / Spatial
- **Data Type:** `GeoJSON / Well-Known Text (WKT)`
- **Description:** GeoJSON or Esri Shapefile vector polygon boundary coordinates.
- **Legal Disclosure:** GIS boundary shapes are administrative depictions for tax assessment and do not substitute for a licensed boundary survey by a Professional Land Surveyor.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `lot_size`
- **Category:** Real Estate / Spatial
- **Data Type:** `Float / Area (Acres/SqFt)`
- **Description:** Gross land area recorded on county tax rolls and recorded subdivision maps.
- **Legal Disclosure:** Plat map boundaries take legal precedence over county tax assessor GIS polygon approximations.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `legal_description`
- **Category:** Real Estate / Title
- **Data Type:** `Text`
- **Description:** Formal written metes-and-bounds, lot/block, or Public Land Survey System (PLSS) description.
- **Legal Disclosure:** The controlling legal definition of real property conveyance in recorded warranty deeds and grant deeds.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `alias_names`
- **Category:** Skip Tracing / Identity
- **Data Type:** `Array of Strings`
- **Description:** Documented legal name variants, prior maiden names, or fictitious business names (DBA).
- **Legal Disclosure:** Critical for cross-referencing judgment liens recorded under alternate name permutations.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `deceased_flag`
- **Category:** Skip Tracing / Identity
- **Data Type:** `Boolean`
- **Description:** Indicator that entity or owner is indexed on SSA Social Security Death Index (SSDI).
- **Legal Disclosure:** Marks property for immediate probate search and probate administration filings.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `phone_carrier`
- **Category:** Skip Tracing / Identity
- **Data Type:** `String`
- **Description:** Originating telecommunications provider for telephone contact records.
- **Legal Disclosure:** Identifies active tier-1 mobile carriers versus disposable VoIP/burner numbers to prioritize outreach quality.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `ssn_verified`
- **Category:** Skip Tracing / Identity
- **Data Type:** `Boolean`
- **Description:** Indicator that Social Security Number passes SSA issuance range and Death Master File checks.
- **Legal Disclosure:** Confirming identity helps prevent false-positive matches on common individual names.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `improvement_bond_1915_act`
- **Category:** Special Taxes & CFD
- **Data Type:** `Currency`
- **Description:** Special assessment lien authorized under 1915 Bond Act.
- **Legal Disclosure:** Direct parcel lien; unpaid balance accelerates foreclosure.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `mello_roos_annual_tax`
- **Category:** Special Taxes & CFD
- **Data Type:** `Currency`
- **Description:** Annual special tax levied under Community Facilities District.
- **Legal Disclosure:** Senior assessment collected on county tax roll.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `mello_roos_bond_maturity_year`
- **Category:** Special Taxes & CFD
- **Data Type:** `Integer`
- **Description:** Year CFD municipal infrastructure bond matures.
- **Legal Disclosure:** Expiration lowers property tax burden and improves net income.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `effective_age`
- **Category:** Structure & Physical
- **Data Type:** `Integer (Years)`
- **Description:** Appraiser-calculated physical age reflecting improvements, renovations, or neglect.
- **Legal Disclosure:** Calculates remaining economic life of commercial and residential improvements.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `foundation_type`
- **Category:** Structure & Physical
- **Data Type:** `String`
- **Description:** Structural foundation design (Raised Pier & Beam, Slab-on-Grade, Stem Wall, Basement).
- **Legal Disclosure:** Directly correlates with seismic retrofitting complexity and flood inundation vulnerability.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `year_built`
- **Category:** Structure & Physical
- **Data Type:** `Integer (Year)`
- **Description:** Recorded year of primary structure construction completion.
- **Legal Disclosure:** Baseline indicator for effective mechanical age, structural framing methods, and plumbing standards.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `hvac_type`
- **Category:** Structure & Utilities
- **Data Type:** `String`
- **Description:** Primary heating, ventilation, and air conditioning system installed.
- **Legal Disclosure:** Critical utility parameter for energy efficiency and replacement reserves.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `adjudicated_basin_flag`
- **Category:** Subsurface & Resources
- **Data Type:** `Boolean`
- **Description:** Groundwater extraction capped by court decree or SGMA.
- **Legal Disclosure:** Imposes strict metered allocations and drilling moratoriums.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `mineral_rights_severed_flag`
- **Category:** Subsurface & Resources
- **Data Type:** `Boolean`
- **Description:** Mineral rights severed from surface estate.
- **Legal Disclosure:** Severed estate allows surface access for extraction.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `timber_production_zone_flag`
- **Category:** Subsurface & Resources
- **Data Type:** `Boolean`
- **Description:** Tax overlay restricting land strictly to timber harvesting.
- **Legal Disclosure:** Mandatory 10-year phase-out; severe tax recapture if breached.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `water_rights_classification`
- **Category:** Subsurface & Resources
- **Data Type:** `String`
- **Description:** Legal doctrine governing extraction (Riparian, Appropriative).
- **Legal Disclosure:** Prior appropriation gives senior holders full priority.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `well_casing_depth`
- **Category:** Subsurface & Water
- **Data Type:** `Float`
- **Description:** Total vertical depth of groundwater well casing in feet.
- **Legal Disclosure:** Assesses aquifer stability and deepening costs.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `well_flow_rate_gpm`
- **Category:** Subsurface & Water
- **Data Type:** `Float`
- **Description:** Sustained yield of well in Gallons Per Minute.
- **Legal Disclosure:** Mandatory 3 to 5 GPM minimum for certificate of occupancy.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `grantee`
- **Category:** Title
- **Data Type:** `String`
- **Description:** Transferee or buyer acquiring title on deed.
- **Legal Disclosure:** Must verify against county recorder index.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `soil_classification`
- **Category:** Topography & Agriculture
- **Data Type:** `String`
- **Description:** USDA NRCS soil survey taxonomy and prime farmland rating.
- **Legal Disclosure:** Governs agricultural yield, septic drainfield absorption viability, and structural foundation expansive clay risks.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `slope_percentage`
- **Category:** Topography & Engineering
- **Data Type:** `Float (Percentage)`
- **Description:** Degrees of inclination or percent slope across parcel topography.
- **Legal Disclosure:** Municipal grading ordinances prohibit or heavily restrict building pads on slopes exceeding 15-20%.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `broadband_carrier_availability`
- **Category:** Utilities & Infrastructure
- **Data Type:** `String`
- **Description:** Terrestrial broadband connectivity (Fiber, Coaxial Cable, Fixed Wireless, Satellite Only).
- **Legal Disclosure:** Significant driver of valuation for remote residential and commercial flex properties.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `electric_service_provider`
- **Category:** Utilities & Off-Grid
- **Data Type:** `String`
- **Description:** Regulated electric utility grid operator (e.g., PG&E, ConEd, Southern Company).
- **Legal Disclosure:** Determines interconnect tariffs, net energy metering (NEM 3.0) policies, and base rate structures.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `grid_interconnection_status`
- **Category:** Utilities & Off-Grid
- **Data Type:** `String (Enum)`
- **Description:** Status of electrical utility meter hookup: Grid-Tied, Off-Grid Solar/Battery, De-energized.
- **Legal Disclosure:** De-energized meters exceeding 12 months often require comprehensive municipal safety reinspections.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `natural_gas_connected`
- **Category:** Utilities & Off-Grid
- **Data Type:** `Boolean`
- **Description:** Availability of direct piped natural gas versus bulk on-site propane tank (LPG).
- **Legal Disclosure:** Propane heating requires bulk tank lease/ownership verification and ongoing delivery logistics.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `sewer_type`
- **Category:** Utilities & Off-Grid
- **Data Type:** `String`
- **Description:** Waste disposal infrastructure: Municipal Public Sewer, On-Site Septic System, Cesspool.
- **Legal Disclosure:** Septic systems require percolation rate testing and county health clearance for transfer.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `water_source`
- **Category:** Utilities & Off-Grid
- **Data Type:** `String`
- **Description:** Primary potable water supply: Municipal City Water, Private Water Well, Shared Mutual.
- **Legal Disclosure:** Private wells require casing yield verification (GPM) and certified chemical potability tests.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `assessed_value`
- **Category:** Valuation
- **Data Type:** `Currency`
- **Description:** Statutory ad-valorem tax roll valuation.
- **Legal Disclosure:** Reflects statutory caps, not FMV.
- **Linked Holders Count:** 4

### Associated Addresses & People

| # | Person / Entity | Address / APN | Indicator Value / Detail | Source Dataset |
|---|---|---|---|---|
| 1 | Pacific Coast Land Holdings LLC | APN 014-220-03 (State: CA, FIPS: 06045) | Assessed Value: $450,000.00 | distress_leads |
| 2 | Redwood Trust | APN 028-110-14 (State: CA, FIPS: 06045) | Assessed Value: $720,000.00 | distress_leads |
| 3 | Mendocino Heritage Corp | APN 005-090-22 (State: CA, FIPS: 06045) | Assessed Value: $310,000.00 | distress_leads |
| 4 | Vested Owner of Record | APN 003-360-15 (State: CA, FIPS: 06045) | Assessed Value: $418,500.00 | distress_leads |

---

## Indicator: `improvement_value`
- **Category:** Valuation & Financial
- **Data Type:** `Currency (USD)`
- **Description:** Statutory assessed value of permanent residential, commercial, or outbuilding structures.
- **Legal Disclosure:** Unpermitted structural modifications or off-grid sheds may not be captured on county tax records.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `land_value`
- **Category:** Valuation & Financial
- **Data Type:** `Currency (USD)`
- **Description:** Statutory assessed value attributed exclusively to raw land excluding improvements.
- **Legal Disclosure:** Used to calculate residual value when analyzing tear-down prospects or agricultural viability.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `rent_zestimate`
- **Category:** Valuation & Financial
- **Data Type:** `Currency (USD/Month)`
- **Description:** Estimated median monthly gross rental revenue for an address.
- **Legal Disclosure:** Modeled metric derived from local multifamily and single-family rental listings. Subject to seasonal rental volatility.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

## Indicator: `zestimate_value`
- **Category:** Valuation & Financial
- **Data Type:** `Currency (USD)`
- **Description:** Algorithmic computer-generated automated valuation model (AVM) estimate.
- **Legal Disclosure:** Proprietary statistical estimation using recent neighborhood sales comparables. Unofficial estimate; does not constitute a formal appraisal.
- **Linked Holders Count:** 0

*No active entity holders currently indexed for this indicator.*

---

