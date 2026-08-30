"""Tests for warehouse eval dataset."""

from trace_learning.eval.dataset import MIN_TOOL_CALLS, EvalDataset, TARGET_QUESTION_COUNT


def test_dataset_has_60_questions():
    dataset = EvalDataset.load()
    assert len(dataset.questions) == TARGET_QUESTION_COUNT


def test_all_questions_require_min_tool_calls():
    dataset = EvalDataset.load()
    for q in dataset.questions:
        assert len(q.expected_tool_calls) >= MIN_TOOL_CALLS, f"{q.id} needs {MIN_TOOL_CALLS}+ tools"


def test_all_questions_use_four_tools():
    dataset = EvalDataset.load()
    counts = {len(q.expected_tool_calls) for q in dataset.questions}
    assert counts == {4}


def test_templates_loaded():
    dataset = EvalDataset.load()
    assert len(dataset.templates) == 15


def test_parameterized_overdue_picks():
    dataset = EvalDataset.load()
    instances = dataset.by_template("overdue-picks")
    assert len(instances) == 4
    dates = {q.params["as_of_date"] for q in instances}
    assert len(dates) == 4


def test_coverage_report_tool_stats():
    dataset = EvalDataset.load()
    report = dataset.coverage_report()
    assert report["avg_tool_calls"] == 4.0
    assert report["min_tool_calls"] == 4
    assert report["by_category"]["outbound"] == 20


def test_all_questions_have_template_id():
    dataset = EvalDataset.load()
    for q in dataset.questions:
        assert q.template_id
        assert dataset.get_template(q.template_id) is not None
