# GitHub Project Agent

Agent LangChain qui clone un depot GitHub, inspecte le code, applique une amelioration limitee, lance une validation autorisee, puis peut ouvrir une pull request.

## Installation

```powershell
cd C:\Users\user\Documents\github_project_agent
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
copy .env.example .env
```

Renseigne `OPENAI_API_KEY` dans `.env`.

Pour GitHub, le plus simple:

```powershell
gh auth login
```

Tu peux aussi utiliser `GITHUB_TOKEN` dans `.env`.

## Utilisation

Mode prudent, sans PR:

```powershell
github-project-agent https://github.com/OWNER/REPO --objectif "Ajoute des tests sur la logique critique et corrige les erreurs evidentes."
```

Autoriser une PR:

```powershell
github-project-agent https://github.com/OWNER/REPO --objectif "Ameliore le README et ajoute une validation CI minimale." --pr
```

## Garde-fous

- L'agent travaille dans `.agent-workspace`.
- Les chemins sont refuses s'ils sortent du depot clone.
- Les commandes de validation sont limitees a une liste connue (`pytest`, `npm run test`, `npm run lint`, etc.).
- La PR n'est ouverte que si tu passes `--pr`.

## Sources utiles

- LangChain recommande maintenant `langchain.agents.create_agent`; ce projet utilise cette API.
- GitHub documente la creation de pull requests via l'API REST; ici, l'ouverture de PR passe par `gh pr create` quand le CLI est installe et authentifie.
