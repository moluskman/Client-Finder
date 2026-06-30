import tkinter as tk
import requests
import csv
import threading


def fetch_businesses(industry, location):
    print(f"Fetching data for {industry} in {location}...")

    sample_results = [
        {"name": "Melb Plumbers", "website": "https://melbplumbers.com.au"},
        {"name": "FixIt Pipes", "website": None},
        {"name": "Cranbourne Plumbing", "website": None},
    ]
    return sample_results


def start_search():
    industry = industry_entry.get()
    location = location_entry.get()

    status_label.config(text=f"Searching for {industry} in {location}...")
    search_button.config(state=tk.DISABLED)

    results = fetch_businesses(industry, location)

    filtered_leads = []
    for business in results:
        if business["website"] is None:
            filtered_leads.append(business)

    with open("leads.csv", "w", newline="") as f:
        fieldnames = ["name", "website"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_leads)

    status_label.config(text=f"Saved {len(filtered_leads)} leads to leads.csv!")
    search_button.config(state=tk.NORMAL)


def run_search_in_thread():
    search_thread = threading.Thread(target=start_search)
    search_thread.start()


root = tk.Tk()  # blank tkinter canvas thing
root.title("Client Finder")
root.geometry("400x300")

industry_label = tk.Label(root, text="Industry:")  # label is text that can be seen
industry_label.pack()
industry_entry = tk.Entry(root)  # entry is like search bar
industry_entry.pack()

location_label = tk.Label(root, text="Location:")
location_label.pack()
location_entry = tk.Entry(root)
location_entry.pack()

search_button = tk.Button(
    root, text="Search", command=run_search_in_thread
)  # button that is connected to search function above
search_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
