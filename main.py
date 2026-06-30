import tkinter as tk
import requests
import csv
import threading
from bs4 import BeautifulSoup


def fetch_businesses(industry, location):
    print(f"Fetching data for {industry} in {location}...")
    clean_industry = industry.replace(" ", "+")
    clean_location = location.replace(" ", "+")
    url = "https://webscraper.io/test-sites/e-commerce/allinone"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    scraped_results = []

    cards = soup.find_all("div", class_="business-card")

    for card in cards:
        name = card.find("h2", class_="biz-name").text

        link_tag = card.find("a", class_="biz-website")

        if link_tag is not None:
            website_url = link_tag["href"]
        else:
            website_url = None

        business_info = {"name": name, "website": website_url}
        scraped_results.append(business_info)

    return scraped_results


def start_search():
    industry = industry_entry.get()
    location = location_entry.get()

    status_label.config(text=f"Searching for {industry} in {location}...")
    search_button.config(state=tk.DISABLED)  # turns off button so it cannot be spammed

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
    search_button.config(state=tk.NORMAL)  # turns button back on after search is done


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
