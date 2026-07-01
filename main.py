import tkinter as tk
from curl_cffi import requests
import csv
import threading
from bs4 import BeautifulSoup


def fetch_businesses(industry, location):
    print(f"Fetching data for {industry} in {location}...")

    # lean user entries
    clean_industry = industry.replace(" ", "+")
    clean_location = location.replace(" ", "+")

    #  parameters for a live business directory URL
    url = f"https://www.yellowpages.com.au/search/listings?clue={clean_industry}&locationClue={clean_location}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, impersonate="chrome", timeout=10)
        if response.status_code != 200:
            print(
                f"Could not retrieve data. Server status code: {response.status_code}"
            )
            return []
    except Exception as e:
        print(f"Network error occurred: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    scraped_results = []

    cards = soup.find_all("div", class_="result")

    for card in cards:
        try:
            name_tag = card.find("a", class_="business-name")
            if name_tag is None:
                continue
            name = name_tag.text.strip()

            link_tag = card.find("a", class_="track-visit-website")

            if link_tag is not None:
                website_url = link_tag["href"]
            else:
                website_url = None

            business_info = {"name": name, "website": website_url}
            scraped_results.append(business_info)

        except Exception as e:
            print(f"Skipping unexpected item layout format: {e}")
            continue

    return scraped_results


def start_search():
    industry = industry_entry.get()
    location = location_entry.get()

    status_label.config(text=f"Searching for {industry} in {location}...")
    search_button.config(state=tk.DISABLED)  # turns off button so it cannot be spammed

    results = fetch_businesses(industry, location)

    filtered_leads = []
    for business in results:
        # filter strictly for businesses missing a website url string
        if business["website"] is None:
            filtered_leads.append(business)

    with open("leads.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = ["name", "website"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_leads)

    status_label.config(text=f"Saved {len(filtered_leads)} leads to leads.csv!")
    search_button.config(state=tk.NORMAL)  # turns button back on after search is done


def run_search_in_thread():
    search_thread = threading.Thread(target=start_search)
    search_thread.start()


#  tkinter ui stuff
root = tk.Tk()
root.title("Client Finder")
root.geometry("400x300")

industry_label = tk.Label(root, text="Industry:")
industry_label.pack()
industry_entry = tk.Entry(root)
industry_entry.pack()

location_label = tk.Label(root, text="Location:")
location_label.pack()
location_entry = tk.Entry(root)
location_entry.pack()

search_button = tk.Button(root, text="Search", command=run_search_in_thread)
search_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
