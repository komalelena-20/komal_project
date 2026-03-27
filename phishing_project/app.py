from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    confidence = None

    if request.method == "POST":
        url = request.form["url"]

        vector = vectorizer.transform([url])

        pred = model.predict(vector)[0]
        prob = model.predict_proba(vector)[0]

        confidence = round(np.max(prob) * 100, 2)

        if pred == 1:
            prediction = "⚠️ Phishing Website"
        else:
            prediction = "✅ Safe Website"

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence
    )

if __name__ == "__main__":
    app.run(debug=True)