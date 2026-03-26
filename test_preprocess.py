from mood_analyzer import MoodAnalyzer

analyzer = MoodAnalyzer()
print('Testing preprocess:')
test_texts = [
    'Hello!!!',
    'I love this 😊',
    'So excited!!! 🎉',
    'No cap 💀',
    'Feeling kinda meh... 🥲',
    'This is fine :('
]

for text in test_texts:
    tokens = analyzer.preprocess(text)
    print(f'Input: "{text}" -> Tokens: {tokens}')
