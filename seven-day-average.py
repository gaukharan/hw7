import csv
import requests


def main():
    # Read NYTimes Covid Database
    download = requests.get(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
    )
    decoded_content = download.content.decode("utf-8")
    file = decoded_content.splitlines()
    reader = csv.DictReader(file)

    # Construct 14 day lists of new cases for each states
    new_cases = calculate(reader)

    # Create a list to store selected states
    states = []
    print("Choose one or more states to view average COVID cases.")
    print("Press enter when done.\n")

    while True:
        state = input("State: ")
        if state in new_cases:
            states.append(state)
        if len(state) == 0:
            break

    print(f"\nSeven-Day Averages")

    # Print out 7-day averages for this week vs last week
    comparative_averages(new_cases, states)


# TODO: Create a dictionary to store 14 most recent days of new cases by state
def calculate(reader):
    new_cases = {}
    previous_cases = {}
    for row in reader:
        state = row['state']
        if state not in new_cases:
            new_cases[state] = []
            previous_cases[state] = 0
        new_case = int(row['cases']) - previous_cases[state]
        new_cases[state].append(new_case)
        previous_cases[state] = int(row['cases'])
        if len(new_cases[state]) > 14:
            new_cases[state].pop(0)
    return new_cases


# TODO: Calculate and print out seven day average for given state
def comparative_averages(new_cases, states):
    for state in states:
        cases = new_cases[state]
        this_week_average = sum(cases[-7:]) / 7
        last_week_average = sum(cases[-14:-7]) / 7
        try:
            increase = (this_week_average - last_week_average) / last_week_average * 100
        except ZeroDivisionError:
            increase = 0
        if increase >= 0:
            print(f"{state}\nAverage cases per day: {int(this_week_average)}\nIncrease of {int(increase)}%.\n")
        else:
            print(f"{state}\nAverage cases per day: {int(this_week_average)}\nDecrease of {int(abs(increase))}%.\n")

main()
