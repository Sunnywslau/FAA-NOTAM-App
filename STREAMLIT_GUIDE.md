# 🚀 Streamlit Dashboard Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Dashboard
```bash
streamlit run streamlit_app.py
```

The dashboard will automatically open in your web browser at `http://localhost:8501`

---

## Dashboard Overview

The dashboard features **three tabs** for different use cases:

1. **🖥️ Monitor Dashboard** - Multi-airport batch monitoring for flight dispatchers
2. **⚙️ Manage Profile** - Create and manage monitoring profiles
3. **🔍 Single Search** - Traditional single airport search

---

## Tab 1: Monitor Dashboard 🖥️

### Purpose
Designed for flight dispatchers who need to monitor multiple airports and specific criteria simultaneously.

### Features
- **Batch Search**: Search multiple airports at once
- **Profile-Based**: Load pre-configured search criteria
- **Real-Time Metrics**: 
  - Total Airports Searched
  - Total NOTAMs Found
  - Last Search Timestamp
- **Color-Coded Results**:
  - 🔴 Red (5+ NOTAMs)
  - 🟡 Yellow (1-4 NOTAMs)
  - 🟢 Green (0 NOTAMs)
- **Grouped Display**: Results organized by airport and criteria type

### How to Use
1. Go to **Manage Profile** tab to create/upload your profile
2. Return to **Monitor Dashboard**
3. Set timeout (10-60 seconds)
4. Click **🔄 Refresh All**
5. View results with metrics and detailed NOTAMs

### No Caching
Every "Refresh All" performs a fresh search using the current profile - no stale data!

---

## Tab 2: Manage Profile ⚙️

### Profile Format
CSV file with three columns:
```csv
FIR/AIRPORT,Type,Keyword
VHHH,Runway,25R|07L
YBBB,Keyword,Tindal|restriction
KJFK,Runway,22L|04R
KLAX,Keyword,CRANE|CLOSED
```

### Column Definitions
- **FIR/AIRPORT**: 4-letter ICAO code (e.g., KJFK, VHHH, CYYZ)
- **Type**: Either `Runway` or `Keyword`
- **Keyword**: 
  - For Runway: Runway identifiers separated by `|` (e.g., `25R|07L`)
  - For Keyword: Search terms separated by `|` (e.g., `CRANE|CLOSED`)
  - Supports regex patterns (e.g., `TWY.*CLSD`)

### Features
- **📁 Upload CSV**: Import existing profiles
- **✏️ Edit In-App**: 
  - Add/remove rows dynamically
  - Modify any field
  - Dynamic row management
- **💾 Save Changes**: Explicit save button (no auto-save)
- **📥 Download CSV**: Export current profile with timestamp

### Workflow
1. Upload CSV or start with empty profile
2. Edit entries (add/delete/modify rows)
3. Click **💾 Save Changes**
4. Switch to Monitor Dashboard to use the profile
5. Download updated profile for future use

---

## Tab 3: Single Search 🔍 (Original Features)

### Features

### 📊 **Summary View**
- View airport name and total NOTAM count
- See NOTAMs categorized by type
- Quick overview without detailed data

### 📋 **All NOTAMs**
- Display all NOTAMs for an airport
- Formatted in standard Q-code format
- Download results as text file
- Real-time pagination (retrieves up to 500 NOTAMs)

### 🛫 **Runway-Specific Search**
- Filter NOTAMs by runway identifier
- Example: Search for "22L", "04R", "31"
- Matches patterns like:
  - `RWY 05`
  - `RWY 31L/05`
  - `RWY 05/31L`
- View detailed NOTAM data in expandable sections
- Download filtered results

### 🔍 **Keyword Search**
- Simple text search: `CRANE`, `CLOSED`, `NAV`
- Regex patterns: `TWY.*CLSD`, `LGT.*U/S`
- Choose search fields:
  - **all** - Search across all text fields
  - **icaoMessage** - Search in Q-code message
  - **keyword** - Search in NOTAM keyword field
  - **traditionalMessage** - Search in traditional format
  - **plainLanguage** - Search in plain language description
- Auto-detection of regex patterns
- Case-insensitive matching
- View results in table format
- Download search results

---

## Usage Examples

### Example 1: Check JFK Airport
1. Enter `KJFK` in the airport code field
2. Select "All NOTAMs"
3. Click "Search"
4. View all 150+ NOTAMs
5. Download if needed

### Example 2: Check Runway 22L at LAX
1. Enter `KLAX` in the airport code field
2. Select "Runway Specific"
3. Enter `22L` as runway code
4. Click "Search"
5. View only NOTAMs affecting Runway 22L

### Example 3: Find All Cranes at ORD
1. Enter `KORD` in the airport code field
2. Select "Keyword Search"
3. Enter `CRANE` as keyword
4. Select search field: "all"
5. Click "Search"
6. View all crane-related NOTAMs

### Example 4: Find Taxiway Closures with Regex
1. Enter `KJFK` in the airport code field
2. Select "Keyword Search"
3. Enter `TWY.*CLSD` as pattern
4. Check "Use Regex Pattern"
5. Click "Search"
6. View all taxiway closures

---

## Common Search Patterns

### Keywords
- `CRANE` - Construction obstacles
- `CLOSED` - Any closures
- `NAV` - Navigation aids
- `OBSTRUCTION` - Obstacles
- `LIGHTING` - Lighting issues

### Regex Patterns
- `TWY.*CLSD` - Taxiway closures (TWY followed by anything, then CLSD)
- `RWY.*CLSD` - Runway closures
- `LGT.*U/S` - Lighting unserviceable (U/S = out of service)
- `CRANE|RIG|TOWER` - Multiple keywords (OR operator)
- `NAV.*OUT` - Navigation aids out of service

---

## Popular Airport Codes

### United States
- `KJFK` - New York JFK International
- `KLAX` - Los Angeles International
- `KORD` - Chicago O'Hare
- `KATL` - Atlanta Hartsfield-Jackson
- `KDFW` - Dallas/Fort Worth
- `KSFO` - San Francisco International
- `KLAS` - Las Vegas McCarran
- `KMIA` - Miami International
- `KDEN` - Denver International
- `KSEA` - Seattle-Tacoma

### International
- `EGLL` - London Heathrow (UK)
- `LFPG` - Paris Charles de Gaulle (France)
- `EDDF` - Frankfurt (Germany)
- `CYYZ` - Toronto Pearson (Canada)
- `RJTT` - Tokyo Haneda (Japan)
- `VHHH` - Hong Kong International
- `YSSY` - Sydney (Australia)
- `OMDB` - Dubai International (UAE)
- `LIRF` - Rome Fiumicino (Italy)

---

## Tips & Tricks

### ✅ Best Practices
1. **Start with Summary** - Get an overview before diving into details
2. **Use Regex for Patterns** - More powerful than simple text search
3. **Search Specific Fields** - Faster and more accurate results
4. **Download Important Results** - Save critical NOTAMs locally
5. **Adjust Timeout** - Increase for busy airports with many NOTAMs

### 🎯 Performance Tips
- Major airports (JFK, LAX, ORD) may have 150+ NOTAMs - be patient
- Keyword search is faster than viewing all NOTAMs
- Summary view is the fastest option
- Increase timeout for airports with many NOTAMs

### 🔍 Search Tips
- Use uppercase for airport codes (auto-converted)
- Regex is case-insensitive
- Use `|` for OR operations: `CRANE|RIG|TOWER`
- Use `.*` to match anything: `TWY.*CLSD`
- Search in specific fields for better performance

---

## Troubleshooting

### "Error: Failed to retrieve data"
- Check internet connection
- Verify airport code is correct (4 letters)
- Try increasing timeout
- Airport might not be in the system

### "No NOTAMs found"
- Airport code might be incorrect
- Airport might have no active NOTAMs
- Try a different search type

### Dashboard won't start
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+ required)
- Try: `streamlit --version` to verify installation

### Search is slow
- Normal for airports with 100+ NOTAMs
- Increase timeout in sidebar
- Try Summary view for quick overview
- Use keyword search instead of "All NOTAMs"

---

## Technical Details

### Architecture
```
Streamlit Dashboard
        ↓
get_notams library (8 functions)
        ↓
FAA NOTAM API (with pagination)
```

### Data Flow
1. User enters search criteria in sidebar
2. Dashboard calls appropriate library function
3. Library retrieves data from FAA API (with pagination)
4. Results displayed in main area
5. User can download results

### Features
- ✅ Real-time API calls to FAA
- ✅ Pagination support (up to 500 NOTAMs)
- ✅ Multiple search modes
- ✅ Regex pattern matching
- ✅ Download capability
- ✅ Responsive design
- ✅ Error handling
- ✅ Progress indicators

---

## Deployment Options

### Local Development
```bash
streamlit run streamlit_app.py
```

### Streamlit Cloud (Free Hosting)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy `streamlit_app.py`

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

---

## Support

For issues or questions:
- Check this guide
- Review [README.md](README.md) for library documentation
- See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for function reference
- Visit [GitHub Issues](https://github.com/Sunnywslau/Get_FAA_NOTAM/issues)

---

**Happy NOTAM Searching!** ✈️
