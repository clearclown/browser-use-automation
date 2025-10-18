# PRISMA 2020 Flow Diagram

## Search Flow

```mermaid
flowchart TD
	%% PRISMA 2020 Flow Diagram

	%% Identification
  DB_IEEE_Xplore["Records from IEEE Xplore<br/>n = 450"]
  DB_PubMed["Records from PubMed<br/>n = 230"]
  DB_arXiv["Records from arXiv<br/>n = 120"]
  OTHER_Citation_searching["Records from Citation searching<br/>n = 25"]

	IDENTIFIED["Records identified<br/>n = 825"]
	DUPLICATES["Duplicate records removed<br/>n = 180"]

	%% Screening
	SCREENED["Records screened<br/>n = 645"]
	SCREEN_EXCLUDED["Records excluded<br/>n = 395"]

	%% Eligibility
	SOUGHT["Reports sought for retrieval<br/>n = 250"]
	NOT_RETRIEVED["Reports not retrieved<br/>n = 8"]
	ASSESSED["Reports assessed for eligibility<br/>n = 242"]
	ELIG_EXCLUDED["Reports excluded<br/>n = 52"]

	%% Included
	INCLUDED["Studies included in review<br/>n = 30<br/>Reports: 33"]

	%% Connections
  DB_IEEE_Xplore --> IDENTIFIED
  DB_PubMed --> IDENTIFIED
  DB_arXiv --> IDENTIFIED
  OTHER_Citation_searching --> IDENTIFIED
  IDENTIFIED --> DUPLICATES
  DUPLICATES --> SCREENED
  SCREENED --> SCREEN_EXCLUDED
  SCREENED --> SOUGHT
  SOUGHT --> NOT_RETRIEVED
  SOUGHT --> ASSESSED
  ASSESSED --> ELIG_EXCLUDED
  ASSESSED --> INCLUDED
```

## Detailed Breakdown

### Identification

**Database Searches:**

- **IEEE Xplore**: 450 records (searched: 2024-10-18)
- **PubMed**: 230 records (searched: 2024-10-18)
- **arXiv**: 120 records (searched: 2024-10-18)

**Other Sources:**

- **Citation searching**: 25 records

**Total Records Identified:** 825
**Duplicate Records Removed:** 180

### Screening

**Records Screened (title/abstract):** 645
**Records Excluded:** 395

**Exclusion Reasons:**

- Not relevant to topic: 320 records
- Not in English: 45 records
- Wrong publication type: 30 records

### Eligibility Assessment

**Reports Sought for Retrieval:** 250
**Reports Not Retrieved:** 8
**Reports Assessed (full-text):** 242
**Reports Excluded:** 52

**Exclusion Reasons:**

- Insufficient data: 35 reports
- Not peer-reviewed: 12 reports
- Duplicate publication: 5 reports

### Included

**Studies Included in Review:** 30
**Total Reports:** 33

---

*Generated: 2025-10-18 06:10:26*
*PRISMA 2020 compliant flow diagram*
