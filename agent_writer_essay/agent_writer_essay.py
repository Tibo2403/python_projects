"""Essay-writing agent converted from Agent_writer_essay.ipynb.

This script builds the original LangGraph workflow as a command-line program:
plan -> research -> draft -> critique -> extra research -> revised draft.
"""

from __future__ import annotations

import argparse
import os
import queue
import threading
from typing import List, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph
from pydantic import BaseModel
from tavily import TavilyClient


PLAN_PROMPT = """You are an expert writer tasked with writing a high level outline of an essay. \
Write such an outline for the user provided topic. Give an outline of the essay along with any relevant notes \
or instructions for the sections."""

WRITER_PROMPT = """You are an essay assistant tasked with writing excellent 5-paragraph essays.\
Generate the best essay possible for the user's request and the initial outline. \
If the user provides critique, respond with a revised version of your previous attempts. \
Utilize all the information below as needed:

------

{content}"""

REFLECTION_PROMPT = """You are a teacher grading an essay submission. \
Generate critique and recommendations for the user's submission. \
Provide detailed recommendations, including requests for length, depth, style, etc."""

RESEARCH_PLAN_PROMPT = """You are a researcher charged with providing information that can \
be used when writing the following essay. Generate a list of search queries that will gather \
any relevant information. Only generate 3 queries max."""

RESEARCH_CRITIQUE_PROMPT = """You are a researcher charged with providing information that can \
be used when making any requested revisions (as outlined below). \
Generate a list of search queries that will gather any relevant information. Only generate 3 queries max."""


class AgentState(TypedDict, total=False):
    task: str
    plan: str
    draft: str
    critique: str
    content: List[str]
    revision_number: int
    max_revisions: int


class Queries(BaseModel):
    queries: List[str]


class EssayWriterAgent:
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0,
        tavily_max_results: int = 2,
        openai_api_key: str | None = None,
        tavily_api_key: str | None = None,
    ) -> None:
        load_dotenv()
        openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        tavily_api_key = tavily_api_key or os.getenv("TAVILY_API_KEY")

        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY is missing.")
        if not tavily_api_key:
            raise ValueError("TAVILY_API_KEY is missing.")

        self.model = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=openai_api_key,
        )
        self.tavily = TavilyClient(api_key=tavily_api_key)
        self.tavily_max_results = tavily_max_results
        self.graph = self._build_graph()

    def _build_graph(self):
        memory = SqliteSaver.from_conn_string(":memory:")
        builder = StateGraph(AgentState)

        builder.add_node("planner", self.plan_node)
        builder.add_node("research_plan", self.research_plan_node)
        builder.add_node("generate", self.generation_node)
        builder.add_node("reflect", self.reflection_node)
        builder.add_node("research_critique", self.research_critique_node)

        builder.set_entry_point("planner")
        builder.add_edge("planner", "research_plan")
        builder.add_edge("research_plan", "generate")
        builder.add_conditional_edges(
            "generate",
            self.should_continue,
            {END: END, "reflect": "reflect"},
        )
        builder.add_edge("reflect", "research_critique")
        builder.add_edge("research_critique", "generate")

        return builder.compile(checkpointer=memory)

    def plan_node(self, state: AgentState):
        messages = [
            SystemMessage(content=PLAN_PROMPT),
            HumanMessage(content=state["task"]),
        ]
        response = self.model.invoke(messages)
        return {"plan": response.content}

    def research_plan_node(self, state: AgentState):
        queries = self.model.with_structured_output(Queries).invoke(
            [
                SystemMessage(content=RESEARCH_PLAN_PROMPT),
                HumanMessage(content=state["task"]),
            ]
        )
        return {"content": self._search(queries.queries, state.get("content", []))}

    def generation_node(self, state: AgentState):
        content = "\n\n".join(state.get("content", []))
        messages = [
            SystemMessage(content=WRITER_PROMPT.format(content=content)),
            HumanMessage(
                content=f"{state['task']}\n\nHere is my plan:\n\n{state['plan']}"
            ),
        ]
        response = self.model.invoke(messages)
        return {
            "draft": response.content,
            "revision_number": state.get("revision_number", 1) + 1,
        }

    def reflection_node(self, state: AgentState):
        messages = [
            SystemMessage(content=REFLECTION_PROMPT),
            HumanMessage(content=state["draft"]),
        ]
        response = self.model.invoke(messages)
        return {"critique": response.content}

    def research_critique_node(self, state: AgentState):
        queries = self.model.with_structured_output(Queries).invoke(
            [
                SystemMessage(content=RESEARCH_CRITIQUE_PROMPT),
                HumanMessage(content=state["critique"]),
            ]
        )
        return {"content": self._search(queries.queries, state.get("content", []))}

    def should_continue(self, state: AgentState):
        if state["revision_number"] > state["max_revisions"]:
            return END
        return "reflect"

    def _search(self, queries: List[str], existing_content: List[str] | None = None):
        content = list(existing_content or [])
        for query in queries:
            response = self.tavily.search(
                query=query,
                max_results=self.tavily_max_results,
            )
            for result in response["results"]:
                content.append(result["content"])
        return content

    def run(self, task: str, max_revisions: int = 2, thread_id: str = "1") -> AgentState:
        thread = {"configurable": {"thread_id": thread_id}}
        final_state: AgentState = {}

        for event in self.graph.stream(
            {
                "task": task,
                "max_revisions": max_revisions,
                "revision_number": 1,
                "content": [],
            },
            thread,
        ):
            node_name, node_state = next(iter(event.items()))
            final_state.update(node_state)
            print(f"\n--- {node_name} ---")
            if "plan" in node_state:
                print(node_state["plan"])
            if "critique" in node_state:
                print(node_state["critique"])
            if "draft" in node_state:
                print(node_state["draft"])

        return final_state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate and revise an essay.")
    parser.add_argument("topic", nargs="*", help="Essay topic or instruction.")
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch a local graphical web interface.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="Port to use for the graphical interface.",
    )
    parser.add_argument(
        "-r",
        "--max-revisions",
        type=int,
        default=2,
        help="Number of critique/revision rounds to run.",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        help="OpenAI chat model to use.",
    )
    parser.add_argument(
        "--thread-id",
        default="1",
        help="LangGraph checkpoint thread id.",
    )
    return parser.parse_args()


def launch_gui(model_name: str, port: int = 7860) -> None:
    try:
        import gradio as gr
    except ImportError as exc:
        raise SystemExit(
            "Gradio is not installed. Run: pip install -r requirements.txt"
        ) from exc

    def write_essay(
        topic: str,
        max_revisions: int,
        openai_api_key: str,
        tavily_api_key: str,
    ):
        if not topic.strip():
            yield "Entre un sujet pour commencer.", "", "", ""
            return

        openai_api_key = openai_api_key.strip() or None
        tavily_api_key = tavily_api_key.strip() or None

        events: queue.Queue[tuple[str, str, str, str] | None] = queue.Queue()

        def worker() -> None:
            try:
                agent = EssayWriterAgent(
                    model_name=model_name,
                    openai_api_key=openai_api_key,
                    tavily_api_key=tavily_api_key,
                )
                thread = {"configurable": {"thread_id": "gui"}}
                plan = ""
                critique = ""
                draft = ""

                for event in agent.graph.stream(
                    {
                        "task": topic.strip(),
                        "max_revisions": int(max_revisions),
                        "revision_number": 1,
                        "content": [],
                    },
                    thread,
                ):
                    node_name, node_state = next(iter(event.items()))
                    if "plan" in node_state:
                        plan = node_state["plan"]
                    if "critique" in node_state:
                        critique = node_state["critique"]
                    if "draft" in node_state:
                        draft = node_state["draft"]

                    status = f"Etape en cours: {node_name}"
                    events.put((status, plan, critique, draft))

                events.put(("Termine.", plan, critique, draft))
            except Exception as exc:  # Gradio displays this in the status field.
                events.put((f"Erreur: {exc}", "", "", ""))
            finally:
                events.put(None)

        threading.Thread(target=worker, daemon=True).start()

        while True:
            item = events.get()
            if item is None:
                break
            yield item

    with gr.Blocks(title="Essay Writer Agent") as demo:
        gr.Markdown("# Essay Writer Agent")
        with gr.Row():
            openai_api_key = gr.Textbox(
                label="OpenAI API key",
                type="password",
                placeholder="sk-...",
            )
            tavily_api_key = gr.Textbox(
                label="Tavily API key",
                type="password",
                placeholder="tvly-...",
            )
        with gr.Row():
            topic = gr.Textbox(
                label="Sujet",
                lines=4,
                placeholder="Ex: What is the difference between LangChain and LangSmith?",
            )
            with gr.Column(scale=1):
                max_revisions = gr.Slider(
                    label="Nombre de revisions",
                    minimum=0,
                    maximum=5,
                    step=1,
                    value=2,
                )
                run_button = gr.Button("Generer", variant="primary")

        status = gr.Textbox(label="Statut", interactive=False)
        draft = gr.Textbox(label="Dissertation finale", lines=18, interactive=False)

        with gr.Accordion("Details", open=False):
            plan = gr.Textbox(label="Plan", lines=10, interactive=False)
            critique = gr.Textbox(label="Derniere critique", lines=10, interactive=False)

        run_button.click(
            write_essay,
            inputs=[topic, max_revisions, openai_api_key, tavily_api_key],
            outputs=[status, plan, critique, draft],
        )

    demo.queue().launch(server_port=port)


def main() -> None:
    args = parse_args()
    if args.gui:
        launch_gui(model_name=args.model, port=args.port)
        return

    task = " ".join(args.topic).strip()
    if not task:
        task = input("Essay topic: ").strip()

    agent = EssayWriterAgent(model_name=args.model)
    final_state = agent.run(
        task=task,
        max_revisions=args.max_revisions,
        thread_id=args.thread_id,
    )

    print("\n=== FINAL DRAFT ===")
    print(final_state.get("draft", "No draft generated."))


if __name__ == "__main__":
    main()
