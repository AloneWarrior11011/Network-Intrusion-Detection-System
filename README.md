
# SQLShield-NIDS

SQLShield-NIDS is an intelligent Network Intrusion Detection System (NIDS) designed to detect and prevent SQL injection attacks in real-time. By leveraging machine learning techniques, this project aims to proactively identify malicious SQL queries and protect databases from one of the most prevalent forms of cyberattacks.


---

## 🚀 Features

- **Machine Learning-Based Detection:** Utilizes a Random Forest Classifier trained on real and synthetic SQL queries to distinguish between normal and malicious entries.
- **Automatic Model Training & Evaluation:** Includes scripts to preprocess data, train models, evaluate performance, and save the trained model and vectorizer for deployment.
- **API Integration:** Can be integrated with applications via a Flask API for real-time prediction and alerting.
- **High Accuracy:** Achieves perfect precision, recall, and F1-score on test datasets (see below).
- **Customizable & Extendable:** Easily retrain the model with new data or adapt it for different types of attacks.

---

## 📊 Model Performance

```
           precision    recall  f1-score   support

        0       1.00      1.00      1.00        41
        1       1.00      1.00      1.00        35

 accuracy                           1.00        76
macro avg       1.00      1.00      1.00        76
weighted avg    1.00      1.00      1.00        76
```

---

## 🛠️ How It Works

1. **Data Preprocessing:** Loads labeled log entries containing both benign and SQL injection queries.
2. **Feature Extraction:** Applies TF-IDF vectorization to convert queries into numerical features.
3. **Model Training:** Trains a Random Forest classifier to distinguish between benign and malicious SQL activity.
4. **Evaluation:** Prints accuracy, confusion matrix, and classification report.
5. **Prediction:** The trained model can classify new SQL queries as normal or malicious.

---

## 📦 Project Structure

```
.
├── sql_model_code_file.ipynb       # Main notebook for model building and testing
├── sql_injection_model_file.ipynb  # Additional experimentation notebook
├── log_entries.csv                 # Input data (not included here)
├── sql_injection_model.joblib      # Saved ML model (generated after training)
├── vectorizer.joblib               # Saved vectorizer (generated after training)
├── myenv/                          # Python virtual environment
└── README.md                       # Project documentation
```

---

## 📥 Getting Started

### Prerequisites

- Python 3.11+
- pip (Python package installer)
- [scikit-learn](https://scikit-learn.org/), pandas, numpy, Flask, seaborn, matplotlib, joblib

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KunalWadhai/SQLShield-NIDS.git
   cd SQLShield-NIDS
   ```

2. **(Optional) Create and activate a virtual environment:**
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the model:**
   - Open `sql_model_code_file.ipynb` in Jupyter Notebook and run all cells.
   - This will create `sql_injection_model.joblib` and `vectorizer.joblib`.

---

## 🧑‍💻 Usage

### Predicting New Queries

You can load the trained model and vectorizer to predict whether a new SQL query is malicious or not:

```python
import joblib
model = joblib.load('sql_injection_model.joblib')
vectorizer = joblib.load('vectorizer.joblib')

input_data = ["SELECT * FROM users WHERE username='admin' OR 1=1 --"]
input_vector = vectorizer.transform(input_data)
prediction = model.predict(input_vector)
print("Malicious" if prediction[0] == 1 else "Normal")
```

### Example Predictions

- `"456 Elm Street, Los Angeles, CA"` → **Normal**
- `"' OR (SELECT CASE WHEN (1=1) THEN 1 ELSE 0 END) --"` → **Malicious**
- `"OR 1=1"` → **Malicious**

---

## 🧪 Example SQL Injection Strings Detected

- `' OR '1'='1' --`
- `' UNION SELECT NULL, username, password FROM users --`
- `' AND SLEEP(10) --`
- `' OR IF(1=1, SLEEP(5), 0) --`

---

## 🎥 Demo



<h3>Working Demo Video</h3>

[![Watch the demo](https://img.youtube.com/vi/3pptvOQN_vE/0.jpg)](https://www.youtube.com/watch?v=3pptvOQN_vE)


