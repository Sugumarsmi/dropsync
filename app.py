import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Page Config
st.set_page_config(layout="wide")

# Sample Data (Replace with real data input)
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        'partner': random.choices(['Delhivery', 'Xpressbees', 'Ekart', 'Aramex', 'Indiapost'], k=100),
        'orders': [random.randint(1, 10) for _ in range(100)],
        'location': random.choices(['Koramangala', 'HSR Layout', 'Whitefield', 'Electronic City'], k=100),
        'timestamp': pd.date_range(start='2025-01-01', periods=100, freq='H')
    })

# Sidebar - Real-time Delivery Input
st.sidebar.header("📌 Real-time Delivery Input")

# User selects a partner to add deliveries
selected_partner = st.sidebar.selectbox("Select Partner", ['Delhivery', 'Xpressbees', 'Ekart', 'Aramex', 'Indiapost'])
new_orders = st.sidebar.number_input("Number of New Orders", min_value=1, max_value=100, step=1)
selected_location = st.sidebar.selectbox("Select Location", ['Koramangala', 'HSR Layout', 'Whitefield', 'Electronic City'])

# Add Button
if st.sidebar.button("➕ Add Delivery"):
    new_entry = pd.DataFrame({'partner': [selected_partner], 'orders': [new_orders], 'location': [selected_location], 'timestamp': [pd.Timestamp.now()]})
    st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
    st.sidebar.success(f"Added {new_orders} orders for {selected_partner} in {selected_location}")

# Aggregate Before Optimization
partner_data_before = st.session_state.data.groupby('partner', as_index=False).agg({'orders': 'sum'})

# Optimize Orders: Merging Smaller Deliveries
optimized_data = partner_data_before.copy()
optimized_data['orders'] = optimized_data['orders'] * 0.85  # Assuming a 15% optimization

# Earnings Calculation (₹3 per delivery)
earnings_today = partner_data_before['orders'].sum() * 3
earnings_week = earnings_today * 7
earnings_month = earnings_today * 30

# Partner Savings Calculation (₹5 saved per optimized delivery)
partner_savings = partner_data_before.copy()
partner_savings['savings_per_day'] = partner_savings['orders'] * 5
partner_savings['savings_per_week'] = partner_savings['orders'] * 5 * 7
partner_savings['savings_per_month'] = partner_savings['orders'] * 5 * 30

# Metrics
fuel_saved = round(partner_data_before['orders'].sum() * 0.15, 2)
manpower_saved = int(partner_data_before['orders'].sum() * 0.1)
total_cost_saved = round(partner_data_before['orders'].sum() * 2.5, 2)

# Sidebar - Key Metrics
st.sidebar.header("📊 Order Processing Metrics")
st.sidebar.metric(label="🚚 Currently Active Drivers", value=10)
st.sidebar.metric(label="📦 Orders Processed Today", value=partner_data_before['orders'].sum())
st.sidebar.metric(label="📦 Orders Processed This Week", value=int(partner_data_before['orders'].sum() * 7))
st.sidebar.metric(label="📦 Orders Processed This Month", value=int(partner_data_before['orders'].sum() * 30))

st.sidebar.header("📉 Optimization Savings")
st.sidebar.metric(label="⛽ Fuel Saved (Liters)", value=fuel_saved)
st.sidebar.metric(label="👨‍🔧 Manpower Saved", value=manpower_saved)
st.sidebar.metric(label="💰 Total Cost Saved (INR)", value=total_cost_saved)

# Main Layout
st.title("📦 Delivery Optimization Dashboard")

# Row 1 - Before and After Optimization (Side-by-Side)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Before Optimization: Deliveries Per Partner")
    fig1 = px.bar(partner_data_before, x='partner', y='orders', title='Before Optimization', color='partner')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("After Optimization: Merged Deliveries")
    fig2 = px.bar(optimized_data, x='partner', y='orders', title='After Optimization', color='partner')
    st.plotly_chart(fig2, use_container_width=True)

# Row 2 - Comparison of Before and After Optimization
st.subheader("📊 Comparison of Orders Before and After Optimization")
fig3 = px.bar(
    pd.concat([partner_data_before.assign(stage='Before Optimization'), 
               optimized_data.assign(stage='After Optimization')]),
    x='partner', y='orders', color='stage', barmode='group', title="Order Comparison"
)
st.plotly_chart(fig3, use_container_width=True)

# Row 3 - Real-time Delivery Tracking & Location Visualization
st.subheader("📍 Real-time Delivery Tracking & Location Insights")
col3, col4 = st.columns(2)

with col3:
    fig4 = px.scatter_mapbox(
        st.session_state.data, lat=[12.9716]*100, lon=[77.5946]*100, color='partner', hover_name='partner',
        zoom=10, title="Delivery Locations (Bengaluru)"
    )
    fig4.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig4, use_container_width=True)

with col4:
    st.dataframe(st.session_state.data[['partner', 'orders', 'location']].sort_values(by="orders", ascending=False))

# Row 4 - Earnings Per Day, Week, and Month
st.subheader("💰 Revenue Earned as a Delivery Aggregator")
fig5 = px.bar(
    pd.DataFrame({'Period': ['Today', 'This Week', 'This Month'], 'Earnings (INR)': [earnings_today, earnings_week, earnings_month]}),
    x='Period', y='Earnings (INR)', title="Earnings Over Time", color='Period'
)
st.plotly_chart(fig5, use_container_width=True)

# Row 5 - Partner Savings Per Day, Week, Month
st.subheader("💸 Cost Savings Per Partner (Daily, Weekly, Monthly)")
fig6 = px.bar(
    partner_savings.melt(id_vars=['partner'], value_vars=['savings_per_day', 'savings_per_week', 'savings_per_month'], 
                         var_name='Time Period', value_name='Savings (INR)'),
    x='partner', y='Savings (INR)', color='Time Period', barmode='group', 
    title="Partner Savings Over Time"
)
st.plotly_chart(fig6, use_container_width=True)

# End of Dashboard
st.success("Dashboard Updated Successfully!")
