# 🍕 Pizza Intelligence Platform

Professional analytics dashboard for pizza business operations. Detects anomalies, forecasts demand, and provides actionable insights through machine learning.

---

## Overview

The Pizza Intelligence Platform is a Streamlit-based analytics application that analyzes pizza order data with the following capabilities:

- **Anomaly Detection**: Identify unusual ordering patterns using Isolation Forest
- **Customer Clustering**: Segment customers into distinct groups via K-Means
- **Demand Forecasting**: Predict next 24 hours using Ridge Regression
- **Recommendations**: Find products frequently ordered together
- **Ingredient Analytics**: Track ingredient popularity and performance
- **Comprehensive Reporting**: Export findings as CSV

---

## Features

### 📊 Overview Dashboard
- Total orders, revenue, and units sold
- Top 10 best-performing products
- Weekly order volume trends
- Hourly order distribution patterns

### ⚠️ Anomaly Detection
- Isolation Forest algorithm
- Adjustable sensitivity (1-20%)
- Temporal feature analysis (hour, day, month)
- Detailed anomaly listings

### 🎯 Customer Clustering
- K-Means segmentation (2-7 clusters)
- Elbow method for optimal K
- PCA visualization in 2D space
- Cluster characteristic analysis

### 🔮 Demand Forecasting
- Ridge Regression model
- 24-hour predictions
- Peak hour identification
- Lag-based temporal features

### 💡 Cross-Sell Recommendations
- Co-occurrence analysis
- Product pair frequency
- Personalized "you may also like"
- Data-driven bundling insights

### 🥬 Ingredient Insights
- Top 15 ingredients by frequency
- Performance metrics per ingredient
- Supply chain planning data
- Menu optimization guidance

### 📄 Report Generation
- Comprehensive anomaly reports
- CSV export functionality
- Date range selection
- Multi-category analysis

---

## Installation

### Requirements
- Python 3.8+
- pip package manager

### Setup
```bash
# 1. Clone/download project
cd pizza_anomaly_detector

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify CSV files present
ls *.csv

# 4. Run application
streamlit run app.py
```

### Verify Installation
```bash
python -c "import streamlit; import pandas; import sklearn; print('✓ All dependencies installed')"
```

---

## Data Structure

Required CSV files:

| File | Columns | Purpose |
|------|---------|---------|
| orders.csv | order_id, date, time | Order metadata |
| order_details.csv | order_id, pizza_id, quantity | Line items |
| pizzas.csv | pizza_id, pizza_type_id, size, price | Product catalog |
| pizza_types.csv | pizza_type_id, name, category, ingredients | Product hierarchy |

---

## Usage Guide

### 1. Date Range Selection
Use sidebar date picker to filter all analyses. Affects:
- Metrics calculations
- Chart data
- ML model training
- Export results

### 2. Anomaly Detection
1. Adjust sensitivity slider (typical: 5-10%)
2. Review expected anomalies indicator
3. Examine hourly distribution chart
4. Review detailed anomaly table

**Interpretation**: Anomalies indicate unusual ordering patterns (events, outages, etc.)

### 3. Clustering Analysis
1. Review elbow method curve
2. Select optimal cluster count
3. Analyze PCA visualization
4. Study cluster profiles

**Use Case**: Segment customers for targeted marketing

### 4. Demand Forecasting
1. Ensure date range has 50+ orders
2. View 24-hour forecast chart
3. Identify peak hours
4. Check statistical summary

**Application**: Staffing and inventory planning

### 5. Recommendations
1. Review top product pairs
2. Select pizza for personalized suggestions
3. Check co-purchase frequency
4. Use for menu bundling

**Purpose**: Cross-selling and promotional planning

### 6. Ingredient Analysis
1. Identify top ingredients
2. Analyze performance metrics
3. Plan supplier orders
4. Optimize menu composition

**Benefit**: Cost control and supply chain efficiency

### 7. Report Export
1. Select analysis date range
2. Click download button
3. Receive CSV file
4. Import to Excel/BI tool

---

## Machine Learning

### Isolation Forest
- **Method**: Unsupervised outlier detection
- **Features**: Temporal (hour, minute, day, month, weekend)
- **Sensitivity**: User-controlled via contamination parameter
- **Output**: Normal (1) or Anomaly (-1)

### K-Means Clustering
- **Method**: Unsupervised customer segmentation
- **Features**: Pizza categories and sizes (one-hot encoded)
- **Optimization**: Elbow method for K selection
- **Standardization**: StandardScaler normalization

### PCA Visualization
- **Purpose**: 2D visualization of high-dimensional clusters
- **Components**: 2 (for visualization)
- **Variance**: Typically 60-80% explained

### Ridge Regression Forecast
- **Method**: Linear regression with L2 regularization
- **Features**: 24-hour lags + temporal indicators
- **Regularization**: Alpha = 1.0
- **Window**: 24-hour ahead prediction

---

## Design System

### Light Mode Color Palette
- **Primary Text**: #2C3E50 (dark blue-gray)
- **Secondary**: #7F8C8D (muted gray)
- **Accent**: #3498DB (professional blue)
- **Success**: #27AE60 (forest green)
- **Warning**: #E74C3C (alert red)
- **Background**: #FAFBFC (off-white)

### Typography
- **Headlines**: System fonts, 600-700 weight
- **Body**: 11-13px, sans-serif
- **Spacing**: Consistent 0.5-2rem increments

### Components
- **Cards**: White backgrounds, subtle borders
- **Buttons**: Professional blue with hover states
- **Inputs**: Clean design with focus rings
- **Charts**: Unified styling, white backgrounds

---

## Performance

### Speed Optimization
- Data caching with @st.cache_data
- First load: ~500ms
- Subsequent loads: ~100ms
- Model training: Dependent on data size

### Chart Performance
- Plotly optimization
- Responsive sizing
- Efficient hover interactions

### Memory Usage
- Typical: <200MB for standard dataset
- Scales with CSV file sizes

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Data files not found" | Verify CSV files in pizza_anomaly_detector/ folder |
| Slow initial load | Normal - first load caches data |
| Empty clustering tab | Select larger date range (>10 unique orders) |
| No forecast data | Select range with >50 orders |
| Chart rendering slow | Clear cache: `streamlit cache clear` |

### Debug Mode
```bash
streamlit run app.py --logger.level=debug
```

---

## Customization

### Change Brand Color
Edit `THEME_CSS` variable:
```python
--color-accent: #YOUR_COLOR;
```

### Modify Chart Heights
```python
plot_chart(fig, title, height=600)
```

### Add Custom Features
1. Extend `X_time` in anomaly detection
2. Add new columns to order data
3. Retrain models with new features

---

## Deployment

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push code to GitHub
2. Connect Streamlit account
3. Deploy from repository

### Docker Container
```bash
docker build -t pizza-app .
docker run -p 8501:8501 pizza-app
```

### Production Considerations
- Add authentication layer
- Connect to database instead of CSV
- Implement monitoring/logging
- Set up automated testing
- Configure CI/CD pipeline

---

## Data Privacy

- Application runs locally
- No data sent to external servers
- CSV files stay on machine
- Reports downloaded to local disk

---

## Supported Browsers
- Chrome/Chromium
- Firefox
- Safari
- Edge

---

## Mobile Support
- Responsive design
- Touch-friendly interface
- Sidebar collapses on mobile
- Charts adapt to screen size

---

## API Integration

To connect to live data instead of CSV:

```python
def load_all_data():
    conn = create_database_connection()
    orders = pd.read_sql("SELECT * FROM orders", conn)
    # ... merge operations
    return orders, order_details, pizzas, pizza_types, sales
```

---

## Monitoring

### Track Usage
```python
import logging
logger = logging.getLogger(__name__)
logger.info("User accessed forecast tab")
```

### Performance Metrics
```python
import time
start = time.time()
# ... process ...
duration = time.time() - start
st.metric("Processing Time", f"{duration:.2f}s")
```

---

## Support & Contribution

### Report Issues
- Document error message
- Include date range
- Specify which tab affected
- Provide sample data if possible

### Contribute
- Test new features locally
- Document changes
- Follow existing code style
- Submit pull requests

---

## License
Open source - modify and distribute freely

---

## Technologies Used

- **Streamlit**: Web framework
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **scikit-learn**: Machine learning
- **Plotly**: Interactive visualizations

---

## Version History

### v1.0
- Initial release
- 7 core features
- Light mode design
- Responsive layout

---

## Future Enhancements

- LSTM forecasting
- DBSCAN clustering
- Real-time updates
- User authentication
- Advanced reporting
- API endpoints

---

## Contact & Questions

For questions or feedback, review the documentation or examine the code comments.

---

**Ready to analyze? Run `streamlit run app.py` and start exploring!** 🚀
