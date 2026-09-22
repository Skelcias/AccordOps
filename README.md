# Contrat de projet — AccordOps

AccordOps est une application qui vérifie si des notes de frais respectent les règles définies par une entreprise.

La première version doit :

lire une liste de dépenses ;
lire une liste de règles ;
associer chaque dépense à la règle correspondante ;
déterminer si elle est conforme ;
expliquer pourquoi une dépense est refusée ou signalée.

Les premières versions fonctionnent uniquement avec des données fictives et du code déterministe, sans IA.

L’IA sera ajoutée plus tard pour comprendre automatiquement des justificatifs et des règles exprimées en langage naturel.


## Niveau 0 — Vérifier une dépense avec Python

### Objectif

Construire une première version déterministe d'AccordOps capable de :

* lire un fichier `expenses.csv` contenant des dépenses ;
* lire un fichier `policy.csv` contenant les règles de l'entreprise ;
* associer chaque dépense à la règle correspondante ;
* déterminer si la dépense respecte le plafond autorisé ;
* signaler explicitement les données invalides ou les catégories inconnues.

Aucune IA n'est utilisée à ce niveau.

### Stack

* Python
* bibliothèque standard `csv`
* Git
* uv pour l'environnement et les dépendances

### Contraintes

* pas de Pandas ;
* pas de base de données ;
* pas d'API ;
* pas de LLM ;
* données entièrement fictives.

### Critère de validation

À partir des deux CSV, le programme doit produire pour chaque dépense un résultat clair :

```text
Restaurant — 47.80 € — plafond 35.00 € → NON CONFORME
Hotel — 162.00 € — plafond 180.00 € → CONFORME
```

Le programme doit également gérer proprement au minimum :

* une catégorie sans règle correspondante ;
* un montant invalide.

## Niveau 1 — Persistance PostgreSQL

### Objectif

Remplacer les fichiers CSV par une base PostgreSQL persistante contenant les dépenses et les politiques de remboursement.

### Stack

- PostgreSQL
- SQL
- psycopg
- Docker
- Python
- pytest

### Fonctionnalités réalisées

- création du schéma SQL ;
- persistance des données avec un volume Docker ;
- connexion Python à PostgreSQL avec psycopg ;
- opérations CRUD sur les dépenses ;
- transactions et rollback ;
- tests d'intégration avec PostgreSQL ;
- migrations SQL ;
- identifiants générés automatiquement avec `IDENTITY`.

### Critère de validation

Les données doivent rester présentes après redémarrage du conteneur PostgreSQL et les tests d'intégration doivent passer.


---

## Niveau 2 — API HTTP avec FastAPI

### Objectif

Exposer les fonctionnalités d'AccordOps via une API HTTP afin de séparer la logique applicative de l'interface utilisée par le client.

### Stack

- FastAPI
- Uvicorn
- Pydantic
- PostgreSQL
- psycopg
- Python

### Fonctionnalités réalisées

API CRUD sur les dépenses :

- `GET /expenses`
- `GET /expenses/{id}`
- `POST /expenses`
- `PATCH /expenses/{id}`
- `DELETE /expenses/{id}`

API sur les politiques :

- `GET /policies`
- `GET /policies/{id}`
- `POST /policies`
- `PATCH /policies/{id}`

La documentation Swagger générée automatiquement par FastAPI est accessible via :

```text
/docs
```

### Validation des données

Les données reçues par l'API sont décrites avec des modèles Pydantic.

Les montants utilisent désormais `Decimal` plutôt que `float` afin d'éviter les approximations binaires sur les valeurs monétaires.

Exemple de validation :

```python
amount: Decimal = Field(ge=0)
```

Les montants négatifs sont donc rejetés avant même d'atteindre la base de données.

### Refactor v1

Le projet commence à séparer les responsabilités :

```text
api.py
    ↓
services.py
    ↓
db.py
    ↓
PostgreSQL
```

- `api.py` : gestion HTTP, routes et codes d'erreur ;
- `schemas.py` : modèles Pydantic des données entrantes ;
- `services.py` : orchestration et logique métier ;
- `db.py` : accès SQL à PostgreSQL.

Les erreurs métier, par exemple `ExpenseNotFoundError`, sont levées dans la couche service puis traduites en erreurs HTTP par l'API.

Une opération métier utilisant plusieurs requêtes SQL partage une seule connexion afin de pouvoir rester dans la même transaction.

### Critère de validation

L'API doit permettre de créer, consulter, modifier et supprimer une dépense, avec :

- validation des entrées ;
- génération automatique des identifiants ;
- persistance PostgreSQL ;
- réponses HTTP cohérentes ;
- erreurs `404` pour les ressources inexistantes.

---

## Niveau 3 — Traitement de justificatifs

### Objectif

Permettre à AccordOps de recevoir des justificatifs réels plutôt que des données déjà structurées manuellement.

Le flux cible devient progressivement :

```text
justificatif
    ↓
extraction du contenu
    ↓
texte brut
    ↓
LLM
    ↓
données structurées
    ↓
moteur de conformité AccordOps
```

### L3.0 — Upload de justificatifs

Une route :

```text
POST /receipts
```

permet de recevoir un fichier via FastAPI avec `UploadFile`.

Types actuellement autorisés :

- `application/pdf`
- `image/png`
- `image/jpeg`

Les fichiers non supportés produisent une erreur HTTP `400`.

Le fichier est actuellement traité directement en mémoire et n'est pas sauvegardé sur disque.

### L3.1 — Extraction de texte PDF

Les PDF contenant déjà du texte sont traités avec `PyPDF`.

Flux :

```text
UploadFile
    ↓
await file.read()
    ↓
bytes
    ↓
BytesIO
    ↓
PdfReader
    ↓
extract_text()
    ↓
texte brut
```

`BytesIO` transforme les bytes présents en mémoire en un objet se comportant comme un fichier, ce qui permet à `PdfReader` de le lire sans créer de fichier temporaire sur disque.

Le texte est extrait page par page puis concaténé.

### Étape suivante

L3.2 ajoutera l'extraction de texte depuis les images et les PDF scannés grâce à un OCR.

Cette étape préparera ensuite l'utilisation d'un LLM pour transformer le texte brut en données structurées telles que :

```text
merchant
date
amount
category
```