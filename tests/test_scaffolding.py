"""Tests for eval dataset and workflow graph."""

from trace_learning.eval.dataset import EvalDataset, QuestionCategory, TARGET_QUESTION_COUNT


def test_dataset_has_60_questions():
    dataset = EvalDataset.load()
    assert len(dataset.questions) == TARGET_QUESTION_COUNT


def test_all_questions_are_multi_tool():
    dataset = EvalDataset.load()
    for q in dataset.questions:
        assert len(q.expected_tool_calls) >= 2, f"{q.id} must require 2+ tools"


def test_templates_loaded():
    dataset = EvalDataset.load()
    assert len(dataset.templates) == 15


def test_parameterized_template_instances():
    dataset = EvalDataset.load()
    late = dataset.by_template("late-orders")
    assert len(late) == 4
    dates = {q.params["as_of_date"] for q in late}
    assert len(dates) == 4


def test_category_balance():
    dataset = EvalDataset.load()
    report = dataset.coverage_report()
    assert report["by_category"]["fulfillment"] == 20
    assert report["by_category"]["parts_trace"] == 16
    assert report["by_category"]["policy"] == 12
    assert report["by_category"]["support"] == 12


def test_part_history_template_variants():
    dataset = EvalDataset.load()
    parts = {q.params["part_number"] for q in dataset.by_template("part-history")}
    assert parts == {"PN-4421", "PN-7782", "PN-3309", "PN-9901"}


def test_all_questions_have_template_id():
    dataset = EvalDataset.load()
    for q in dataset.questions:
        assert q.template_id
        assert dataset.get_template(q.template_id) is not None
