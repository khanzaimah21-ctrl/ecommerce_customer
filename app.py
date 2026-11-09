import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ecommerce Customer EDA", layout="wide")

st.title("Ecommerce Customer EDA Dashboard")
st.write("Analysis of 500 customers - What makes customers spend more?")

@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_customers.csv")
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")

min_member, max_member = st.sidebar.slider(
    "Length of Membership (Years)",
    float(df['Length of Membership'].min()),
    float(df['Length of Membership'].max()),
    (float(df['Length of Membership'].min()), float(df['Length of Membership'].max()))
)

min_app, max_app = st.sidebar.slider(
    "Time on App (Mins)",
    float(df['Time on App'].min()),
    float(df['Time on App'].max()),
    (float(df['Time on App'].min()), float(df['Time on App'].max()))
)

# Apply Filters
filtered_df = df[
    (df['Length of Membership'] >= min_member) &
    (df['Length of Membership'] <= max_member) &
    (df['Time on App'] >= min_app) &
    (df['Time on App'] <= max_app)
]

# --- 4 KPIs ---
st.subheader("Key Numbers")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Yearly Spent", f"${filtered_df['Yearly Amount Spent'].mean():.2f}")
col2.metric("Total Customers", len(filtered_df))
col3.metric("Avg Membership", f"{filtered_df['Length of Membership'].mean():.2f} Years")
col4.metric("Avg Time on App", f"{filtered_df['Time on App'].mean():.2f} Mins")

st.markdown("---")

# --- GRAPH 1 + 2 ---
c1, c2 = st.columns(2)
with c1:
    st.subheader("1. Distribution of Yearly Amount Spent")
    fig1 = px.histogram(filtered_df, x="Yearly Amount Spent", nbins=30, title="Most customers spend 450-550 USD")
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("2. Length of Membership vs Spending")
    fig2 = px.scatter(filtered_df, x="Length of Membership", y="Yearly Amount Spent", title="Longer Membership = More Spending (0.81)")
    st.plotly_chart(fig2, use_container_width=True)

# --- GRAPH 3 + 4 ---
c3, c4 = st.columns(2)
with c3:
    st.subheader("3. Time on App vs Spending")
    fig3 = px.scatter(filtered_df, x="Time on App", y="Yearly Amount Spent", title="App Time Increases Spending (0.50)")
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.subheader("4. Time on Website vs Spending")
    fig4 = px.scatter(filtered_df, x="Time on Website", y="Yearly Amount Spent", title="Website Time Has No Effect (-0.00)")
    st.plotly_chart(fig4, use_container_width=True)

# --- GRAPH 5 + HEATMAP ---
c5, c6 = st.columns(2)
with c5:
    st.subheader("5. Avg Session Length vs Spending")
    fig5 = px.scatter(filtered_df, x="Avg. Session Length", y="Yearly Amount Spent", title="Weak Relationship (0.36)")
    st.plotly_chart(fig5, use_container_width=True)

with c6:
    st.subheader("6. Correlation Heatmap")
    fig, ax = plt.subplots()
    sns.heatmap(filtered_df[['Avg. Session Length','Time on App','Time on Website','Length of Membership','Yearly Amount Spent']].corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

st.markdown("---")

# --- FINDINGS + CHECKBOX ---
st.subheader("Key Findings & Business Recommendation")
st.write("1. **Length of Membership is the strongest driver (0.81).** Loyal / old customers spend much more.")
st.write("2. **Time on App is the second driver (0.50).** Customers who spend more time on App, spend more.")
st.write("3. **Time on Website has almost zero correlation (-0.00).** Customers spend 37 mins on Website but it does not increase spending.")
st.write("4. **Recommendation:** Company should invest in the **App**, not the Website.")

if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)