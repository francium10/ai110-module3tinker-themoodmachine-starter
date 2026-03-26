# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

from typing import List, Dict, Tuple, Optional
import re

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        Improvements implemented:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Removes punctuation (except emojis)
          - Handles simple emojis separately (":)", ":-(", "🥲", "😂", etc.)
          - Normalizes repeated characters ("soooo" -> "soo")
          - Splits on spaces
          - Additional: Handles contractions by splitting them (e.g., "don't" -> ["don", "t"])
        """
        # Strip whitespace and lowercase
        cleaned = text.strip().lower()

        # Normalize repeated characters (more than 2 repeats -> 2)
        cleaned = re.sub(r'(.)\1{2,}', r'\1\1', cleaned)

        # Remove punctuation but keep emojis
        # Emojis are typically Unicode characters, so we'll split and filter
        # For simplicity, we'll use a regex to remove common punctuation
        cleaned = re.sub(
            r'[^\w\s\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', '', cleaned)

        # Split on spaces
        tokens = cleaned.split()

        # Handle simple text emojis by keeping them as is
        # For complex emojis, they should already be preserved by the regex above

        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        Improvements implemented:
          - Basic scoring: +1 for positive words, -1 for negative words
          - Negation handling: flips polarity when negation precedes sentiment words
          - Emoji scoring: strong signals for emojis (😊=+2, 💀=-2, ❤️=+2, etc.)
          - Contraction handling: recognizes "dont", "cant", "wont" as negations
        """
        tokens = self.preprocess(text)
        score = 0

        # Define negation words and emoji scores
        negations = {"not", "never", "no", "dont", "cant",
                     "wont", "isnt", "arent", "wasnt", "werent"}
        emoji_scores = {
            "😊": 2, "😀": 2, "😄": 2, "😃": 2, "😁": 2, "🥰": 2, "😍": 2,
            "❤️": 2, "💖": 2, "💕": 2, "💗": 2, "💓": 2, "💞": 2, "💘": 2,
            "💀": -2, "😭": -2, "😢": -2, "😞": -2, "😔": -2, "😟": -2, "😕": -2,
            "🥲": -1, "🙃": -1, "😅": 1, "😂": 1, "🤣": 1, "😉": 1, "😎": 1,
            "🎉": 2, "💯": 1, "🔥": 1, "👍": 1, "👎": -1, "❤️‍🩹": -1
        }

        # Process tokens with negation awareness
        i = 0
        while i < len(tokens):
            token = tokens[i]
            multiplier = 1  # Default polarity

            # Check for negation in current or previous token
            if token in negations or (i > 0 and tokens[i-1] in negations):
                multiplier = -1

            # Score based on word lists
            if token in self.positive_words:
                score += 1 * multiplier
            elif token in self.negative_words:
                score -= 1 * multiplier

            # Score emojis
            if token in emoji_scores:
                score += emoji_scores[token]

            i += 1

        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        Current mapping:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        TODO: You can adjust this mapping if it makes sense for your model.
        For example:
          - Use different thresholds (for example score >= 2 to be "positive")
          - Add a "mixed" label for scores close to zero
        Just remember that whatever labels you return should match the labels
        you use in TRUE_LABELS in dataset.py if you care about accuracy.
        """
        score = self.score_text(text)

        if score > 0:
            return "positive"
        elif score < 0:
            return "negative"
        else:
            return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0

        for token in tokens:
            if token in self.positive_words:
                positive_hits.append(token)
                score += 1
            if token in self.negative_words:
                negative_hits.append(token)
                score -= 1

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
