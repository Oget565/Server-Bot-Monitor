import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import os


def graph_cpu_load(db_report):
    now = datetime.datetime.now()
    window_start = now - datetime.timedelta(hours=24)

    times = []
    loads = []

    for entry in db_report:
        t = datetime.datetime.fromtimestamp(entry['timestamp'])
        if t >= window_start:
            times.append(t)
            loads.append(entry['cpu_prcnt'])

    if not times:
        times = [window_start, now]
        loads = [0, 0]

    times, loads = zip(*sorted(zip(times, loads)))

    plt.figure(figsize=(14, 6))
    plt.title("CPU Usage - Last 24 Hours", fontsize=14, fontweight='bold')
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("CPU Load (%)", fontsize=12)

    plt.plot(times, loads, linewidth=1.5)

    plt.grid(True, alpha=0.5, color='gray')
    plt.ylim(0, 100)

    ax = plt.gca()
    ax.set_xlim(window_start, now)

    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.gcf().autofmt_xdate()
    plt.tight_layout()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, 'cpu_load.png')

    print(f"Saving graph to: {save_path}")
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
