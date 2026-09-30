# AccordOps — Handover pour reprise avec un futur GPT

## 1. Contexte et objectif d'apprentissage

AccordOps est un projet personnel conçu pour apprendre et démontrer les compétences attendues d'un **AI Engineer / Forward AI Engineer**.

Contrainte importante : le projet est volontairement développé "à l'ancienne", avec l'objectif de **comprendre et écrire le code soi-même**. Le rôle du GPT accompagnateur doit être celui d'un **professeur / reviewer / pair programming léger** :
- expliquer les concepts ;
- proposer les prochaines étapes ;
- corriger les erreurs ;
- donner du code seulement quand c'est pertinent ou quand l'exercice devient du boilerplate répétitif ;
- éviter de produire tout le projet à la place de l'utilisateur ;
- favoriser l'autonomie et la compréhension.

Préférence importante : **à chaque étape, dire explicitement s'il faut faire un commit Git ou non**, et proposer un message de commit en français quand c'est pertinent.

Le projet est un fil conducteur pour revoir puis pratiquer :
- Python ;
- Git ;
- uv ;
- SQL/PostgreSQL ;
- Docker ;
- Psycopg ;
- tests ;
- FastAPI ;
- Pydantic ;
- architecture backend ;
- OCR/document processing ;
- LLM ;
- Structured Outputs ;
- embeddings ;
- pgvector ;
- RAG ;
- puis plus tard HITL, LangGraph, API externes, observabilité, CI/CD, Azure, etc.

---

# 2. Identité fonctionnelle d'AccordOps

AccordOps vérifie si des **notes de frais** respectent les règles d'une entreprise.

Le produit a évolué progressivement :

```text
Justificatif PDF / image
        ↓
Extraction de texte
(PyPDF ou OCR)
        ↓
LLM
(extraction structurée)
        ↓
TicketExpense métier
        ↓
Règles déterministes SQL / Python
        ↓
Conforme / Non conforme / Review
```

Le RAG est ensuite ajouté pour les règles qui ne peuvent pas être représentées par un simple `category + max_amount`.

Principe architectural important :

```text
LLM → extrait / interprète
Python → décide
```

Le LLM ne doit pas être responsable d'une décision déterministe qui peut être codée explicitement.

---

# 3. Repo / stack actuelle

Repo GitHub : `AccordOps`

Stack actuellement utilisée :
- Python 3.13
- uv
- pytest
- PostgreSQL 17
- Docker Compose
- Psycopg 3
- pgvector
- FastAPI
- Uvicorn
- Pydantic
- PyPDF
- Pillow
- pytesseract / Tesseract OCR
- OpenAI API
- OpenAI embeddings
- python-dotenv

Arborescence approximative :

```text
AccordOps/
├── compose.yaml
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
├── helpful_notes.md
├── documents/
│   └── policies/
│       └── expense_policy.md
├── sql/
│   ├── schema.sql
│   └── migrations/
│       ├── 001_auto_ids.sql
│       └── 002_add_vector_store.sql
├── src/
│   └── accordops/
│       ├── api.py
│       ├── db.py
│       ├── schemas.py
│       ├── services.py
│       ├── llm.py
│       ├── embedder.py
│       ├── rag.py
│       ├── main.py
│       └── test_vector.py
└── tests/
    ├── test_main.py
    └── test_db_integration.py
```

---

# 4. Environnement PostgreSQL / Docker

Le PostgreSQL AccordOps tourne dans Docker.

Port :

```text
localhost:5433 → PostgreSQL Docker
```

Le port `5432` est déjà utilisé par un autre PostgreSQL local.

Le service Docker utilise désormais une image compatible pgvector, type :

```yaml
image: pgvector/pgvector:pg17
```

Connexion via :

```bash
docker compose exec postgres psql -U ao_admin -d AO_DB
```

Commandes utiles :

```text
\dt
\d expenses
\d policy
\d document_chunks
\dx
\q
```

Attention : le changement d'image PostgreSQL a provoqué un warning de collation :

```text
database "AO_DB" has a collation version mismatch
```

Il n'a pas bloqué les tests de développement.

---

# 5. Modèle SQL actuel

Tables principales :

## policy

Conceptuellement :

```sql
id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY
category VARCHAR(150) UNIQUE NOT NULL
max_amount DECIMAL(10,2) NOT NULL CHECK (max_amount >= 0)
```

## expenses

Conceptuellement :

```sql
id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY
category VARCHAR(150) NOT NULL
amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0)
```

Pas de FK obligatoire de `expenses.category` vers `policy.category`, car une catégorie inconnue peut être un cas métier à traiter explicitement.

## document_chunks

Ajoutée avec `002_add_vector_store.sql` :

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE document_chunks (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category VARCHAR(150),
    source VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536) NOT NULL
);
```

Le modèle d'embedding utilisé actuellement retourne 1536 dimensions.

---

# 6. Niveau 0 — Python / CSV

La première version fonctionnait avec :
- `expenses.csv`
- `policy.csv`

Objectif :
- associer catégorie de dépense et policy ;
- comparer montant et plafond ;
- gérer catégorie inconnue ;
- gérer montant invalide ;
- produire un résultat structuré.

Cette logique a servi d'apprentissage et a ensuite été progressivement remplacée par une architecture plus propre.

---

# 7. Niveau 1 — PostgreSQL / persistance

Compétences déjà travaillées :
- SQL ;
- contraintes ;
- PostgreSQL ;
- Docker Compose ;
- volumes ;
- Psycopg ;
- CRUD ;
- transactions ;
- rollback ;
- tests d'intégration ;
- migrations ;
- IDs automatiques avec `IDENTITY`.

Important :
- `with get_connection() as conn:` commit automatiquement si tout va bien et rollback en cas d'exception.
- Les tests DB utilisent `rollback()` pour ne pas polluer la base.

Migration IDs automatiques :
`001_auto_ids.sql`

Les anciennes tables avaient déjà des IDs, donc les séquences ont été recalées manuellement après ajout de l'identity.

---

# 8. Niveau 2 — FastAPI / architecture backend

API existante autour de `expenses` et `policies`.

Routes principales :

```text
GET    /expenses
GET    /expenses/{id}
POST   /expenses
PATCH  /expenses/{id}
DELETE /expenses/{id}

GET    /policies
GET    /policies/{id}
POST   /policies
PATCH  /policies/{id}
```

Swagger :

```text
http://127.0.0.1:8000/docs
```

Commande Uvicorn :

```bash
uv run uvicorn accordops.api:app --reload
```

Architecture actuelle :

```text
api.py
   ↓
services.py
   ↓
db.py
   ↓
PostgreSQL
```

Rôles :
- `api.py` : HTTP, routes, codes HTTP, `HTTPException`
- `schemas.py` : modèles Pydantic
- `services.py` : orchestration et logique métier
- `db.py` : SQL / accès PostgreSQL

Principe important :

```text
services.py → erreurs métier
api.py      → traduction en erreurs HTTP
```

Exemples :
- `ExpenseNotFoundError`
- `PolicyNotFoundError`

Une opération métier doit idéalement partager une même connexion / transaction.

---

# 9. Pydantic / modèles métier

Les montants métier utilisent `Decimal`.

Exemple :

```python
class ExpenseCreate(BaseModel):
    category: str
    amount: Decimal = Field(ge=0)
```

Piège déjà rencontré :

```python
merchant: str | None
```

signifie "champ obligatoire mais nullable".

Pour un champ réellement optionnel :

```python
merchant: str | None = None
```

Pour les champs optionnels :

```python
if new_amount is not None:
```

et pas :

```python
if new_amount:
```

car `0` est une valeur valide mais falsey.

---

# 10. Niveau 3 — documents / OCR / LLM

## Upload

Route :

```text
POST /receipts
```

Types acceptés :
- `application/pdf`
- `image/png`
- `image/jpeg`

Le fichier est lu avec :

```python
content = await file.read()
```

`content` est un `bytes`.

---

# 11. PDF extraction

PyPDF est utilisé.

Flux :

```text
bytes
→ io.BytesIO
→ PdfReader
→ pages
→ extract_text()
→ texte
```

Exemple de logique :

```python
file_like_object = io.BytesIO(content)
reader = PdfReader(file_like_object)

text_content = []

for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
        text_content.append(page_text)

return "\n".join(text_content)
```

`BytesIO` ne rend pas les bytes "physiques" : il les encapsule dans un objet file-like en mémoire.

---

# 12. OCR image

Tesseract / pytesseract est utilisé pour une première version OCR.

Flux :

```text
bytes
→ BytesIO
→ Pillow Image
→ pytesseract.image_to_string()
→ texte
```

Exemple :

```python
image = Image.open(io.BytesIO(content))
texte = pytesseract.image_to_string(image)
```

Limite observée :
- texte imprimé propre : bon résultat ;
- écriture manuscrite : très mauvais / `Empty page!!`.

---

# 13. OpenAI API / LLM structured extraction

Le SDK OpenAI est utilisé dans `llm.py`.

Connexion :

```python
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

La clé est dans `.env`, jamais à commit.

Structured output utilisé avec :

```python
client.responses.parse(...)
```

Il existe deux modèles distincts :

## TicketExpenseLLM

Contrat adapté au LLM.

Le montant est en `float`, car `Decimal` a causé une erreur JSON Schema avec Structured Outputs :

```text
Invalid JSON schema: regex lookaround is not supported
```

## TicketExpense

Modèle métier interne.

Le montant est en `Decimal`.

Conversion :

```python
Decimal(str(llm_expense.amount))
```

et pas :

```python
Decimal(llm_expense.amount)
```

pour éviter de récupérer les imprécisions binaires du float.

---

# 14. Grounding des catégories

Initialement, le LLM renvoyait `category = null`, même pour :

```text
Restaurant Chez Marcel
```

Solution :
- récupérer les catégories autorisées dans PostgreSQL ;
- les fournir au LLM ;
- demander de choisir uniquement parmi ces catégories ;
- sinon retourner `null`.

Comportement validé :
- restaurant → `restaurant`
- tennis → `null`

---

# 15. Vérification déterministe de conformité

Un modèle `ComplianceResult` existe.

Statuts :

```python
Literal["conforme", "non conforme", "review"]
```

Champs conceptuels :
- status
- category
- amount
- max_amount
- difference
- reason

Fonction :

```python
check_ticket_expense(expense: TicketExpense) -> ComplianceResult
```

Logique :

```text
category absente
OU amount absent
OU policy absente
→ review

sinon :
amount <= max_amount
→ conforme

amount > max_amount
→ non conforme
```

L'early return a été introduit pour simplifier la logique.

---

# 16. Niveau 4 — RAG

Le RAG a été volontairement rendu utile au lieu d'être ajouté artificiellement.

La table `policy` contient les règles structurées simples :

```text
restaurant → 35 EUR
hotel → 180 EUR
```

Le document Markdown contient les règles contextuelles :

```text
alcool non remboursable
minibar non remboursable
taxi accepté après 22h
train 1re classe soumis à validation
etc.
```

Donc :

```text
SQL → décision déterministe simple
RAG → règles riches / contexte / justification
```

---

# 17. Corpus RAG

Fichier :

```text
documents/policies/expense_policy.md
```

Exemples de règles :

```text
## Restaurant
Le plafond standard est de 35 EUR par repas.
Un justificatif est obligatoire.
Les boissons alcoolisées ne sont pas remboursables.
Un dépassement peut être accepté lors d'un déplacement international avec validation du manager.

## Hôtel
Le plafond standard est de 180 EUR par nuit.
Une facture nominative est obligatoire.
Les frais de minibar et les services de divertissement ne sont pas remboursables.

## Taxi
Les taxis sont remboursables lorsque :
- les transports en commun ne sont plus disponibles ;
- le déplacement a lieu avant 6h ou après 22h ;
- le salarié transporte du matériel professionnel encombrant.

## Train
Les billets de seconde classe sont remboursables.
La première classe nécessite une justification et une validation managériale.
```

---

# 18. Chunking — leçon importante

Première stratégie :
- 1 section `##` = 1 chunk.

Problème :
le chunk restaurant contenait toutes les règles restaurant.

Nouvelle stratégie :
- 1 règle / paragraphe = 1 chunk ;
- la catégorie de la section est conservée comme metadata.

Exemple :

```python
{
    "category": "restaurant",
    "content": "restaurant -- Les boissons alcoolisées ne sont pas remboursables."
}
```

Fonction actuelle dans `rag.py` :

```python
def chunker(path: Path):
    sections = []
    category = None

    with path.open() as f:
        for line in f:
            line = line.strip()

            if line.startswith("##"):
                category = line.removeprefix("## ").strip().lower()
                continue

            if line.startswith("# ") or not line:
                continue

            if category is not None:
                sections.append(
                    {
                        "category": category,
                        "content": f"{category} -- {line}",
                    }
                )

    return sections
```

Cette version est simple et adaptée au format fictif actuel.

---

# 19. Embeddings

Fichier :

```text
src/accordops/embedder.py
```

Modèle :

```text
text-embedding-3-small
```

Fonction :

```python
def embed_text(text: str):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small",
    )
    return response.data[0].embedding
```

Dimension constatée :

```text
1536
```

---

# 20. pgvector

Extension activée via :

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Le Python utilise :

```python
from pgvector.psycopg import register_vector
```

et dans `get_connection()` :

```python
register_vector(conn)
```

Fonction d'insertion :

```python
def add_document_chunk(conn, category, source, content, embedding):
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO document_chunks(category,source,content,embedding) VALUES(%s,%s,%s,%s) RETURNING id",
            (category, source, content, embedding),
        )
        row = cursor.fetchone()
        return row[0]
```

---

# 21. Indexation du corpus

Exemple de script :

```python
chunks = chunker(Path("documents/policies/expense_policy.md"))

with get_connection() as conn:
    for chunk in chunks:
        category = chunk["category"]
        embedding = embed_text(chunk["content"])

        add_document_chunk(
            conn,
            source="expense_policy.md",
            embedding=embedding,
            content=chunk["content"],
            category=category,
        )
```

Pour nettoyer les chunks pendant les tests :

```sql
TRUNCATE TABLE document_chunks RESTART IDENTITY;
```

---

# 22. Retrieval sémantique

Fonction DB :

```python
def search_similar_chunks(conn, query_embedding, limit=3):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT category, source, content,
                   embedding <=> %s::vector AS distance
            FROM document_chunks
            ORDER BY distance
            LIMIT %s
            """,
            (query_embedding, limit),
        )
        return cursor.fetchall()
```

Important :
- `<=>` = distance cosinus pgvector ;
- distance plus petite = plus proche sémantiquement.

Bug rencontré :
sans `::vector`, PostgreSQL voyait :

```text
vector <=> double precision[]
```

et levait :

```text
operator does not exist: vector <=> double precision[]
```

Le cast explicite `%s::vector` a corrigé le problème.

---

# 23. Retrieval validé

Query :

```text
Est-ce que les boissons alcoolisées sont remboursées au restaurant ?
```

Top résultats :

```text
restaurant -- Les boissons alcoolisées ne sont pas remboursables.
hôtel -- Les frais de minibar et les services de divertissement ne sont pas remboursables.
restaurant -- Un justificatif est obligatoire.
```

Le top 1 est exactement la règle pertinente.

Donc **L4.4 est validé**.

---

# 24. Dernier état Git connu

Derniers jalons connus :

```text
L3.5 : contraindre l'extraction LLM aux catégories métier
L3.6 : ajouter la vérification déterministe de conformité
L4.1 : ajouter le corpus documentaire et le chunking par section
L4.2 : ajouter la génération d'embeddings
L4.3 : ajouter le stockage vectoriel avec pgvector
L4.4 : ajouter l'indexation documentaire et le retrieval sémantique
```

Dernier commit recommandé :

```bash
git add .
git commit -m "L4.4 : ajouter l'indexation documentaire et le retrieval sémantique"
git push
```

Avant reprise :

```bash
git status
git log --oneline --decorate -10
```

---

# 25. PROCHAINE ÉTAPE EXACTE — L4.5

La prochaine étape est :

```text
L4.5 — génération grounded avec citations
```

Objectif :

```text
question utilisateur
→ embedding
→ top chunks
→ LLM reçoit uniquement ces chunks
→ réponse basée sur les chunks
→ source/citation
```

Exemple :

```text
Question :
"Est-ce que l'alcool est remboursé au restaurant ?"

Retrieval :
restaurant -- Les boissons alcoolisées ne sont pas remboursables.

LLM :
"Non. Selon la politique de remboursement, les boissons alcoolisées ne sont pas remboursables."

Source :
expense_policy.md
```

Faire d'abord le pipeline manuellement :

```text
query
→ embed_text(query)
→ search_similar_chunks()
→ construire un contexte
→ appel LLM
→ réponse
```

Ne pas utiliser LangChain immédiatement.

---

# 26. Suite prévue après L4.5

## L4.6
Évaluation du retrieval :
- petit dataset de questions ;
- chunk attendu ;
- top-k ;
- recall@k simple ;
- groundedness.

## L4.7
Amélioration retrieval :
- metadata filtering ;
- éventuellement hybrid search dense + keyword/BM25 ;
- reranking ;
- query rewriting si besoin.

## L4.8
Comparer éventuellement une implémentation LangChain / LlamaIndex avec l'implémentation maison.

## Niveau 5
HITL / workflow :
- proposition LLM ;
- validation/correction utilisateur ;
- insertion DB seulement après validation ;
- statut review.

## Niveau 6
API externe fictive :
- comptabilité / remboursement ;
- retries ;
- timeout ;
- idempotence ;
- sécurité.

## Niveau 7
Industrialisation :
- Docker complet ;
- CI/CD ;
- logs ;
- observabilité ;
- tests ;
- évaluation IA ;
- coûts ;
- latence ;
- sécurité.

## Plus tard
LangGraph si le workflow devient réellement complexe :
- branching ;
- retries ;
- review humaine ;
- actions externes ;
- états multiples.

Ne pas utiliser LangGraph juste "pour cocher la case".

## Plus tard
Azure :
- Azure OpenAI / Microsoft Foundry ;
- Azure AI Search ;
- Azure PostgreSQL ;
- Key Vault ;
- monitoring ;
- déploiement cloud.

---

# 27. Philosophie de progression

Ne pas surarchitecturer trop tôt.

Toujours préférer :

```text
problème réel
→ besoin concret
→ ajout de la brique
```

plutôt que :

```text
framework tendance
→ chercher artificiellement où le placer
```

---

# 28. Style d'accompagnement souhaité pour le futur GPT

L'utilisateur veut :
- réponses en français ;
- explications claires ;
- éviter les longs cours sauf demande explicite ;
- apprendre réellement les concepts ;
- coder lui-même ;
- éviter le copier-coller de code généré quand la partie est pédagogique ;
- accepter du boilerplate fourni lorsque refaire le même CRUD n'apporte rien ;
- obtenir un feedback précis sur son code ;
- recevoir une explication du "pourquoi", pas seulement la correction ;
- ne pas surarchitecturer ;
- ne pas introduire une techno sans utilité réelle ;
- être guidé vers une architecture professionnelle mais compréhensible.

À chaque étape :
1. expliquer la mission ;
2. laisser l'utilisateur tenter ;
3. corriger ;
4. dire explicitement si un commit est recommandé ;
5. proposer un message de commit en français.

---

# 29. Commandes de reprise rapide

Depuis la racine :

```bash
uv sync
docker compose up -d
uv run pytest -v
uv run uvicorn accordops.api:app --reload
```

Swagger :

```text
http://127.0.0.1:8000/docs
```

Connexion PostgreSQL :

```bash
docker compose exec postgres psql -U ao_admin -d AO_DB
```

Vérifier pgvector :

```text
\dx
\d document_chunks
```

Git :

```bash
git status
git log --oneline --decorate -10
```

---

# 30. Prompt de reprise à donner au futur GPT

> Je reprends mon projet AccordOps. Lis entièrement le document de handover joint avant de répondre. Je développe ce projet moi-même pour apprendre réellement le métier d'AI Engineer / Forward AI Engineer : ne code pas tout à ma place. Agis comme professeur, reviewer et pair programming léger. Mon dernier jalon validé est L4.4 : indexation documentaire + retrieval sémantique avec OpenAI embeddings et pgvector. La prochaine étape prévue est L4.5 : génération grounded à partir des chunks récupérés, avec source/citation. À chaque étape, dis-moi explicitement si je dois commit ou non et propose un message de commit en français quand c'est pertinent.
