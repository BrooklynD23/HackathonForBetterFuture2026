"""Tests for the pipeline funnel visualization tab."""

import pandas as pd
import plotly.graph_objects as go
import pytest

from src.ui.pipeline_tab import (
    FUNNEL_STAGES,
    aggregate_funnel_stages,
    create_funnel_chart,
    load_pipeline_data,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_pipeline_csv(tmp_path: object) -> str:
    """Create a minimal pipeline CSV for testing."""
    csv_path = tmp_path / "pipeline_sample_data.csv"  # type: ignore[union-attr]
    csv_path.write_text(
        "event_name,speaker_name,match_score,rank,stage,stage_order\n"
        "Event A,Speaker 1,0.90,1,Attended,3\n"
        "Event A,Speaker 2,0.80,2,Contacted,1\n"
        "Event A,Speaker 3,0.70,3,Matched,0\n"
        "Event B,Speaker 1,0.85,1,Member Inquiry,4\n"
        "Event B,Speaker 2,0.75,2,Confirmed,2\n"
        "Event B,Speaker 3,0.65,3,Contacted,1\n"
    )
    return str(csv_path)


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Return a small pipeline DataFrame."""
    return pd.DataFrame({
        "event_name": ["E1", "E1", "E2", "E2", "E3"],
        "speaker_name": ["S1", "S2", "S1", "S2", "S1"],
        "match_score": [0.9, 0.8, 0.7, 0.6, 0.5],
        "rank": [1, 2, 1, 2, 1],
        "stage": ["Attended", "Contacted", "Matched", "Member Inquiry", "Confirmed"],
        "stage_order": [3, 1, 0, 4, 2],
    })


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestLoadPipelineData:
    def test_load_pipeline_data_from_csv(self, sample_pipeline_csv: str) -> None:
        df = load_pipeline_data(sample_pipeline_csv)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 6
        assert "stage" in df.columns
        assert "event_name" in df.columns

    def test_load_pipeline_data_missing_file(self, tmp_path: object) -> None:
        missing = str(tmp_path / "no_such_file.csv")  # type: ignore[union-attr]
        df = load_pipeline_data(missing)
        assert isinstance(df, pd.DataFrame)
        assert df.empty


class TestAggregateFunnelStages:
    def test_aggregate_funnel_stages_monotonically_decreasing(
        self, sample_df: pd.DataFrame
    ) -> None:
        stage_counts = aggregate_funnel_stages(sample_df)
        values = list(stage_counts.values())
        for i in range(len(values) - 1):
            assert values[i] >= values[i + 1], (
                f"Funnel not monotonically decreasing at index {i}: "
                f"{values[i]} < {values[i + 1]}"
            )

    def test_funnel_stages_correct_order(self, sample_df: pd.DataFrame) -> None:
        stage_counts = aggregate_funnel_stages(sample_df)
        stage_names = list(stage_counts.keys())
        expected = [
            "Discovered",
            "Matched",
            "Contacted",
            "Confirmed",
            "Attended",
            "Member Inquiry",
        ]
        assert stage_names == expected

    def test_funnel_stages_count_is_six(self, sample_df: pd.DataFrame) -> None:
        stage_counts = aggregate_funnel_stages(sample_df)
        assert len(stage_counts) == 6

    def test_discovered_equals_total_rows(self, sample_df: pd.DataFrame) -> None:
        stage_counts = aggregate_funnel_stages(sample_df)
        assert stage_counts["Discovered"] == len(sample_df)


class TestHoverData:
    def test_hover_data_includes_names(self, sample_df: pd.DataFrame) -> None:
        stage_counts = aggregate_funnel_stages(sample_df)
        fig = create_funnel_chart(sample_df, stage_counts)
        trace = fig.data[0]
        assert trace.hovertext is not None
        hover_str = str(trace.hovertext)
        # Speaker and event names should appear in hover tooltips
        assert any(
            name in hover_str
            for name in ["S1", "S2", "E1", "E2", "E3"]
        )


class TestEmptyData:
    def test_empty_data_handled_gracefully(self) -> None:
        empty_df = pd.DataFrame(
            columns=["event_name", "speaker_name", "match_score", "rank", "stage", "stage_order"]
        )
        stage_counts = aggregate_funnel_stages(empty_df)
        assert len(stage_counts) == 6
        assert all(v == 0 for v in stage_counts.values())

    def test_empty_data_chart_returns_figure(self) -> None:
        empty_df = pd.DataFrame(
            columns=["event_name", "speaker_name", "match_score", "rank", "stage", "stage_order"]
        )
        stage_counts = aggregate_funnel_stages(empty_df)
        fig = create_funnel_chart(empty_df, stage_counts)
        assert isinstance(fig, go.Figure)


class TestCreateFunnelChart:
    def test_create_funnel_chart_returns_figure(
        self, sample_df: pd.DataFrame
    ) -> None:
        stage_counts = aggregate_funnel_stages(sample_df)
        fig = create_funnel_chart(sample_df, stage_counts)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) >= 1

    def test_funnel_chart_has_correct_stage_labels(
        self, sample_df: pd.DataFrame
    ) -> None:
        stage_counts = aggregate_funnel_stages(sample_df)
        fig = create_funnel_chart(sample_df, stage_counts)
        trace = fig.data[0]
        expected_stages = list(FUNNEL_STAGES.keys())
        assert list(trace.y) == expected_stages
