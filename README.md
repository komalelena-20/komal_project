**AI Powered Phishing URL Detection System** 
 Overview :

This project is a Machine Learning-based web application that detects whether a given URL is Safe (Legitimate) or Phishing (Malicious).

It uses a trained classification model along with TF-IDF vectorization to analyze URL patterns and provide real-time predictions through a user-friendly Flask web interface.  
**Features**
* Detects phishing and safe URLs instantly
* Machine Learning based prediction
* Web interface using Flask
* Real-time results with confidence score
 * Simple and clean UI
**Technologies Used**
Python
Pandas
Scikit-learn
TF-IDF Vectorizer
Flask
HTML & CSS
**Dataset**
File: phishing_url_dataset_unique.csv
Contains labeled URLs:
0 → Safe
1 → Phishing
**How It Works**
Dataset is loaded and preprocessed
URLs are converted into numerical features using TF-IDF
A machine learning model is trained on the dataset
Model and vectorizer are saved using .pkl files
Flask app loads the model
User enters a URL
Model predicts whether it is Safe or Phishing
**Example Results**
URL	Prediction
https://www.google.com
	✅ Safe
https://www.wikipedia.org
	✅ Safe
http://paypal-login-security-update.com
	⚠️ Phishing
http://verify-your-amazon-account-now.net
	⚠️ Phishing
**Project Structure**
phishing_project/
│── app.py
│── train_model.py
│── model.pkl
│── vectorizer.pkl
│── Phishing/
│   └── phishing_url_dataset_unique.csv
│── templates/
│   └── index.html
│── static/
│   └── style.css
**How to Run**
1. Install dependencies
pip install pandas scikit-learn flask
2. Train the model
python train_model.py
3. Run the app
python app.py
4. Open in browser
http://127.0.0.1:5000

**Future Improvements**
Improve model accuracy
Add probability visualization
Deploy online
Convert into browser extension
Use deep learning models

**Author**

Komal

**Acknowledgement**

This project is developed as part of learning Machine Learning and Cybersecurity concepts.

