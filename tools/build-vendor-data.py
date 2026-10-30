#!/usr/bin/env python3
"""Regenerate scripts/licensed-vendors-data.js from the Licensed Vendor sheet.

    python3 tools/build-vendor-data.py            # fetch the live sheet
    python3 tools/build-vendor-data.py tab1.csv fundraiser.csv   # or local CSVs

Tab 1 (gid 628597651) is the vendor directory. Internal Fundraiser status is
not in tab 1 yet, so it is read from the "Internal Fundraiser List" tab
(gid 1205685996) by vendor name. When that column lands in tab 1, read it from
there and drop the second fetch.

The sheet's Product Categories cell is hand-typed and occasionally loses a
separator ("Youth Appare lMen's/Unisex …", "Youth Apparel Automobile
Products"), so categories are recovered by matching the known names below
rather than by splitting on "|" alone. Anything left unmatched is reported.
"""
import csv
import io
import json
import re
import sys
import urllib.request
from pathlib import Path

SHEET = 'https://docs.google.com/spreadsheets/d/1VKnJmfSxk5DOfvy97eczktvwPwL-Eo6KhKh0P8YB7MY/export?format=csv&gid='
TAB_VENDORS = '628597651'
TAB_FUNDRAISER = '1205685996'
OUT = Path(__file__).resolve().parent.parent / 'scripts' / 'licensed-vendors-data.js'

# Parent buckets for the Product Categories filter, in display order.
BUCKETS = [
    ('Apparel', ["Infant/Toddler Apparel", "Youth Apparel", "Women's Apparel",
                 "Men's Fashion Apparel", "Men's/Unisex Fleece",
                 "Men's/Unisex Loungewear & Sleepwear", "Men's/Unisex Outerwear",
                 "Men's/Unisex Performance Apparel", "Men's/Unisex T-shirts",
                 "Men's/Unisex Headwear", "Footwear"]),
    ('Team & Athletic', ["Balls", "Sports Equipment", "Jerseys/Uniforms",
                         "Authentic Hockey Jerseys"]),
    ('Jewelry & Accessories', ["Clothing Accessories", "Personal Accessories",
                               "Jewelry", "Class Rings"]),
    ('Home & Housewares', ["Domestics", "Furniture/Furnishings", "Housewares",
                           "Drinkware", "Holiday Accessories"]),
    ('Toys, Games & Kids', ["Toys", "Games", "Infant Products"]),
    ('Gifts & Collectibles', ["Gifts & Novelties", "Collectibles"]),
    ('Office, School & Print', ["Office Products", "Paper Products", "Stationery",
                                "School Supplies", "Publishing", "Signage Products",
                                "Checks"]),
    ('Health & Consumables', ["Health/Beauty", "Consumables",
                              "Personal Protection Equipment"]),
    ('Electronics & Auto', ["Electronics & Content", "Automobile Products"]),
    ('Licensing', ["Premium Royalties"]),
]
KNOWN = [c for _, cats in BUCKETS for c in cats]

# Typos in the sheet that break name matching.
REPAIRS = [('Youth Appare l', 'Youth Apparel | ')]


def rows(source):
    if Path(source).exists():
        text = Path(source).read_text(encoding='utf-8')
    else:
        with urllib.request.urlopen(SHEET + source) as r:
            text = r.read().decode('utf-8')
    # Row 1 is a title, row 2 the header.
    return [r for r in list(csv.reader(io.StringIO(text)))[2:] if r and r[0].strip()]


def categories(cell, vendor):
    for bad, good in REPAIRS:
        cell = cell.replace(bad, good)
    found, rest = [], cell
    for name in sorted(KNOWN, key=len, reverse=True):   # longest first: "Youth Apparel" before "Apparel"
        if name in rest:
            found.append(name)
            rest = rest.replace(name, '|')
    leftover = re.sub(r'[|\s]+', ' ', rest).strip()
    if leftover:
        print(f'  unmatched category text for {vendor}: {leftover!r}', file=sys.stderr)
    return [c for c in KNOWN if c in found]


def blank(value):
    value = value.strip()
    return '' if value in ('', '—', '-', 'N/A', 'n/a') else value


def phone(value):
    digits = re.sub(r'\D', '', value)
    if len(digits) == 10:
        return f'{digits[:3]}-{digits[3:6]}-{digits[6:]}', digits
    return value, digits


def website(value):
    value = blank(value)
    if not value:
        return '', ''
    href = value if re.match(r'https?://', value) else 'https://' + value
    label = re.sub(r'^https?://', '', value).rstrip('/')
    return label, href


def main():
    tab1, fund = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else (TAB_VENDORS, TAB_FUNDRAISER)
    fundraisers = {r[0].strip() for r in rows(fund)}
    vendors = []
    for r in rows(tab1):
        name = r[0].strip()
        tel_label, tel = phone(blank(r[2]))
        site_label, site = website(r[4])
        vendors.append({
            'name': name,
            'contact': blank(r[1]),
            'phone': tel_label, 'tel': tel,
            'email': blank(r[3]),
            'website': site_label, 'url': site,
            'address': blank(r[5]),
            'categories': categories(r[6], name),
            'fundraiser': name in fundraisers,
        })
    missing = fundraisers - {v['name'] for v in vendors}
    if missing:
        print(f'  fundraiser vendors not in tab 1: {sorted(missing)}', file=sys.stderr)
    vendors.sort(key=lambda v: v['name'].lower())

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(
        '// GENERATED by tools/build-vendor-data.py from the Licensed Vendor sheet — do not edit by hand.\n'
        'window.UMD_BRAND_SITE_VENDOR_BUCKETS = '
        + json.dumps([{'title': t, 'categories': c} for t, c in BUCKETS], ensure_ascii=False) + ';\n'
        'window.UMD_BRAND_SITE_VENDORS = '
        + json.dumps(vendors, ensure_ascii=False, indent=1) + ';\n', encoding='utf-8')
    print(f'{len(vendors)} vendors ({sum(v["fundraiser"] for v in vendors)} internal fundraiser) → {OUT}')


if __name__ == '__main__':
    main()
