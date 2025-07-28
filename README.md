# Fraud Message Detection

An AI-powered Flask application that classifies text messages as **fraudulent** or **safe**. The project includes:

- A **text classification pipeline** (TF‑IDF + Logistic Regression) saved as `fraud_pipeline.joblib`.
- A simple **Flask** backend with two endpoints:
  - `GET /` — serves the web interface (`index.html`).
  - `POST /detect` — accepts JSON `{"message": "..."}` and returns a JSON label.
- **CORS** enabled for cross-origin requests.
- Sample and augmented datasets in CSV format.

---

## 📦 Project Structure

```
├── app.py                   # Flask application
├── fraud_pipeline.joblib    # Serialized ML pipeline
├── templates/
│   └── index.html           # Front-end UI
├── static/                  # Static assets (images)
├── dataset/                 # Raw and augmented CSV data
│   ├── FMDS.csv
├── requirements.txt         # Python dependencies
├── .gitignore               # Ignored files/folders
└── README.md                # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/ZahedShaikh08/Fraud-Detection-System
```

### 2. Set up a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare the model

If you already have `fraud_pipeline.joblib`, skip this. Otherwise, train the pipeline:

```bash
python train_model.py  # script to train & save the joblib
```

### 5. Run the application

```bash
python app.py
```

The server will start on port **5000** by default. Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## 📡 API Usage

### Detect Fraudulent Messages

**Endpoint**: `POST /detect`

**Request**:

```json
{
  "message": "Your bank account is at risk. Click here."
}
```

**Response**:

```json
{
  "result": "Fraudulent"  // or "Non-Fraudulent"
}
```

### Health Check (optional)

If implemented, `GET /ping` returns `{ "status": "API is live" }`.

---

## 🛠 Development

- **Linting**: `flake8`
- **Testing**: Add your own `pytest` suites
- **Model updates**: modify `train_pipeline.py` and regenerate `fraud_pipeline.joblib`

---

## 🤝 Contributing

Feel free to submit issues or pull requests. Follow the standard GitHub flow:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/xyz`)
3. Commit your changes
4. Submit a Pull Request

---

## 📄 License

This project is released under the MIT License. See `LICENSE` for details.
