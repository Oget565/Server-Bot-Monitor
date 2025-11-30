import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import os

def graph_cpu_load(db_report):
    now = datetime.datetime.now()
    window_start = now - datetime.timedelta(hours=24)

    time = []
    load = []

    for entry in db_report:
        dt = datetime.datetime.fromtimestamp(entry['timestamp'])
        time.append(dt)
        load.append(entry['cpu_prcnt'])

    plt.figure(figsize=(14, 6))
    plt.title("CPU Usage - Last 24 Hours", fontsize=14, fontweight='bold')
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("CPU Load", fontsize=12)

    plt.plot(time, load, linewidth=1.5)
    plt.xlim(window_start, now)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.gcf().autofmt_xdate()

    plt.grid(True, alpha=0.5, color='gray')
    #plt.ylim(0, 100)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, 'cpu_load.png')

    print(f"Saving graph to: {save_path}")
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
