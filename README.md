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


## Niveau 2 — API HTTP avec FastAPI

### Objectif

Exposer les fonctionnalités d'AccordOps via une API HTTP.

### Stack

- FastAPI
- Uvicorn
- Pydantic
- PostgreSQL
- psycopg

### Fonctionnalités actuelles

- démarrage d'une API FastAPI ;
- documentation Swagger automatique avec `/docs` ;
- `GET /expenses` pour récupérer toutes les dépenses ;
- `GET /expenses/{id}` pour récupérer une dépense précise ;
- gestion d'une dépense inexistante avec une erreur HTTP `404`.

### Étapes suivantes

- `POST /expenses` ;
- validation des données avec Pydantic ;
- mise à jour et suppression via l'API ;
- gestion plus propre des erreurs HTTP.