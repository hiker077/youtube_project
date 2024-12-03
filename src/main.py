from api.main import main

    
# if __name__ == "__main__":
#     main()





#     Data_Engineer_Project/
# │
# ├── youtube_project/
# │   ├── data/
# │   │   ├── raw/                    # Store raw, unprocessed data (e.g., initial API responses)
# │   │   ├── processed/              # Store cleaned and processed data
# │   │   └── README.md               # Document the purpose and usage of this folder
# │   │
# │   ├── src/                        # Source code for the project
# │   │   ├── api/                    # Code for interacting with APIs
# │   │   │   ├── youtube_api.py      # Handles YouTube API interactions
# │   │   │   └── __init__.py         # Makes the folder a Python package
# │   │   │
# │   │   ├── data_processing/        # Code for transforming data
# │   │   │   ├── processing.py       # Cleaning and processing raw data
# │   │   │   └── __init__.py         # Makes the folder a Python package
# │   │   │
# │   │   ├── dashboard/              # Code for the Dash dashboard
# │   │   │   ├── app.py              # Main dashboard application
# │   │   │   ├── layout.py           # Dashboard layout components
# │   │   │   ├── callbacks.py        # Dash callbacks
# │   │   │   └── __init__.py         # Makes the folder a Python package
# │   │   │
# │   │   ├── config/                 # Configuration files
# │   │   │   ├── settings.py         # Project-wide settings (e.g., API keys, paths)
# │   │   │   ├── logging_config.py   # Logging configuration
# │   │   │   └── __init__.py         # Makes the folder a Python package
# │   │   │
# │   │   ├── utils/                  # Utility functions used across the project
# │   │   │   ├── helpers.py          # General-purpose helper functions
# │   │   │   └── __init__.py         # Makes the folder a Python package
# │   │   │
# │   │   └── main.py                 # Entry point to run both API data retrieval and dashboard
# │   │
# │   ├── tests/                      # Tests for the project
# │   │   ├── test_api.py             # Tests for API functionality
# │   │   ├── test_processing.py      # Tests for data processing functions
# │   │   └── test_dashboard.py       # Tests for dashboard callbacks and layout
# │   │
# │   └── README.md                   # Overview and instructions for the project
# │
# ├── requirements.txt                # Python dependencies
# ├── setup.py                        # Optional: For making the project installable as a package
# └── .gitignore                      # Files and folders to ignore in version control
