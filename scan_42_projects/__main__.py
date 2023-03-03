import requests
import io
import PyPDF2
import csv
import os
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import argparse


def get_already_scanned(path_to_csv: str) -> list:
    if not os.path.isfile(path_to_csv):
        return []
    with open(path_to_csv, "r") as f:
        already_scanned = [int(row[0]) for row in csv.reader(f) if row[0].isdigit()]
    return already_scanned


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(1),
    retry=retry_if_exception_type(requests.exceptions.ConnectionError),
)
def get_subject_from_pdf(link: str) -> str | None: 
    res = requests.get(link)
    if res.status_code != 200:
        return None
    temp = io.BytesIO(res.content)
    pdfReader = PyPDF2.PdfReader(temp)
    subject = pdfReader.pages[0].extract_text().split("\n")[0]
    return subject


def main(path_to_csv: str) -> None:
    already_scanned = get_already_scanned(path_to_csv)

    with open(path_to_csv, "a") as f:
        writer = csv.writer(f)

        if not already_scanned:
            writer.writerow(["id", "subject", "link"])

        for i in range(0, 100000):

            if i in already_scanned:
                continue

            link = f"https://cdn.intra.42.fr/pdf/pdf/{i}/en.subject.pdf"

            subject = get_subject_from_pdf(link)

            print(f"Project {i} : {subject}")

            writer.writerow([i, subject, link])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path_to_csv",
        type=str,
        help="Path to the csv file containing the projects",
    )
    args = parser.parse_args()
    main(args.path_to_csv)