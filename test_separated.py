from mood_analyzer import MoodAnalyzer

analyzer = MoodAnalyzer()

# Test the separated logic
test_cases = [
    ('I love this class', 'positive'),
    ('Today was a terrible day', 'negative'),
    ('This is fine', 'neutral'),
    ('Feeling tired but kind of hopeful', 'mixed'),
    ('So excited!!! 🎉', 'positive'),
    ('No cap 💀', 'negative'),
    ('I do not love this class', 'negative'),
    ('Lowkey stressed but highkey proud', 'mixed'),
    ('Got a promotion but lost my wallet', 'mixed'),
]

print('Testing separated scoring and labeling logic:')
print('=' * 50)

for text, expected in test_cases:
    score, has_pos, has_neg = analyzer.score_text(text)
    predicted = analyzer.predict_label(text)
    status = '✓' if predicted == expected else '✗'
    print(f'{status} "{text}"')
    print(f'    Score: {score}, Has Pos: {has_pos}, Has Neg: {has_neg}')
    print(f'    Expected: {expected}, Got: {predicted}')
    print()
