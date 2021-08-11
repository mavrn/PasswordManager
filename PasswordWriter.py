import csv
from pathlib import Path


FIELDNAMES = ["Site", "Username", "Password"]


def create_file():
    csv_path = str(Path(__file__).resolve().parent) + "\\passwords.csv"
    if not Path(csv_path).exists():
        print("Creating passwords.csv...")
        with open("passwords.csv", "w", newline='', encoding='utf-8') as new_csv:
            writer = csv.DictWriter(new_csv, fieldnames=FIELDNAMES)
            writer.writeheader()


def set_pw(pw_info):
    with open("passwords.csv", "a", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(pw_info)


def get_pw(site):
    with open("passwords.csv") as file:
        reader = list(csv.reader(file, delimiter=","))
        for row in reader:
            if row[0] == site:
                return [row[1], row[2]]
        return None


def replace_pw(site, new_user, new_pw):
    with open("passwords.csv") as inp:
        file = list(csv.reader(inp, delimiter=","))
    with open("passwords.csv", "w", newline='', encoding='utf-8') as out:
        writer = csv.writer(out)
        for row in file:
            if row[0] == site:
                writer.writerow([site, new_user, new_pw])
            else:
                writer.writerow(row)


def delete_pw(site):
    with open("passwords.csv") as inp:
        file = list(csv.reader(inp, delimiter=","))
    with open("passwords.csv", "w", newline='', encoding='utf-8') as out:
        writer = csv.writer(out)
        for row in file:
            if row[0] != site:
                writer.writerow(row)


def get_sites():
    with open("passwords.csv") as file:
        reader = list(csv.reader(file, delimiter=","))
        sites = [row[0] for row in reader]
        if len(sites) == 1:
            return []
        else:
            return sites[1:]


def get_credentials():
    with open("passwords.csv") as file:
        reader = list(csv.reader(file, delimiter=","))
        if len(reader) == 1:
            return []
        else:
            return reader[1:][:]
