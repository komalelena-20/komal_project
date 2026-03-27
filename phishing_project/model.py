import os
import pandas as pd
import numpy as np
import re
import joblib
from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.utils import resample
from scipy.sparse import hstack

# ================= LOAD DATA =================
df = pd.read_csv("Phishing/phishing_url_dataset_unique.csv")

df = df[['url', 'label']]
df.dropna(inplace=True)

# ================= BALANCE DATASET =================
df_safe = df[df['label'] == 0]
df_phish = df[df['label'] == 1]

df_safe_down = resample(
    df_safe,
    replace=False,
    n_samples=len(df_phish),
    random_state=42
)

df = pd.concat([df_safe_down, df_phish])

# ================= FEATURE ENGINEERING =================
def extract_features(url):
    features = []
    
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()

    full_url = domain + path

    # Basic URL features
    features.append(len(full_url))  # URL length
    features.append(domain.count('.'))  # subdomain count
    features.append(1 if '-' in domain else 0)  # hyphen in domain
    features.append(1 if any(char.isdigit() for char in domain) else 0)  # numbers in domain
    features.append(len(domain))  # domain length
    features.append(len(path))  # path length
    
    # Suspicious keywords
    suspicious_words = ["login","verify","update","bank","secure","account","free","bonus","cashback"]
    features.extend([1 if word in full_url else 0 for word in suspicious_words])

    # Suspicious TLD
    features.append(1 if domain.endswith((".xyz",".top",".tk",".ml",".ga",".cf")) else 0)

    return features


# ================= TF-IDF =================
vectorizer = TfidfVectorizer(
    max_features=3000,
    ngram_range=(1,2),
    stop_words='english'
)

X_text = vectorizer.fit_transform(df['url'])

X_manual = np.array([extract_features(url) for url in df['url']])

X = hstack([X_text, X_manual])
y = df['label']

# ================= TRAIN TEST SPLIT =================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ================= MODEL =================
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=25,
    class_weight='balanced',
    random_state=42
)

model.fit(X_train, y_train)

# ================= EVALUATION =================
y_pred = model.predict(X_test)

print("\nModel Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# ================= SAVE =================
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\nModel and Vectorizer saved successfully.")

# ================= TEST LOOP =================
while True:
    url = input("\nEnter URL (or type exit): ")
    if url.lower() == "exit":
        break
    
    text_features = vectorizer.transform([url])
    manual_features = np.array([extract_features(url)])
    
    final_features = hstack([text_features, manual_features])
    
    prediction = model.predict(final_features)[0]
    confidence = model.predict_proba(final_features)[0][prediction] * 100
    
    print(f"Confidence: {confidence:.2f}%")
    
    if prediction == 1:
        print("⚠️ Phishing URL")
    else:
        print("✅ Safe URL")