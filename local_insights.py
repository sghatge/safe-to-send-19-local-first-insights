"""Campaign insights that provably never leave your machine.

Runs the analysis inside a no-network guard: any attempt to open a connection, from this code
or from a library it imports, raises NetworkBlocked. Then it reads a results CSV and flags
markets whose rates are unusual compared with the rest. Standard library only.
"""
import contextlib
import csv
import socket
import statistics
import sys


class NetworkBlocked(RuntimeError):
    pass


@contextlib.contextmanager
def no_network():
    """Block outbound connections and DNS for everything inside the block."""
    def refuse(*args, **kwargs):
        raise NetworkBlocked("network access attempted inside a local-only block")
    saved = (socket.socket.connect, socket.socket.connect_ex, socket.getaddrinfo, socket.create_connection)
    socket.socket.connect = refuse
    socket.socket.connect_ex = refuse
    socket.getaddrinfo = refuse
    socket.create_connection = refuse
    try:
        yield
    finally:
        socket.socket.connect, socket.socket.connect_ex, socket.getaddrinfo, socket.create_connection = saved


def load(path):
    with open(path, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        sent = int(r["sent"])
        r["open_rate"] = int(r["opens"]) / sent
        r["click_rate"] = int(r["clicks"]) / sent
        r["unsub_rate"] = int(r["unsubscribes"]) / sent
    return rows


def outliers(rows, metric, z=2.0):
    """Leave-one-out z-score, so one extreme market doesn't hide itself by inflating the spread."""
    flagged = []
    for r in rows:
        others = [o[metric] for o in rows if o is not r]
        mu, sd = statistics.mean(others), statistics.pstdev(others) or 1e-9
        score = (r[metric] - mu) / sd
        if abs(score) >= z:
            flagged.append((r["market"], metric, r[metric], mu, score))
    return flagged


def report(rows):
    lines = ["| Market | Sent | Open | Click | Unsub |", "|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: -r["open_rate"]):
        lines.append(f"| {r['market']} | {int(r['sent']):,} | {r['open_rate']:.1%} | {r['click_rate']:.1%} | {r['unsub_rate']:.2%} |")
    flags = []
    for m in ("open_rate", "click_rate", "unsub_rate"):
        flags += outliers(rows, m)
    lines.append("")
    for market, metric, val, mu, score in flags:
        lines.append(f"- **{market}** {metric.replace('_', ' ')} {val:.2%} vs {mu:.2%} for the other markets (z = {score:+.1f})")
    return "\n".join(lines) if flags else "\n".join(lines + ["- no unusual markets"])


def main(path):
    with no_network():
        print(report(load(path)))
        print("\n(analysis ran with network access blocked)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "examples/black_friday_results.csv")
