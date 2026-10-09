# Enterprise Data Indicator & Schema Specification

This document provides complete technical, legal, and operational disclosures for all indexed attributes across public record, municipal, and commercial registry feeds.

---

## 1. Real Estate & Parcel Geometrics

### `apn` (Assessor Parcel Number)
* **Definition:** A unique identifier assigned by county tax assessors to identify parcels of land for property tax tracking and zoning administration.
* **Format:** Alphanumeric, strictly county-specific (e.g., `014-220-03-00` or `123456789`).
* **Source Feeds:** County Tax Assessor, PropMix PubRec, County GIS ArcServer.
* **Accuracy & Disclosure:** Non-static. APNs can undergo splits, mergers, or redistricting. Cannot be verified without matching against `fips` (Federal Information Processing Standard) county code.

### `assessed_value`
* **Definition:** The dollar value placed on land and improvements by the local government taxation authority for ad valorem property tax calculation.
* **Components:** Land Value + Improvement/Structure Value.
* **Disclosure:** Assessed values rarely equal current market transactions or fair market value. They are governed by statutory assessment caps (e.g., California Proposition 13 limiting increases to 2% annually until a reassessment trigger occurs).

### `tax_delinquency`
* **Definition:** A binary flag or cumulative dollar value indicating unpaid ad valorem county property taxes after the final statutory statutory delinquency date.
* **Risk Profile:** High-priority distress signal. Uncured delinquency initiates statutory redemption periods (typically 3–5 years), followed by County Tax Sale auctions.

---

## 2. Title, Liens & Legal Encumbrances

### `lis_pendens`
* **Definition:** Latin for "suit pending." A recorded formal notice that legal action has been initiated affecting title to real property.
* **Operational Significance:** Marks the formal legal initiation of pre-foreclosure proceedings before a court-ordered auction or judicial sale.
* **Verification:** Requires County Recorder verification against county case number and docket indexing.

### `notice_of_default` (NOD)
* **Definition:** A public notice filed by a trustee or mortgage servicer with the County Recorder declaring that a borrower has defaulted on a promissory note secured by a deed of trust.
* **Execution Window:** In non-judicial foreclosure states, triggers a statutory cure window (typically 90 days) before a Notice of Trustee Sale can be published.

### `lien_type` & `open_balance`
* **Definition:** A legal claim placed against an asset to secure payment of a debt or legal obligation.
* **Sub-Classifications:**
  * **Tax Liens:** IRS Federal Tax Liens (priority claim), State Franchise Tax Liens, Municipal Utility Liens.
  * **Mechanic's Liens:** Filed by unpaid contractors, subcontractors, or material suppliers; attaches directly to real property.
  * **Judicial Liens:** Recorded judgments resulting from court decisions.

---

## 3. Identity & Entity Verification

### `corporate_status` & `ein`
* **Definition:** Secretary of State entity registration status (Active, Delinquent, Suspended, Dissolved) alongside Federal Employer Identification Number.
* **Verification Criteria:** A company marked "Suspended" (e.g., FTB suspended in CA) cannot legally contract, defend a lawsuit, or execute valid deeds of transfer.
