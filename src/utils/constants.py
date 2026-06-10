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


# --------------------------------------------------------------------------
# Access gate (deterrent only; shared password, client-side).
# GATE_HASH is the SHA-256 hash of the shared access password. Keep it in sync
# with the data-governance hub (_config.yml gate_hash). Starter password:
# CSUdata2026 -- CHANGE IT (regenerate the hash and replace below).
# --------------------------------------------------------------------------

GATE_HASH = "863008d1bad2456b0b5c8abf04dae82c1e636ba89f5c876fa5daf2daaac91d6a"


def gate_div(title):
    """HTML for the password overlay shown until the correct password is entered."""
    return (
        "<div id='gate' class='gate' style='display:none'>"
        "<form id='gateForm' class='gate-box'>"
        f"<h1>{title}</h1>"
        "<p class='muted'>This site is restricted. Enter the access password to continue.</p>"
        "<input type='password' id='gatePwd' placeholder='Password' "
        "autocomplete='current-password' autofocus>"
        "<button type='submit'>Enter</button>"
        "<p id='gateErr' class='gate-err' style='display:none'>Incorrect password. Try again.</p>"
        "</form></div>"
    )


def gate_script():
    """Inline JS that compares a SHA-256 of the entry against GATE_HASH and reveals the site."""
    return (
        "<script>\n"
        "(function(){\n"
        "  var H='" + GATE_HASH + "';\n"
        "  var gate=document.getElementById('gate'),site=document.getElementById('site'),"
        "form=document.getElementById('gateForm'),pwd=document.getElementById('gatePwd'),"
        "err=document.getElementById('gateErr');\n"
        "  function reveal(){gate.style.display='none';site.style.display='';}\n"
        "  async function sha(t){var b=await crypto.subtle.digest('SHA-256',"
        "new TextEncoder().encode(t));return Array.from(new Uint8Array(b)).map("
        "function(x){return x.toString(16).padStart(2,'0');}).join('');}\n"
        "  if(sessionStorage.getItem('csu_gate_ok')==='1'){reveal();}"
        "else{gate.style.display='';if(pwd)pwd.focus();}\n"
        "  form.addEventListener('submit',async function(e){e.preventDefault();"
        "var h=await sha(pwd.value);if(h===H){sessionStorage.setItem('csu_gate_ok','1');reveal();}"
        "else{err.style.display='block';pwd.value='';pwd.focus();}});\n"
        "})();\n"
        "</script>"
    )
