import pandas as pd
import argparse

def main(path_to_csv: str, output_path: str) -> None:
    df = pd.read_csv(path_to_csv)
    df = df.dropna(subset=['subject'])
    df = df.drop_duplicates(subset=['subject'])
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_csv", type=str, help="path to csv file")
    parser.add_argument("output_path", type=str, help="path to output csv file")
    args = parser.parse_args()
    main(args.path_to_csv, args.output_path)
