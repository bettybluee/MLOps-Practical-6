import pandas as pd, os, sqlite3
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

class Classifier:
    def __init__(self, data_file="data/processed/books_clean.csv", db_file="data/books.db"):
        self.data_file = data_file
        self.db_file = db_file
        os.makedirs("logs", exist_ok=True)

    def load_data(self, source="csv"):
        if source == "csv":
            df = pd.read_csv(self.data_file)
        elif source == "sqlite":
            conn = sqlite3.connect(self.db_file)
            df = pd.read_sql("SELECT * FROM books;", conn)
            conn.close()
        else:
            raise ValueError("source must be 'csv' or 'sqlite'")
        print(f"Loaded {len(df)} rows for classification")
        return df

    def preprocess(self, df):
        X_train, X_test, y_train, y_test = train_test_split(
            df["title"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
        )
        vec = TfidfVectorizer()
        X_train_vec = vec.fit_transform(X_train)
        X_test_vec = vec.transform(X_test)
        return X_train_vec, X_test_vec, y_train, y_test, vec

    def train_and_evaluate(self, X_train_vec, X_test_vec, y_train, y_test, classifier_type="logistic"):
        if classifier_type == "logistic":
            clf = LogisticRegression(max_iter=1000)
        elif classifier_type == "nb":
            clf = MultinomialNB()
        else:
            raise ValueError("classifier_type must be 'logistic' or 'nb'")
        
        clf.fit(X_train_vec, y_train)
        y_pred = clf.predict(X_test_vec)
        acc = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {acc:.3f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))

        # Save metrics
        pd.DataFrame([{"accuracy": acc}]).to_csv("logs/metrics.csv", index=False)
        print("Metrics saved to logs/metrics.csv")

        return clf

if __name__ == "__main__":
    classifier = Classifier()
    df = classifier.load_data(source="csv")          # 또는 source="sqlite"
    X_train_vec, X_test_vec, y_train, y_test, vec = classifier.preprocess(df)
    clf = classifier.train_and_evaluate(
        X_train_vec, X_test_vec, y_train, y_test, classifier_type="logistic"
    )

    # --- 7. save model + vectorizer ---
    import joblib
    import os

    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, "models/model.pkl")
    joblib.dump(vec, "models/vectorizer.pkl")

    print("Model and vectorizer saved in 'models/'")
