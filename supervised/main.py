from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from pipeline import df  # Import the DataFrame created in pipeline.py

# 1. Convert text labels to numbers (ham = 0, spam = 1)
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

# 2. Split the data (holding back 20% for the exam)
X_train, X_test, y_train, y_test = train_test_split(df['message'], df['label'], test_size=0.2, random_state=42)

# 3. Create the Professional Pipeline
spam_filter = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('ai_model', MultinomialNB())
])

# 4. Train the entire pipeline at once!
spam_filter.fit(X_train, y_train)

# 5. Take the Final Exam
predictions = spam_filter.predict(X_test)
print(f"Accuracy on hidden test messages: {accuracy_score(y_test, predictions) * 100:.2f}%")
