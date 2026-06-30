import tkinter as tk


def start_search():
    industry = industry_entry.get()
    location = location_entry.get()
    print(f"Searching for {industry} in {location}...")


root = tk.Tk()
root.title("Lead Generator")
root.geometry("400x300")

industry_label = tk.Label(root, text="Industry:")
industry_label.pack()

industry_entry = tk.Entry(root)
industry_entry.pack()

industry_label = tk.Label(root, text="Location:")
industry_label.pack()

industry_entry = tk.Entry(root)
industry_entry.pack()

search_button = tk.Button(root, text="Search", command=start_search)
search_button.pack()


root.mainloop()
