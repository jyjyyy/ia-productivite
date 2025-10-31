import csv
import os
from datetime import datetime

# Dossiers utilisés
DATA_FILE = "data/outils.csv"
OUTPUT_DIR = "articles"
STATE_FILE = "data/state.txt"

# Vérifie que le dossier existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Charge l'état (pour savoir quels outils ont déjà été publiés)
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        published = set(line.strip() for line in f.readlines())
else:
    published = set()

# Ouvre la base CSV des outils
with open(DATA_FILE, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        titre = row["titre"]
        if titre in published:
            continue  # déjà publié

        categorie = row["categorie"]
        lien = row["lien"]
        description = row["description"]

        # Crée le contenu markdown
        slug = titre.lower().replace(" ", "-").replace("’", "").replace("'", "")
        filename = f"{OUTPUT_DIR}/{slug}.md"

        content = f"""---
title: "{titre}"
description: "{description}"
date: {datetime.now().strftime("%Y-%m-%d")}
---

# 🧠 {titre}

**Catégorie :** {categorie}  
**Lien :** [{lien}]({lien})

---

## 🚀 Présentation

{description}

## 💡 Pourquoi l’utiliser ?
- Gratuit et simple à tester
- Idéal pour améliorer ta productivité
- Compatible avec d’autres outils IA

## 🔗 Ressources utiles
- [Aller sur le site officiel]({lien})
- [Découvre d'autres outils IA gratuits](../index.html)
"""

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        # Ajoute le titre à la liste des publiés
        with open(STATE_FILE, "a", encoding="utf-8") as f:
            f.write(titre + "\n")

        print(f"✅ Article créé : {filename}")
        break  # ne crée qu’un seul article à la fois
