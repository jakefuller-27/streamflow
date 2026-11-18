import numpy as np
import matplotlib.pyplot as plt


def load_streamflow(filename):
    """Read the streamflow CSV. Return the dates and a 2D array of flows (cfs), one column per gauge."""

    data = np.genfromtxt(filename,
                         delimiter=",",
                         skip_header=1,
                         dtype=str)

    dates = data[:, 0]
    flows = data[:, 1:6].astype(float)

    return dates, flows


def plot_streamflow(dates, flows, sites):
    """Plot the flow at each gauge, with the same title, labels, and formatting as the Matplotlib HW."""

    plt.plot(dates, flows[:, 0], label=sites[0])
    plt.plot(dates, flows[:, 1], label=sites[1])
    plt.plot(dates, flows[:, 2], label=sites[2])
    plt.plot(dates, flows[:, 3], label=sites[3])
    plt.plot(dates, flows[:, 4], label=sites[4])

    plt.title("Provo River Streamflow Data (2021)")
    plt.xlabel("Date")
    plt.ylabel("Flowrate (cfs)")

    plt.legend(title="Site Numbers")
    plt.grid()

    plt.xticks(rotation=45)

    plt.show()


def summarize(dates, flows, sites):
    """Summarize the maximum, minimum, and average flow for each gauge."""
    # Excel check for 10163000: Max = 131.0, Average = 56.95
    # Check your Excel numbers for gauge 10163000 and add them here:
    # Max = _____    Average = _____

    print(f"{'Gauge':<12}{'Max (cfs)':>12}{'Date of max':>22}{'Min (cfs)':>12}{'Avg (cfs)':>12}")

    with open("streamflow_summary.csv", "w") as file:
        file.write("Gauge,Max (cfs),Date of max,Min (cfs),Avg (cfs)\n")

        for i in range(len(sites)):
            maximum = np.max(flows[:, i])
            minimum = np.min(flows[:, i])
            average = np.mean(flows[:, i])
            max_index = np.argmax(flows[:, i])
            date_of_max = dates[max_index]

            print(f"{sites[i]:<12}{maximum:>12.1f}{date_of_max:>22}{minimum:>12.1f}{average:>12.1f}")

            file.write(f"{sites[i]},{maximum:.1f},{date_of_max},{minimum:.1f},{average:.1f}\n")

# Main program
sites = ["10163000", "10155200", "10155500", "10154200", "10155000"]

dates, flows = load_streamflow("June-2021-Provo-River-Streamflow-Rates (2).csv")

summarize(dates, flows, sites)

# Ask the user for a flow threshold in cfs.
threshold = float(input("Enter a flow threshold (cfs): "))

# Count how many 15-minute readings are above the threshold for each gauge.
# Each reading represents 0.25 hours, so multiply the count by 0.25.
for i in range(len(sites)):
    hours = np.sum(flows[:, i] > threshold) * 0.25
    print(f"{sites[i]}: {hours:.2f} hours above threshold")

plot_streamflow(dates, flows, sites)
