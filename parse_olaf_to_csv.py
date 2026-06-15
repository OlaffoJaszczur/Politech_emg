"""Convert raw EMG scan exports in Olaf/ to CSV files for filtering/signal processing.

Each source .txt file has a 5-line header followed by tab-separated
"Time [s]" / "Voltage [V]" samples:

    Source File Name:	Scan
    Signal:	Time - Ref1 Voltage - Samples

    Time	Time Signal
    [ s ]	[ V ]
    0	-0.000201617
    ...

This script reads every .txt file in the Olaf/ folder and writes a
corresponding .csv file (with "time_s,voltage_v" header) into Olaf/csv/.
"""

import csv
from pathlib import Path

SOURCE_DIR = Path(__file__).parent / "Olaf"
OUTPUT_DIR = SOURCE_DIR / "csv"
HEADER_LINES = 5


def convert_file(src_path: Path, dst_path: Path) -> None:
    with src_path.open("r", encoding="utf-8") as src, \
            dst_path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.writer(dst)
        writer.writerow(["time_s", "voltage_v"])

        for _ in range(HEADER_LINES):
            next(src)

        for line in src:
            line = line.strip()
            if not line:
                continue
            time_str, voltage_str = line.split("\t")
            writer.writerow([float(time_str), float(voltage_str)])


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    txt_files = sorted(SOURCE_DIR.glob("*.txt"))
    for src_path in txt_files:
        dst_path = OUTPUT_DIR / (src_path.stem + ".csv")
        convert_file(src_path, dst_path)
        print(f"Converted {src_path.name} -> {dst_path.relative_to(SOURCE_DIR.parent)}")

    print(f"Done. {len(txt_files)} files converted into {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
