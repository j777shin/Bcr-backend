"""
Generates `data/01_countries_update.csv` from primary sources.

Country universe: 127 Parties with DNA appointed for Article 6.4
(UNFCCC, 9 Apr 2026: https://unfccc.int/node/627860).

Per country we score five **binary indicators** from primary sources
(no synthesised composite scoring at the global level):

  1. flag_dna_appointed       — UNFCCC (true for all 127 here)
  2. flag_pr_submitted        — UNFCCC Art.6.4 Supervisory Body (~47, heuristic)
  3. flag_ndc_blue_carbon     — supplementary research note (curated subset)
  4. flag_bilateral_a6_2      — public bilateral cooperative-approach roster
  5. flag_market_operational  — supplementary research note + ICAP/World Bank

`components_count` = sum of the five flags (0–5).
`readiness_tier` is derived from the count: 5 → Advanced ·
3–4 → Developing · ≤2 → Early stage. `readiness_score = components_count * 20`.

UNFCCC dimension scores are written **only for Indonesia** (curated).

CAAS dimension scores are written for **Indonesia (curated)** plus
the 38 peer countries in the NDC tracker (synthesised — see
`CAAS_SYNTH` table below). All other countries leave the dim
columns blank.

Re-run: python scripts/generate_127_countries.py
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, '..', 'data'))

# ── DNA-appointed parties (UNFCCC, 9 Apr 2026; 127 entries) ──────────────────
DNA_COUNTRIES = [
    'Albania', 'Argentina', 'Armenia', 'Austria', 'Azerbaijan',
    'Bahamas (The)', 'Bangladesh', 'Belize', 'Benin', 'Bhutan',
    'Bolivia', 'Botswana', 'Brazil', 'Burkina Faso', 'Burundi',
    'Cabo Verde', 'Cambodia', 'Cameroon', 'Central African Republic',
    'Chad', 'Chile', 'China (People\'s Republic)', 'Colombia', 'Congo',
    'Cook Islands', 'Costa Rica', 'Côte d\'Ivoire', 'Cuba', 'Czechia',
    'Democratic Republic of the Congo', 'Djibouti', 'Dominican Republic',
    'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Eritrea', 'Eswatini',
    'Ethiopia', 'European Union', 'Fiji', 'Finland', 'France',
    'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece',
    'Guatemala', 'Guinea', 'Guyana', 'Haiti', 'Honduras', 'India',
    'Indonesia', 'Iraq', 'Israel', 'Jamaica', 'Jordan', 'Kazakhstan',
    'Kenya', 'Kyrgyzstan', 'Lao People\'s Democratic Republic',
    'Lebanon', 'Lesotho', 'Liberia', 'Liechtenstein', 'Madagascar',
    'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Mauritania', 'Mauritius',
    'Mexico', 'Monaco', 'Mongolia', 'Morocco', 'Mozambique', 'Myanmar',
    'Namibia', 'Nepal', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria',
    'Oman', 'Pakistan (Islamic Republic of)', 'Palau', 'Panama',
    'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines',
    'Republic of Korea', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia',
    'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Seychelles',
    'Sierra Leone', 'Solomon Islands', 'Somalia', 'South Africa',
    'Sri Lanka', 'State of Palestine', 'Sweden', 'Switzerland',
    'Thailand', 'Timor-Leste', 'Togo', 'Tunisia', 'Türkiye',
    'Uganda', 'Ukraine', 'United Arab Emirates',
    'United Kingdom of Great Britain and Northern Ireland',
    'United Republic of Tanzania', 'Uruguay', 'Uzbekistan',
    'Vanuatu', 'Viet Nam', 'Zambia', 'Zimbabwe',
]
assert len(DNA_COUNTRIES) == 127, f'Expected 127, got {len(DNA_COUNTRIES)}'

NAME_TO_ISO3_OVERRIDES = {
    'Bahamas (The)': 'BHS', 'Bolivia': 'BOL',
    'China (People\'s Republic)': 'CHN', 'Côte d\'Ivoire': 'CIV',
    'Democratic Republic of the Congo': 'COD', 'European Union': 'EUU',
    'Lao People\'s Democratic Republic': 'LAO',
    'Pakistan (Islamic Republic of)': 'PAK',
    'Republic of Korea': 'KOR', 'State of Palestine': 'PSE',
    'Türkiye': 'TUR',
    'United Kingdom of Great Britain and Northern Ireland': 'GBR',
    'United Republic of Tanzania': 'TZA', 'Viet Nam': 'VNM',
    'Czechia': 'CZE', 'Eswatini': 'SWZ', 'Cabo Verde': 'CPV',
    'Timor-Leste': 'TLS',
}

# ── Indicator data — primary or heuristic with explicit provenance ──────────

# (2) Participation Requirements submitted to UNFCCC Art.6.4 SB.
# UNFCCC's May 2026 update reports "44 Parties, mostly in Africa" + 5 named
# (Gambia, Guinea, Indonesia, Mauritius, Tanzania). The full ~47-party list
# lives only in the interactive IETA tracker. As a heuristic that matches
# UNFCCC's qualitative description, we flag every African DNA-appointed
# party (46) + Indonesia (1) = 47 parties. Note in DATA.md flags this as
# "heuristic pending IETA verification".
AFRICAN_DNA_ISO3 = {
    'BEN', 'BWA', 'BFA', 'BDI', 'CPV', 'CMR', 'CAF', 'TCD', 'COG', 'CIV',
    'COD', 'DJI', 'EGY', 'ERI', 'SWZ', 'ETH', 'GAB', 'GMB', 'GHA', 'GIN',
    'KEN', 'LSO', 'LBR', 'MDG', 'MWI', 'MLI', 'MRT', 'MUS', 'MAR', 'MOZ',
    'NAM', 'NER', 'NGA', 'RWA', 'STP', 'SEN', 'SYC', 'SLE', 'SOM', 'ZAF',
    'TZA', 'TGO', 'TUN', 'UGA', 'ZMB', 'ZWE',
}
PR_SUBMITTED_ISO3 = AFRICAN_DNA_ISO3 | {'IDN'}  # 47 total

# (3) NDC explicitly includes blue carbon ecosystems
# Source: Blue Carbon Dashboard Supplementary Information.docx (curated)
NDC_BLUE_CARBON_ISO3 = {
    'IDN', 'BRA', 'KEN', 'VNM', 'AUS', 'USA', 'CHN', 'SYC', 'GBR',
    'CRI', 'KOR', 'FJI', 'BHS', 'MEX', 'COL', 'PAN', 'PHL', 'CHL',
    'BGD', 'VUT', 'BLZ', 'ZAF', 'THA', 'CPV', 'DOM', 'GAB', 'NAM',
    'JOR', 'MHL', 'PLW', 'SGP', 'JPN', 'EUU', 'FRA', 'ISL', 'NOR',
    'CAN', 'TON', 'MDV',
}

# (4) Article 6.2 cooperative approach signed (host or buyer side)
# Public roster from UNFCCC Art.6.2 reporting + bilateral MoU announcements.
BILATERAL_A6_2_ISO3 = {
    'IDN', 'VNM', 'KHM', 'THA', 'PHL', 'BGD', 'LAO', 'MNG', 'MEX',
    'CRI', 'CHL', 'PER', 'URY', 'PRY', 'GHA', 'SEN', 'KEN', 'RWA',
    'MWI', 'TUN', 'MAR', 'GEO', 'VUT', 'BTN', 'PNG', 'PLW', 'NPL',
    'MDG', 'FJI', 'LKA', 'JPN', 'KOR', 'CHE', 'SWE', 'NOR',
}

# (5) Domestic carbon market operational (ETS, carbon tax, or active
# offset programme). Source: supplementary doc Market Status column +
# ICAP ETS Map + World Bank Carbon Pricing Dashboard.
MARKET_OPERATIONAL_ISO3 = {
    'IDN', 'KEN', 'AUS', 'USA', 'CHN', 'GBR', 'CRI', 'KOR', 'BHS',
    'COL', 'MEX', 'ISL', 'FRA', 'EUU', 'NOR', 'CAN', 'SGP', 'JPN',
    'BLZ', 'ZAF', 'CHL', 'ARG', 'CHE', 'SWE', 'FIN', 'DEU', 'GRC',
    'PRT', 'AUT', 'EST', 'CZE',
}


def lookup_iso(name: str, name_to_iso: dict) -> str:
    if name in NAME_TO_ISO3_OVERRIDES:
        return NAME_TO_ISO3_OVERRIDES[name]
    key = name.strip().lower()
    if key in name_to_iso:
        return name_to_iso[key]
    bare = key.split('(')[0].strip()
    if bare in name_to_iso:
        return name_to_iso[bare]
    for k, v in name_to_iso.items():
        if bare and (k.startswith(bare) or bare in k):
            return v
    raise KeyError(f'No ISO-3 for: {name}')


# ── ISO-3 → ISO-2 for emoji flag computation ────────────────────────────────
ISO3_TO_ISO2 = {
    'ALB':'AL','ARG':'AR','ARM':'AM','AUT':'AT','AZE':'AZ','BHS':'BS','BGD':'BD',
    'BLZ':'BZ','BEN':'BJ','BTN':'BT','BOL':'BO','BWA':'BW','BRA':'BR','BFA':'BF',
    'BDI':'BI','CPV':'CV','KHM':'KH','CMR':'CM','CAF':'CF','TCD':'TD','CHL':'CL',
    'CHN':'CN','COL':'CO','COG':'CG','COK':'CK','CRI':'CR','CIV':'CI','CUB':'CU',
    'CZE':'CZ','COD':'CD','DJI':'DJ','DOM':'DO','ECU':'EC','EGY':'EG','SLV':'SV',
    'EST':'EE','ERI':'ER','SWZ':'SZ','ETH':'ET','EUU':'EU','FJI':'FJ','FIN':'FI',
    'FRA':'FR','GAB':'GA','GMB':'GM','GEO':'GE','DEU':'DE','GHA':'GH','GRC':'GR',
    'GTM':'GT','GIN':'GN','GUY':'GY','HTI':'HT','HND':'HN','IND':'IN','IDN':'ID',
    'IRQ':'IQ','ISR':'IL','JAM':'JM','JOR':'JO','KAZ':'KZ','KEN':'KE','KGZ':'KG',
    'LAO':'LA','LBN':'LB','LSO':'LS','LBR':'LR','LIE':'LI','MDG':'MG','MWI':'MW',
    'MYS':'MY','MDV':'MV','MLI':'ML','MRT':'MR','MUS':'MU','MEX':'MX','MCO':'MC',
    'MNG':'MN','MAR':'MA','MOZ':'MZ','MMR':'MM','NAM':'NA','NPL':'NP','NZL':'NZ',
    'NIC':'NI','NER':'NE','NGA':'NG','OMN':'OM','PAK':'PK','PLW':'PW','PAN':'PA',
    'PNG':'PG','PRY':'PY','PER':'PE','PHL':'PH','KOR':'KR','RWA':'RW','KNA':'KN',
    'LCA':'LC','STP':'ST','SAU':'SA','SEN':'SN','SYC':'SC','SLE':'SL','SLB':'SB',
    'SOM':'SO','ZAF':'ZA','LKA':'LK','PSE':'PS','SWE':'SE','CHE':'CH','THA':'TH',
    'TLS':'TL','TGO':'TG','TUN':'TN','TUR':'TR','UGA':'UG','UKR':'UA','ARE':'AE',
    'GBR':'GB','TZA':'TZ','URY':'UY','UZB':'UZ','VUT':'VU','VNM':'VN','ZMB':'ZM',
    'ZWE':'ZW','JPN':'JP','CAN':'CA','AUS':'AU','SGP':'SG','NOR':'NO','USA':'US',
    'PRT':'PT','MHL':'MH','TON':'TO','ISL':'IS',
}


def emoji_flag(iso3: str) -> str:
    iso2 = ISO3_TO_ISO2.get(iso3)
    if not iso2 or len(iso2) != 2:
        return ''
    return ''.join(chr(ord(c) - ord('A') + 0x1F1E6) for c in iso2.upper())


def tier_from_count(n: int) -> str:
    if n >= 5:
        return 'Advanced'
    if n >= 3:
        return 'Developing'
    return 'Early stage'


def context_note(iso3: str, count: int, flags: dict) -> str:
    if iso3 == 'IDN':
        return 'Art.6.2 · Art.6.4 · 2nd NDC submitted Oct 2025 · 5/5 indicators met'
    bits = [f'{count}/5 indicators met']
    if flags['flag_pr_submitted']:
        bits.append('PR submitted')
    if flags['flag_bilateral_a6_2']:
        bits.append('Art.6.2 bilateral')
    if flags['flag_market_operational']:
        bits.append('domestic market operational')
    return ' · '.join(bits)


# ── Dimension scoring (curated for Indonesia; synthesised for peers) ────────

# Indonesia — curated, primary
IDN_UNFCCC = dict(dim_1_strategic=88, dim_2_legal=92, dim_3_institutional=82,
                  dim_4_operational=72, dim_5_infrastructure=78)
IDN_CAAS = dict(caas_a_legal=90, caas_b_mrv=75, caas_c_finance=80,
                caas_d_social=65, caas_e_registry=70)

# CAAS synth for the 38 NDC-tracker peer countries. Tuned to each country's
# known Art.6 + carbon market context as of 2025–early-2026; intended as
# illustrative dashboard data, not authoritative CAAS scoring.
CAAS_SYNTH = {
    'BRA': (80, 75, 60, 60, 65),
    'KEN': (78, 65, 78, 70, 65),
    'CRI': (88, 78, 75, 78, 70),
    'MEX': (70, 70, 65, 60, 65),
    'KOR': (92, 88, 90, 70, 85),
    'CHL': (78, 70, 70, 68, 65),
    'BGD': (60, 50, 45, 55, 50),
    'VNM': (72, 65, 60, 60, 58),
    'PHL': (65, 58, 50, 60, 55),
    'THA': (70, 65, 60, 60, 60),
    'ZAF': (75, 68, 65, 60, 65),
    'CHN': (82, 75, 80, 50, 78),
    'GBR': (90, 85, 88, 75, 88),
    'USA': (78, 75, 70, 65, 78),
    'AUS': (80, 78, 72, 65, 75),
    'JPN': (88, 82, 78, 70, 82),
    'CAN': (88, 82, 80, 70, 80),
    'EUU': (92, 88, 92, 80, 90),
    'FRA': (90, 85, 88, 78, 88),
    'NOR': (90, 85, 85, 75, 85),
    'ISL': (85, 75, 75, 75, 75),
    'SGP': (88, 75, 80, 65, 78),
    'COL': (75, 65, 65, 60, 62),
    'BLZ': (65, 55, 60, 65, 58),
    'BHS': (70, 60, 65, 55, 60),
    'FJI': (60, 50, 50, 65, 50),
    'VUT': (55, 50, 50, 65, 50),
    'DOM': (50, 45, 45, 50, 45),
    'GAB': (55, 50, 45, 55, 45),
    'NAM': (50, 45, 40, 50, 45),
    'JOR': (55, 50, 45, 50, 50),
    'MHL': (50, 45, 40, 55, 45),
    'PLW': (55, 45, 45, 65, 45),
    'TON': (50, 45, 40, 55, 45),
    'MDV': (55, 50, 50, 65, 50),
    'SYC': (65, 60, 55, 70, 60),
    'PAN': (60, 55, 55, 60, 55),
    'CPV': (55, 50, 50, 60, 50),
}


def main():
    ref_path = os.path.join(DATA, '14_countries_ref.csv')
    name_to_iso = {}
    with open(ref_path) as f:
        for row in csv.DictReader(f):
            name_to_iso[row['country_name'].strip().lower()] = row['country_code']

    rows = []
    distribution = {}
    for name in DNA_COUNTRIES:
        iso3 = lookup_iso(name, name_to_iso)
        flags = {
            'flag_dna_appointed':      True,
            'flag_pr_submitted':       iso3 in PR_SUBMITTED_ISO3,
            'flag_ndc_blue_carbon':    iso3 in NDC_BLUE_CARBON_ISO3,
            'flag_bilateral_a6_2':     iso3 in BILATERAL_A6_2_ISO3,
            'flag_market_operational': iso3 in MARKET_OPERATIONAL_ISO3,
        }
        count = sum(flags.values())
        tier = tier_from_count(count)
        distribution[count] = distribution.get(count, 0) + 1

        # Dimensions
        unfccc = IDN_UNFCCC if iso3 == 'IDN' else {}
        if iso3 == 'IDN':
            caas = IDN_CAAS
        elif iso3 in CAAS_SYNTH:
            a, b, c, d, e = CAAS_SYNTH[iso3]
            caas = dict(caas_a_legal=a, caas_b_mrv=b, caas_c_finance=c,
                        caas_d_social=d, caas_e_registry=e)
        else:
            caas = {}

        rows.append({
            'country_code':      iso3,
            'country_name':      name,
            'flag_emoji':        emoji_flag(iso3),
            'readiness_score':   count * 20,
            'readiness_tier':    tier,
            'context_note':      context_note(iso3, count, flags),
            'dim_1_strategic':       unfccc.get('dim_1_strategic', ''),
            'dim_2_legal':           unfccc.get('dim_2_legal', ''),
            'dim_3_institutional':   unfccc.get('dim_3_institutional', ''),
            'dim_4_operational':     unfccc.get('dim_4_operational', ''),
            'dim_5_infrastructure':  unfccc.get('dim_5_infrastructure', ''),
            'caas_a_legal':    caas.get('caas_a_legal', ''),
            'caas_b_mrv':      caas.get('caas_b_mrv', ''),
            'caas_c_finance':  caas.get('caas_c_finance', ''),
            'caas_d_social':   caas.get('caas_d_social', ''),
            'caas_e_registry': caas.get('caas_e_registry', ''),
            'flag_dna_appointed':       'true' if flags['flag_dna_appointed']       else 'false',
            'flag_pr_submitted':        'true' if flags['flag_pr_submitted']        else 'false',
            'flag_ndc_blue_carbon':     'true' if flags['flag_ndc_blue_carbon']     else 'false',
            'flag_bilateral_a6_2':      'true' if flags['flag_bilateral_a6_2']      else 'false',
            'flag_market_operational':  'true' if flags['flag_market_operational']  else 'false',
            'components_count': count,
        })

    fieldnames = list(rows[0].keys())
    out_path = os.path.join(DATA, '01_countries_update.csv')
    with open(out_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print(f'✓ Wrote {len(rows)} countries to {out_path}')
    print(f'  Distribution by components_count: {sorted(distribution.items())}')
    print(f'  PR-submitted: {sum(1 for r in rows if r["flag_pr_submitted"] == "true")}')
    print(f'  CAAS-scored:  {sum(1 for r in rows if r["caas_a_legal"] != "")}')


if __name__ == '__main__':
    main()
