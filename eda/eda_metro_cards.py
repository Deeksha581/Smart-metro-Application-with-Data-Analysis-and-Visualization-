import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ======================================================
# STYLE FOR ATTRACTIVE GRAPHS
# ======================================================
plt.style.use("seaborn-v0_8-darkgrid")
sns.set_palette("Set2")

# ======================================================
# PATHS
# ======================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "namma_metro_dataset_10000.xlsx")
EDA_DIR = os.path.join(BASE_DIR, "eda")
PLOTS_DIR = os.path.join(BASE_DIR, "eda", "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)
# ======================================================
# CLEAN OLD PLOTS (AUTO DELETE)
# ======================================================
for file in os.listdir(PLOTS_DIR):
    if file.endswith(".png"):
        os.remove(os.path.join(PLOTS_DIR, file))

# 3. IMPORT & INSPECT DATA
users = pd.read_excel(DATASET_PATH, sheet_name="Users")
cards = pd.read_excel(DATASET_PATH, sheet_name="MetroCards")
print("\n USERS INFO")
print(users.info())
print("\nCARDS INFO")
print(cards.info())
print("\n DATA TYPES")
print(cards.dtypes)
# ======================================================
# LOAD DATA
# ======================================================
users = pd.read_excel(DATASET_PATH, sheet_name="Users")
cards = pd.read_excel(DATASET_PATH, sheet_name="MetroCards")

# ======================================================
# BASIC CLEANING
# ======================================================
users["card_number"] = users["card_number"].fillna("NO_CARD")
cards["issued_date"] = pd.to_datetime(cards["issued_date"], errors="coerce")
cards["balance"] = cards["balance"].fillna(cards["balance"].median())
cards["issued_year"] = cards["issued_date"].dt.year

cards["balance_category"] = pd.cut(
    cards["balance"],
    bins=[0, 100, 300, 600, 1000, 5000],
    labels=["Very Low", "Low", "Medium", "High", "Very High"]
)
# 5. OUTLIER DETECTION (IQR METHOD) #
Q1 = cards["balance"].quantile(0.25)
Q3 = cards["balance"].quantile(0.75)
IQR = Q3 - Q1
LOWER = Q1 - 1.5 * IQR
UPPER = Q3 + 1.5 * IQR
cards["balance_outlier"] = np.where(
    (cards["balance"] < LOWER) | (cards["balance"] > UPPER),
    1, 0
)
print("\n📌 OUTLIERS COUNT:", cards["balance_outlier"].sum())
# 6. DATA TRANSFORMATION #
cards["issued_year"] = cards["issued_date"].dt.year
users["has_card_flag"] = users["has_card"].map({"Yes": 1, "No": 0})
cards["balance_category"] = pd.cut(
    cards["balance"],
    bins=[0, 100, 300, 600, 1000, 5000],
    labels=["Very Low", "Low", "Medium", "High", "Very High"]
)
# 7. DESCRIPTIVE STATISTICS #
stats = cards["balance"].describe()
stats["variance"] = cards["balance"].var()
stats["skewness"] = cards["balance"].skew()
stats.to_csv(os.path.join(EDA_DIR, "balance_statistics.csv"))
print("\n📊 BALANCE STATISTICS")
print(stats)
users.describe(include="all").to_csv(os.path.join(EDA_DIR,
    "users_stats.csv"))
cards.describe(include="all").to_csv(os.path.join(EDA_DIR,
    "cards_stats.csv"))
# ======================================================
# 1. DONUT CHART – CARD OWNERSHIP
# ======================================================
plt.figure(figsize=(6,6))
users["has_card"].value_counts().plot.pie(
    autopct="%1.1f%%", startangle=90, wedgeprops=dict(width=0.4)
)
plt.title("Metro Card Ownership Distribution")
plt.ylabel("")
plt.savefig(os.path.join(PLOTS_DIR, "01_card_ownership_donut.png"))
plt.close()

# ======================================================
# 2. HISTOGRAM + KDE – BALANCE
# ======================================================
plt.figure(figsize=(8,5))
sns.histplot(cards["balance"], bins=30, kde=True)
plt.title("Smart Card Balance Distribution")
plt.xlabel("Balance (₹)")
plt.savefig(os.path.join(PLOTS_DIR, "02_balance_hist_kde.png"))
plt.close()

# ======================================================
# 3. BOX PLOT – BALANCE
# ======================================================
plt.figure(figsize=(7,5))
sns.boxplot(x=cards["balance"])
plt.title("Balance Outlier Detection")
plt.savefig(os.path.join(PLOTS_DIR, "03_balance_boxplot.png"))
plt.close()

# ======================================================
# 4. VIOLIN PLOT – BALANCE
# ======================================================
plt.figure(figsize=(7,5))
sns.violinplot(x=cards["balance"], inner="quartile")
plt.title("Balance Distribution (Violin)")
plt.savefig(os.path.join(PLOTS_DIR, "04_balance_violin.png"))
plt.close()

# ======================================================
# 5. HORIZONTAL BAR – CARD STATUS
# ======================================================
plt.figure(figsize=(7,4))
status_counts = cards["status"].value_counts()
sns.barplot(x=status_counts.values, y=status_counts.index)
plt.title("Metro Card Status Distribution")
plt.xlabel("Number of Cards")
plt.savefig(os.path.join(PLOTS_DIR, "05_card_status_bar.png"))
plt.close()

# ======================================================
# 6. LINE PLOT – YEAR WISE ISSUANCE
# ======================================================
year_counts = cards["issued_year"].value_counts().sort_index()
plt.figure(figsize=(8,5))
sns.lineplot(x=year_counts.index, y=year_counts.values, marker="o")
plt.title("Year-wise Metro Card Issuance")
plt.xlabel("Year")
plt.ylabel("Cards Issued")
plt.savefig(os.path.join(PLOTS_DIR, "06_issued_year_line.png"))
plt.close()

# ======================================================
# 7. AREA CHART – GROWTH TREND
# ======================================================
plt.figure(figsize=(8,5))
year_counts.plot(kind="area", alpha=0.6)
plt.title("Growth of Metro Cards Over Years")
plt.xlabel("Year")
plt.ylabel("Total Cards")
plt.savefig(os.path.join(PLOTS_DIR, "07_issued_year_area.png"))
plt.close()

# ======================================================
# 8. SCATTER – BALANCE VS YEAR
# ======================================================
plt.figure(figsize=(8,5))
sns.scatterplot(x="issued_year", y="balance", data=cards)
plt.title("Balance vs Issued Year")
plt.savefig(os.path.join(PLOTS_DIR, "08_balance_vs_year_scatter.png"))
plt.close()

# ======================================================
# 9. BOX + STRIP – BALANCE VS STATUS
# ======================================================
plt.figure(figsize=(8,5))
sns.boxplot(x="status", y="balance", data=cards)
sns.stripplot(x="status", y="balance", data=cards, color="black", alpha=0.4)
plt.title("Balance vs Card Status")
plt.savefig(os.path.join(PLOTS_DIR, "09_balance_vs_status.png"))
plt.close()

# ======================================================
# 10. COUNT PLOT – BALANCE CATEGORY
# ======================================================
plt.figure(figsize=(7,4))
sns.countplot(x="balance_category", data=cards)
plt.title("User Balance Category Distribution")
plt.xlabel("Balance Category")
plt.savefig(os.path.join(PLOTS_DIR, "10_balance_category.png"))
plt.close()

# ======================================================
# 11. PIE – BALANCE CATEGORY SHARE
# ======================================================
plt.figure(figsize=(6,6))
cards["balance_category"].value_counts().plot.pie(autopct="%1.1f%%")
plt.title("Balance Category Share")
plt.ylabel("")
plt.savefig(os.path.join(PLOTS_DIR, "11_balance_category_pie.png"))
plt.close()

# ======================================================
# 12. KDE CURVE – BALANCE DENSITY
# ======================================================
plt.figure(figsize=(7,5))
sns.kdeplot(cards["balance"], fill=True)
plt.title("Balance Density Curve")
plt.savefig(os.path.join(PLOTS_DIR, "12_balance_kde.png"))
plt.close()

# ======================================================
# 13. COUNT PLOT – USERS WITH / WITHOUT CARD
# ======================================================
plt.figure(figsize=(6,4))
sns.countplot(x="has_card", data=users)
plt.title("Users With vs Without Metro Card")
plt.savefig(os.path.join(PLOTS_DIR, "13_has_card_count.png"))
plt.close()

# ======================================================
# 14. BAR – CARDS ISSUED PER YEAR
# ======================================================
plt.figure(figsize=(8,5))
year_counts.plot(kind="bar")
plt.title("Cards Issued Per Year")
plt.xlabel("Year")
plt.ylabel("Count")
plt.savefig(os.path.join(PLOTS_DIR, "14_cards_per_year_bar.png"))
plt.close()

# ======================================================
# 15. CORRELATION HEATMAP
# ======================================================
plt.figure(figsize=(8,6))
sns.heatmap(
    cards.select_dtypes(include=np.number).corr(),
    annot=True,
    cmap="RdYlGn",
    linewidths=0.5
)
plt.title("Correlation Heatmap – Metro Card Data")
plt.savefig(os.path.join(PLOTS_DIR, "15_correlation_heatmap.png"))
plt.close()

print("✅ 15 ATTRACTIVE EDA VISUALIZATIONS GENERATED")
print(f"📊 Check folder: {PLOTS_DIR}")