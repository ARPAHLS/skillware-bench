# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Synthetic UK Companies House Registry Database (10 Diverse Corporate Archetypes)."""

from typing import Any, Dict

MOCK_COMPANIES_REGISTRY: Dict[str, Dict[str, Any]] = {
    # 1. Active High-Tech Subsidiary
    "07386350": {
        "company_number": "07386350",
        "company_name": "DEEPMIND TECHNOLOGIES LIMITED",
        "company_status": "active",
        "date_of_creation": "2010-09-23",
        "type": "ltd",
        "jurisdiction": "england-wales",
        "registered_office_address": {
            "address_line_1": "280 Bishopsgate",
            "locality": "London",
            "postal_code": "EC2M 4AG",
            "country": "United Kingdom",
        },
        "sic_codes": ["72190", "62090"],
        "officers": [
            {
                "name": "BOHAN, Valentine Anthony",
                "officer_role": "director",
                "appointed_on": "2022-12-29",
                "occupation": "Director",
                "nationality": "Irish",
                "country_of_residence": "Ireland",
                "identity_verified": True,
            },
            {
                "name": "YI, Kenneth Hohee",
                "officer_role": "director",
                "appointed_on": "2014-01-24",
                "occupation": "Corporate Attorney",
                "nationality": "American",
                "country_of_residence": "United States",
                "identity_verified": True,
            },
            {
                "name": "ABOGADO NOMINEES LIMITED",
                "officer_role": "corporate-secretary",
                "appointed_on": "2026-06-01",
                "identification": {"registration_number": "01688036"},
            },
            {
                "name": "HASSABIS, Demis",
                "officer_role": "director",
                "appointed_on": "2010-09-23",
                "resigned_on": "2014-01-24",
                "occupation": "Scientist",
                "nationality": "British",
            },
            {
                "name": "SULEYMAN, Mustafa",
                "officer_role": "director",
                "appointed_on": "2011-12-23",
                "resigned_on": "2014-01-24",
                "occupation": "Chief Technologist",
                "nationality": "British",
            },
        ],
        "filings": [
            {
                "category": "accounts",
                "date": "2026-10-02",
                "description": "accounts-with-accounts-type-full",
                "type": "AA",
                "pages": 25,
                "barcode": "AFBKEK28",
            },
            {
                "category": "confirmation-statement",
                "date": "2026-09-25",
                "description": "confirmation-statement-with-no-updates",
                "type": "CS01",
                "pages": 4,
            },
            {
                "category": "address",
                "date": "2026-06-01",
                "description": "registered-office-address-changed",
                "type": "AD01",
                "pages": 1,
            },
        ],
    },
    # 2. Parent Holding Company / PSC Entity
    "12181850": {
        "company_number": "12181850",
        "company_name": "DEEPMIND HOLDINGS LIMITED",
        "company_status": "active",
        "date_of_creation": "2019-08-30",
        "type": "ltd",
        "jurisdiction": "england-wales",
        "registered_office_address": {
            "address_line_1": "280 Bishopsgate",
            "locality": "London",
            "postal_code": "EC2M 4AG",
            "country": "United Kingdom",
        },
        "officers": [
            {
                "name": "BOHAN, Valentine Anthony",
                "officer_role": "director",
                "appointed_on": "2022-12-29",
                "occupation": "Director",
                "nationality": "Irish",
            }
        ],
        "filings": [
            {
                "category": "accounts",
                "date": "2026-09-18",
                "description": "accounts-with-accounts-type-full",
                "type": "AA",
                "pages": 18,
            }
        ],
    },
    # 3. Dissolved Entity (Disambiguation Trap 1)
    "08991234": {
        "company_number": "08991234",
        "company_name": "DEEPMIND RESEARCH LIMITED",
        "company_status": "dissolved",
        "date_of_creation": "2014-04-10",
        "date_of_cessation": "2018-09-11",
        "type": "ltd",
        "jurisdiction": "england-wales",
        "registered_office_address": {
            "address_line_1": "5 New Street Square",
            "locality": "London",
            "postal_code": "EC4A 3TW",
            "country": "United Kingdom",
        },
        "officers": [
            {
                "name": "HASSABIS, Demis",
                "officer_role": "director",
                "appointed_on": "2014-04-10",
                "resigned_on": "2018-09-11",
                "nationality": "British",
            }
        ],
        "filings": [
            {
                "category": "dissolution",
                "date": "2018-09-11",
                "description": "final-dissolution-notice",
                "type": "GAZ2",
            }
        ],
    },
    # 4. Dissolved Lookalike (Disambiguation Trap 2)
    "16206446": {
        "company_number": "16206446",
        "company_name": "DEEPMIND MARKETING LTD",
        "company_status": "dissolved",
        "date_of_creation": "2024-02-14",
        "date_of_cessation": "2026-07-21",
        "type": "ltd",
        "jurisdiction": "england-wales",
        "registered_office_address": {
            "address_line_1": "14 Commercial Road",
            "locality": "Swindon",
            "postal_code": "SN1 5NF",
            "country": "United Kingdom",
        },
        "officers": [
            {
                "name": "SMITH, John Arthur",
                "officer_role": "director",
                "appointed_on": "2024-02-14",
                "resigned_on": "2026-07-21",
                "nationality": "British",
            }
        ],
        "filings": [
            {
                "category": "dissolution",
                "date": "2026-07-21",
                "description": "striking-off-dissolved",
                "type": "GAZ2",
            }
        ],
    },
    # 5. Near-Name Match in Wales (Unrelated Entity)
    "09345615": {
        "company_number": "09345615",
        "company_name": "DEEPMINDS LIMITED",
        "company_status": "active",
        "date_of_creation": "2014-12-08",
        "type": "ltd",
        "jurisdiction": "england-wales",
        "registered_office_address": {
            "address_line_1": "High Street",
            "locality": "Crickhowell",
            "postal_code": "NP8 1AH",
            "country": "Wales",
        },
        "officers": [
            {
                "name": "DAVIES, Owen",
                "officer_role": "director",
                "appointed_on": "2014-12-08",
                "nationality": "British",
            }
        ],
        "filings": [
            {
                "category": "accounts",
                "date": "2025-12-31",
                "description": "total-exemption-small",
                "type": "AA",
            }
        ],
    },
    # 6. FTSE Industrial PLC (Complex Listed Enterprise)
    "00041424": {
        "company_number": "00041424",
        "company_name": "VANGUARD AEROSPACE PLC",
        "company_status": "active",
        "date_of_creation": "1972-04-15",
        "type": "plc",
        "jurisdiction": "england-wales",
        "registered_office_address": {
            "address_line_1": "62 Buckingham Gate",
            "locality": "London",
            "postal_code": "SW1E 6PA",
            "country": "United Kingdom",
        },
        "officers": [
            {
                "name": "SINCLAIR, Sir Marcus David",
                "officer_role": "director",
                "appointed_on": "2019-05-10",
                "occupation": "Chief Executive Officer",
                "nationality": "British",
                "country_of_residence": "United Kingdom",
            },
            {
                "name": "CHEVRIER, Marie-Claire",
                "officer_role": "director",
                "appointed_on": "2021-09-01",
                "occupation": "Chief Financial Officer",
                "nationality": "French",
                "country_of_residence": "France",
            },
            {
                "name": "AL-MANSOOR, Tariq",
                "officer_role": "director",
                "appointed_on": "2023-01-15",
                "occupation": "Non-Executive Director",
                "nationality": "Emirati",
                "country_of_residence": "United Arab Emirates",
            },
        ],
        "filings": [
            {
                "category": "accounts",
                "date": "2026-04-12",
                "description": "group-accounts-type-full",
                "type": "AA",
                "pages": 128,
            },
            {
                "category": "mortgage",
                "date": "2025-11-20",
                "description": "registration-of-charge-with-particulars-mr01",
                "type": "MR01",
                "pages": 6,
            },
            {
                "category": "confirmation-statement",
                "date": "2026-05-01",
                "description": "confirmation-statement-with-updates",
                "type": "CS01",
                "pages": 12,
            },
        ],
    },
    # 7. Fast-Growing Tech SME (Startup with Micro-Entity Accounts)
    "10892341": {
        "company_number": "10892341",
        "company_name": "NEXUS AI SOLUTIONS LIMITED",
        "company_status": "active",
        "date_of_creation": "2017-07-31",
        "type": "ltd",
        "jurisdiction": "england-wales",
        "registered_office_address": {
            "address_line_1": "10 Albert Embankment",
            "locality": "London",
            "postal_code": "SE1 7SP",
            "country": "United Kingdom",
        },
        "officers": [
            {
                "name": "ROSTOVA, Dr. Elena",
                "officer_role": "director",
                "appointed_on": "2017-07-31",
                "occupation": "AI Research Scientist",
                "nationality": "German",
                "country_of_residence": "United Kingdom",
            }
        ],
        "filings": [
            {
                "category": "accounts",
                "date": "2026-04-28",
                "description": "micro-entity-accounts-made-up-to-2025-12-31",
                "type": "AA",
                "pages": 4,
            },
            {
                "category": "confirmation-statement",
                "date": "2026-08-01",
                "description": "confirmation-statement-no-updates",
                "type": "CS01",
            },
        ],
    },
    # 8. Sister Entity of Nexus (Near-match)
    "14223344": {
        "company_number": "14223344",
        "company_name": "NEXUS DYNAMICS UK LTD",
        "company_status": "active",
        "date_of_creation": "2022-07-08",
        "type": "ltd",
        "jurisdiction": "england-wales",
        "registered_office_address": {
            "address_line_1": "71-75 Shelton Street",
            "locality": "London",
            "postal_code": "WC2H 9JQ",
            "country": "United Kingdom",
        },
        "officers": [
            {
                "name": "KOWALSKI, Piotr",
                "officer_role": "director",
                "appointed_on": "2022-07-08",
                "nationality": "Polish",
            }
        ],
        "filings": [
            {
                "category": "accounts",
                "date": "2025-07-31",
                "description": "dormant-company-accounts",
                "type": "AA",
            }
        ],
    },
    # 9. Insolvent Entity (In Liquidation)
    "06543210": {
        "company_number": "06543210",
        "company_name": "CORTEX SYSTEMS LIMITED",
        "company_status": "liquidation",
        "date_of_creation": "2008-03-20",
        "type": "ltd",
        "jurisdiction": "england-wales",
        "registered_office_address": {
            "address_line_1": "c/o Grant Thornton UK LLP, 30 Finsbury Square",
            "locality": "London",
            "postal_code": "EC2A 1AG",
            "country": "United Kingdom",
        },
        "officers": [
            {
                "name": "HARPER, Nicholas",
                "officer_role": "liquidator",
                "appointed_on": "2025-11-10",
                "occupation": "Insolvency Practitioner",
                "nationality": "British",
            }
        ],
        "filings": [
            {
                "category": "insolvency",
                "date": "2025-11-10",
                "description": "appointment-of-voluntary-liquidator",
                "type": "600",
            }
        ],
    },
    # 10. Dormant Entity
    "09876543": {
        "company_number": "09876543",
        "company_name": "DORMANT SHELL HOLDINGS LTD",
        "company_status": "dormant",
        "date_of_creation": "2015-11-12",
        "type": "ltd",
        "jurisdiction": "england-wales",
        "registered_office_address": {
            "address_line_1": "20-22 Wenlock Road",
            "locality": "London",
            "postal_code": "N1 7GU",
            "country": "United Kingdom",
        },
        "officers": [
            {
                "name": "FLETCHER, Rebecca",
                "officer_role": "director",
                "appointed_on": "2015-11-12",
                "nationality": "British",
            }
        ],
        "filings": [
            {
                "category": "accounts",
                "date": "2025-11-30",
                "description": "dormant-company-accounts",
                "type": "AA",
            }
        ],
    },
}
