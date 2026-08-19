# 🏠 House Price Prediction App

An end-to-end machine learning project that predicts Indian house prices using property features. Includes a Jupyter notebook for EDA & model training, a FastAPI backend serving predictions, and a React frontend for user interaction.

---

## Architecture

```
┌────────────┐       POST /predict       ┌────────────────┐      .predict()     ┌──────────────┐
│   React    │  ──────────────────────►  │  FastAPI       │  ─────────────────►  │  Scikit-learn │
│  Frontend  │  ◄──────────────────────  │  Backend       │  ◄─────────────────  │  Pipeline     │
│  (Vite)    │    { predicted_price }     │  (Uvicorn)     │    numpy array       │  (RandomForest)│
└────────────┘                           └────────────────┘                      └──────────────┘
     :5173                                    :8000                              house_price.pkl
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Notebook** | Python 3.13, pandas, scikit-learn, matplotlib, seaborn |
| **Backend** | FastAPI, Uvicorn, Pydantic, joblib |
| **Frontend** | React 19, TypeScript, Vite 8, React Router 7 |
| **ML Model** | RandomForestRegressor (scikit-learn pipeline with ColumnTransformer) |

---

## Project Structure

```
house-price-project/
├── notebooks/
│   ├── house_price_model.ipynb   # EDA, cleaning, model training & export
│   └── data/                     # Raw CSV (not committed — see below)
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── api/routes/
│   │   │   └── prediction.py     # /health & /predict endpoints
│   │   ├── schemas/
│   │   │   └── prediction.py     # Pydantic request/response models
│   │   ├── services/
│   │   │   ├── inference.py      # Model loading & prediction
│   │   │   └── preprocessing.py  # Feature engineering for requests
│   │   └── core/
│   │       └── config.py         # Settings via pydantic-settings
│   ├── models/                   # Model artifacts (see setup below)
│   │   └── locations.json        # Valid location list
│   ├── tests/
│   │   └── test_prediction.py    # pytest tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.tsx               # React Router setup
│   │   ├── pages/                # HomePage, ResultPage, NotFoundPage
│   │   ├── components/           # PredictionForm
│   │   ├── api/                  # API client
│   │   ├── types/                # TypeScript interfaces
│   │   └── data/                 # locations.json for dropdown
│   ├── package.json
│   ├── vite.config.ts
│   └── .env.example
├── models/                       # Top-level model artifact placeholder
├── .gitignore
└── README.md
```

---

## Dataset

**Source**: [House Prices in India](https://www.kaggle.com/datasets/juhibhojani/house-price) on Kaggle

The raw CSV (`~100 MB`, 187 531 rows × 21 columns) is **not committed** to this repo.

### Download Instructions

1. Install the Kaggle CLI (already in `requirements.txt`):
   ```bash
   pip install kaggle
   ```
2. Place your [Kaggle API token](https://www.kaggle.com/settings) at `~/.kaggle/kaggle.json`.
3. Download the dataset:
   ```bash
   mkdir -p notebooks/data
   kaggle datasets download -d mohamedafsal007/house-prices-in-india -p notebooks/data --unzip
   ```
   The notebook expects the file at `notebooks/data/house_prices.csv`.

---

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm 9+

### 1. Model File (required before running the backend)

The trained model (`house_price.pkl`, ~406 MB) is **not committed** because it exceeds GitHub's 50 MB limit. You must obtain it before starting the backend.

**Option A — Re-train from the notebook:**
1. Download the dataset (see [Dataset](#dataset) above).
2. Install notebook dependencies:
   ```bash
   cd backend
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   cd ..
   ```
3. Open `notebooks/house_price_model.ipynb` and run all cells (Kernel → Restart & Run All).
4. Copy the exported artifacts into the backend:
   ```bash
   # macOS / Linux
   cp notebooks/house_price.pkl backend/models/house_price.pkl
   cp notebooks/locations.json  backend/models/locations.json

   # Windows (PowerShell)
   Copy-Item notebooks\house_price.pkl backend\models\house_price.pkl
   Copy-Item notebooks\locations.json  backend\models\locations.json
   ```

**Option B — Download a pre-built model** (if hosted):
```bash
curl -L -o backend/models/house_price.pkl <YOUR_MODEL_URL>
```

### 2. Backend

```bash
cd backend

# Create virtual environment (skip if already created in step 1)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# Install dependencies (skip if already installed in step 1)
pip install -r requirements.txt

# Configure environment
cp .env.example .env          # macOS / Linux
copy .env.example .env        # Windows

# Run tests
pytest tests -v

# Start the server
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env          # macOS / Linux
copy .env.example .env        # Windows

# Start dev server
npm run dev

# Production build
npm run build
```

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Default | Description |
|---|---|---|
| `MODEL_PATH` | `models/house_price.pkl` | Path to the trained model file |
| `LOCATIONS_PATH` | `models/locations.json` | Path to valid locations JSON |

### Frontend (`frontend/.env`)

| Variable | Default | Description |
|---|---|---|
| `VITE_API_BASE_URL` | `http://localhost:8000` | Backend API base URL |

---

## API Reference

### `GET /health`

Health check endpoint.

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{"status": "ok"}
```

### `POST /predict`

Predict house price for given property features.

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "location": "thane",
    "area_sqft": 1000,
    "floor_num": 5,
    "bathroom": 2,
    "balcony": 1,
    "parking": 1,
    "furnishing": "Semi-Furnished",
    "transaction": "Resale",
    "ownership": "Freehold",
    "facing": "East",
    "status": "Ready to Move"
  }'
```

**Response:**
```json
{"predicted_price": 4523019.5}
```

**Request Body:**

| Field | Type | Description |
|---|---|---|
| `location` | string | Property location (e.g. `"thane"`, `"mumbai"`) |
| `area_sqft` | float | Carpet / super area in sq ft |
| `floor_num` | int | Floor number |
| `bathroom` | int | Number of bathrooms |
| `balcony` | int | Number of balconies |
| `parking` | int | Number of parking spaces |
| `furnishing` | string | `"Furnished"` / `"Semi-Furnished"` / `"Unfurnished"` |
| `transaction` | string | `"New Property"` / `"Resale"` |
| `ownership` | string | `"Freehold"` / `"Leasehold"` / `"Co-operative Society"` / `"Power of Attorney"` |
| `facing` | string | `"East"` / `"West"` / `"North"` / `"South"` / `"North-East"` / etc. |
| `status` | string | `"Ready to Move"` / `"Under Construction"` |

---

## Model Performance

**Best model: RandomForest (raw target)**

| Metric | Value |
|--------|-------|
| **MAE** | ₹ 9,80,945 |
| **RMSE** | ₹ 41,77,399 |
| **R²** | 0.8867 |
| **5-fold CV R²** | 0.4799 ± 0.2794 |

### All Models Compared

| Model | MAE | RMSE | R² |
|-------|-----|------|----|
| LinearRegression (raw) | 4,328,764 | 7,810,284 | 0.6041 |
| LinearRegression (log) | 4,119,116 | 15,794,340 | −0.6192 |
| **RandomForest (raw)** | **980,945** | **4,177,399** | **0.8867** |
| RandomForest (log) | 963,055 | 4,241,550 | 0.8832 |
| GradientBoosting (raw) | 2,088,845 | 4,516,095 | 0.8676 |
| GradientBoosting (log) | 2,122,286 | 5,469,723 | 0.8058 |

---

## Screenshots

_TODO: add screenshots of the running app._

---

## License

This project is for educational purposes.
