from datetime import datetime

import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.services.analytics import AnalyticsService
from src.schemas import NoteAnalytics
from src.database.models import Note


@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)


@pytest.fixture
def analytics_service(mock_db_session):
    return AnalyticsService(db=mock_db_session)


def test_get_notes_analytics_empty(analytics_service):

    analytics_service.db.query.return_value.all.return_value = []

    result = analytics_service.get_notes_analytics()

    assert isinstance(result, NoteAnalytics)
    assert result.total_word_count == 0
    assert result.average_note_length == 0.0
    assert result.most_common_words == []
    assert result.longest_notes == []
    assert result.shortest_notes == []


def test_get_notes_analytics_with_notes(analytics_service):

    note1 = Note(
        id=1,
        title="Test",
        content="This is a test note.",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        user_id=1
    )
    note2 = Note(
        id=2,
        title="Test1",
        content="Another test note for analysis.",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        user_id=1
    )
    analytics_service.db.query.return_value.all.return_value = [note1, note2]

    result = analytics_service.get_notes_analytics()
    assert isinstance(result, NoteAnalytics)
    assert result.total_word_count > 0
    assert result.average_note_length > 0
    assert len(result.longest_notes) <= 3
    assert len(result.shortest_notes) <= 3


def test_tokenize_and_clean(analytics_service):

    text = "This is a test, with punctuation!"
    expected_tokens = [
        "test",
        "punctuation",
    ]

    tokens = analytics_service._tokenize_and_clean(text)

    assert sorted(tokens) == sorted(expected_tokens)


def test_get_most_common_words(analytics_service):

    words = ["test", "test", "example", "example", "example"]
    expected_common = [("example", 3), ("test", 2)]

    common_words = analytics_service._get_most_common_words(words)

    assert sorted(common_words) == sorted(expected_common)


if __name__ == "__main__":
    pytest.main()
