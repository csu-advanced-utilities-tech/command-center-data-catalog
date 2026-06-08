"""Shared constants for the Command Center Data Catalog build."""

SITE_TITLE = "Command Center Data Catalog"

# Two-way cross-link with the Data Governance hub.
GOVERNANCE_HUB_URL = "https://csu-advanced-utilities-tech.github.io/data-governance/"

# Business-domain grouping for catalog tables. Order here = display order on the
# index page. Tables not listed fall into OTHER_DOMAIN automatically. Keep this in
# sync with the governance hub's "Scope & Data Domains" section.
DOMAIN_MAP = {
    "Premises & Locations": [
        "ADDRESS", "SERVICELOCATIONS", "GPSLOCATIONS",
    ],
    "Endpoints & Meters": [
        "ENDPOINTS", "METERS", "ENDPOINTMODELS", "METERCONFIGURATION",
        "ENDPOINTMETERCONFIGURATION", "RFENDPOINTPROPERTIES",
    ],
    "Network & Collection": [
        "COLLECTORS", "COLLECTORSTATS", "RSSDEVICES",
    ],
    "Interval & Register Reads": [
        "INTERVALDATA", "INTERVALDATALATESTVALUES", "INTERVALTYPES",
        "IDREADINGLOGS", "IDREADINGLATESTVALUES",
    ],
    "Commands & Control": [
        "COMMANDLOG", "COMMANDSSENT", "COMMANDRESPONSE", "COMMANDTYPES",
        "COMMANDSTATUSCODES", "PACKETTYPES",
    ],
    "Events, Errors & Status": [
        "EVENTLOG", "EVENTTYPES", "ERRORLOG", "ERRORTYPES", "STATUSCODES",
        "ENDPOINTSTATUSCODEHISTORY",
    ],
    "Plans & Schedules": [
        "PLANS", "PLANTYPES", "PLANSCHEDULES", "READ_SCHEDULE", "BILLINGCYCLES",
    ],
    "Grouping & Org": [
        "GROUPS", "GROUPTYPES", "ENDPOINTGROUPASSOC",
    ],
    "Access & Admin": [
        "USERS", "USERROLE", "DATADEFINITIONS", "DATABASE_MAINT_ARCHIVE",
        "ENDPOINTDEPLOYMENTSTATISTICS", "ENDPOINTNOTES",
    ],
}

OTHER_DOMAIN = "Other / Uncategorized"

# Reverse lookup, built once at import.
_TABLE_TO_DOMAIN = {
    table: domain for domain, tables in DOMAIN_MAP.items() for table in tables
}


def domain_for(table_name):
    """Return the domain label for a table (case-insensitive); OTHER_DOMAIN if unmapped."""
    return _TABLE_TO_DOMAIN.get(str(table_name).upper(), OTHER_DOMAIN)
