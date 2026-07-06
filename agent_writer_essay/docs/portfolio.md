# Essay Writer Agent

LangGraph workflow that plans, researches, drafts, critiques, and revises essays from either a CLI or a local Gradio interface.

## Portfolio Angle

- Demonstrates graph-based agent orchestration with explicit planner, researcher, writer, and critic nodes.
- Provides both command-line and graphical workflows.
- Keeps API keys local through `.env` or password fields in the UI.

## Demo Story

1. Start the Gradio UI with `python .\agent_writer_essay.py --gui`.
2. Enter a topic and API keys.
3. Show the generated plan, critique, and final draft.

## Next Improvements

- Add source citations in the final draft.
- Add export to Markdown and DOCX.
- Add model and search-result controls in the CLI.
