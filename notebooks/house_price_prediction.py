# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)

# %%
df = pd.read_csv("data/house_prices.csv")
print("Shape:", df.shape)

# %%
df.columns.tolist()

# %%
df.head()

# %%
df.info()

# %%
df.describe()

# %%
missing_pct = df.isna().mean().sort_values(ascending=False) * 100
print("% missing per column:\n")
print(missing_pct.round(2).to_string())

# %%
def parse_amount(x):
    if not isinstance(x, str):
        return None
    x = x.strip().lower()
    try:
        if "lac" in x:
            return float(x.replace("lac", "").strip()) * 1e5
        if "cr" in x:
            return float(x.replace("cr", "").strip()) * 1e7
        return float(x.replace(",", ""))
    except ValueError:
        return None

df["price_clean"] = df["Amount(in rupees)"].apply(parse_amount)
print(f"Rows with a usable price: {df['price_clean'].notna().sum():,} / {len(df):,}")

# %%
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df["price_clean"].dropna(), bins=100, color="#4c72b0", edgecolor="white")
axes[0].set_title("Price Distribution (raw)")
axes[0].set_xlabel("Price (₹)")
axes[0].set_ylabel("Count")

sns.histplot(df["price_clean"].dropna(), log_scale=True, bins=80, ax=axes[1],
             color="#55a868", edgecolor="white")
axes[1].set_title("Price Distribution (log scale)")
axes[1].set_xlabel("Price (₹)")

plt.tight_layout()
plt.show()

# %%
def parse_area(x):
    if not isinstance(x, str):
        return np.nan
    x = x.strip().lower()
    try:
        if "sqm" in x:
            return float(x.replace("sqm", "").strip()) * 10.764
        if "sqft" in x:
            return float(x.replace("sqft", "").strip())
        return float(x.replace(",", ""))
    except ValueError:
        return np.nan

df["carpet_area_sqft"] = df["Carpet Area"].apply(parse_area)

mask = df["price_clean"].notna() & df["carpet_area_sqft"].notna()
sample = df.loc[mask].sample(n=min(5000, mask.sum()), random_state=42)

plt.figure(figsize=(10, 6))
plt.scatter(sample["carpet_area_sqft"], sample["price_clean"],
            alpha=0.3, s=10, color="#c44e52")
plt.xlabel("Carpet Area (sqft)")
plt.ylabel("Price (₹)")
plt.title("Price vs Carpet Area (sample of 5,000 listings)")
plt.ticklabel_format(style="plain", axis="y")
plt.tight_layout()
plt.show()

# %%
loc_price = (df.loc[df["price_clean"].notna()]
             .groupby("location")["price_clean"]
             .agg(["mean", "count"])
             .query("count >= 100")
             .nlargest(15, "mean"))

plt.figure(figsize=(12, 6))
plt.barh(loc_price.index[::-1], loc_price["mean"][::-1] / 1e7,
         color="#8172b2", edgecolor="white")
plt.xlabel("Average Price (₹ Cr)")
plt.title("Top-15 Locations by Average Price (min 100 listings)")
plt.tight_layout()
plt.show()

# %%
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

furn_data = df.loc[df["price_clean"].notna() & df["Furnishing"].notna()]
order = [o for o in ["Unfurnished", "Semi-Furnished", "Furnished"]
         if o in furn_data["Furnishing"].unique()]
sns.boxplot(data=furn_data, x="Furnishing", y="price_clean",
            order=order, ax=axes[0], palette="Set2", showfliers=False)
axes[0].set_ylabel("Price (₹)")
axes[0].set_title("Price by Furnishing Status")
axes[0].ticklabel_format(style="plain", axis="y")

df["bathroom_num"] = pd.to_numeric(df["Bathroom"], errors="coerce")
bath_data = df.loc[df["price_clean"].notna() & df["bathroom_num"].notna()]
bath_data = bath_data[bath_data["bathroom_num"].between(1, 6)]
sns.boxplot(data=bath_data, x="bathroom_num", y="price_clean",
            ax=axes[1], palette="Set3", showfliers=False)
axes[1].set_xlabel("Number of Bathrooms")
axes[1].set_ylabel("Price (₹)")
axes[1].set_title("Price by Number of Bathrooms")
axes[1].ticklabel_format(style="plain", axis="y")

plt.tight_layout()
plt.show()

# %%
print(f"Before: {len(df):,} rows")
df = df.dropna(subset=["price_clean"])
print(f"After: {len(df):,} rows")

# %%
df["super_area_sqft"] = df["Super Area"].apply(parse_area)

print("Carpet Area non-null:", df["carpet_area_sqft"].notna().sum())
print("Super Area  non-null:", df["super_area_sqft"].notna().sum())

df["area_sqft"] = df["carpet_area_sqft"].fillna(df["super_area_sqft"])
print("Combined    non-null:", df["area_sqft"].notna().sum())

# %%
def parse_floor(x):
    if not isinstance(x, str):
        return np.nan
    x = x.strip().lower()
    if "basement" in x:
        return -1
    if "ground" in x:
        return 0
    if "out of" in x:
        try:
            return int(x.split("out of")[0].strip())
        except ValueError:
            return np.nan
    try:
        return int(x)
    except ValueError:
        return np.nan

df["floor_num"] = df["Floor"].apply(parse_floor)
print("Floor parsed non-null:", df["floor_num"].notna().sum())
print(df["floor_num"].describe())

# %%
df["bathroom_num"] = pd.to_numeric(df["Bathroom"], errors="coerce")
df["balcony_num"] = pd.to_numeric(df["Balcony"], errors="coerce")

def parse_car_parking(x):
    if not isinstance(x, str):
        return np.nan
    total = 0
    for part in x.split(","):
        part = part.strip()
        try:
            total += int(part.split()[0])
        except (ValueError, IndexError):
            pass
    return total if total > 0 else np.nan

df["parking_num"] = df["Car Parking"].apply(parse_car_parking)

for col in ["bathroom_num", "balcony_num", "parking_num", "floor_num"]:
    median_val = df[col].median()
    df[col] = df[col].fillna(median_val)
    print(f"{col}: imputed missing with median = {median_val}")

# %%
TOP_N = 50

def reduce_cardinality(series, top_n=TOP_N):
    top = series.value_counts().nlargest(top_n).index
    return series.where(series.isin(top), other="other")

df["location_clean"] = reduce_cardinality(df["location"].fillna("other"))
df["society_clean"] = reduce_cardinality(df["Society"].fillna("other"))

print(f"location: {df['location'].nunique()} unique -> {df['location_clean'].nunique()} categories")
print(f"Society:  {df['Society'].nunique()} unique -> {df['society_clean'].nunique()} categories")

# %%
drop_cols = ["Index", "Title", "Description", "Dimensions", "Plot Area",
             "Amount(in rupees)", "Price (in rupees)",
             "Carpet Area", "Super Area", "Floor",
             "Bathroom", "Balcony", "Car Parking",
             "location", "Society"]

df = df.drop(columns=[c for c in drop_cols if c in df.columns])
print(f"Remaining columns ({len(df.columns)}):")
print(df.columns.tolist())

# %%
mask_area = df["area_sqft"].notna() & (df["area_sqft"] > 0)
df.loc[mask_area, "price_per_sqft"] = (
    df.loc[mask_area, "price_clean"] / df.loc[mask_area, "area_sqft"]
)

before = len(df)
low = df["price_per_sqft"].quantile(0.01)
high = df["price_per_sqft"].quantile(0.99)

df = df[
    df["price_per_sqft"].isna() |
    df["price_per_sqft"].between(low, high)
]
print(f"Outlier removal: {before:,} -> {len(df):,} rows (dropped {before - len(df):,})")
print(f"Price-per-sqft kept range: {low:,.0f} - {high:,.0f}")

df = df.drop(columns=["price_per_sqft"])

# %%
print(f"Final shape: {df.shape}")
print(f"\nColumn types:\n{df.dtypes}\n")
print(f"Remaining nulls:\n{df.isna().sum()}\n")
df.head()

# %%
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from sklearn.base import clone
import sklearn, joblib, json, time

print("scikit-learn version:", sklearn.__version__)

# %%
numeric_features = ["area_sqft", "floor_num", "bathroom_num", "balcony_num", "parking_num"]
categorical_features = ["location_clean", "Furnishing", "Transaction", "Ownership",
                         "facing", "Status"]

X = df[numeric_features + categorical_features].copy()
y = df["price_clean"].copy()

print(f"X shape: {X.shape}")
print(f"y shape: {y.shape}")
print(f"\ny stats:\n{y.describe()}")

# %%
preprocessor = ColumnTransformer([
    ("num", Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale",  StandardScaler()),
    ]), numeric_features),
    ("cat", Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ]), categorical_features),
])

# %%
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Train: {X_train.shape[0]:,}   Test: {X_test.shape[0]:,}")

# %%
regressors = {
    "LinearRegression":  LinearRegression(),
    "RandomForest":      RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
    "GradientBoosting":  GradientBoostingRegressor(n_estimators=100, learning_rate=0.1,
                                                    max_depth=5, random_state=42),
}

results = []

for name, reg in regressors.items():
    for use_log in [False, True]:
        label = f"{name} ({'log' if use_log else 'raw'})"
        print(f"\n{'='*60}")
        print(f"Training: {label}")

        pipe = Pipeline([("prep", clone(preprocessor)), ("reg", clone(reg))])

        yt = np.log1p(y_train) if use_log else y_train

        t0 = time.time()
        pipe.fit(X_train, yt)
        train_time = time.time() - t0

        preds = pipe.predict(X_test)
        if use_log:
            preds = np.expm1(preds)

        mae  = mean_absolute_error(y_test, preds)
        rmse = root_mean_squared_error(y_test, preds)
        r2   = r2_score(y_test, preds)

        results.append({
            "Model": label,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
            "Train time (s)": round(train_time, 1),
            "pipeline": pipe,
            "preds": preds,
            "use_log": use_log,
        })

        print(f"  MAE : {mae:,.0f}")
        print(f"  RMSE: {rmse:,.0f}")
        print(f"  R2  : {r2:.4f}")
        print(f"  Time: {train_time:.1f}s")

# %%
results_df = pd.DataFrame(results).drop(columns=["pipeline", "preds", "use_log"])
results_df["MAE"] = results_df["MAE"].apply(lambda x: f"{x:,.0f}")
results_df["RMSE"] = results_df["RMSE"].apply(lambda x: f"{x:,.0f}")
results_df["R2"] = results_df["R2"].apply(lambda x: f"{x:.4f}")
print(results_df.to_string(index=False))

# %%
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

for i, res in enumerate(results):
    ax = axes[i]
    sample_idx = np.random.RandomState(42).choice(len(y_test), size=min(3000, len(y_test)), replace=False)
    actual = y_test.values[sample_idx]
    predicted = res["preds"][sample_idx]

    ax.scatter(actual, predicted, alpha=0.2, s=8, color="#4c72b0")
    lim_max = max(actual.max(), predicted.max()) * 1.05
    ax.plot([0, lim_max], [0, lim_max], "r--", linewidth=1, label="Perfect")
    ax.set_xlim(0, lim_max)
    ax.set_ylim(0, lim_max)
    ax.set_xlabel("Actual Price")
    ax.set_ylabel("Predicted Price")
    ax.set_title(res["Model"], fontsize=10)
    ax.legend(fontsize=8)
    ax.ticklabel_format(style="plain", axis="both")

plt.suptitle("Predicted vs Actual", fontsize=14, y=1.02)
plt.tight_layout()
plt.show()

# %%
best_idx = max(range(len(results)), key=lambda i: float(results[i]["R2"]))
best = results[best_idx]
print(f"Best model: {best['Model']}")
print(f"  MAE : {best['MAE']:,.0f}")
print(f"  RMSE: {best['RMSE']:,.0f}")
print(f"  R2  : {best['R2']:.4f}")

# %%
best_pipe = best["pipeline"]
yt_cv = np.log1p(y) if best["use_log"] else y

cv_scores = cross_val_score(best_pipe, X, yt_cv, cv=5, scoring="r2", n_jobs=-1)
print(f"5-fold CV R2 scores: {cv_scores.round(4)}")
print(f"Mean R2: {cv_scores.mean():.4f}  +/-  {cv_scores.std():.4f}")

# %%
joblib.dump(best_pipe, "house_price.pkl")
print("Model saved to house_price.pkl")

loaded = joblib.load("house_price.pkl")
sample = X_test.iloc[[0]]
pred = loaded.predict(sample)
if best["use_log"]:
    pred = np.expm1(pred)
print(f"\nReloaded prediction: {pred[0]:,.0f}")
print(f"Actual value:        {y_test.iloc[0]:,.0f}")

# %%
locations = sorted(df["location_clean"].unique().tolist())
json.dump(locations, open("locations.json", "w"))
print(f"Saved {len(locations)} locations to locations.json")
print("First 10:", locations[:10])

# %%
print(f"\nPin these in requirements.txt:")
print(f"scikit-learn=={sklearn.__version__}")
print(f"numpy=={np.__version__}")
print(f"pandas=={pd.__version__}")
