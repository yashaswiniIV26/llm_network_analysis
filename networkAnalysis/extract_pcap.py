# extract_pcap.py
import pyshark
import csv

INPUT_PCAP = "sample.pcap"
OUTPUT_CSV = "flows.csv"

def safe_attr(pkt, attr_path, default=""):
    """Get nested attributes like pkt.ip.src safely."""
    try:
        parts = attr_path.split('.')
        cur = pkt
        for p in parts:
            cur = getattr(cur, p)
        return str(cur)
    except Exception:
        return default

def run():
    cap = pyshark.FileCapture(INPUT_PCAP, keep_packets=False)
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ts", "src", "src_port", "dst", "dst_port", "proto", "length"])
        for pkt in cap:
            try:
                ts = safe_attr(pkt, "sniff_timestamp")
                # IP fields (skip packets without IP)
                src = safe_attr(pkt, "ip.src")
                dst = safe_attr(pkt, "ip.dst")
                if not src or not dst:
                    continue
                # protocol and ports
                proto = safe_attr(pkt, "transport_layer") or safe_attr(pkt, "highest_layer")
                src_port = ""
                dst_port = ""
                # TCP/UDP ports
                if "TCP" in pkt:
                    src_port = safe_attr(pkt, "tcp.srcport")
                    dst_port = safe_attr(pkt, "tcp.dstport")
                elif "UDP" in pkt:
                    src_port = safe_attr(pkt, "udp.srcport")
                    dst_port = safe_attr(pkt, "udp.dstport")
                length = safe_attr(pkt, "length") or safe_attr(pkt, "frame_info.len")
                writer.writerow([ts, src, src_port, dst, dst_port, proto, length])
            except Exception:
                # keep going if a packet has an unexpected structure
                continue
    cap.close()
    print(f"Wrote {OUTPUT_CSV}")

if __name__ == "__main__":
    run()
