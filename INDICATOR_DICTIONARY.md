# Master Public Record & Municipal Data Indicator Dictionary
**Enterprise Governance Notice:** Operational taxonomy and statutory regulatory disclosures across public record APIs, spatial GIS layers, encumbrance feeds, and municipal open data.

---

## Chain of Title

### `document_type`
- **Data Type:** `String`
- **Aliases / Synonyms:** deed_type,instrument_type,conveyance_type
- **Description:** Legal classification of recorded real estate instrument.
- **Legal & Operational Disclosure:** Distinguishes between Grant Deeds (warranting title free of unannounced encumbrances) versus Quitclaim Deeds (conveying solely grantor's current interest without title warranties).

### `grantor`
- **Data Type:** `String`
- **Aliases / Synonyms:** seller,transferor,prior_owner,grantor_name
- **Description:** Transferor, seller, or grantor relinquishing legal title in a recorded deed conveyance.
- **Legal & Operational Disclosure:** Must verify grantor matches preceding recorded grantee to ensure unbroken marketable chain of title.

### `instrument_number`
- **Data Type:** `String`
- **Aliases / Synonyms:** book_page,doc_number,recorder_id,recording_number
- **Description:** Unique county recorder document identifier or book/page reference.
- **Legal & Operational Disclosure:** Direct locator needed by title plants and county recorders to pull stamped microfiche or scanned deed copies.

### `recording_date`
- **Data Type:** `ISO-8601 Date`
- **Aliases / Synonyms:** doc_recording_date,filing_date,recorded_timestamp
- **Description:** Timestamp when deed or document was indexed by the County Recorder.
- **Legal & Operational Disclosure:** Establishes statutory legal priority under state recording acts (race-notice or notice jurisdictions).

### `sale_price`
- **Data Type:** `Currency (USD)`
- **Aliases / Synonyms:** purchase_price,consideration_amount,deed_amount,sales_price
- **Description:** Documentary transfer tax declared consideration paid for property transfer.
- **Legal & Operational Disclosure:** In non-disclosure states (e.g., TX, NM, UT), sale price is not disclosed on deed; documentary transfer tax calculations or MLS data must be utilized.

---

## Commercial & Debt

### `mechanics_lien_amount`
- **Data Type:** `Currency (USD)`
- **Aliases / Synonyms:** contractor_lien,mechanic_claim,construction_lien
- **Description:** Statutory mechanic's lien filed by unpaid general contractors or material suppliers.
- **Legal & Operational Disclosure:** Must be perfected via lawsuit within statutory deadlines (e.g., 90 days in CA) or become unenforceable.

### `ucc_1_filing_number`
- **Data Type:** `String`
- **Aliases / Synonyms:** ucc_filing,fixture_filing,ucc_id
- **Description:** Uniform Commercial Code fixture filing index with the Secretary of State.
- **Legal & Operational Disclosure:** Attaches security interest to property fixtures (HVAC units, commercial solar panels, heavy equipment).

---

## Commercial & Encumbrance

### `commercial_solar_ppa_flag`
- **Data Type:** `Boolean`
- **Aliases / Synonyms:** solar_ppa,solar_lease_lien
- **Description:** Recorded Solar Power Purchase Agreement or fixture UCC lien.
- **Legal & Operational Disclosure:** Obligates buyer to assume long-term energy purchase contracts or negotiate costly buyout terms.

---

## Commercial & Tax Roll

### `pace_financing_lien`
- **Data Type:** `Currency (USD)`
- **Aliases / Synonyms:** pace_lien,heroe_assessment,clean_energy_lien
- **Description:** Property Assessed Clean Energy (PACE) special tax assessment recorded on property.
- **Legal & Operational Disclosure:** Senior lien collecting repayment through county property tax bills; must be subordinated or paid off.

---

## Debt

### `open_balance`
- **Data Type:** `Currency`
- **Aliases / Synonyms:** loan_balance,lien_balance
- **Description:** Principal balance on mortgage or judgment liens.
- **Legal & Operational Disclosure:** Payoff demand statement required for per-diem balance.

---

## Distress

### `auction_date`
- **Data Type:** `Timestamp`
- **Aliases / Synonyms:** sale_date,foreclosure_date
- **Description:** Scheduled trustee or tax default auction date.
- **Legal & Operational Disclosure:** Subject to bankruptcy automatic stays.

### `lis_pendens`
- **Data Type:** `Docket`
- **Aliases / Synonyms:** suit_pending,notice_of_action
- **Description:** Recorded public notice of pending judicial litigation.
- **Legal & Operational Disclosure:** Constructive legal notice of foreclosure.

### `notice_of_default`
- **Data Type:** `Document`
- **Aliases / Synonyms:** nod,default_notice
- **Description:** Public notice filed by trustee declaring default.
- **Legal & Operational Disclosure:** Triggers statutory 90-day cure window.

### `tax_delinquency`
- **Data Type:** `Currency`
- **Aliases / Synonyms:** delinquent_taxes,back_taxes
- **Description:** Unpaid property tax balance past grace period.
- **Legal & Operational Disclosure:** Triggers statutory tax sale if uncured.

---

## Distress & Encumbrance

### `hoa_delinquency_amount`
- **Data Type:** `Currency (USD)`
- **Aliases / Synonyms:** hoa_arrears,past_due_hoa,condo_assessment_lien
- **Description:** Past-due homeowners association dues and assessment liens.
- **Legal & Operational Disclosure:** In super-priority lien states, HOA liens can extinguish first-position mortgages if foreclosed.

---

## Distress & Foreclosure

### `default_amount`
- **Data Type:** `Currency (USD)`
- **Aliases / Synonyms:** cure_amount,reinstatement_amount,arrearage_balance
- **Description:** Total delinquency balance required to cure default and reinstate loan.
- **Legal & Operational Disclosure:** Includes past-due payments, late charges, and legal fees. Does not represent total accelerated mortgage balance.

### `notice_of_sale`
- **Data Type:** `Document Reference / Date`
- **Aliases / Synonyms:** not_of_trustee_sale,nots,notice_of_trustee_sale,sheriff_sale_notice
- **Description:** Recorded notice specifying the exact auction date, time, and location for trustee or sheriff auction.
- **Legal & Operational Disclosure:** Published at least 20 to 21 days before auction across local newspapers and county public bulletin systems.

---

## Distress & Legal

### `bankruptcy_chapter`
- **Data Type:** `String (Enum: 7, 11, 12, 13)`
- **Aliases / Synonyms:** bankruptcy_filing,bkr_chapter,bankruptcy_type
- **Description:** Federal court bankruptcy jurisdiction filing (Chapter 7, 11, or 13).
- **Legal & Operational Disclosure:** Imposes immediate nationwide automatic stay halting all foreclosure, eviction, or collection enforcement actions without relief from stay.

### `case_number`
- **Data Type:** `String`
- **Aliases / Synonyms:** docket_number,court_case_id,case_id
- **Description:** Official court or county clerk tracking docket number.
- **Legal & Operational Disclosure:** Mandatory key required to pull direct civil complaint filings, lis pendens abstracts, or probate dockets.

### `judgment_amount`
- **Data Type:** `Currency (USD)`
- **Aliases / Synonyms:** judgment_lien_amount,court_award,court_judgment
- **Description:** Liquidated damages awarded by a court recorded as a general judgment lien.
- **Legal & Operational Disclosure:** Attaches automatically to all real property owned by debtor in county where abstract of judgment is recorded.

---

## Distress & Liens

### `lien_type`
- **Data Type:** `String`
- **Aliases / Synonyms:** encumbrance_type,claim_type,lien_classification
- **Description:** Legal classification of encumbrance recorded against title.
- **Legal & Operational Disclosure:** Priority generally dictated by recording date ('first in time, first in right') except for statutory super-priority tax liens, HOA assessment liens, and federal tax liens.

### `tax_delinquent_year`
- **Data Type:** `Integer (Year)`
- **Aliases / Synonyms:** default_year,delinquency_start_year
- **Description:** The tax year in which property taxes were first declared in default.
- **Legal & Operational Disclosure:** Statutory clock for tax sale auctions runs directly from this initial declaration date.

---

## Entity Verification

### `corporate_status`
- **Data Type:** `String`
- **Aliases / Synonyms:** sos_status,entity_status,business_standing
- **Description:** Secretary of State business registration standing (Active, Suspended, Dissolved, Forfeited).
- **Legal & Operational Disclosure:** Entities marked 'Suspended' (e.g., by CA Franchise Tax Board) lack legal capacity to contract, convey real property, or defend court actions.

### `ein`
- **Data Type:** `String (XX-XXXXXXX)`
- **Aliases / Synonyms:** fein,federal_tax_id,tax_ein
- **Description:** Federal Employer Identification Number issued by Internal Revenue Service.
- **Legal & Operational Disclosure:** Required for business entity verification, commercial debt matching, and corporate tax lien tracking.

### `registered_agent`
- **Data Type:** `String`
- **Aliases / Synonyms:** agent_for_service,resident_agent,statutory_agent
- **Description:** Individual or corporate entity authorized to receive service of process on behalf of an entity.
- **Legal & Operational Disclosure:** Primary point of contact for legal service of quiet title or pre-litigation settlement demands.

---

## Environmental / Climate

### `sea_level_rise_exposure`
- **Data Type:** `Float (Feet)`
- **Aliases / Synonyms:** slr_risk,coastal_inundation
- **Description:** NOAA projected coastal inundation under progressive 1-6 foot sea rise models.
- **Legal & Operational Disclosure:** Governs coastal development permits (CDP) under state Coastal Commissions.

---

## Environmental / Conservation

### `wetlands_flag`
- **Data Type:** `Boolean`
- **Aliases / Synonyms:** nwi_wetland,jurisdictional_wetland
- **Description:** USFWS National Wetlands Inventory (NWI) jurisdictional wetlands indicator.
- **Legal & Operational Disclosure:** Triggers Clean Water Act Section 404 Army Corps of Engineers permitting; severely limits physical land disturbance.

---

## Environmental / Contamination

### `superfund_npl_proximity`
- **Data Type:** `Float (Miles)`
- **Aliases / Synonyms:** cercla_site,epa_superfund,toxic_proximity
- **Description:** Proximity distance to EPA Comprehensive Environmental Response (CERCLA) Superfund site.
- **Legal & Operational Disclosure:** Creates potential joint and strict liability under federal CERCLA without bona fide prospective purchaser status.

---

## Environmental / Hazard

### `base_flood_elevation`
- **Data Type:** `Float (Feet)`
- **Aliases / Synonyms:** bfe,flood_elevation
- **Description:** FEMA modeled water surface elevation of a 100-year flood event.
- **Legal & Operational Disclosure:** Critical for building pad permits and elevation certificate compliance.

### `flood_zone`
- **Data Type:** `String`
- **Aliases / Synonyms:** fema_zone,flood_hazard_zone,floodplain
- **Description:** FEMA Special Flood Hazard Area (SFHA) designation (e.g., Zone A, AE, V, X).
- **Legal & Operational Disclosure:** Determines mandatory federal flood insurance purchase requirements under NFIP. Affects debt service and insurability.

### `wildfire_hazard_severity`
- **Data Type:** `String (Enum)`
- **Aliases / Synonyms:** fire_zone,vhfhsz,wildfire_risk
- **Description:** CAL FIRE / State Fire Marshal hazard classification (LRA/SRA: Moderate, High, Very High).
- **Legal & Operational Disclosure:** Very High Fire Hazard Severity Zones (VHFHSZ) trigger mandatory defensible space and strict home-hardening building codes.

---

## Environmental / Seismic

### `earthquake_fault_zone`
- **Data Type:** `Boolean`
- **Aliases / Synonyms:** alquist_priolo,fault_zone,seismic_fault
- **Description:** State geological survey designated active fault rupture hazard zone (e.g., Alquist-Priolo).
- **Legal & Operational Disclosure:** Prohibits human-occupancy structures directly astride active fault traces; requires licensed geologic fault investigation.

### `liquefaction_susceptibility`
- **Data Type:** `String (Enum: Low/Med/High)`
- **Aliases / Synonyms:** liquefaction_zone,soil_liquefaction
- **Description:** Susceptibility of saturated granular soil to strength loss during ground shaking.
- **Legal & Operational Disclosure:** Requires deep foundation engineering, pile driving, or soil densification mitigation.

---

## Mortgage & Securitization

### `current_interest_rate`
- **Data Type:** `Float (Percentage)`
- **Aliases / Synonyms:** nominal_rate,note_rate,mortgage_rate
- **Description:** Effective nominal interest rate recorded on promissory note or modification agreement.
- **Legal & Operational Disclosure:** Critical for debt-service coverage ratio (DSCR) underwriting.

### `heloc_draw_limit`
- **Data Type:** `Currency (USD)`
- **Aliases / Synonyms:** credit_line_cap,heloc_limit,revolving_cap
- **Description:** Maximum credit line capacity established on revolving Home Equity Line of Credit.
- **Legal & Operational Disclosure:** Unused credit capacity impacts borrower total debt capacity.

### `interest_rate_type`
- **Data Type:** `String (Enum: Fixed, ARM)`
- **Aliases / Synonyms:** rate_type,loan_type_rate,rate_structure
- **Description:** Interest rate classification: Fixed Rate (FRM), Adjustable (ARM), or Variable.
- **Legal & Operational Disclosure:** ARM notes in high-interest environments signal imminent debt-service reset shocks.

### `lender_name`
- **Data Type:** `String`
- **Aliases / Synonyms:** beneficiary,mortgagee,original_lender
- **Description:** Original beneficiary or lending institution named on deed of trust.
- **Legal & Operational Disclosure:** Distinguishes between GSE-backed loans (Fannie/Freddie), private money hard-money lenders, and seller-carry notes.

### `loan_maturity_date`
- **Data Type:** `ISO-8601 Date`
- **Aliases / Synonyms:** maturity_date,note_expiration,balloon_date
- **Description:** Stated legal maturity date of promissory note.
- **Legal & Operational Disclosure:** Matured loans with unpaid principal balloons represent high-priority recapitalization or distress opportunities.

### `mers_min_number`
- **Data Type:** `String (18-digit)`
- **Aliases / Synonyms:** mers_id,min_number,mers_tracking
- **Description:** Mortgage Electronic Registration Systems (MERS) 18-digit identification number.
- **Legal & Operational Disclosure:** Enables tracking of unrecorded electronic mortgage assignment transfers across secondary markets.

### `original_loan_amount`
- **Data Type:** `Currency (USD)`
- **Aliases / Synonyms:** note_amount,original_principal,face_value_loan
- **Description:** Original face value of promissory note secured by deed of trust.
- **Legal & Operational Disclosure:** Does not reflect amortization; baseline used for calculating original loan-to-value (LTV).

### `prepayment_penalty_flag`
- **Data Type:** `Boolean`
- **Aliases / Synonyms:** prepay_penalty,prepayment_clause
- **Description:** Clause imposing financial penalty for early principal payoff within statutory window.
- **Legal & Operational Disclosure:** Critical for calculating refinancing friction or accelerated acquisition costs.

### `servicer_name`
- **Data Type:** `String`
- **Aliases / Synonyms:** loan_servicer,note_servicer,current_servicer
- **Description:** Mortgage loan servicing entity collecting debt payments and managing escrow.
- **Legal & Operational Disclosure:** Points of contact for payoff demand letters, short sale packages, and loss mitigation.

### `subordination_status`
- **Data Type:** `String (Enum: 1st, 2nd, Junior)`
- **Aliases / Synonyms:** lien_priority,seniority_rank,mortgage_position
- **Description:** Lien seniority rank: 1st Trust Deed, 2nd Home Equity Line (HELOC), Mezzanine, or Junior.
- **Legal & Operational Disclosure:** Junior liens are wiped out in senior foreclosure sales unless surplus equity exists.

---

## Municipal & Structure

### `asbestos_hazard_indicator`
- **Data Type:** `Boolean`
- **Aliases / Synonyms:** acm_hazard,asbestos_flag
- **Description:** Indicator derived from construction pre-dating 1989 EPA ban on asbestos-containing materials.
- **Legal & Operational Disclosure:** Requires formal asbestos survey before demolition or renovation under NESHAP regulations.

### `lead_paint_risk_indicator`
- **Data Type:** `Boolean`
- **Aliases / Synonyms:** lead_hazard,pre_1978_lead
- **Description:** Binary indicator based on structure pre-dating federal 1978 residential ban.
- **Legal & Operational Disclosure:** Mandates federal EPA Title X lead-based paint disclosure prior to leasing or conveyance.

---

## Municipal / Enforcement

### `code_violation_count`
- **Data Type:** `Integer`
- **Aliases / Synonyms:** code_violations,blight_citations,municipal_citations
- **Description:** Active municipal code citations, blight complaints, or health department notices.
- **Legal & Operational Disclosure:** High violation velocity signals absentee owner neglect or deferred structural maintenance.

### `demolition_order_pending`
- **Data Type:** `Boolean`
- **Aliases / Synonyms:** demo_order,razing_order,abatement_demolition
- **Description:** Recorded administrative notice of intent to demolish nuisance structure.
- **Legal & Operational Disclosure:** Property risks direct municipal demolition assessment liens if nuisance is not abated.

### `red_tag_status`
- **Data Type:** `Boolean`
- **Aliases / Synonyms:** condemned_flag,unsafe_occupancy,red_tagged
- **Description:** Municipal building department order declaring structure unsafe for human occupancy.
- **Legal & Operational Disclosure:** Immediate prohibition on tenancy; requires building permits and structural certification to clear.

### `unpermitted_work_flag`
- **Data Type:** `Boolean`
- **Aliases / Synonyms:** unpermitted_addition,bootleg_structure,illegal_construction
- **Description:** Assessor or planning flag indicating construction completed without building permits.
- **Legal & Operational Disclosure:** Buyer inherits legal liability to bring unpermitted square footage to code or demolish it.

---

## Open Data / Infrastructure

### `agency_name`
- **Data Type:** `String`
- **Aliases / Synonyms:** custodian,data_owner,issuing_agency,source_agency
- **Description:** Government body or county agency with custodial responsibility for the record.
- **Legal & Operational Disclosure:** Establishes statutory custody and source authenticity for court-admissible audit trails.

### `ckan_package_id`
- **Data Type:** `UUID String`
- **Aliases / Synonyms:** dataset_id,ckan_id,package_uuid
- **Description:** UUID identifier for open datasets indexed on Data.gov / CKAN platforms.
- **Legal & Operational Disclosure:** Identifies open datasets for programmatic metadata retrieval and schema monitoring.

### `download_url`
- **Data Type:** `URI`
- **Aliases / Synonyms:** resource_url,data_link,direct_download
- **Description:** Direct link to raw machine-readable data feeds (CSV, GeoJSON, Parquet, REST API).
- **Legal & Operational Disclosure:** Must verify HTTPS certificates and transport status prior to initiating scheduled automated ingestion.

### `update_frequency`
- **Data Type:** `String (ISO Period)`
- **Aliases / Synonyms:** refresh_rate,ingest_frequency,cadence
- **Description:** Frequency schedule at which source custodian refreshes public data records.
- **Legal & Operational Disclosure:** Determines pipeline synchronization cadences. Real estate distress requires weekly cycles, whereas zoning overlays are typically annual.

---

## Parcel

### `apn`
- **Data Type:** `String`
- **Aliases / Synonyms:** parcel_id,pin,tax_id
- **Description:** Assessor Parcel Number identifying county tax unit.
- **Legal & Operational Disclosure:** Must verify against county FIPS.

---

## Probate & Estate

### `estate_tax_lien_flag`
- **Data Type:** `Boolean`
- **Aliases / Synonyms:** form_706_lien,federal_estate_lien
- **Description:** Statutory federal estate tax lien (IRC Section 6324) attaching to gross estate assets.
- **Legal & Operational Disclosure:** Clouds title for 10 years post-decedent death unless formal Certificate of Discharge is obtained.

### `iaea_full_authority_flag`
- **Data Type:** `Boolean`
- **Aliases / Synonyms:** iaea_full,iaea_powers
- **Description:** Independent Administration of Estates Act full authority indicator.
- **Legal & Operational Disclosure:** Permits executor to sell real property without mandatory court overbid auction procedures.

### `letters_testamentary_issued`
- **Data Type:** `Boolean`
- **Aliases / Synonyms:** letters_issued,executor_authority,probate_authority
- **Description:** Judicial order appointing personal representative or executor with power of sale.
- **Legal & Operational Disclosure:** Confirms legal authority of executor to enter into binding purchase agreements under IAEA.

### `probate_case_number`
- **Data Type:** `String`
- **Aliases / Synonyms:** estate_docket,probate_id,probate_filing
- **Description:** Superior court probate docket tracking decedent estate administration.
- **Legal & Operational Disclosure:** Requires probate court approval or Letters of Administration before executing valid conveyance deed.

---

## Probate & Title

### `survivorship_rights_flag`
- **Data Type:** `Boolean`
- **Aliases / Synonyms:** joint_tenancy_right,right_of_survivorship
- **Description:** Vesting type establishing automatic right of survivorship (Joint Tenancy, Community Property).
- **Legal & Operational Disclosure:** Allows title to vest automatically in surviving co-owner by recording Affidavit of Death without probate.

---

## Real Estate / Municipal

### `zoning_code`
- **Data Type:** `String`
- **Aliases / Synonyms:** zoning,land_use_code,zoning_district,use_designation
- **Description:** Municipal or county land-use classification regulating physical development and density.
- **Legal & Operational Disclosure:** Determines permissible structure types (e.g., R-1 Single Family, AG Agricultural, C-2 Commercial). Overlays (e.g., riparian, wildfire hazard, slope) further restrict development rights.

---

## Real Estate / Spatial

### `fips`
- **Data Type:** `String (5-digit)`
- **Aliases / Synonyms:** fips_code,county_fips,jurisdiction_code
- **Description:** Federal Information Processing Standard 5-digit county identifier code.
- **Legal & Operational Disclosure:** Mandatory for resolving duplicate or overlapping APN formats across disparate US county jurisdictions.

### `gis_geometry`
- **Data Type:** `GeoJSON / Well-Known Text (WKT)`
- **Aliases / Synonyms:** boundary_polygon,parcel_geom,spatial_geometry,shape_coordinates
- **Description:** GeoJSON or Esri Shapefile vector polygon boundary coordinates.
- **Legal & Operational Disclosure:** GIS boundary shapes are administrative depictions for tax assessment and do not substitute for a licensed boundary survey by a Professional Land Surveyor.

### `lot_size`
- **Data Type:** `Float / Area (Acres/SqFt)`
- **Aliases / Synonyms:** parcel_area,lot_sqft,acreage,gross_area
- **Description:** Gross land area recorded on county tax rolls and recorded subdivision maps.
- **Legal & Operational Disclosure:** Plat map boundaries take legal precedence over county tax assessor GIS polygon approximations.

---

## Real Estate / Title

### `legal_description`
- **Data Type:** `Text`
- **Aliases / Synonyms:** metes_and_bounds,plss_description,plat_legal
- **Description:** Formal written metes-and-bounds, lot/block, or Public Land Survey System (PLSS) description.
- **Legal & Operational Disclosure:** The controlling legal definition of real property conveyance in recorded warranty deeds and grant deeds.

---

## Skip Tracing / Identity

### `alias_names`
- **Data Type:** `Array of Strings`
- **Aliases / Synonyms:** aka,fka,dba_name,alternate_names
- **Description:** Documented legal name variants, prior maiden names, or fictitious business names (DBA).
- **Legal & Operational Disclosure:** Critical for cross-referencing judgment liens recorded under alternate name permutations.

### `deceased_flag`
- **Data Type:** `Boolean`
- **Aliases / Synonyms:** is_deceased,ssdi_match,death_indicator
- **Description:** Indicator that entity or owner is indexed on SSA Social Security Death Index (SSDI).
- **Legal & Operational Disclosure:** Marks property for immediate probate search and probate administration filings.

### `phone_carrier`
- **Data Type:** `String`
- **Aliases / Synonyms:** telecom_carrier,carrier_name,wireless_provider
- **Description:** Originating telecommunications provider for telephone contact records.
- **Legal & Operational Disclosure:** Identifies active tier-1 mobile carriers versus disposable VoIP/burner numbers to prioritize outreach quality.

### `ssn_verified`
- **Data Type:** `Boolean`
- **Aliases / Synonyms:** ssn_valid,ssn_match,identity_verified
- **Description:** Indicator that Social Security Number passes SSA issuance range and Death Master File checks.
- **Legal & Operational Disclosure:** Confirming identity helps prevent false-positive matches on common individual names.

---

## Structure & Physical

### `effective_age`
- **Data Type:** `Integer (Years)`
- **Aliases / Synonyms:** adjusted_age,economic_age
- **Description:** Appraiser-calculated physical age reflecting improvements, renovations, or neglect.
- **Legal & Operational Disclosure:** Calculates remaining economic life of commercial and residential improvements.

### `foundation_type`
- **Data Type:** `String`
- **Aliases / Synonyms:** foundation_style,substructure
- **Description:** Structural foundation design (Raised Pier & Beam, Slab-on-Grade, Stem Wall, Basement).
- **Legal & Operational Disclosure:** Directly correlates with seismic retrofitting complexity and flood inundation vulnerability.

### `year_built`
- **Data Type:** `Integer (Year)`
- **Aliases / Synonyms:** construction_year,built_year,vintage
- **Description:** Recorded year of primary structure construction completion.
- **Legal & Operational Disclosure:** Baseline indicator for effective mechanical age, structural framing methods, and plumbing standards.

---

## Structure & Utilities

### `hvac_type`
- **Data Type:** `String`
- **Aliases / Synonyms:** heating_system,cooling_system,climate_control
- **Description:** Primary heating, ventilation, and air conditioning system installed.
- **Legal & Operational Disclosure:** Critical utility parameter for energy efficiency and replacement reserves.

---

## Title

### `grantee`
- **Data Type:** `String`
- **Aliases / Synonyms:** buyer,new_owner
- **Description:** Transferee or buyer acquiring title on deed.
- **Legal & Operational Disclosure:** Must verify against county recorder index.

---

## Topography & Agriculture

### `soil_classification`
- **Data Type:** `String`
- **Aliases / Synonyms:** usda_soil,soil_type,soil_map_unit
- **Description:** USDA NRCS soil survey taxonomy and prime farmland rating.
- **Legal & Operational Disclosure:** Governs agricultural yield, septic drainfield absorption viability, and structural foundation expansive clay risks.

---

## Topography & Engineering

### `slope_percentage`
- **Data Type:** `Float (Percentage)`
- **Aliases / Synonyms:** grade_slope,topographic_slope,incline
- **Description:** Degrees of inclination or percent slope across parcel topography.
- **Legal & Operational Disclosure:** Municipal grading ordinances prohibit or heavily restrict building pads on slopes exceeding 15-20%.

---

## Utilities & Infrastructure

### `broadband_carrier_availability`
- **Data Type:** `String`
- **Aliases / Synonyms:** internet_carrier,fiber_available,broadband_type
- **Description:** Terrestrial broadband connectivity (Fiber, Coaxial Cable, Fixed Wireless, Satellite Only).
- **Legal & Operational Disclosure:** Significant driver of valuation for remote residential and commercial flex properties.

---

## Utilities & Off-Grid

### `electric_service_provider`
- **Data Type:** `String`
- **Aliases / Synonyms:** electric_utility,power_provider,grid_operator
- **Description:** Regulated electric utility grid operator (e.g., PG&E, ConEd, Southern Company).
- **Legal & Operational Disclosure:** Determines interconnect tariffs, net energy metering (NEM 3.0) policies, and base rate structures.

### `grid_interconnection_status`
- **Data Type:** `String (Enum)`
- **Aliases / Synonyms:** meter_status,power_connected,grid_status
- **Description:** Status of electrical utility meter hookup: Grid-Tied, Off-Grid Solar/Battery, De-energized.
- **Legal & Operational Disclosure:** De-energized meters exceeding 12 months often require comprehensive municipal safety reinspections.

### `natural_gas_connected`
- **Data Type:** `Boolean`
- **Aliases / Synonyms:** gas_service,piped_gas,propane_flag
- **Description:** Availability of direct piped natural gas versus bulk on-site propane tank (LPG).
- **Legal & Operational Disclosure:** Propane heating requires bulk tank lease/ownership verification and ongoing delivery logistics.

### `sewer_type`
- **Data Type:** `String`
- **Aliases / Synonyms:** septic_system,wastewater,sewer_service
- **Description:** Waste disposal infrastructure: Municipal Public Sewer, On-Site Septic System, Cesspool.
- **Legal & Operational Disclosure:** Septic systems require percolation rate testing and county health clearance for transfer.

### `water_source`
- **Data Type:** `String`
- **Aliases / Synonyms:** potable_water,water_service,well_water
- **Description:** Primary potable water supply: Municipal City Water, Private Water Well, Shared Mutual.
- **Legal & Operational Disclosure:** Private wells require casing yield verification (GPM) and certified chemical potability tests.

---

## Valuation

### `assessed_value`
- **Data Type:** `Currency`
- **Aliases / Synonyms:** tax_value,assessment
- **Description:** Statutory ad-valorem tax roll valuation.
- **Legal & Operational Disclosure:** Reflects statutory caps, not FMV.

---

## Valuation & Financial

### `improvement_value`
- **Data Type:** `Currency (USD)`
- **Aliases / Synonyms:** structure_value,building_assessed_value,improvements
- **Description:** Statutory assessed value of permanent residential, commercial, or outbuilding structures.
- **Legal & Operational Disclosure:** Unpermitted structural modifications or off-grid sheds may not be captured on county tax records.

### `land_value`
- **Data Type:** `Currency (USD)`
- **Aliases / Synonyms:** assessed_land,land_roll_value
- **Description:** Statutory assessed value attributed exclusively to raw land excluding improvements.
- **Legal & Operational Disclosure:** Used to calculate residual value when analyzing tear-down prospects or agricultural viability.

### `rent_zestimate`
- **Data Type:** `Currency (USD/Month)`
- **Aliases / Synonyms:** estimated_rent,rental_avm,rent_estimate
- **Description:** Estimated median monthly gross rental revenue for an address.
- **Legal & Operational Disclosure:** Modeled metric derived from local multifamily and single-family rental listings. Subject to seasonal rental volatility.

### `zestimate_value`
- **Data Type:** `Currency (USD)`
- **Aliases / Synonyms:** avm_estimate,zestimate,market_estimate
- **Description:** Algorithmic computer-generated automated valuation model (AVM) estimate.
- **Legal & Operational Disclosure:** Proprietary statistical estimation using recent neighborhood sales comparables. Unofficial estimate; does not constitute a formal appraisal.

---

