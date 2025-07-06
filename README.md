# 🧠 MITREmapper

Generate MITRE ATT&CK Navigator heatmaps directly from a `.txt` file of TTPs (e.g., `T1059`, `T1566.001`).  
This tool supports **ATT&CK Enterprise v17**, automatically maps tactics from the official STIX dataset, and produces fully compatible **Navigator layer v4.5** JSON files.

> 🎯 A weekend project built to streamline cyber threat visualization on MITRE Heatmap for CTI, red team, and DFIR use cases and completely knock ouyt the manual mapping which takes forever of your precious time. LoL 😜

---

## 🚀 Features

- ✅ Compatible with **MITRE ATT&CK Enterprise v17**
- ✅ Generates **Navigator layer v4.5** JSON
- ✅ Supports techniques + sub-techniques
- ✅ Auto-downloads the official MITRE STIX dataset if missing
- ✅ Prompts for **custom score** per TTP (e.g., 1, 5)
- ✅ Highlights techniques correctly in Navigator
- ✅ CLI-ready and easy to extend

---

## 📂 Input Example (`ttps.txt`)

```
T1059
T1059.001
T1566.001
T1082
T1110
```

---

## 📦 Output

Generates a file called `navigator_layer_v4.5.json` that you can upload directly into:

📍 [MITRE ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/)

---

## 💻 How to Run

```bash
python mitre_layer_generator.py
```

You'll be prompted to enter a custom score for the heatmap (e.g., `2`, `3.5`), which determines the heatmap intensity in Navigator.

---

## 📁 Files Explained

| File                     | Purpose                                 |
|--------------------------|-----------------------------------------|
| `mitre_layer_generator.py` | Main script to generate the layer      |
| `enterprise-attack.json` | Auto-downloaded STIX dataset (v17)     |
| `ttps.txt`               | Your input list of MITRE TTPs          |
| `navigator_layer_v4.5.json` | Final output to import into Navigator |

---

## 🔧 Requirements

- Python 3.7+
- Internet connection (only if STIX file is missing)
- No external libraries required (uses `requests`, `json`, etc.)

---

## ⛯ Use Cases

- Visualize TTP coverage during red team engagements
- Map threat actor techniques from intel reports
- Build CTI heatmaps for board-level or SOC reporting
- Quickly generate layer JSONs for tabletop exercises

---


## 🛡️ License

MIT License — feel free to fork, modify, and enhance.  
Attribution appreciated if reused publicly 🙏

---

### ✨ Made with automation mindset, caffeine and curiosity by Saurabh, feel free to tag me if you are sharing this on social media.  
