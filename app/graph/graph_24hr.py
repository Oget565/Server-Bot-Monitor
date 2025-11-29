import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import os
from collections import defaultdict


def graph_cpu_load(db_report):
    raw_time = []
    raw_load = []

    for db_data in db_report:
        raw_time.append(datetime.datetime.fromtimestamp(db_data['timestamp']))
        raw_load.append(db_data['cpu_prcnt'])

    interval_hours = 2
    interval_seconds = interval_hours * 3600
    buckets = defaultdict(list)

    for time_point, load_point in zip(raw_time, raw_load):
        timestamp = time_point.timestamp()
        bucket_key = int(timestamp // interval_seconds) * interval_seconds
        buckets[bucket_key].append(load_point)

    averaged_time = []
    averaged_load = []

    for bucket_timestamp in sorted(buckets.keys()):
        averaged_time.append(datetime.datetime.fromtimestamp(bucket_timestamp))
        averaged_load.append(sum(buckets[bucket_timestamp]) / len(buckets[bucket_timestamp]))

    plt.figure(figsize=(12, 6))
    plt.title("CPU Usage")
    plt.xlabel("Time")
    plt.ylabel("Load")
    plt.plot(averaged_time, averaged_load, linewidth=2, marker='o', markersize=4)

    now = datetime.datetime.now()
    now_rounded = now.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)
    twenty_four_hours_ago = (now - datetime.timedelta(hours=24)).replace(minute=0, second=0, microsecond=0)

    plt.xlim(twenty_four_hours_ago, now_rounded)

    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.gcf().autofmt_xdate()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    graph_dir = current_dir
    os.makedirs(graph_dir, exist_ok=True)

    save_path = os.path.join(graph_dir, 'cpu_load.png')
    print(f"Saving graph to: {save_path}")

    plt.savefig(save_path, dpi=150)
    plt.close()