# FILMS-ANALYTICS

Analyse de données cinématographique en temps réel avec une API REST. Un projet de **data science + data engineering** combinant exploration API, batching intelligent, caching stratégique et visualisations interactives.

---

## Vue d'ensemble

**FILMS-ANALYTICS** interroge une API REST pour extraire, transformer et visualiser des données sur :
- **9 700+ films** (titres, genres, années)
- **100 000+ notes** (ratings utilisateurs)
- **Tags** appliqués par les utilisateurs aux films

Le projet démontre :
- **ETL robuste** : batching avec throttling pour respecter les limites API
- **Caching intelligent** : parquet + métadonnées JSON pour éviter les requêtes redondantes
- **Analyse exploratoire** : agrégations pandas, statistiques par utilisateur/genre
- **Visualisations interactives** : graphiques Plotly exportés en HTML

---

## Cas d'usage & insights

### 1. Distribution des genres 
Quels genres dominent le catalogue ? Top 10 par fréquence.  
[Voir le graphique](output/genre_counts.html)

### 2. Évolution temporelle
Combien de films par année ? Tendances du catalogue.  
[Voir le graphique](output/movies_by_year.html)

### 3. Top films par engagement
Les 20 films les plus évalués et leurs notes moyennes.  
[Voir le graphique](output/top_movies_by_ratings.html)

### 4. Analyses avancées
Genres favoris des utilisateurs actifs (ratings ≥ 4.0) → tags associés.  
(Détails dans `flm_data_analysis.ipynb`)

---

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| **API Client** | `filmsapisdk` (wrapper custom) |
| **Backend API** | REST sur Render (https://datatech.onrender.com) |
| **Data Processing** | Python 3.12, Pandas, NumPy |
| **Visualization** | Plotly Express |
| **Caching** | Parquet (PyArrow) + JSON |
| **Notebooks** | Jupyter (VS Code) |

---

## Structure du projet

```
FILMS-ANALYTICS/
├── flm_data_analysis.ipynb      # Exploration API, agrégations, business analytics
├── flm_data_viz.ipynb           # Visualisations avec caching
├── output/                       # Données & graphiques générés
│   ├── genre_counts.html         # Bar chart genres
│   ├── genre_counts.parquet      # Cache parquet
│   ├── genre_counts_meta.json    # Metadata (movie_count)
│   ├── movies_by_year.html       # Bar chart timeline
│   ├── movies_by_year.parquet
│   ├── movies_by_year_meta.json
│   ├── top_movies_by_ratings.html  # Bar chart avec couleur (rating moyen)
│   ├── top_movies_by_ratings.parquet
│   └── meta_top_movies.json      # Metadata (movie_count + rating_count)
├── .github/
│   └── copilot-instructions.md  # Conventions & patterns pour AI agents
└── README.md
```

---

## Démarrage rapide

- **Prérequis**
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install pandas plotly matplotlib seaborn pyarrow filmsapisdk kaleido
```

- **Exécution**
1. Ouvrir `flm_data_analysis.ipynb` pour explorer l'API et les données brutes
2. Exécuter `flm_data_viz.ipynb` pour générer caches et visualisations
3. Consulter les graphiques HTML dans `output/`

- **Observations clés**
- **Throttling** : 0.5s entre les requêtes batch (intentionnel, respecte limites API)
- **Caching** : Détecte si données changées via métadonnées (movie_count, rating_count)
- **Formats** : `output_format='dict'` pour itération, `'pandas'` pour DataFrames

---

## Patterns & conventions

### Batching
```python
limit, skip = 200, 0
while True:
    batch = client.list_movies(limit=limit, skip=skip, output_format='dict')
    if not batch:
        break
    # traiter batch
    skip += limit
    time.sleep(0.5)  # Crucial : respect limites API
```

### Caching avec validation
```python
# Lire metadata
if meta_file.exists():
    cached_count = json.load(meta_file)["movie_count"]
else:
    cached_count = 0

# Décision : cache ou refetch
api_count = client.get_analytics().movie_count
if cache_file.exists() and cached_count == api_count:
    df = pd.read_parquet(cache_file)  # Rapide
else:
    df = fetch_from_api()  # Lent
    df.to_parquet(cache_file, index=False)
    json.dump({"movie_count": api_count}, meta_file)
```

### Parsing & transformation
```python
# Années depuis titres : "Forrest Gump (1994)"
year = int(re.search(r"\((\d{4})\)$", title).group(1))

# Genres pipe-delimiters
genres = "Action|Drama|Sci-Fi".split('|')

# Agrégation avec defaultdict
from collections import defaultdict
user_counts = defaultdict(int)
for rating in ratings:
    user_counts[rating["userId"]] += 1
```

---

## Métriques & insights extraits

| Métrique | Valeur | Source |
|----------|--------|--------|
| Films totaux | ~9 742 | API analytics |
| Notes totales | ~100 836 | API analytics |
| Genres distincts | 20+ | Parsing |
| Films avec notes | 4 000+ | Agrégation |
| Utilisateurs actifs | 600+ | Counts by userId |

---

## Points forts du projet

1. **Respect des ressources** : Batching + throttling → pas de rate-limiting
2. **Optimisation** : Cache parquet réutilisable, pas de refetch inutile
3. **Robustesse** : Try/except sur fetches per-item, fallbacks gracieux
4. **Reproductibilité** : Métadonnées sauvegardées, notebooks exécutables
5. **Documentation** : Conventions en `.github/copilot-instructions.md`

---

## Apprentissages & compétences démontrées

- **Data Engineering** : API consumption, ETL pipelines, caching strategies
- **Data Analysis** : Pandas aggregations, time-series extraction, user behavior analysis
- **Data Visualization** : Plotly interactive charts, color scales, layouts
- **Python** : Batch processing, exception handling, functional transformations
- **Best Practices** : Logging, metadata management, rate-limit awareness

---

## Liens utiles

- [Graphiques générés](output/) — Explore les visualisations HTML
- [Notebooks interactifs](.) — `flm_data_analysis.ipynb` et `flm_data_viz.ipynb`
- [Conventions de code](../.github/copilot-instructions.md) — Patterns & standards

---

## Licence & Contexte

Projet de **portfolio / apprentissage** démontrant des compétences en data science et data engineering.  
Données : API REST publique (simulation pédagogique).

---

**Dernière mise à jour** : Janvier 2026
