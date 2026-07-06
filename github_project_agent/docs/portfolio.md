# GitHub Project Agent

LangChain-powered local agent that clones a GitHub repository, inspects it, applies a scoped improvement, runs an allowlisted validation command, and can open a pull request when explicitly authorized.

## Portfolio Angle

- Shows agentic coding with practical guardrails instead of unconstrained shell access.
- Uses path validation to prevent edits outside the cloned repository.
- Keeps pull-request creation opt-in via `--pr`.

## Demo Story

1. Run the agent against a small public repository.
2. Ask for a narrow improvement such as README cleanup or a missing test.
3. Review the local diff before allowing a PR.

## Next Improvements

- Add a dry-run planning mode.
- Add richer repository summary output before edits.
- Persist validation logs under `.agent-workspace`.
