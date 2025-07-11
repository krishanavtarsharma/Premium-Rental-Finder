import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import requests
from io import BytesIO
import random

# Set page configuration
st.set_page_config(
    page_title="🏠 Premium Rental Finder",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with real estate theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    body {
        background: linear-gradient(rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.95));
        color: #333;
    }
    
    .title {
        font-size: 3rem !important;
        font-weight: 800;
        background: linear-gradient(135deg, #4361ee, #3a0ca3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: fadeIn 1.5s ease;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #5a5a5a;
        text-align: center;
        margin-bottom: 2rem;
        animation: slideIn 1.2s ease;
    }
    
    .property-card {
        background: white;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(67, 97, 238, 0.15);
        margin-bottom: 30px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border-left: 5px solid #4361ee;
        overflow: hidden;
        position: relative;
        padding: 20px;
    }
    
    .property-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 30px rgba(67, 97, 238, 0.25);
    }
    
    .property-counter {
        background: linear-gradient(135deg, #4361ee, #3a0ca3);
        color: white;
        padding: 8px 20px;
        border-radius: 30px;
        font-size: 1rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 10px rgba(67, 97, 238, 0.25);
        animation: pulse 2s infinite;
    }
    
    .tag {
        display: inline-block;
        background: rgba(67, 97, 238, 0.15);
        color: #4361ee;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 5px 5px 0;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #4361ee, #3a0ca3) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(67, 97, 238, 0.3) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(67, 97, 238, 0.4) !important;
        background: linear-gradient(135deg, #3a0ca3, #4361ee) !important;
    }
    
    .stSelectbox, .stSlider, .stMultiSelect, .stTextInput, .stNumberInput {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        border: 2px solid #e0e0e0 !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        padding: 10px 15px !important;
    }
    
    .footer {
        text-align: center;
        color: #6c757d;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 2px dashed #4361ee;
    }
    
    .contact-form {
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        padding: 30px;
        border-radius: 16px;
        border: 2px solid #e0e0e0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    }
    
    .highlight {
        background: linear-gradient(120deg, #4cc9f0, #4361ee);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-weight: 700;
    }
    
    .animated-text {
        display: inline-block;
        animation: bounce 1.5s infinite;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4361ee, #3a0ca3);
        color: white;
        padding: 20px;
        border-radius: 0 20px 20px 0;
    }
    
    [data-testid="stSidebar"] .stSelectbox, 
    [data-testid="stSidebar"] .stSlider, 
    [data-testid="stSidebar"] .stMultiSelect {
        background-color: rgba(255,255,255,0.9) !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, 
    [data-testid="stSidebar"] h5, 
    [data-testid="stSidebar"] h6 {
        color: white !important;
    }
    
    /* Chart styling */
    .stPlotlyChart {
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        padding: 15px;
        background: white;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        height: 100%;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(67, 97, 238, 0.25);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
        color: #4361ee;
    }
    </style>
""", unsafe_allow_html=True)

# ========================
# DATA AND UTILITY FUNCTIONS
# ========================

# Property data with additional details
rental_data = {
    "Jaipur": [
        {
            "name": "Shree Residency Premium",
            "rent": 8000,
            "rooms": 2,
            "address": "Vaishali Nagar, Jaipur",
            "image": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=600&q=80",
            "tags": ["Balcony", "Parking", "24/7 Security", "WiFi"],
            "property_type": "Apartment",
            "furnishing": "Semi-Furnished",
            "area": 850,
            "posted": "2023-05-15",
            "rating": 4.3,
            "agent": "Raj Properties",
            "agent_rating": 4.7
        },
        {
            "name": "Pink City Villas",
            "rent": 12000,
            "rooms": 3,
            "address": "Mansarovar, Jaipur",
            "image": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=600&q=80",
            "tags": ["Swimming Pool", "Gym", "Garden", "AC"],
            "property_type": "Villa",
            "furnishing": "Fully Furnished",
            "area": 1200,
            "posted": "2023-06-20",
            "rating": 4.7,
            "agent": "Pink City Realty",
            "agent_rating": 4.9
        },
        {
            "name": "Amber Residences",
            "rent": 15000,
            "rooms": 3,
            "address": "C-Scheme, Jaipur",
            "image": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=600&q=80",
            "tags": ["Furnished", "Pet Friendly", "AC", "Parking"],
            "property_type": "Apartment",
            "furnishing": "Fully Furnished",
            "area": 1100,
            "posted": "2023-07-05",
            "rating": 4.5,
            "agent": "Amber Estates",
            "agent_rating": 4.6
        },
        {
            "name": "Royal Gardens",
            "rent": 10000,
            "rooms": 2,
            "address": "Malviya Nagar, Jaipur",
            "image": "https://images.unsplash.com/photo-1575517111839-3a3843ee7f5d?auto=format&fit=crop&w=600&q=80",
            "tags": ["Garden", "Parking", "24/7 Security"],
            "property_type": "Apartment",
            "furnishing": "Unfurnished",
            "area": 950,
            "posted": "2023-08-10",
            "rating": 4.2,
            "agent": "Royal Properties",
            "agent_rating": 4.4
        }
    ],
    "Delhi": [
        {
            "name": "Urban Heights Elite",
            "rent": 15000,
            "rooms": 2,
            "address": "Rohini, Delhi",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80",
            "tags": ["Modern Kitchen", "Lift", "Power Backup"],
            "property_type": "Apartment",
            "furnishing": "Semi-Furnished",
            "area": 900,
            "posted": "2023-06-25",
            "rating": 4.4,
            "agent": "Delhi Homes",
            "agent_rating": 4.8
        },
        {
            "name": "Capital Homes",
            "rent": 22000,
            "rooms": 3,
            "address": "Dwarka, Delhi",
            "image": "https://images.unsplash.com/photo-1600585154076-7c1c2b69a511?auto=format&fit=crop&w=600&q=80",
            "tags": ["Club House", "Play Area", "Maintenance"],
            "property_type": "Apartment",
            "furnishing": "Fully Furnished",
            "area": 1150,
            "posted": "2023-07-15",
            "rating": 4.6,
            "agent": "Capital Realty",
            "agent_rating": 4.7
        },
        {
            "name": "Connaught Luxury",
            "rent": 35000,
            "rooms": 3,
            "address": "Connaught Place, Delhi",
            "image": "https://images.unsplash.com/photo-1505691723518-36a5ac3be353?auto=format&fit=crop&w=600&q=80",
            "tags": ["Penthouse", "City View", "Smart Home"],
            "property_type": "Penthouse",
            "furnishing": "Fully Furnished",
            "area": 1800,
            "posted": "2023-08-01",
            "rating": 4.9,
            "agent": "Luxury Estates",
            "agent_rating": 4.9
        }
    ],
    "Mumbai": [
        {
            "name": "Sea View Towers",
            "rent": 30000,
            "rooms": 2,
            "address": "Bandra West, Mumbai",
            "image": "https://images.unsplash.com/photo-1600585154350-8121a5e243b2?auto=format&fit=crop&w=600&q=80",
            "tags": ["Sea Facing", "Modular Kitchen", "Park"],
            "property_type": "Apartment",
            "furnishing": "Fully Furnished",
            "area": 1000,
            "posted": "2023-07-10",
            "rating": 4.8,
            "agent": "Coastal Properties",
            "agent_rating": 4.8
        },
        {
            "name": "Skyline Premium",
            "rent": 35000,
            "rooms": 3,
            "address": "Andheri West, Mumbai",
            "image": "https://images.unsplash.com/photo-1600585154346-1e8d9a0c6116?auto=format&fit=crop&w=600&q=80",
            "tags": ["High Ceiling", "Concierge", "WiFi"],
            "property_type": "Apartment",
            "furnishing": "Fully Furnished",
            "area": 1250,
            "posted": "2023-08-05",
            "rating": 4.7,
            "agent": "Skyline Realty",
            "agent_rating": 4.7
        },
        {
            "name": "Marine Drive Residences",
            "rent": 50000,
            "rooms": 4,
            "address": "Marine Drive, Mumbai",
            "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=600&q=80",
            "tags": ["Luxury", "Beach Access", "Serviced"],
            "property_type": "Penthouse",
            "furnishing": "Fully Furnished",
            "area": 2200,
            "posted": "2023-08-15",
            "rating": 5.0,
            "agent": "Oceanfront Estates",
            "agent_rating": 4.9
        }
    ]
}

# Create a DataFrame for analytics
def create_analytics_df():
    data = []
    for city, properties in rental_data.items():
        for prop in properties:
            data.append({
                "City": city,
                "Rent": prop["rent"],
                "Rooms": prop["rooms"],
                "Property Type": prop["property_type"],
                "Area": prop["area"],
                "Rating": prop["rating"],
                "Furnishing": prop["furnishing"]
            })
    return pd.DataFrame(data)

# ========================
# SIDEBAR
# ========================
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: white;'>🏠 Rental Finder</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; margin-bottom: 30px;'><span class='animated-text'>🔍</span> Find your dream home</div>", unsafe_allow_html=True)
    
    # User profile section
    st.markdown("### 👤 User Profile")
    user_name = st.text_input("Name", "Krishan Sharma")
    user_email = st.text_input("Email", "krishan@example.com")
    user_phone = st.text_input("Phone", "+91 9876543210")
    
    st.markdown("---")
    
    # Advanced filters
    st.markdown("### 🔍 Advanced Filters")
    area = st.selectbox("📍 Select City", ["", "Jaipur", "Delhi", "Mumbai"], index=0)
    
    if area:
        min_rent, max_rent = st.slider(
            "💰 Monthly Rent Range (₹)", 
            5000, 
            60000, 
            (5000, 40000), 
            step=1000
        )
        
        selected_bhk = st.multiselect(
            "🛏️ BHK Configuration", 
            [1, 2, 3, 4], 
            default=[1, 2, 3]
        )
        
        # FIXED: Corrected property types assignment
        property_types = list(set([p["property_type"] for p in rental_data[area]]))
        selected_types = st.multiselect(
            "🏢 Property Type", 
            property_types, 
            default=property_types
        )
        
        furnishing_options = ["Fully Furnished", "Semi-Furnished", "Unfurnished"]
        selected_furnishing = st.multiselect(
            "🪑 Furnishing Type", 
            furnishing_options, 
            default=furnishing_options
        )
        
        min_rating = st.slider(
            "⭐ Minimum Rating", 
            1.0, 
            5.0, 
            4.0, 
            step=0.1
        )
        
        min_area = st.slider(
            "📏 Minimum Area (sq ft)", 
            500, 
            3000, 
            800, 
            step=50
        )
        
        sort_order = st.selectbox(
            "📊 Sort By", 
            ["Rent: Low to High", "Rent: High to Low", "Rating: High to Low", "Newest First"],
            index=0
        )
        
        st.markdown("---")
        
        # Save search button
        if st.button("💾 Save Search Preferences", use_container_width=True):
            st.success("Search preferences saved!")

# ========================
# MAIN CONTENT
# ========================

# Header section
st.markdown(
    """
    <p class="title">
        <span class="animated-text">🏠</span> Premium <span class="highlight">Rental</span> Finder
    </p>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    """
    <p class="subtitle">
        Find your <span class="highlight">dream home</span> with our curated selection of premium properties
    </p>
    """, 
    unsafe_allow_html=True
)

# Property listings section
if area:
    # Filter properties
    filtered = [
        p for p in rental_data[area]
        if min_rent <= p["rent"] <= max_rent 
        and p["rooms"] in selected_bhk
        and p["property_type"] in selected_types
        and p["furnishing"] in selected_furnishing
        and p["rating"] >= min_rating
        and p["area"] >= min_area
    ]
    
    # Sorting
    if sort_order == "Rent: Low to High":
        filtered.sort(key=lambda x: x["rent"])
    elif sort_order == "Rent: High to Low":
        filtered.sort(key=lambda x: x["rent"], reverse=True)
    elif sort_order == "Rating: High to Low":
        filtered.sort(key=lambda x: x["rating"], reverse=True)
    
    # Property counter
    st.markdown(f'<div class="property-counter">{len(filtered)} Properties Found in {area}</div>', unsafe_allow_html=True)
    
    if filtered:
        # Create columns for property display
        cols = st.columns(2)
        
        for i, prop in enumerate(filtered):
            with cols[i % 2]:
                with st.container():
                    st.markdown(f"<div class='property-card'>", unsafe_allow_html=True)
                    
                    # Property image with error handling
                    try:
                        response = requests.get(prop["image"], timeout=10)
                        if response.status_code == 200:
                            img = Image.open(BytesIO(response.content))
                            st.image(img, use_column_width=True, caption=prop["name"])
                        else:
                            st.error("Failed to load property image")
                    except Exception as e:
                        st.error(f"Error loading image: {str(e)}")
                    
                    # Property details
                    st.markdown(f"<h3 style='color:#3a0ca3;'>{prop['name']}</h3>", unsafe_allow_html=True)
                    
                    # Price and rating
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"<h4>₹{prop['rent']}/month</h4>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<div style='background:#e6eeff; border-radius:20px; padding:5px 10px; text-align:center;'>"
                                    f"<span style='color:#ff9800; font-weight:bold;'>★</span> {prop['rating']}/5.0</div>", 
                                    unsafe_allow_html=True)
                    
                    # Details
                    st.markdown(f"""
                        <div style="margin:15px 0;">
                            <div style="display:flex; justify-content:space-between;">
                                <div>🛏️ <strong>{prop['rooms']} BHK</strong></div>
                                <div>🏢 <strong>{prop['property_type']}</strong></div>
                            </div>
                            <div style="display:flex; justify-content:space-between; margin-top:10px;">
                                <div>📏 <strong>{prop['area']} sq ft</strong></div>
                                <div>🪑 <strong>{prop['furnishing']}</strong></div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Tags
                    st.markdown('<div style="margin:15px 0;">', unsafe_allow_html=True)
                    for tag in prop.get("tags", []):
                        st.markdown(f'<span class="tag">{tag}</span>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Address and agent
                    st.markdown(f"<div style='margin:10px 0;'>📍 {prop['address']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div>🤝 Agent: {prop['agent']} (⭐ {prop['agent_rating']})</div>", unsafe_allow_html=True)
                    
                    # Action buttons
                    col1, col2, col3 = st.columns([2,2,1])
                    with col1:
                        if st.button("📞 Contact Agent", key=f"contact_{i}", use_container_width=True):
                            st.session_state.selected_property = prop
                    with col2:
                        if st.button("💖 Save Property", key=f"save_{i}", use_container_width=True):
                            st.success(f"Saved {prop['name']} to your favorites!")
                    with col3:
                        maps_url = f"https://www.google.com/maps/search/?api=1&query={prop['address'].replace(' ', '+')}"
                        st.markdown(f'<a href="{maps_url}" target="_blank" style="text-decoration:none; color:white;"><button style="width:100%; height:100%; background:#4361ee; border:none; border-radius:8px; color:white; padding:8px;">🗺️</button></a>', unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No properties found matching your criteria. Try adjusting your filters.")
        st.image("https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=600&q=80", 
                 caption="Find your dream home with us", use_column_width=True)
    
    # Analytics section
    st.markdown("---")
    st.markdown("## 📊 Market Insights")
    
    analytics_df = create_analytics_df()
    city_df = analytics_df[analytics_df['City'] == area]
    
    # Create tabs for different analytics
    tab1, tab2, tab3, tab4 = st.tabs(["Rent Distribution", "Property Types", "Area vs Rent", "Market Trends"])
    
    with tab1:
        st.markdown(f"### Rent Distribution in {area}")
        if not city_df.empty:
            fig = px.histogram(city_df, x="Rent", nbins=20, color_discrete_sequence=['#4361ee'])
            fig.update_layout(bargap=0.1)
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics
            avg_rent = city_df['Rent'].mean()
            med_rent = city_df['Rent'].median()
            col1, col2 = st.columns(2)
            col1.metric("Average Rent", f"₹{int(avg_rent):,}/month")
            col2.metric("Median Rent", f"₹{int(med_rent):,}/month")
        else:
            st.warning("No data available for analytics in this area")
    
    with tab2:
        st.markdown(f"### Property Types in {area}")
        if not city_df.empty:
            type_counts = city_df['Property Type'].value_counts().reset_index()
            type_counts.columns = ['Property Type', 'Count']
            fig = px.pie(type_counts, names='Property Type', values='Count', 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for property types")
    
    with tab3:
        st.markdown(f"### Area vs Rent in {area}")
        if not city_df.empty:
            fig = px.scatter(city_df, x="Area", y="Rent", color="Property Type",
                             hover_name="Property Type", size_max=20,
                             color_discrete_sequence=['#4361ee', '#3a0ca3', '#7209b7'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for area vs rent")
    
    with tab4:
        st.markdown(f"### Rental Trends in {area}")
        
        # Generate trend data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
        avg_rents = [15000, 15200, 15500, 15700, 16000, 16200, 16500, 16800]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=avg_rents, 
                                 mode='lines+markers', 
                                 name='Average Rent',
                                 line=dict(color='#4361ee', width=3)))
        fig.update_layout(title='Monthly Average Rent Trend',
                          xaxis_title='Month',
                          yaxis_title='Average Rent (₹)')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Market Insights")
        st.info("""
        - Rental prices in **{area}** have increased by **12%** over the past year
        - Demand for **3 BHK apartments** has grown by **18%** in the last quarter
        - The **{popular_area}** area has seen the highest price appreciation
        """.format(area=area, popular_area=random.choice(["Vaishali Nagar", "Mansarovar", "C-Scheme"])))
    
    # Contact form
    st.markdown("---")
    st.markdown("## 📝 Contact an Agent")
    
    with st.form("contact_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name*", "Krishan Sharma")
        with col2:
            email = st.text_input("Email*", "krishan@example.com")
        
        phone = st.text_input("Phone*", "+91 9876543210")
        
        # Create list of property names with rent info
        property_options = [f"{p['name']} (₹{p['rent']}/month)" for p in filtered] if filtered else ["Select a property"]
        selected_property = st.selectbox("Select Property*", property_options)
        
        message = st.text_area("Message", "I'm interested in this property and would like to schedule a viewing...", height=150)
        
        submitted = st.form_submit_button("📨 Submit Inquiry")
        if submitted:
            if name and email and phone:
                # Extract clean property name
                clean_property = selected_property.split(' (₹')[0]
                st.success(f"✨ Thank you {name}! Your inquiry for **{clean_property}** has been submitted. An agent will contact you within 24 hours.")
                
                # Show confirmation animation
                with st.spinner("Sending your inquiry..."):
                    time.sleep(2)
                    st.balloons()
            else:
                st.error("Please fill all required fields (marked with *)")
    
    # Features section
    st.markdown("---")
    st.markdown("## 🌟 Why Choose Us?")
    
    features = [
        {"icon": "🔍", "title": "Verified Listings", "desc": "All properties are personally verified by our team"},
        {"icon": "💰", "title": "No Brokerage Fees", "desc": "Save money with our zero brokerage policy"},
        {"icon": "📱", "title": "Mobile App", "desc": "Access properties on the go with our mobile application"},
        {"icon": "🛡️", "title": "Rental Agreement", "desc": "Free legal assistance for rental agreements"},
        {"icon": "🔑", "title": "Quick Move-in", "desc": "Most properties available for immediate occupancy"},
        {"icon": "📊", "title": "Market Insights", "desc": "Get expert analysis of rental market trends"}
    ]
    
    cols = st.columns(3)
    for i, feature in enumerate(features):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{feature['icon']}</div>
                    <h3>{feature['title']}</h3>
                    <p>{feature['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# City selection prompt
else:
    st.info("👈 Please select a city from the sidebar to start exploring properties")
    
    # Show city highlights
    st.markdown("## 🏙️ Popular Cities")
    
    cities = [
        {"name": "Jaipur", "image": "https://images.unsplash.com/photo-1597586124394-fbd6ef244026?auto=format&fit=crop&w=600&q=80", 
         "desc": "The Pink City with heritage properties"},
        {"name": "Delhi", "image": "https://images.unsplash.com/photo-1580651214613-f4692d6d138f?auto=format&fit=crop&w=600&q=80", 
         "desc": "India's capital with diverse neighborhoods"},
        {"name": "Mumbai", "image": "https://images.unsplash.com/photo-1567599758401-5f8f8c0f0e4d?auto=format&fit=crop&w=600&q=80", 
         "desc": "Financial capital with sea-view apartments"}
    ]
    
    cols = st.columns(3)
    for i, city in enumerate(cities):
        with cols[i]:
            st.image(city["image"], use_column_width=True)
            st.markdown(f"<h3 style='text-align:center;'>{city['name']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;'>{city['desc']}</p>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align:center;'><a href='#')>Explore Properties</a></div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div class="footer">
        <p style="font-size: 1.1rem; font-weight: 600; color: #4361ee; margin-bottom: 10px;">
            <span class="animated-text">🏠</span> Premium Rental Finder
        </p>
        <p style="margin-bottom: 5px;">🌐 Find your perfect home with our curated selection of premium properties</p>
        <p style="margin-top: 15px;">📞 +91 9876543210 | ✉️ info@rentalfinder.com | 🌐 www.rentalfinder.com</p>
        <p style="margin-top: 20px;">© 2023 Premium Rental Finder. All rights reserved.</p>
    </div>
    """, 
    unsafe_allow_html=True
)