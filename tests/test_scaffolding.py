"""Tests for eval dataset and workflow graph."""

from trace_learning.eval.dataset import EvalDataset, QuestionCategory, TARGET_QUESTION_COUNT
from trace_learning.graph.store import WorkflowGraphStore


def test_dataset_has_60_questions():
    dataset = EvalDataset.load()
    assert len(dataset.questions) == TARGET_QUESTION_COUNT


def test_dataset_category_balance():
    dataset = EvalDataset.load()
    report = dataset.coverage_report()
    assert report["rag"] == 15
    assert report["mcp"] == 15
    assert report["builtin"] == 15
    assert report["multi_step"] == 15


def test_all_questions_have_expected_answers():
    dataset = EvalDataset.load()
    for q in dataset.questions:
        assert q.expected_answer, f"{q.id} missing expected_answer"


def test_workflow_graph_loads():
    store = WorkflowGraphStore()
    assert len(store.graphs) >= 1
    wf = store.get("wf-onboarding-check")
    assert wf is not None
    assert "mcp_read_file" in wf.tool_sequence()


def test_workflow_match():
    store = WorkflowGraphStore()
    matched = store.match("Tell me about onboarding for a new hire")
    assert matched is not None
    assert matched.id == "wf-onboarding-check"
