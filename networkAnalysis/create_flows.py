import pandas as pd

# Input and output files
PACKET_CSV = "flows.csv"     # from extract_pcap.py
FLOW_CSV = "netflows.csv"    # new aggregated flows

def create_flows():
    df = pd.read_csv(PACKET_CSV)

    # 5-tuple (unique identifier for each flow)
    flow_key = ["src", "dst", "src_port", "dst_port", "proto"]

    # Group packets into flows
    grouped = df.groupby(flow_key)

    flows = []

    for key, group in grouped:
        flow = {
            "src": key[0],
            "dst": key[1],
            "src_port": key[2],
            "dst_port": key[3],
            "proto": key[4],
            "packet_count": len(group),
            "total_bytes": group["length"].astype(int).sum(),
            "start_time": group["ts"].min(),
            "end_time": group["ts"].max(),
            "duration": group["ts"].max() - group["ts"].min()
        }
        flows.append(flow)

    flow_df = pd.DataFrame(flows)
    flow_df.to_csv(FLOW_CSV, index=False)

    print(f"Wrote {FLOW_CSV} with {len(flow_df)} flows")

if __name__ == "__main__":
    create_flows()
