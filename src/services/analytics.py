from collections import Counter
from typing import List, Tuple

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sqlalchemy.orm import Session

from src.database import models
from src.schemas import NoteAnalytics

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("punkt_tab")


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
        self.stop_words = set(stopwords.words("english"))

    def get_notes_analytics(self):
        notes = self.db.query(models.Note).all()

        if not notes:
            return NoteAnalytics(
                total_word_count=0,
                average_note_length=0.0,
                most_common_words=[],
                longest_notes=[],
                shortest_notes=[],
            )

        note_lengths = []
        all_words = []

        for note in notes:
            words = self._tokenize_and_clean(note.content)
            note_lengths.append((len(words), note))
            all_words.extend(words)

        note_lengths.sort(key=lambda x: x[0])

        shortest_notes = [note for _, note in note_lengths[:3]]
        longest_notes = [note for _, note in reversed(note_lengths[-3:])]

        total_words = len(all_words)
        avg_length = total_words / len(notes) if notes else 0.0
        most_common = self._get_most_common_words(all_words)

        return NoteAnalytics(
            total_word_count=total_words,
            average_note_length=avg_length,
            most_common_words=most_common,
            longest_notes=longest_notes,
            shortest_notes=shortest_notes,
        )

    def _tokenize_and_clean(self, text: str) -> List[str]:
        tokens = word_tokenize(text.lower())
        return [
            word for word in tokens if word.isalnum() and word not in self.stop_words
        ]

    def _get_most_common_words(
        self, words: List[str], top_n: int = 10
    ) -> List[Tuple[str, int]]:
        word_counts = Counter(words)
        return word_counts.most_common(top_n)
