import re

test_dict = {
    "base1_WLE_earnings": 1000,
    "base1_toage_earnings": 1000,
    "base2_WLE_earnings": 2000,
    "base2_toage_earnings": 2000,
    "base3_WLE_earnings": "",
    "base3_toage_earnings": "",
    "credit1_WLE_earnings": 100,
    "credit2_WLE_earnings": 200,
    "credit3_WLE_earnings": 300,
    "base1_WLE_pretrial_meals_adj": 10,
    "base1_WLE_pretrial_benefits_adj": 20,
    "base1_WLE_eff_tax_rate": 0.2,
}

projection_type = "WLE"
# Base earnings variable stems and suffixes
if projection_type == "WLE":
    base_earnings_stem = "base1_WLE"
elif projection_type == "toage":
    base_earnings_stem = "base1_toage"
else:
    raise ValueError("Invalid projection type")

base_earnings_suffixes = [
    "_earnings",
    "_eff_tax_rate",
    "_growth_rate",
    "_pretrial_loss_notax",
    "_pretrial_loss_taxed",
    "_posttrial_loss_notax",
    "_posttrial_loss_taxed",
    "_total_loss_notax",
    "_total_loss_taxed",
]

# Regex to identify unique base instances
pattern = r"base(\d+)"
bases = set()
for key in test_dict.keys():
    bases.update(re.findall(pattern, key))

confirmed_bases = set()
for base in bases:
    for suffix in base_earnings_suffixes:
        variable = f"{base_earnings_stem}{suffix}"
        if test_dict.get(variable, None):
            confirmed_bases.add(base)
        else:
            continue

print(bases)
