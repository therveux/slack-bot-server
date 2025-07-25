# 🤖 slack-bot-server

Un backend léger en **Python (FastAPI)** pour automatiser des commandes Slack personnalisées (comme `/trads`)

---

## 🚀 Fonctionnalités

- 🔌 Webhook Slack (slash commands comme `/trads`)
- ⚙️ Déploiement sur [Render](https://render.com)
- 📜 Géré avec [`poetry`](https://python-poetry.org/)
- 🌐 Serveur HTTP via `uvicorn`

---

## 🧪 Lancer en local

### 1. Prérequis

- Python ≥ 3.10
- Poetry installé  
  👉 [Installer poetry](https://python-poetry.org/docs/#installation)

### 2. Installer les dépendances

```bash
make install
```

### 3. Lancer le serveur

```bash
make dev
```

---

## 🚀 Déploiement sur Render

### 1. Générer le `requirements.txt`

Render n’utilise pas Poetry directement, donc exporte les dépendances avec :

```bash
poetry export --format requirements.txt --without-hashes --output requirements.txt
```

👉 Ce fichier est à régénérer **à chaque changement de dépendance**.

### 2. Configurer Render

- **Build command**:

  ```bash
  pip install -r requirements.txt
  ```

- **Start command**:

  ```bash
  PYTHONPATH=src uvicorn slack_bot_server.main:app --host 0.0.0.0 --port $PORT
  ```

- Ajoute les secrets Slack/API dans l'interface Render

---

## 🛠️ Commandes utiles (via `Makefile`)

```bash
make run        # Lance le serveur en prod (Render-compatible)
make dev        # Lance avec auto-reload (poetry + FastAPI)
make export     # Génère le requirements.txt
```

---

## 🔐 Configuration (env)

Ajoute un fichier `.env` si nécessaire :

```
SLACK_SIGNING_SECRET=...
SLACK_BOT_TOKEN=...
```

Et charge-le dans `main.py` avec `os.getenv(...)` ou `python-dotenv` (optionnel).

---

## 📬 Tester un endpoint

```bash
curl -X POST https://slack-bot-server-staging.up.railway.app/slack \
  -H "Content-Type: application/json" \
  -d '{"text": "Bonjour"}'
```

---

## 👥 Contributeurs

- 🧑‍💻 Maintenu par [Théo Herveux](https://github.com/therveux)

---

## 📝 Licence

MIT – Libre à utiliser, modifier et adapter.
