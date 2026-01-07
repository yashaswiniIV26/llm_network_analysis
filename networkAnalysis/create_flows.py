import pandas as pd

def run(packets_file="packets.csv", output_file="flows.csv"):
    """
    Convert packet-level CSV into flow-level aggregated CSV.
    """

    df = pd.read_csv(packets_file)

    flows = []
    current = {}

    for _, row in df.iterrows():
        key = (row["src"], row["dst"], row["src_port"], row["dst_port"], row["proto"])

        if key not in current:
            current[key] = {
                "src": row["src"],
                "dst": row["dst"],
                "src_port": row["src_port"],
                "dst_port": row["dst_port"],
                "proto": row["proto"],
                "packet_count": 0,
                "total_bytes": 0,
                "start_time": row["ts"],
                "end_time": row["ts"]
            }

        c = current[key]
        c["packet_count"] += 1
        c["total_bytes"] += row["length"]
        c["end_time"] = row["ts"]

    for _, value in current.items():
        value["duration"] = value["end_time"] - value["start_time"]
        flows.append(value)

    pd.DataFrame(flows).to_csv(output_file, index=False)
    print(f"[OK] Flows saved to {output_file}")


if __name__ == "__main__":
    run()
