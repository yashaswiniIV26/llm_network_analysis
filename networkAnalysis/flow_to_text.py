import pandas as pd

INPUT = "netflows.csv"
OUTPUT = "flow_texts.csv"

def flow_to_text(row):
    return (
        f"Network flow using {row['proto']} protocol. "
        f"Source {row['src']}:{row['src_port']} communicated with "
        f"destination {row['dst']}:{row['dst_port']}. "
        f"Packet count {row['packet_count']}. "
        f"Total bytes transferred {row['total_bytes']}. "
        f"Flow duration {row['duration']} seconds."
    )

def run():
    df = pd.read_csv(INPUT)
    df["text"] = df.apply(flow_to_text, axis=1)
    df.to_csv(OUTPUT, index=False)
    print(f"Wrote {OUTPUT}")

if __name__ == "__main__":
    run()
