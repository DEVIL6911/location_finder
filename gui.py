import streamlit as st
import folium
from streamlit_folium import folium_static
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from opencage.geocoder import OpenCageGeocode
import re

# Page configuration
st.set_page_config(
    page_title="📱 Phone Number Location Tracker",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
            
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .success-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(79, 172, 254, 0.3);
    }
    
    .error-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(250, 112, 154, 0.3);
    }
    
    .metric-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #667eea;
        font-size: 1.1rem;
        padding: 0.5rem;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">📱 Phone Number Location Tracker</h1>', unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.markdown("## 🔧 Configuration")
api_key = st.sidebar.text_input(
    "OpenCage API Key", 
    value="ENTER YOUR OWN API KEY HERE",
    type="password",
    help="Get your free API key from opencagedata.com"
)

st.sidebar.markdown("## ℹ️ About")
st.sidebar.info(
    "This application tracks the location of phone numbers using:\n"
    "- 📞 Phone number validation\n"
    "- 🌍 Geographic location\n" 
    "- 🏢 Carrier information\n"
    "- ⏰ Time zone details\n"
    "- 🗺️ Interactive mapping"
)

# Main content
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📞 Enter Phone Number")
    
    # Phone number input
    phone_input = st.text_input(
        "Phone Number",
        placeholder="e.g., +1234567890, +911234567890",
        help="Include country code (e.g., +1 for US, +91 for India)"
    )
    
    # Country code helper
    st.markdown("**Common Country Codes:**")
    country_codes = {
        "🇺🇸 United States": "+1",
        "🇬🇧 United Kingdom": "+44", 
        "🇮🇳 India": "+91",
        "🇩🇪 Germany": "+49",
        "🇫🇷 France": "+33",
        "🇯🇵 Japan": "+81"
    }
    
    selected_country = st.selectbox("Quick Select Country", ["Select..."] + list(country_codes.keys()))
    
    if selected_country != "Select...":
        suggested_number = country_codes[selected_country] + "XXXXXXXXXX"
        st.info(f"Format: {suggested_number}")
    
    # Track button
    track_button = st.button("🔍 Track Location", use_container_width=True)

with col2:
    st.markdown("### 🗺️ Location Map")
    
    if track_button and phone_input:
        try:
            # Validate and parse phone number
            with st.spinner("📡 Analyzing phone number..."):
                # Clean the input
                cleaned_number = re.sub(r'[^\d+]', '', phone_input)
                
                # Parse phone number
                parsed_number = phonenumbers.parse(cleaned_number, None)
                
                # Check if number is valid
                if not phonenumbers.is_valid_number(parsed_number):
                    st.markdown('<div class="error-card">❌ Invalid phone number format!</div>', unsafe_allow_html=True)
                    st.stop()
                
                # Get location information
                location = geocoder.description_for_number(parsed_number, "en")
                time_zones = timezone.time_zones_for_number(parsed_number)
                carrier_name = carrier.name_for_number(parsed_number, "en")
                
                # Display basic info
                st.markdown('<div class="success-card">✅ Phone number successfully analyzed!</div>', unsafe_allow_html=True)
                
                # Create metrics
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("📍 Location", location if location else "Unknown")
                    st.metric("🏢 Carrier", carrier_name if carrier_name else "Unknown")
                
                with col_b:
                    st.metric("🌍 Country Code", f"+{parsed_number.country_code}")
                    st.metric("⏰ Time Zone", time_zones[0] if time_zones else "Unknown")
            
            # Get coordinates using OpenCage
            if location and api_key:
                with st.spinner("🌍 Getting coordinates..."):
                    try:
                        geo_client = OpenCageGeocode(api_key)
                        results = geo_client.geocode(location)
                        
                        if results and len(results) > 0:
                            lat = results[0]['geometry']['lat']
                            lng = results[0]['geometry']['lng']
                            
                            # Create folium map
                            m = folium.Map(location=[lat, lng], zoom_start=8)
                            
                            # Add marker
                            folium.Marker(
                                [lat, lng],
                                popup=f"""
                                <div style="font-family: Arial; min-width: 200px;">
                                    <h4>📱 Phone Location</h4>
                                    <p><strong>📍 Location:</strong> {location}</p>
                                    <p><strong>🏢 Carrier:</strong> {carrier_name}</p>
                                    <p><strong>📞 Number:</strong> {phone_input}</p>
                                    <p><strong>📊 Coordinates:</strong><br>
                                    Lat: {lat:.4f}<br>
                                    Lng: {lng:.4f}</p>
                                </div>
                                """,
                                tooltip=f"Click for details about {phone_input}",
                                icon=folium.Icon(color='red', icon='phone', prefix='fa')
                            ).add_to(m)
                            
                            # Add circle for approximate area
                            folium.Circle(
                                location=[lat, lng],
                                radius=50000,  # 50km radius
                                popup="Approximate coverage area",
                                color='blue',
                                fillColor='lightblue',
                                fillOpacity=0.3
                            ).add_to(m)
                            
                            # Display map
                            folium_static(m, width=700, height=400)
                            
                            # Additional information
                            st.markdown("### 📊 Detailed Information")
                            
                            info_cols = st.columns(2)
                            with info_cols[0]:
                                st.markdown(f"""
                                <div class="metric-container">
                                    <h4>📞 Phone Details</h4>
                                    <p><strong>Original Number:</strong> {phone_input}</p>
                                    <p><strong>Formatted:</strong> {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}</p>
                                    <p><strong>National Format:</strong> {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)}</p>
                                    <p><strong>Country Code:</strong> +{parsed_number.country_code}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with info_cols[1]:
                                st.markdown(f"""
                                <div class="metric-container">
                                    <h4>🌍 Geographic Details</h4>
                                    <p><strong>Location:</strong> {location}</p>
                                    <p><strong>Coordinates:</strong> {lat:.6f}, {lng:.6f}</p>
                                    <p><strong>Carrier:</strong> {carrier_name if carrier_name else 'Not available'}</p>
                                    <p><strong>Time Zones:</strong> {', '.join(time_zones) if time_zones else 'Not available'}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                        else:
                            st.warning("🔍 Could not find precise coordinates for this location.")
                            st.info("Try using a more specific phone number or check if the number is correct.")
                            
                    except Exception as e:
                        st.error(f"❌ Geocoding error: {str(e)}")
                        st.info("Please check your OpenCage API key or try again later.")
            else:
                if not location:
                    st.warning("📍 Location information not available for this number.")
                if not api_key:
                    st.warning("🔑 Please enter your OpenCage API key in the sidebar.")
                    
        except phonenumbers.NumberParseException as e:
            st.markdown(f'<div class="error-card">❌ Error parsing phone number: {str(e)}</div>', unsafe_allow_html=True)
            st.info("💡 Make sure to include the country code (e.g., +1 for US numbers)")
            
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
    
    elif track_button and not phone_input:
        st.markdown('<div class="error-card">❌ Please enter a phone number!</div>', unsafe_allow_html=True)
    
    else:
        # Default map
        default_map = folium.Map(location=[20.5937, 78.9629], zoom_start=4)  # India center
        folium.Marker(
            [20.5937, 78.9629],
            popup="📱 Enter a phone number to track its location",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(default_map)
        folium_static(default_map, width=700, height=400)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🔒 <strong>Privacy Notice:</strong> This tool is for educational purposes only. 
    Always respect privacy laws and get proper consent before tracking phone numbers.</p>
    <p>Made with ❤️ using Streamlit | Get your free OpenCage API key at 
    <a href="https://opencagedata.com/" target="_blank">opencagedata.com</a></p>
</div>
""", unsafe_allow_html=True)

# Instructions in expander
with st.expander("📖 How to Use"):
    st.markdown("""
    ### Step-by-step Instructions:
    
    1. **Get an API Key** 🔑
       - Visit [OpenCage Data](https://opencagedata.com/) 
       - Sign up for a free account
       - Get your API key and enter it in the sidebar
    
    2. **Enter Phone Number** 📞
       - Include the country code (e.g., +1 for US, +91 for India)
       - Use the country selector for quick formatting help
       - Examples: +1234567890, +911234567890
    
    3. **Track Location** 🔍
       - Click the "Track Location" button
       - View the results on the interactive map
       - Check detailed information below the map
    
    ### Features:
    - ✅ Phone number validation
    - 🌍 Geographic location detection  
    - 🏢 Carrier/service provider identification
    - ⏰ Time zone information
    - 🗺️ Interactive map visualization
    - 📊 Detailed formatting and analysis
    
    ### Important Notes:
    - 🔒 Respect privacy and legal requirements
    - 📱 Results depend on available public data
    - 🌐 Some numbers may have limited location info
    - 🔑 Free API key allows 2,500 requests/day
    """)