from marx import create_network
from config import required
import pandas as pd


def to_file(nodes):
    with open("nodes.csv", "w", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(
            out_file, ["direction", "url", "philosopher", "connection"]
        )
        writer.writeheader()
        for lst in nodes:
            for record in lst:
                writer.writerow(record.__dict__)


if __name__ == "__main__":
    nodes = create_network(required)
    to_file(nodes)
    df = pd.read_csv("nodes.csv")
    df = df.drop_duplicates()
    df.to_csv("nodes_filtered.csv", index=False)
