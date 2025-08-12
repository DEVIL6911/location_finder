# 📱 Phone Number Location Tracker

An interactive **Phone Number Location Tracker** built with **Python**, **Streamlit**, and **Folium**.  
This application validates phone numbers, detects their location & carrier details, and visualizes them on an **interactive map**.  

---

## 🚀 Features

- **📞 Phone Number Validation**
- **🌍 Geographic Location Detection**
- **🏢 Carrier / Service Provider Identification**
- **⏰ Time Zone Information**
- **🗺️ Interactive Map Visualization**
- **📊 Detailed Formatting & Analysis**

---

## 🛠 Tech Stack

- **[Streamlit](https://streamlit.io/)** – UI framework
- **[phonenumbers](https://pypi.org/project/phonenumbers/)** – Number validation & details
- **[Folium](https://python-visualization.github.io/folium/)** – Interactive maps
- **[OpenCage Geocoder API](https://opencagedata.com/)** – Geocoding services
- **Python Libraries:** `re`, `streamlit-folium`

---

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone  https://github.com/DEVIL6911/location_finder.git
   cd phone-number-tracker

Create Virtual Environment (Optional but recommended)

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Get Your OpenCage API Key

Visit opencagedata.com

Sign up for a free account

Get your API key

▶ Usage
Run the Streamlit app:

bash
Copy
Edit
streamlit run app.py
Enter your OpenCage API Key in the sidebar.

Enter the phone number with country code
Example: +1234567890 or +911234567890

Click Track Location to:

View details in a clean dashboard

See the location on an interactive map


