import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import filedialog, messagebox


def scrape_website():
    url = url_entry.get()

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        links = soup.find_all("a")
        link_data = []
        for link in links:
            link_url = link.get("href")
            link_text = link.text.strip()
            link_data.append({"url": link_url, "text": link_text})

        headings = soup.find_all(["h1", "h2", "h3"])
        heading_text = [heading.text.strip() for heading in headings]

        save_to_csv(link_data)

        messagebox.showinfo("Success", "Web scraping completed successfully.")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Connection error: {str(e)}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def save_to_csv(data):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

    if file_path:
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=["url", "text"])
                writer.writeheader()
                writer.writerows(data)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {str(e)}")


window = tk.Tk()
window.title("Web Scraper")

url_label = tk.Label(window, text="URL:")
url_label.pack()

url_entry = tk.Entry(window, width=50)
url_entry.pack()

scrape_button = tk.Button(window, text="Scrape", command=scrape_website)
scrape_button.pack()

window.mainloop()
