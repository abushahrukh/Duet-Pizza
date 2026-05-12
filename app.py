import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.linear_model import Ridge
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import os
import base64
import warnings
warnings.filterwarnings('ignore')

# ==================== IMAGE LOADING ====================
def load_image_b64(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, filename)
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

try:
    BG_B64   = load_image_b64("pizza_backgrounds.png")
    LOGO_B64 = load_image_b64("pizza_logo.png")
except Exception:
    BG_B64   = None
    LOGO_B64 = None

# ==================== PAGE CONFIG & THEME ====================
st.set_page_config(
    page_title="Pizza Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== BRAND THEME ====================
_bg_css = f"""url('data:image/png;base64,{BG_B64}')""" if BG_B64 else "none"

THEME_CSS = f"""
<style>
    /* ---- Background image ---- */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > .main {{
        background-image: {_bg_css} !important;
        background-size: cover !important;
        background-attachment: fixed !important;
        background-position: center !important;
        background-color: #FAF5EF !important;
    }}

    /* Semi-transparent overlay so content stays readable */
    [data-testid="stAppViewContainer"] > .main > div {{
        background: rgba(255, 252, 248, 0.88);
        border-radius: 12px;
    }}

    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}

    [data-testid="stSidebar"] {{
        background-color: #FFFFFF !important;
        border-right: 2px solid #E8D5D5 !important;
    }}

    /* ---- Body text ---- */
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] li,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {{
        color: #1A1A1A !important;
    }}

    /* ---- Headings ---- */
    h1, h2, h3, h4, h5, h6,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        color: #1A1A1A !important;
        font-weight: 700 !important;
    }}

    [data-testid="stMarkdownContainer"] h2 {{
        border-bottom: 2px solid #E8D5D5;
        padding-bottom: 0.6rem;
        margin-top: 1.5rem;
    }}

    /* ---- Metrics ---- */
    [data-testid="stMetric"] {{
        background: rgba(255,255,255,0.95);
        border: 1px solid #E8D5D5;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 8px rgba(180,30,30,0.08);
    }}

    [data-testid="stMetricLabel"] > div {{
        color: #4A4A4A !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }}

    [data-testid="stMetricValue"] > div {{
        color: #C8102E !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }}

    /* ---- Tabs ---- */
    [data-testid="stTabs"] [role="tablist"] {{
        border-bottom: 2px solid #E8D5D5;
        background: transparent;
    }}

    [data-testid="stTabs"] [role="tab"] {{
        padding: 0.85rem 1.4rem !important;
        color: #4A4A4A !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border-bottom: 3px solid transparent !important;
        background: transparent !important;
    }}

    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
        color: #C8102E !important;
        border-bottom-color: #C8102E !important;
    }}

    [data-testid="stTabs"] [role="tab"]:hover {{
        color: #1A1A1A !important;
        background: rgba(200,16,46,0.06) !important;
    }}

    /* ---- Sidebar caption ---- */
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
        color: #4A4A4A !important;
        font-size: 0.82rem !important;
        line-height: 1.5;
    }}

    /* ---- Alerts ---- */
    [data-testid="stAlert"] {{
        border-radius: 8px !important;
        border-left-width: 4px !important;
        border-left-style: solid !important;
        background: rgba(255,255,255,0.95) !important;
    }}

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] div {{
        color: #1A1A1A !important;
        font-size: 0.9rem !important;
    }}

    [data-testid="stAlert"][kind="info"]    {{ border-left-color: #C8102E !important; background-color: rgba(200,16,46,0.06) !important; }}
    [data-testid="stAlert"][kind="warning"] {{ border-left-color: #D68910 !important; background-color: #FEF3E2 !important; }}
    [data-testid="stAlert"][kind="success"] {{ border-left-color: #1E8449 !important; background-color: #EAFAF1 !important; }}
    [data-testid="stAlert"][kind="error"]   {{ border-left-color: #C0392B !important; background-color: #FDEDEC !important; }}

    /* ---- Buttons ---- */
    .stButton > button,
    .stDownloadButton > button {{
        background-color: #C8102E !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 7px !important;
        font-weight: 700 !important;
        padding: 0.55rem 1.4rem !important;
        box-shadow: 0 2px 6px rgba(200,16,46,0.25) !important;
        transition: background 0.2s ease !important;
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        background-color: #A00D25 !important;
        box-shadow: 0 4px 12px rgba(200,16,46,0.35) !important;
    }}

    /* ---- Inputs ---- */
    [data-testid="stSelectbox"] label,
    [data-testid="stSlider"] label,
    [data-testid="stDateInput"] label {{
        color: #1A1A1A !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }}

    /* ---- Dataframe ---- */
    [data-testid="stDataFrame"] {{
        border: 1px solid #E8D5D5 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
        background: rgba(255,255,255,0.95) !important;
    }}

    /* ---- Header container ---- */
    .header-container {{
        background: linear-gradient(120deg, #C8102E 0%, #1A1A1A 100%);
        border-radius: 12px;
        padding: 1.6rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 18px rgba(200,16,46,0.22);
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }}

    .header-logo {{
        height: 72px;
        width: auto;
        flex-shrink: 0;
    }}

    .header-text {{ flex: 1; }}

    .header-title {{
        font-size: 2rem;
        font-weight: 800;
        color: #FFFFFF !important;
        margin: 0 0 0.3rem 0;
        letter-spacing: -0.3px;
    }}

    .header-subtitle {{
        font-size: 0.95rem;
        color: rgba(255,255,255,0.82) !important;
        margin: 0;
        font-weight: 400;
    }}

    /* ---- Insight cards ---- */
    .insight-card {{
        background: rgba(255,255,255,0.95);
        border: 1px solid #E8D5D5;
        border-radius: 8px;
        padding: 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }}

    .insight-title  {{ font-weight: 700; color: #1A1A1A; font-size: 0.95rem; }}
    .insight-value  {{ font-size: 1.5rem; color: #C8102E; font-weight: 700; }}
    .insight-subtitle {{ font-size: 0.82rem; color: #4A4A4A; }}

    /* ---- Scrollbar ---- */
    ::-webkit-scrollbar {{ width: 7px; height: 7px; }}
    ::-webkit-scrollbar-track {{ background: #FAF5EF; }}
    ::-webkit-scrollbar-thumb {{ background: #D5A0A0; border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: #C8102E; }}
</style>
"""

st.markdown(THEME_CSS, unsafe_allow_html=True)

# ==================== DATA LOADING ====================
@st.cache_data(show_spinner=False)
def load_all_data():
    """Load and merge all pizza order data."""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        orders = pd.read_csv(os.path.join(base_dir, "orders.csv"), parse_dates=["date"], encoding='latin1')
        orders["datetime"] = pd.to_datetime(orders["date"].astype(str) + " " + orders["time"])
        
        order_details = pd.read_csv(os.path.join(base_dir, "order_details.csv"), encoding='latin1')
        pizzas = pd.read_csv(os.path.join(base_dir, "pizzas.csv"), encoding='latin1')
        pizza_types = pd.read_csv(os.path.join(base_dir, "pizza_types.csv"), encoding='latin1')
        
        sales = order_details.merge(pizzas, on="pizza_id")
        sales = sales.merge(pizza_types, on="pizza_type_id")
        sales = sales.merge(orders, on="order_id")
        
        return orders, order_details, pizzas, pizza_types, sales
    except FileNotFoundError:
        st.error("Data files not found. Ensure CSV files are in the same folder as app.py.")
        st.stop()

# Load data
with st.spinner(" Loading data..."):
    orders, order_details, pizzas, pizza_types, sales = load_all_data()

# ==================== HELPER FUNCTIONS ====================
def get_date_range_filter():
    """Get and apply date range filter from sidebar."""
    min_date = orders["date"].min()
    max_date = orders["date"].max()
    
    date_range = st.sidebar.date_input(
        " Select Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    else:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[0])
    
    return start_date, end_date

def filter_data(start_date, end_date):
    """Filter sales and orders by date range."""
    sales_mask = (sales["date"] >= start_date) & (sales["date"] <= end_date)
    orders_mask = (orders["date"] >= start_date) & (orders["date"] <= end_date)
    return sales[sales_mask], orders[orders_mask]

def plot_chart(fig, title, height=500):
    """Standardized chart rendering."""
    axis_style = dict(
        showgrid=True,
        gridwidth=1,
        gridcolor="#E2E8F0",
        showline=True,
        linewidth=1.5,
        linecolor="#94A3B8",
        tickfont=dict(family="Arial, sans-serif", color="#1A2535", size=12),
        title_font=dict(family="Arial, sans-serif", color="#1A2535", size=13),
        ticks="outside",
        tickcolor="#94A3B8",
    )
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="Arial, sans-serif", color="#1A2535", size=12),
        title_font=dict(size=16, color="#1A2535", family="Arial, sans-serif"),
        hovermode="x unified",
        margin=dict(l=60, r=40, t=65, b=60),
        height=height,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#1A2535", size=12),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#CBD5E1",
            borderwidth=1
        )
    )
    fig.update_xaxes(**axis_style)
    fig.update_yaxes(**axis_style)
    st.plotly_chart(fig, use_container_width=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    if LOGO_B64:
        st.markdown(
            f'''<div style="text-align:center;padding:1rem 0 0.5rem;">
                <img src="data:image/png;base64,{LOGO_B64}"
                     style="width:75%;max-width:200px;height:auto;" />
            </div>''',
            unsafe_allow_html=True
        )
    else:
        st.markdown("### Duet Pizza")
    st.markdown("---")
    
    start_date, end_date = get_date_range_filter()
    filtered_sales, filtered_orders = filter_data(start_date, end_date)
    
    st.markdown("---")
    st.markdown("** Data**")
    col1, col2 = st.columns(2)
    col1.metric("Orders", f"{len(filtered_orders):,}")
    col2.metric("Units Sold", f"{filtered_sales['quantity'].sum():,}")
    
    st.markdown("---")
    st.markdown("** About**")
    st.caption(
        "Machine learning analytics platform for order analysis, "
        "demand forecasting, and business intelligence."
    )

# ==================== MAIN HEADER ====================
_logo_tag = f'<img class="header-logo" src="data:image/png;base64,{LOGO_B64}" />' if LOGO_B64 else ""
st.markdown(f"""
<div class="header-container">
    {_logo_tag}
    <div class="header-text">
        <div class="header-title">Duet Pizza Intelligence</div>
        <div class="header-subtitle">Anomaly detection, demand forecasting, and business analytics</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== KEY METRICS ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        " Total Orders",
        f"{len(filtered_orders):,}",
        help="Orders in selected period"
    )

with col2:
    total_pizzas = filtered_sales['quantity'].sum()
    st.metric(
        " Units Sold",
        f"{total_pizzas:,}",
        help="Total pizza units"
    )

with col3:
    total_revenue = (filtered_sales['quantity'] * filtered_sales['price']).sum()
    st.metric(
        " Revenue",
        f"${total_revenue:,.0f}",
        help="Total revenue"
    )

with col4:
    unique_pizzas = filtered_sales['pizza_id'].nunique()
    st.metric(
        " Varieties",
        f"{unique_pizzas}",
        help="Different pizza types"
    )

st.markdown("---")

# ==================== TABBED INTERFACE ====================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    " Overview",
    " Anomalies",
    " Clustering",
    " Forecast",
    " Recommendations",
    " Ingredients",
    " Report"
])

# ========== TAB 1: OVERVIEW ==========
with tab1:
    st.markdown("## Business Overview")
    st.markdown("Key performance indicators and operational trends.")
    st.markdown("---")
    
    # Top Pizzas
    st.markdown("### Top Performing Products")
    top_pizzas = filtered_sales.groupby("name")["quantity"].sum().reset_index()
    top_pizzas = top_pizzas.sort_values("quantity", ascending=False).head(10)
    
    fig_top = go.Figure()
    fig_top.add_trace(go.Bar(
        x=top_pizzas["quantity"],
        y=top_pizzas["name"],
        orientation='h',
        marker=dict(color="#3498DB", line=dict(color="#2C3E50", width=0.5)),
        hovertemplate="<b>%{y}</b><br>Units: %{x}<extra></extra>"
    ))
    fig_top.update_layout(title="Top 10 Products", xaxis_title="Units Sold", yaxis_title="", height=400)
    plot_chart(fig_top, "Top Products", height=400)
    
    # Weekly Order Volume
    st.markdown("### Weekly Volume")
    filtered_orders["week"] = filtered_orders["date"].dt.isocalendar().week
    weekly_sales = filtered_orders.groupby("week").size().reset_index(name="orders")
    
    fig_weekly = go.Figure()
    fig_weekly.add_trace(go.Scatter(
        x=weekly_sales["week"],
        y=weekly_sales["orders"],
        mode='lines+markers',
        fill='tozeroy',
        line=dict(color="#27AE60", width=3),
        marker=dict(size=8, color="#27AE60"),
        hovertemplate="Week %{x}<br>Orders: %{y}<extra></extra>"
    ))
    fig_weekly.update_layout(title="Orders by Week", xaxis_title="Week", yaxis_title="Orders", height=400)
    plot_chart(fig_weekly, "Weekly", height=400)
    
    # Hourly Distribution
    st.markdown("### Hourly Pattern")
    filtered_orders_copy = filtered_orders.copy()
    filtered_orders_copy["hour"] = filtered_orders_copy["datetime"].dt.hour
    hourly = filtered_orders_copy.groupby("hour").size().reset_index(name="count")
    
    fig_hourly = go.Figure()
    fig_hourly.add_trace(go.Bar(
        x=hourly["hour"],
        y=hourly["count"],
        marker=dict(color="#E67E22", line=dict(color="#2C3E50", width=0.5)),
        hovertemplate="Hour %{x}:00<br>Orders: %{y}<extra></extra>"
    ))
    fig_hourly.update_layout(title="Hourly Orders", xaxis_title="Hour", yaxis_title="Orders", height=400, xaxis=dict(tickmode='linear', tick0=0, dtick=1))
    plot_chart(fig_hourly, "Hourly", height=400)

# ========== TAB 2: TEMPORAL ANOMALIES ==========
with tab2:
    st.markdown("## Anomaly Detection")
    st.markdown("Identify unusual ordering patterns using machine learning.")
    st.markdown("---")
    
    # Feature Engineering
    orders_copy = orders.copy()
    orders_copy["hour"] = orders_copy["datetime"].dt.hour
    orders_copy["minute"] = orders_copy["datetime"].dt.minute
    orders_copy["day_of_week"] = orders_copy["datetime"].dt.dayofweek
    orders_copy["month"] = orders_copy["datetime"].dt.month
    orders_copy["is_weekend"] = (orders_copy["day_of_week"] >= 5).astype(int)
    
    # Sensitivity Control
    st.markdown("### Detection Settings")
    col1, col2 = st.columns([1, 3])
    with col1:
        contamination = st.slider("Sensitivity", 0.01, 0.20, 0.05, 0.01, help="3-10% typical")
    with col2:
        st.info(f"~{int(len(orders_copy) * contamination)} anomalies expected")
    
    # Model
    X_time = orders_copy[["hour", "minute", "day_of_week", "month", "is_weekend"]]
    model_time = IsolationForest(contamination=contamination, random_state=42)
    orders_copy["anomaly"] = model_time.fit_predict(X_time)
    orders_copy["anomaly_label"] = orders_copy["anomaly"].map({1: "Normal", -1: "Anomaly"})
    
    filtered_anomaly = orders_copy[(orders_copy["date"] >= start_date) & (orders_copy["date"] <= end_date)]
    
    # Metrics
    st.markdown("### Results")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Orders", f"{len(filtered_anomaly):,}")
    with col2:
        anomaly_count = (filtered_anomaly["anomaly_label"] == "Anomaly").sum()
        st.metric("Anomalies Found", f"{anomaly_count:,}")
    with col3:
        pct = (anomaly_count / len(filtered_anomaly) * 100) if len(filtered_anomaly) > 0 else 0
        st.metric("Rate", f"{pct:.1f}%")
    
    # Visualization
    st.markdown("### Distribution")
    hist_data = filtered_anomaly.groupby(["hour", "anomaly_label"]).size().reset_index(name="count")
    
    fig_hist = go.Figure()
    for label in ["Normal", "Anomaly"]:
        data = hist_data[hist_data["anomaly_label"] == label]
        fig_hist.add_trace(go.Bar(
            x=data["hour"],
            y=data["count"],
            name=label,
            marker=dict(color="#3498DB" if label == "Normal" else "#E74C3C"),
            hovertemplate=f"%{{x}}: {label}=%{{y}}<extra></extra>"
        ))
    
    fig_hist.update_layout(title="Order Distribution", xaxis_title="Hour", yaxis_title="Count", barmode="stack", height=450, xaxis=dict(tickmode='linear', tick0=0, dtick=1))
    plot_chart(fig_hist, "Distribution", height=450)
    
    # Table
    st.markdown("### Detected Anomalies")
    anomaly_df = filtered_anomaly[filtered_anomaly["anomaly_label"] == "Anomaly"][["order_id", "date", "time", "hour", "day_of_week"]].copy()
    
    if len(anomaly_df) > 0:
        anomaly_df.columns = ["Order ID", "Date", "Time", "Hour", "Day"]
        st.dataframe(anomaly_df, use_container_width=True, hide_index=True)
    else:
        st.success(" No anomalies detected")

# ========== TAB 3: ORDER CLUSTERING ==========
with tab3:
    st.markdown("## Customer Clustering")
    st.markdown("Segment orders into distinct customer groups.")
    st.markdown("---")
    
    if len(filtered_sales) > 10:
        cat_dummies = pd.get_dummies(filtered_sales[["order_id", "category"]], columns=["category"], prefix="cat")
        size_dummies = pd.get_dummies(filtered_sales[["order_id", "size"]], columns=["size"], prefix="size")
        order_features = cat_dummies.groupby("order_id").sum().join(size_dummies.groupby("order_id").sum(), how="outer").fillna(0)
        
        if len(order_features) > 1:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(order_features)
            
            # Elbow Method
            st.markdown("### Optimal K Selection")
            inertia = []
            for k in range(2, min(8, len(order_features))):
                km = KMeans(n_clusters=k, random_state=42, n_init=10)
                km.fit(X_scaled)
                inertia.append(km.inertia_)
            
            fig_elbow = go.Figure()
            fig_elbow.add_trace(go.Scatter(
                x=list(range(2, min(8, len(order_features)))),
                y=inertia,
                mode='lines+markers',
                marker=dict(size=10, color="#3498DB"),
                line=dict(width=3, color="#3498DB"),
                hovertemplate="K=%{x}<br>Inertia: %{y:.0f}<extra></extra>"
            ))
            fig_elbow.update_layout(title="Elbow Method", xaxis_title="Clusters", yaxis_title="Inertia", height=350)
            plot_chart(fig_elbow, "Elbow", height=350)
            
            # User Selection
            st.markdown("### Configuration")
            k = st.slider("Number of Clusters", 2, min(7, len(order_features)), 4)
            
            # K-Means
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            clusters = km.fit_predict(X_scaled)
            order_features["cluster"] = clusters
            
            # PCA
            st.markdown("### Visualization")
            pca = PCA(n_components=2)
            pca_result = pca.fit_transform(X_scaled)
            pca_df = pd.DataFrame(pca_result, columns=["PC1", "PC2"])
            pca_df["cluster"] = clusters.astype(str)
            
            fig_pca = px.scatter(
                pca_df, x="PC1", y="PC2", color="cluster",
                title=f"Segments (Variance: {pca.explained_variance_ratio_.sum():.1%})",
                height=450,
                color_discrete_sequence=["#3498DB", "#E74C3C", "#27AE60", "#E67E22", "#9B59B6", "#1ABC9C", "#34495E"]
            )
            fig_pca.update_traces(marker=dict(size=10, opacity=0.7, line=dict(width=1, color="#2C3E50")))
            plot_chart(fig_pca, "Clusters", height=450)
            
            # Profiles
            st.markdown("### Cluster Profiles")
            cluster_profile = order_features.drop("cluster", axis=1).groupby(order_features["cluster"]).mean()
            st.dataframe(cluster_profile, use_container_width=True)
        else:
            st.warning("Need more data for clustering")
    else:
        st.info("Select a larger date range")

# ========== TAB 4: DEMAND FORECAST ==========
with tab4:
    st.markdown("## Demand Forecasting")
    st.markdown("Predict next 24 hours of orders using historical patterns.")
    st.markdown("---")
    
    if len(orders) > 50:
        orders_copy = orders.copy()
        orders_copy["hour_bin"] = orders_copy["datetime"].apply(lambda x: x.replace(minute=0, second=0, microsecond=0))
        hourly = orders_copy.groupby("hour_bin").size().reset_index(name="count")
        hourly = hourly.sort_values("hour_bin")
        
        if len(hourly) > 24:
            # Features
            for lag in range(1, 25):
                hourly[f"lag_{lag}"] = hourly["count"].shift(lag)
            hourly["hour_of_day"] = hourly["hour_bin"].dt.hour
            hourly["day_of_week"] = hourly["hour_bin"].dt.dayofweek
            
            # Train
            train = hourly.dropna().copy()
            X_cols = [f"lag_{l}" for l in range(1, 25)] + ["hour_of_day", "day_of_week"]
            X = train[X_cols]
            y = train["count"]
            
            model = Ridge(alpha=1.0)
            model.fit(X, y)
            
            # Forecast
            last_actuals = hourly["count"].values[-24:].tolist()
            if len(last_actuals) < 24:
                last_actuals = [0] * (24 - len(last_actuals)) + last_actuals
            
            last_hour_bin = hourly["hour_bin"].iloc[-1]
            future = []
            recent_counts = last_actuals.copy()
            
            for i in range(1, 25):
                lag_features = recent_counts[-24:]
                pred_hour = (last_hour_bin + timedelta(hours=i)).hour
                pred_dow = (last_hour_bin + timedelta(hours=i)).dayofweek
                features = lag_features + [pred_hour, pred_dow]
                pred = model.predict([features])[0]
                pred_count = max(0, int(round(pred)))
                future.append({
                    "hour_bin": last_hour_bin + timedelta(hours=i),
                    "order_count": pred_count
                })
                recent_counts.append(pred_count)
            
            future_df = pd.DataFrame(future)
            combined = pd.concat([
                hourly[["hour_bin", "count"]].rename(columns={"count": "order_count"}),
                future_df
            ]).reset_index(drop=True)
            
            # Visualization
            st.markdown("### 24-Hour Forecast")
            fig_forecast = go.Figure()
            
            hist = combined[combined["hour_bin"] <= last_hour_bin]
            fig_forecast.add_trace(go.Scatter(
                x=hist["hour_bin"],
                y=hist["order_count"],
                mode='lines+markers',
                name="Historical",
                line=dict(color="#3498DB", width=3),
                marker=dict(size=6),
                hovertemplate="<b>Historical</b><br>%{x}<br>Orders: %{y}<extra></extra>"
            ))
            
            fcst = combined[combined["hour_bin"] > last_hour_bin]
            fig_forecast.add_trace(go.Scatter(
                x=fcst["hour_bin"],
                y=fcst["order_count"],
                mode='lines+markers',
                name="Forecast",
                line=dict(color="#27AE60", width=3, dash='dash'),
                marker=dict(size=6),
                hovertemplate="<b>Forecast</b><br>%{x}<br>Orders: %{y}<extra></extra>"
            ))
            
            fig_forecast.add_vrect(
                x0=future_df["hour_bin"].iloc[0],
                x1=future_df["hour_bin"].iloc[-1],
                fillcolor="#27AE60",
                opacity=0.1,
                layer="below",
                line_width=0
            )
            
            fig_forecast.update_layout(title="Demand Forecast", xaxis_title="Time", yaxis_title="Orders", height=450, hovermode='x unified')
            plot_chart(fig_forecast, "Forecast", height=450)
            
            # Stats
            st.markdown("### Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Peak Hour", f"{future_df.loc[future_df['order_count'].idxmax(), 'hour_bin'].hour}:00")
            with col2:
                st.metric("Peak Orders", f"{future_df['order_count'].max():.0f}")
            with col3:
                st.metric("Avg/hr", f"{future_df['order_count'].mean():.1f}")
            with col4:
                st.metric("Total", f"{future_df['order_count'].sum():.0f}")
            
            # Table
            st.markdown("### Hourly Details")
            display_df = future_df.copy()
            display_df["hour_bin"] = display_df["hour_bin"].dt.strftime("%Y-%m-%d %H:%M")
            display_df.columns = ["Hour", "Forecast"]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.warning("Need more historical data")
    else:
        st.info("Need larger date range")

# ========== TAB 5: RECOMMENDATIONS ==========
with tab5:
    st.markdown("## Smart Recommendations")
    st.markdown("Identify products frequently ordered together.")
    st.markdown("---")
    
    # Co-occurrence
    order_items = filtered_sales.groupby("order_id")["pizza_id"].apply(list).reset_index()
    from itertools import combinations
    co_occur = {}
    for items in order_items["pizza_id"]:
        if len(items) < 2:
            continue
        for pair in combinations(sorted(set(items)), 2):
            co_occur[pair] = co_occur.get(pair, 0) + 1
    
    if co_occur:
        st.markdown("### Product Pairings")
        rec_df = pd.DataFrame(
            [(p1, p2, cnt) for (p1, p2), cnt in co_occur.items()],
            columns=["pizza1", "pizza2", "count"]
        )
        rec_df = rec_df.sort_values("count", ascending=False)
        pizza_name_map = filtered_sales[["pizza_id", "name"]].drop_duplicates().set_index("pizza_id")["name"].to_dict()
        rec_df["pizza1_name"] = rec_df["pizza1"].map(pizza_name_map)
        rec_df["pizza2_name"] = rec_df["pizza2"].map(pizza_name_map)
        
        display_rec = rec_df[["pizza1_name", "pizza2_name", "count"]].head(10).copy()
        display_rec.columns = ["Product 1", "Product 2", "Co-Orders"]
        st.dataframe(display_rec, use_container_width=True, hide_index=True)
    else:
        st.info("Not enough paired data")
    
    # Item Recommendations
    st.markdown("---")
    st.markdown("### Cross-Sell")
    
    pizza_options = sorted(filtered_sales["name"].unique())
    selected_pizza = st.selectbox("Select product:", pizza_options)
    
    if selected_pizza:
        try:
            pid = filtered_sales[filtered_sales["name"] == selected_pizza]["pizza_id"].iloc[0]
            orders_with_pid = filtered_sales[filtered_sales["pizza_id"] == pid]["order_id"].unique()
            other_pizzas = filtered_sales[
                (filtered_sales["order_id"].isin(orders_with_pid)) & 
                (filtered_sales["pizza_id"] != pid)
            ]
            recs = other_pizzas.groupby("name").size().reset_index(name="frequency")
            recs = recs.sort_values("frequency", ascending=False).head(8)
            
            if len(recs) > 0:
                st.markdown(f"**Often ordered with {selected_pizza}:**")
                
                cols = st.columns(len(recs))
                for idx, (col, (_, row)) in enumerate(zip(cols, recs.iterrows())):
                    with col:
                        st.metric(row["name"], f"{row['frequency']:.0f}x")
            else:
                st.info("No recommendations")
        except:
            st.warning("Could not generate recommendations")

# ========== TAB 6: INGREDIENT INSIGHTS ==========
with tab6:
    st.markdown("## Ingredient Analytics")
    st.markdown("Analyze ingredient popularity and performance.")
    st.markdown("---")
    
    # Extract ingredients
    ing_list = []
    for _, row in filtered_sales.iterrows():
        if pd.notna(row["ingredients"]):
            for ing in row["ingredients"].split(","):
                ing_list.extend([ing.strip()] * int(row["quantity"]))
    
    if ing_list:
        ing_series = pd.Series(ing_list)
        top_ing = ing_series.value_counts().head(15).reset_index()
        top_ing.columns = ["ingredient", "count"]
        
        st.markdown("### Top Ingredients")
        fig_ing = go.Figure()
        fig_ing.add_trace(go.Bar(
            y=top_ing["ingredient"],
            x=top_ing["count"],
            orientation='h',
            marker=dict(color="#9B59B6", line=dict(color="#2C3E50", width=0.5)),
            hovertemplate="<b>%{y}</b><br>Orders: %{x}<extra></extra>"
        ))
        fig_ing.update_layout(title="Ingredient Frequency", xaxis_title="Orders", yaxis_title="", height=450)
        plot_chart(fig_ing, "Ingredients", height=450)
        
        # Performance
        st.markdown("---")
        st.markdown("### Performance")
        pizza_ing_sales = filtered_sales.groupby(["pizza_id", "name", "ingredients"])["quantity"].sum().reset_index()
        ing_performance = []
        for _, row in pizza_ing_sales.iterrows():
            if pd.notna(row["ingredients"]):
                for ing in row["ingredients"].split(","):
                    ing_performance.append({"ingredient": ing.strip(), "pizza_sales": row["quantity"]})
        
        if ing_performance:
            ing_perf_df = pd.DataFrame(ing_performance)
            ing_avg = ing_perf_df.groupby("ingredient")["pizza_sales"].mean().reset_index()
            ing_avg = ing_avg.sort_values("pizza_sales", ascending=False).head(10)
            
            fig_perf = go.Figure()
            fig_perf.add_trace(go.Bar(
                y=ing_avg["ingredient"],
                x=ing_avg["pizza_sales"],
                orientation='h',
                marker=dict(color="#1ABC9C", line=dict(color="#2C3E50", width=0.5)),
                hovertemplate="<b>%{y}</b><br>Avg Sales: %{x:.1f}<extra></extra>"
            ))
            fig_perf.update_layout(title="Performance", xaxis_title="Avg Units", yaxis_title="", height=400)
            plot_chart(fig_perf, "Performance", height=400)
    else:
        st.info("No ingredient data")

# ========== TAB 7: FULL REPORT ==========
with tab7:
    st.markdown("## Export Report")
    st.markdown("Download comprehensive analysis.")
    st.markdown("---")
    
    # Compile Report
    orders_copy = orders.copy()
    orders_copy["hour"] = orders_copy["datetime"].dt.hour
    orders_copy["day_of_week"] = orders_copy["datetime"].dt.dayofweek
    orders_copy["month"] = orders_copy["datetime"].dt.month
    orders_copy["is_weekend"] = (orders_copy["day_of_week"] >= 5).astype(int)
    
    X_time = orders_copy[["hour", "day_of_week", "month", "is_weekend"]]
    model_time = IsolationForest(contamination=0.05, random_state=42)
    orders_copy["anomaly"] = model_time.fit_predict(X_time)
    temporal_anomalies = orders_copy[orders_copy["anomaly"] == -1][["order_id", "date", "time"]].head(50)
    
    # Sales Anomalies
    pizza_sales_sum = filtered_sales.groupby(["name", "size", "category"]).agg({
        "quantity": "sum",
        "price": "first"
    }).reset_index()
    
    le = LabelEncoder()
    pizza_sales_sum["cat_code"] = le.fit_transform(pizza_sales_sum["category"])
    X_sales = pizza_sales_sum[["quantity", "price", "cat_code"]]
    model_sales = IsolationForest(contamination=0.1, random_state=42)
    pizza_sales_sum["sales_anomaly"] = model_sales.fit_predict(X_sales)
    sales_anomalies = pizza_sales_sum[pizza_sales_sum["sales_anomaly"] == -1][
        ["name", "size", "category", "quantity", "price"]
    ]
    
    # Summary
    st.markdown("### Contents")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Time Anomalies", len(temporal_anomalies))
    col2.metric("Sales Anomalies", len(sales_anomalies))
    col3.metric("Period", f"{start_date.date()}")
    col4.metric("Days", f"{(end_date - start_date).days}")
    
    st.markdown("---")
    
    if len(temporal_anomalies) > 0 or len(sales_anomalies) > 0:
        report_data = []
        
        if len(temporal_anomalies) > 0:
            temporal_anomalies["type"] = "Time"
            report_data.append(temporal_anomalies[["order_id", "date", "time", "type"]])
        
        if len(sales_anomalies) > 0:
            sales_anomalies["type"] = "Sales"
            report_data.append(sales_anomalies[["name", "type"]])
        
        if report_data:
            final_report = pd.concat(report_data, ignore_index=True)
            csv = final_report.to_csv(index=False)
            
            st.download_button(
                label=" Download Report (CSV)",
                data=csv,
                file_name=f"report_{start_date.date()}_{end_date.date()}.csv",
                mime="text/csv"
            )
            
            st.markdown("### Preview")
            st.dataframe(final_report.head(20), use_container_width=True, hide_index=True)
    else:
        st.success(" No anomalies detected")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(
    "Built with Streamlit • scikit-learn • Plotly | "
    "Isolation Forest • K-Means • Ridge Regression"
)
