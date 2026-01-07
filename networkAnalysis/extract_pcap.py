import subprocess
import pandas as pd
import csv
from io import StringIO

def run(INPUT_PCAP="sample.pcap", OUTPUT_FILE="packets.csv"):

    print("[INFO] Extracting packets using TShark...")

    tshark_cmd = [
        "tshark",
        "-r", INPUT_PCAP,
        "-T", "fields",
        "-e", "frame.time_epoch",
        "-e", "ip.src",
        "-e", "ip.dst",
        "-e", "tcp.srcport",
        "-e", "tcp.dstport",
        "-e", "udp.srcport",
        "-e", "udp.dstport",
        "-e", "_ws.col.Protocol",
        "-e", "frame.len",
        "-E", "separator=,",
        "-E", "quote=d",
    ]

    result = subprocess.run(tshark_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("[ERROR] TShark failed:", result.stderr)
        raise RuntimeError("TShark error")

    print("\n[DEBUG] Raw TShark Output:")
    print(result.stdout)

    packets = []
    
    # Use CSV reader to properly parse quoted fields
    reader = csv.reader(StringIO(result.stdout))

    for row in reader:
        if not row:
            continue

        # row structure:
        # [ts, src, dst, tcp_src, tcp_dst, udp_src, udp_dst, proto, length]

        try:
            ts = float(row[0]) if row[0] else 0
            src = row[1] if row[1] else "N/A"
            dst = row[2] if row[2] else "N/A"

            tcp_src = row[3] or None
            tcp_dst = row[4] or None
            udp_src = row[5] or None
            udp_dst = row[6] or None

            proto = row[7] or "UNK"
            length = int(row[8]) if row[8].isdigit() else 0

            src_port = tcp_src or udp_src or -1
            dst_port = tcp_dst or udp_dst or -1

            packets.append({
                "ts": ts,
                "src": src,
                "dst": dst,
                "src_port": src_port,
                "dst_port": dst_port,
                "proto": proto,
                "length": length
            })

        except Exception as e:
            print("ROW PARSE ERROR:", row, e)
            continue

    df = pd.DataFrame(packets)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"[OK] Extracted {len(df)} packets → {OUTPUT_FILE}")


if __name__ == "__main__":
    run()
