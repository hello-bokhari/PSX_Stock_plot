import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import pytz

# Step 1: Setup plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 6))
fig.suptitle('MARI Live Price & Volume (GMT+5)', fontsize=14)

# Step 2: Update function
def update(frame):
    try:
        url = "https://dps.psx.com.pk/timeseries/int/MARI"
        response = requests.get(url)
        data = response.json()['data']

        df = pd.DataFrame(data, columns=["timestamp", "price", "volume"])
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='s', utc=True).dt.tz_convert('Asia/Karachi')
        df = df.sort_values('datetime')

        ax1.clear()
        ax2.clear()

        ax1.plot(df['datetime'], df['price'], marker='o', linestyle='-')
        ax1.set_title("Price (PKR)")
        ax1.grid(True)

        ax2.bar(df['datetime'], df['volume'], width=0.001, color='orange', alpha=0.6)
        ax2.set_title("Volume")
        ax2.set_ylabel("Shares")
        ax2.set_xlabel("Time")
        ax2.grid(True)

        fig.tight_layout()
    except Exception as e:
        print("Error:", e)

# Step 3: Assign animation to a variable that stays in scope
ani = FuncAnimation(fig, update, interval=10000, cache_frame_data=False)

# Step 4: Show plot (this keeps the GUI alive)
plt.show()
