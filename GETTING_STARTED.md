# 🚀 Getting Started

## 5-Minute Setup

### Step 1: Prepare Files
```
pizza_anomaly_detector/
├── orders.csv
├── order_details.csv
├── pizzas.csv
├── pizza_types.csv
└── app.py              ← Your main app
```

### Step 2: Install & Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Step 3: Explore
1. **Sidebar**: Set your date range (filters all analyses)
2. **📊 Overview**: Key metrics & trends
3. **⚠️ Anomalies**: Unusual ordering patterns
4. **🎯 Clustering**: Customer segments
5. **🔮 Forecast**: Next 24 hours
6. **💡 Recommendations**: Cross-sell opportunities
7. **🥬 Ingredients**: Procurement insights
8. **📄 Report**: Export as CSV

---

## 📊 Features by Tab

### 📊 **Overview Tab**
What: KPIs, trends, top products
Use: Daily performance check
See: Orders, revenue, weekly volume, hourly patterns

### ⚠️ **Anomalies Tab**
What: Unusual patterns (Isolation Forest ML)
Use: Find operational issues
Do: Adjust sensitivity, review flagged orders

### 🎯 **Clustering Tab**
What: Customer segments (K-Means + PCA)
Use: Understand customer types
Do: Select optimal K, view characteristics

### 🔮 **Forecast Tab**
What: Next 24 hours (Ridge Regression)
Use: Staff & inventory planning
Do: See peak hours, plan accordingly

### 💡 **Recommendations Tab**
What: Products frequently bought together
Use: Menu bundling, cross-selling
Do: Review pairs, select product for suggestions

### 🥬 **Ingredients Tab**
What: Ingredient popularity & performance
Use: Supplier planning, menu optimization
Do: Identify top ingredients, procurement decisions

### 📄 **Report Tab**
What: Complete analysis export
Use: Share with stakeholders
Do: Download CSV with all findings

---

## 💡 Usage Tips

### **Date Range**
- Sidebar date picker filters all analyses
- 3 months for seasonal patterns
- 1 week for recent detailed analysis

### **Anomaly Detection**
- **5% sensitivity**: Standard operations
- **10% sensitivity**: More lenient
- **1% sensitivity**: Overly sensitive

### **Clustering**
- Look for "elbow" in curve
- Usually 3-5 clusters optimal
- Higher K = finer segments

### **Forecasting**
- Needs 50+ historical orders
- Works best with 3+ months
- Use for next 24 hours

---

## 🔍 Color Meanings

| Color | Meaning |
|-------|---------|
| 🔵 Blue | Primary data, active states |
| 🟢 Green | Success, forecasts, positive |
| 🟠 Orange | Secondary data, attention |
| 🔴 Red | Warnings, anomalies, alerts |
| 🟣 Purple | Ingredients, analysis |
| 🔷 Teal | Performance, efficiency |

---

## 📱 Mobile Support
- Responsive design
- Touch-friendly inputs
- Sidebar collapses on narrow screens
- Swipeable tabs on phones

---

## 🐛 Troubleshooting

**"Data files not found"**
→ Ensure CSVs in pizza_anomaly_detector/ folder

**"Not enough data for clustering"**
→ Select larger date range

**"Forecast tab empty"**
→ Need >50 orders (try 3+ months)

**Slow loading**
→ Run: `streamlit cache clear`

---

**You're ready! Happy analyzing! 🎉**
