from mood_analyzer import MoodAnalyzer

analyzer = MoodAnalyzer()

# Test cases for score_text method
test_cases = [
    ("I love this class", 1, "Basic positive"),
    ("I do not love this class", -1, "Negation flips positive"),
    ("Today was a terrible day", -1, "Basic negative"),
    ("Never been happier", 1, "Negation doesn't affect positive"),
    ("So excited!!! 🎉", 3, "Word + emoji bonus"),
    ("No cap 💀", -2, "Negative word + emoji"),
    ("Feeling tired but kind of hopeful", 0, "Mixed cancels out"),
    ("This is fine", 0, "Neutral"),
    ("I absolutely love getting stuck in traffic", 1, "Sarcasm not detected"),
]

print("Testing score_text method:")
print("=" * 50)

for text, expected_score, description in test_cases:
    actual_score = analyzer.score_text(text)
    status = "✓" if actual_score == expected_score else "✗"
    print(f"{status} {description}")
    print(f"  Text: '{text}'")
    print(f"  Expected: {expected_score}, Got: {actual_score}")
    print()
