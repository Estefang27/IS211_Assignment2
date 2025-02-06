import argparse
import urllib.request
import logging
from datetime import datetime
import sys


def downloadData(url):
    """Downloads the data from the provided URL"""
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error downloading the data: {e}")
        sys.exit(1)


def processData(file_content):
    person_data = {}
    logger = logging.getLogger('IS211Assignment2OJ')

    lines = file_content.strip().split("\n")

    for i, line in enumerate(lines[1:], start=2):  # Skip the header and start counting from line 2
        try:
            id, name, birthday = line.split(',')
            birthday = datetime.strptime(birthday, "%d/%m/%Y")
            person_data[int(id)] = (name, birthday)
        except ValueError:
            logger.error(f"Error processing line #{i} for ID #{id}")

    return person_data


def displayPerson(id, personData):
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y-%m-%d')}")
    else:
        print("No user found with that ID")


def setupLogging():
    logger = logging.getLogger('IS211Assignment2OJ')
    logger.setLevel(logging.ERROR)
    handler = logging.FileHandler('errors.log')
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def main(url):
    setupLogging()
    print(f"Fetching data from {url}...")

    # Download data
    csvData = downloadData(url)

    # Process data
    personData = processData(csvData)

    # Ask for user input
    while True:
        try:
            user_input = int(input("Enter an ID to lookup (enter 0 or a negative number to exit): "))
            if user_input <= 0:
                break
            displayPerson(user_input, personData)
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
