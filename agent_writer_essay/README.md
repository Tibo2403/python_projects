# Essay Writer Agent

Programme extrait de `Agent_writer_essay.ipynb`.

## Installation

```powershell
cd C:\Users\user\Documents\agent_writer_essay
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Crée ensuite un fichier `.env` dans ce dossier avec tes clés:

```env
OPENAI_API_KEY=...
TAVILY_API_KEY=...
OPENAI_MODEL=gpt-3.5-turbo
```

## Utilisation

```powershell
python .\agent_writer_essay.py "what is the difference between langchain and langsmith"
```

Tu peux limiter ou augmenter le nombre de révisions:

```powershell
python .\agent_writer_essay.py "Sujet de dissertation" --max-revisions 1
```

## Interface graphique

```powershell
python .\agent_writer_essay.py --gui
```

Le programme ouvrira une interface web locale Gradio dans le navigateur.
Tu peux entrer les clés API directement dans l'interface. Si tu préfères, tu peux aussi les garder dans un fichier `.env`.

Si le port `7860` est déjà utilisé:

```powershell
python .\agent_writer_essay.py --gui --port 7861
```
