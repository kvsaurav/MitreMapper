#July_5th_2025 
import json
import os
import requests


print(" Welcome to MITREMapper by Saurabh")
print()


# Ensure MITRE STIX File Exists 
def ensure_stix_file(stix_path):
    if not os.path.exists(stix_path):
        print("📥 STIX file not found. Downloading...")
        url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
        response = requests.get(url)
        response.raise_for_status()
        with open(stix_path, "w") as f:
            f.write(response.text)
        print("✅ Downloaded:", stix_path)
    else:
        print("✅ STIX file found:", stix_path)

#Load STIX JSON to local if nOt found
def load_stix_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def build_ttp_tactic_mapping(stix_data):
    tactic_lookup = {}
    for obj in stix_data["objects"]:
        if obj.get("type") == "attack-pattern":
            for ref in obj.get("external_references", []):
                if ref.get("source_name") == "mitre-attack" and ref.get("external_id", "").startswith("T"):
                    ttp_id = ref["external_id"]
                    tactics = [p["phase_name"] for p in obj.get("kill_chain_phases", []) if p["kill_chain_name"] == "mitre-attack"]
                    if ttp_id in tactic_lookup:
                        tactic_lookup[ttp_id] = list(set(tactic_lookup[ttp_id] + tactics))
                    else:
                        tactic_lookup[ttp_id] = tactics
    return tactic_lookup


def load_ttps_from_txt(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def generate_navigator_json(input_txt, output_json, mapping, user_score):
    raw_ttps = load_ttps_from_txt(input_txt)
    techniques = []

    for ttp in raw_ttps:
        if ttp in mapping:
            for tactic in mapping[ttp]:
                if '.' in ttp:
                    tech_id, sub_id = ttp.split('.')
                    techniques.append({
                        "techniqueID": tech_id,
                        "subtechniqueID": sub_id,
                        "tactic": tactic,
                        "score": user_score,
                        "comment": "",
                        "enabled": True,
                        "metadata": [],
                        "showSubtechniques": True
                    })
                else:
                    techniques.append({
                        "techniqueID": ttp,
                        "tactic": tactic,
                        "score": user_score,
                        "comment": "",
                        "enabled": True,
                        "metadata": [],
                        "showSubtechniques": True
                    })

    navigator_layer = {
        "version": "4.5",
        "name": "TTP Heatmap from TXT",
        "domain": "enterprise-attack",
        "description": f"Generated from TTP list with score={user_score}",
        "techniques": techniques,
        "gradient": {
            "colors": ["#ffffff", "#ff6666"],
            "minValue": 0,
            "maxValue": user_score
        },
        "legendItems": [
            {"label": f"Score: {user_score}", "color": "#ff6666"}
        ],
        "metadata": [],
        "filters": {
            "platforms": [
                "Windows", "macOS", "Linux", "Cloud", "Office 365", "Azure AD",
                "Google Workspace", "SaaS", "Network", "IaaS", "Containers"
            ]
        },
        "layout": {
            "layout": "side"
        }
    }

    with open(output_json, 'w') as f:
        json.dump(navigator_layer, f, indent=4)

# Main Script - Don't even touch it for god's sake 
if __name__ == "__main__":
    stix_path = "enterprise-attack.json"
    input_txt_path = "ttps.txt"
    output_json_path = "navigator_layer_v4.5.json"

    try:
        ensure_stix_file(stix_path)
        stix_data = load_stix_data(stix_path)
        tactic_mapping = build_ttp_tactic_mapping(stix_data)

        user_score = input("Enter a score for all TTPs you wanna assign (e.g - 1, 2.5 etc): ")
        try:
            user_score = float(user_score)
        except ValueError:
            print(" Invalid input. Defaulting to score = 1.0")
            user_score = 1.0

        generate_navigator_json(input_txt_path, output_json_path, tactic_mapping, user_score)
        print(f"\nNavigator JSON saved as: {output_json_path}")

    except Exception as e:
        print(f" Error: {str(e)}")
