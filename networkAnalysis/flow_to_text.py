import pandas as pd

def run(flows_file="flows.csv", output_file="flow_texts.csv"):
    """
    Convert each network flow into a clean, SOC-style
    natural-language description for LLM processing.
    """

    df = pd.read_csv(flows_file)
    desc_list = []

    for _, row in df.iterrows():

        # Clean source and destination
        src_ip = row["src"] if pd.notna(row["src"]) else "Unknown"
        dst_ip = row["dst"] if pd.notna(row["dst"]) else "Unknown"

        src_port = row["src_port"] if pd.notna(row["src_port"]) else "Unknown"
        dst_port = row["dst_port"] if pd.notna(row["dst_port"]) else "Unknown"

        proto = row["proto"] if pd.notna(row["proto"]) else "Unknown"

        packet_count = int(row["packet_count"]) if pd.notna(row["packet_count"]) else 0
        total_bytes = int(row["total_bytes"]) if pd.notna(row["total_bytes"]) else 0
        duration = round(float(row["duration"]), 4) if pd.notna(row["duration"]) else 0.0

        desc = (
            f"Network flow observed using {proto} protocol. "
            f"Source address {src_ip} on port {src_port} communicated with "
            f"destination address {dst_ip} on port {dst_port}. "
            f"The flow consisted of {packet_count} packets, "
            f"transferring a total of {total_bytes} bytes over "
            f"a duration of {duration} seconds."
        )

        desc_list.append([desc])

    pd.DataFrame(desc_list, columns=["text"]).to_csv(output_file, index=False)
    print(f"[OK] Flow descriptions saved to {output_file}")


if __name__ == "__main__":
    run()
