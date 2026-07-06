from __future__ import annotations

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from .config import Settings
from .git_tools import RepoContext, build_tools


SYSTEM_PROMPT = """Tu es un agent senior charge d'ameliorer des projets GitHub.

Objectif:
- Comprendre le depot avant de modifier.
- Chercher des ameliorations petites, utiles et verifiables.
- Privilegier les corrections de bugs, tests, lint, README, typage, CI et ergonomie.
- Ne pas reecrire tout le projet.
- Avant une PR, produire un diff et resumer les risques.

Regles:
- Clone ou mets a jour le depot avant toute inspection.
- Lis les fichiers pertinents au lieu de deviner.
- Garde les changements limites et coherents avec le style du projet.
- Lance une validation disponible quand c'est possible.
- N'ouvre une PR que si l'utilisateur l'a demande explicitement dans son objectif.
- Reponds en francais, clairement, avec les fichiers touches et la validation.
"""


def build_agent(settings: Settings):
    llm = ChatOpenAI(model=settings.openai_model, temperature=0.1)
    context = RepoContext(settings.workspace, settings.github_token)
    return create_agent(model=llm, tools=build_tools(context), system_prompt=SYSTEM_PROMPT)


def run_agent(repo_url: str, objective: str, create_pr: bool = False) -> str:
    settings = Settings.from_env()
    agent = build_agent(settings)
    pr_instruction = (
        "Si des changements sont utiles, cree une branche, commit et ouvre une PR."
        if create_pr
        else "Ne cree pas de PR. Fais les changements localement et montre le diff."
    )
    result = agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Depot: {repo_url}\nObjectif: {objective}\n{pr_instruction}",
                )
            ]
        }
    )
    return result["messages"][-1].content
