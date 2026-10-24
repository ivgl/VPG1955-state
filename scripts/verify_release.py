#!/usr/bin/env python3
"""Read-only check of the current canonical VPI1955_MAIN start release.
Run from any directory: python3 scripts/verify_release.py
This script never writes official state, Sheets, or player actions.
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
IDS = ("USA","URS","GBR","FRA","FRG","JPN","CHN","EGY","IND","ISR","ITA","YUG")
SPECIAL = ("modules/APPROVED_EXTENSIONS.json","modules/GBR_1955_trade_regimes_approved.json")

def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def close(a, b, atol=0.001):
    return abs(float(a) - float(b)) <= atol

def main():
    errors = []
    try:
        h, m, config = load("HEAD.json"),load("manifest_1955.json"),load("campaign_config.json")
    except Exception as exc:
        print("ERROR: cannot load HEAD, manifest or configuration:", exc)
        return 1
    if h.get("manifest_sha256") != digest(ROOT / "manifest_1955.json"):
        errors.append("HEAD sha256 does not match current manifest")
    for field in ("campaign_id","release_id","year"):
        if h.get(field)!=m.get(field):
            errors.append(f"HEAD/manifest {field} mismatch")
    if h.get("year")!=1955 or h.get("phase")!="PREPARE" or h.get("campaign_id")!="VPI1955_MAIN":
        errors.append("Unexpected year, phase or campaign")
    if config.get("public_launch_ready") is not False:
        errors.append("Public launch flag must remain false until actual start")
    if config.get("turn_duration",{}).get("submission_days")!=3 or config.get("turn_duration",{}).get("judging_days")!=4:
        errors.append("3+4 day schedule not configured")
    files=m.get("files",[])
    names=[f.get("path") for f in files]
    if len(files)!=32 or len(set(names))!=32:
        errors.append("Expected 32 distinct manifest files, including two approved extensions")
    if any(x not in names for x in SPECIAL):
        errors.append("The approved GBR extension/index are missing from the manifest")
    if sum(str(x).startswith("countries/") for x in names)!=12 or sum(x in names for x in (f"modules/{country_id}.json" for country_id in IDS))!=12:
        errors.append("Expected twelve countries and twelve country modules")
    for item in files:
        path=ROOT/item.get("path","")
        if not path.is_file():
            errors.append(f"Missing file: {item.get('path')}")
            continue
        if digest(path)!=item.get("sha256"):
            errors.append(f"SHA mismatch: {item.get('path')}")
        if path.stat().st_size!=item.get("bytes"):
            errors.append(f"Byte size mismatch: {item.get('path')}")
        try:load(item["path"])
        except Exception as exc:errors.append(f"Invalid JSON {item.get('path')}: {exc}")
    for country_id in IDS:
        c=load(f"countries/{country_id}.json")
        module=load(f"modules/{country_id}.json")
        s=c["economy"]["stats"];econ=c["economy"]
        if c.get("id")!=country_id or module.get("country_id")!=country_id:
            errors.append(f"{country_id} ID mismatch")
        if not close(s["fiscal_revenue_total_billion"]-s["fiscal_spending_total_billion"],s["fiscal_budget_balance_billion"]):
            errors.append(f"{country_id} budget identity")
        if not close(s["exports_billion"]-s["imports_billion"],s["net_exports_billion"]):
            errors.append(f"{country_id} trade identity")
        for side in ("export","import"):
            if not close(sum(econ[f"trade_{side}_shares"].values()),100):
                errors.append(f"{country_id} {side} composition !=100%")
        inventory=c["military"].get("equipment_inventory_1955",{})
        if len(inventory)!=15:
            errors.append(f"{country_id} does not contain 15 equipment classes")
        for typ,unit in inventory.items():
            g=unit.get("generations",{})
            total=unit.get("total",0);ready=unit.get("combat_ready",0)
            series=[total,ready,g.get("modern",0),g.get("previous",0),g.get("obsolete",0)]
            if any(not isinstance(v,int) or v<0 for v in series):
                errors.append(f"{country_id}/{typ} invalid count")
            if sum(series[2:])!=total or ready>total:
                errors.append(f"{country_id}/{typ} count identity")
        mm=c["military"]["industrial_military_capacity_1955"]
        if not mm["capacity_not_actual_output"]:
            errors.append(f"{country_id}: production capacity incorrectly interpreted as output")
        if module.get("public_mechanics",{}).get("approval")!="ADMIN_APPROVED":
            errors.append(f"{country_id}: public page not marked approved")
        if module.get("public_mechanics",{}).get("mechanics_count")!=3:
            errors.append(f"{country_id}: expected 3 approved mechanics")
        if not module["public_mechanics"]["public_url"].startswith("https://ivgl.github.io/VPG1955/countries/"):
            errors.append(f"{country_id}: public mechanics URL missing")
    world=load("world_1955.json")
    if world.get("year")!=1955 or len(world.get("players",[]))!=12:
        errors.append("World year or player count incorrect")
    ext=load("modules/APPROVED_EXTENSIONS.json")
    for entry in ext["extensions"]:
        if entry.get("file") not in names or entry.get("status")!="FINAL_APPROVED_FOR_GAMEPLAY":
            errors.append("Supplement index contains missing or unapproved extension")
    gbr=load("modules/GBR_1955_trade_regimes_approved.json")
    b=load("countries/GBR.json")
    for k in ("exports_billion","imports_billion","net_exports_billion","reserves_billion"):
        if not close(gbr["locked_baseline"][k],b["economy"]["stats"][k],1e-6):
            errors.append("GBR trade extension baseline mismatch: "+k)
    for side in ("exports","imports"):
        for sector,weights in gbr["trade_zone_model"]["allocation"][side].items():
            if not close(sum(weights.values()),100):
                errors.append(f"GBR {side}/{sector} zone allocation does not equal 100")
    if errors:
        for error in errors: print("ERROR:",error)
        return 1
    print(f"PASS: HEAD -> SHA256 manifest; {len(files)} files; 12 countries; 12 modules; "
          "180 equipment classes; 12 public mechanics links; GBR approved extension; "
          "financial and trade identities; PREPARE and turn schedule")
    return 0
if __name__=="__main__":
    sys.exit(main())
