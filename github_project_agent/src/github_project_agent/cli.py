from __future__ import annotations

import argparse

from .agent import run_agent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="github-project-agent",
        description="Agent LangChain pour ameliorer un depot GitHub.",
    )
    parser.add_argument("repo_url", help="URL du depot GitHub, ex: https://github.com/owner/repo")
    parser.add_argument(
        "--objectif",
        default="Trouve une amelioration simple, implemente-la, puis verifie-la.",
        help="Objectif donne a l'agent.",
    )
    parser.add_argument(
        "--pr",
        action="store_true",
        help="Autorise l'agent a pousser une branche et ouvrir une pull request.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    print(run_agent(args.repo_url, args.objectif, args.pr))


if __name__ == "__main__":
    main()

