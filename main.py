import warnings
import urllib3

# 1. Silence the warning immediately
warnings.filterwarnings("ignore", category=urllib3.exceptions.NotOpenSSLWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 2. Now import your custom library and other tools
from faa_notam_lib import FAAClient
import datetime

# Credentials (NEVER HARDCODE IN GITHUB)
# You can set these as environment variables or pass them to the client
import os
ID = os.getenv("FAA_ID", "your_id_here")
SECRET = os.getenv("FAA_SECRET", "your_secret_here")
client = FAAClient(ID, SECRET)

runways_to_test = ["07R", "07L", "07C", "25R", "25L", "25C"]
airport = "VHHH"

print(f"--- VERIFICATION TEST FOR {airport} ---")

for rwy in runways_to_test:
    results = client.search_notams(airport, rwy, search_type="runway")
    
    print(f"\n{'='*20} RUNWAY {rwy} ({len(results)} Matches) {'='*20}")
    
    if not results:
        print(f"No specific NOTAMs found for RWY {rwy}.")
    else:
        for n in results:
            print(f"\n[ID: {n['id']}]")
            # We print the raw text to verify the 'RWY' mention
            print(f"TEXT: {n['text']}")
            # We print a snippet of ICAO to see the runway pair if it exists
            if n['full_icao']:
                # Pull the 'E)' line specifically if possible, or just the whole thing
                print(f"ICAO: {n['full_icao'].split('E)')[-1].strip() if 'E)' in n['full_icao'] else n['full_icao']}")
            print("-" * 30)

print(f"\n{'='*60}")
print("Verification Complete.")