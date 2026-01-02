# FAA NOTAM Search & Filter Tool

A robust Python utility and Dashboard designed to interface with the FAA Federal NOTAM System (FNS). This tool provides specialized filtering for aviation professionals, allowing for precise runway-specific data extraction and general keyword searches.

## 🚀 Features
*   **Secure Authentication**: Handles OAuth2 client credentials flow with automatic token refreshing.
*   **Streamlit Dashboard**: A full GUI for monitoring multiple airports and running ad-hoc searches.
*   **Dual-Layer Search Logic**:
    *   **Keyword Mode**: Case-insensitive substring and Regex matching.
    *   **Runway Mode**: Advanced Regex logic to isolate specific runway designations.

## 🛠 Installation & Deployment

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Secrets**
    The app requires FAA API credentials.
    *   **Local Development**: Create a file at `.streamlit/secrets.toml`:
        ```toml
        FAA_ID = "your_client_id"
        FAA_SECRET = "your_client_secret"
        ```
    *   **Streamlit Cloud**: Add the same keys to the **Secrets** section in the app settings.

3.  **Run the Dashboard**
    ```bash
    streamlit run streamlit_app.py
    ```

## 📂 Project Structure
*   `faa_notam_lib.py`: Core library for FAA API interaction with auto-token renewal.
*   `streamlit_app.py`: Main dashboard (Batch Search enabled).
*   `.streamlit/secrets.toml`: (Local only) Secure credentials storage.

## 📖 Search Logic Documentation
### 1. The Runway Regex
To avoid "False Positives", the tool uses a specific pattern:
*   **Anchor**: Requires the keyword `RWY` or `RUNWAY`.
*   **Isolation**: Uses Negative Lookbehind `(?<!\d)` and Lookahead `(?![0-9])` to ensure a search for `7` doesn't match `17` or `27`.

### 2. Batch Search
*   **Caching**: Results are cached in session state to allow instant Expand/Collapse without re-hitting the API.
*   **Ordering**: Results strictly follow the order of the source table.
*   **Normalization**: All inputs are automatically converted to uppercase for robust matching.

## ⚠️ Notes
This tool is configured to handle `NotOpenSSLWarning` typically seen on macOS systems using LibreSSL. The filtering is handled at the entry point of the application to ensure clean terminal output.