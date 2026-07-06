import ast
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "agent_writer_essay.py"


def parse_source():
    return ast.parse(SOURCE.read_text(encoding="utf-8"))


def test_workflow_prompts_are_defined():
    tree = parse_source()
    names = {
        node.targets[0].id
        for node in tree.body
        if isinstance(node, ast.Assign)
        and node.targets
        and isinstance(node.targets[0], ast.Name)
    }

    assert {
        "PLAN_PROMPT",
        "WRITER_PROMPT",
        "REFLECTION_PROMPT",
        "RESEARCH_PLAN_PROMPT",
        "RESEARCH_CRITIQUE_PROMPT",
    } <= names


def test_cli_exposes_gui_and_revision_options():
    source = SOURCE.read_text(encoding="utf-8")
    assert "--gui" in source
    assert "--max-revisions" in source
    assert "--model" in source
