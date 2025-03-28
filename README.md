# YouTube Dashboard Project

## 📋 Overview
This project provides a robust data visualization dashboard for analyzing YouTube channel statistics. It integrates data processing, a user-friendly interactive dashboard built with Dash and Plotly, and a structured backend architecture to handle the required computations and transformations.



![Screenshot dashboardu](assets/Screenshot_1.png)

![Screenshot dashboardu](assets/Screenshot_2.png)
---

## 🎬 Demo

[Link to video](assets/Video.mp4)
--- 

## 🌟 Features
- **Automated Data Retrieval**: Fetches data using the Google API.
- **Data Processing**: Cleans and transforms raw YouTube data for streamlined use in visualizations.
- **Interactive Dashboard**: Provides dynamic charts, filters and tables for intuitive exploration of video statistics.
- **KPI Metrics**: Displays key performance indicators such as average views, likes, and comments.
- **Customizable Filters**: Allows users to slice data based on date, category, and video duration.
---

## 🔧 Technology

- Python 3.8+
- Dash
- Pandas
- Plotly
- Requests (to API)
--- 

## 📦 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Recommended: Virtual environment tool (e.g., `venv` or `conda`)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hiker077/youtube_project.git 
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### ⚙️ Configuration

**Set Up Environment Variables**:
   - Copy `.env.share` to `.env`.
   - Update `.env` with your configurations. Define: 
     - API_KEY - API key generated by YouTube. 
     - CHANNEL_ID - YouTube channel_id that you gone analyse.

### 🚀 Run the Application**
   ```bash
   python src/main.py
   ```

**Access the Dashboard**:
   Open your web browser and navigate to `http://127.0.0.1:8050`.

---

## 🔍 Project Structure
```
.
├── data
│   ├── data_processed         # Contains processed data files.
│   ├── images                 # Stores images used in the dashboard (e.g., logos).
│   └── raw_data               # Raw input data files.
│
├── src
│   ├── api                    # Backend API module.
│   │   ├── __init__.py
│   │   └── main.py            # API endpoint definitions.
│   │
│   ├── config                 # Configuration files.
│   │   ├── __init__.py
│   │   └── logging_config.yaml
│   │
│   ├── dashboard              # Dashboard modules.
│   │   ├── __init__.py
│   │   ├── callbacks.py       # Callback functions for interactive dashboard components.
│   │   ├── layout.py          # Defines the layout of the dashboard.
│   │   └── utilities.py       # Helper functions for dashboard.
│   │
│   ├── data_processing        # Data transformation and preprocessing.
│   │   ├── __init__.py
│   │   └── utilities.py       # Data cleaning and filtering logic.
│   │
│   ├── logs                       # Stores application logs.
│   │   └── project.log
│   └── main.py
├── .env                       # Environment variables.
├── .env.share                 # Environment variables for sharing.
├── .gitignore                 # Git ignore file.
├── README.md                  # Project documentation.
└── requirements.txt           # Python dependencies.
```

---

## 🌱 Future Enhancements
- Improve responsiveness for mobile devices.
- Integrate additional APIs for enriched insights.
- Enable export of filtered data.
- Improvements of charts (x and y axis description)

---

## 📬 Contact

[Arkadiusz Kostrzewa] - [arkadiusz.kostrzewa92@gmail.com] - [www.linkedin.com/in/arkadiusz-kostrzewaa]


---
