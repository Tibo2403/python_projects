from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import shutil
import subprocess
from urllib.parse import urlparse


MAX_READ_BYTES = 80_000
ALLOWED_COMMANDS = {
    "npm test",
    "npm run test",
    "npm run lint",
    "npm run build",
    "pnpm test",
    "pnpm lint",
    "pnpm build",
    "pytest",
    "python -m pytest",
    "ruff check .",
}


@dataclass(frozen=True)
class RepoContext:
    workspace: Path
    github_token: str | None = None

    def repo_path(self, repo_url: str) -> Path:
        owner, name = parse_repo_slug(repo_url)
        return (self.workspace / owner / name).resolve()


def parse_repo_slug(repo_url: str) -> tuple[str, str]:
    if repo_url.startswith("git@github.com:"):
        slug = repo_url.removeprefix("git@github.com:").removesuffix(".git")
    else:
        parsed = urlparse(repo_url)
        parts = parsed.path.strip("/").removesuffix(".git").split("/")
        if len(parts) < 2:
            raise ValueError("URL GitHub invalide. Exemple: https://github.com/owner/repo")
        slug = "/".join(parts[-2:])
    owner, name = slug.split("/", 1)
    return owner, name


def build_tools(context: RepoContext):
    from langchain.tools import tool

    def run_git(args: list[str], cwd: Path | None = None) -> str:
        env = os.environ.copy()
        if context.github_token:
            env["GITHUB_TOKEN"] = context.github_token
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            timeout=120,
            check=False,
        )
        return command_output(result)

    def inside_repo(repo_url: str, relative_path: str = ".") -> Path:
        repo = context.repo_path(repo_url)
        target = (repo / relative_path).resolve()
        if not str(target).startswith(str(repo)):
            raise ValueError("Chemin refuse: sortie du repertoire du repo.")
        return target

    @tool
    def clone_or_update_repo(repo_url: str) -> str:
        """Clone le depot GitHub dans le workspace local, ou fait un fetch s'il existe deja."""
        context.workspace.mkdir(parents=True, exist_ok=True)
        path = context.repo_path(repo_url)
        if path.exists():
            return run_git(["fetch", "--all", "--prune"], cwd=path)
        path.parent.mkdir(parents=True, exist_ok=True)
        return run_git(["clone", repo_url, str(path)], cwd=context.workspace)

    @tool
    def list_files(repo_url: str, glob: str = "*") -> str:
        """Liste les fichiers du depot. Utilise un glob simple comme *.py, src/**/*.ts, etc."""
        repo = context.repo_path(repo_url)
        if not repo.exists():
            return "Depot non clone. Appelle d'abord clone_or_update_repo."
        paths = sorted(p for p in repo.glob(glob) if p.is_file() and ".git" not in p.parts)
        return "\n".join(str(p.relative_to(repo)) for p in paths[:300])

    @tool
    def read_file(repo_url: str, relative_path: str) -> str:
        """Lit un fichier du depot, tronque si le fichier est trop gros."""
        path = inside_repo(repo_url, relative_path)
        data = path.read_bytes()
        suffix = "" if len(data) <= MAX_READ_BYTES else "\n\n[TRONQUE: fichier trop long]"
        return data[:MAX_READ_BYTES].decode("utf-8", errors="replace") + suffix

    @tool
    def write_file(repo_url: str, relative_path: str, content: str) -> str:
        """Ecrit ou remplace un fichier dans le depot clone."""
        path = inside_repo(repo_url, relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        return f"Ecrit: {relative_path}"

    @tool
    def run_validation(repo_url: str, command: str) -> str:
        """Lance une commande de validation autorisee dans le repo."""
        if command not in ALLOWED_COMMANDS:
            allowed = ", ".join(sorted(ALLOWED_COMMANDS))
            return f"Commande refusee. Commandes autorisees: {allowed}"
        repo = context.repo_path(repo_url)
        result = subprocess.run(
            command.split(),
            cwd=repo,
            text=True,
            capture_output=True,
            timeout=240,
            check=False,
        )
        return command_output(result)

    @tool
    def git_diff(repo_url: str) -> str:
        """Affiche les changements locaux non commites."""
        return run_git(["diff", "--", "."], cwd=context.repo_path(repo_url))

    @tool
    def create_branch_commit_and_pr(repo_url: str, branch: str, title: str, body: str) -> str:
        """Cree une branche, commit les changements, push, puis ouvre une PR avec gh si disponible."""
        repo = context.repo_path(repo_url)
        messages = [
            run_git(["checkout", "-B", branch], cwd=repo),
            run_git(["add", "."], cwd=repo),
            run_git(["commit", "-m", title], cwd=repo),
            run_git(["push", "-u", "origin", branch], cwd=repo),
        ]
        gh = shutil.which("gh")
        if not gh:
            messages.append("gh introuvable: branche poussee, PR a ouvrir manuellement.")
            return "\n".join(messages)
        result = subprocess.run(
            [gh, "pr", "create", "--title", title, "--body", body],
            cwd=repo,
            text=True,
            capture_output=True,
            timeout=120,
            check=False,
        )
        messages.append(command_output(result))
        return "\n".join(messages)

    return [
        clone_or_update_repo,
        list_files,
        read_file,
        write_file,
        run_validation,
        git_diff,
        create_branch_commit_and_pr,
    ]


def command_output(result: subprocess.CompletedProcess[str]) -> str:
    output = "\n".join(part for part in [result.stdout, result.stderr] if part)
    if not output.strip():
        output = f"Commande terminee avec code {result.returncode}."
    return output[-20_000:]
