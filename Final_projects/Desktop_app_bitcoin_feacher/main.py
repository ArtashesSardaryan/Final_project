import tkinter as tk
from tkinter import filedialog, messagebox
import requests
try:
    import xlsxwriter
except ImportError as err:
    print("Install xlsxwriter")
    exit()

def fetch_cryptocurrency_data(symbol):
    '''Getting info about crypto'''
    url = f'https://api.coingecko.com/api/v3/coins/{symbol}'
    try:
        print(f"Sending request to {url}...")  
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        print(f"Received response: {data}")  
        return {
            'Name': data['name'],
            'Symbol': data['symbol'].upper(),
            'Current price': data['market_data']['current_price']['usd'],
            'Market Cap': data['market_data']['market_cap']['usd'],
            'Total Volume': data['market_data']['total_volume']['usd'],
            'Price Change (24h)': data['market_data']['price_change_percentage_24h']
        }
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"Cryptocurrency with symbol '{symbol}' not found.")
        else:
            print(f"HTTP error: {http_err}")
        return None
    except Exception as e:
        print(f"An error has occurred: {e}")
        return None

def process_file():
    print("Processing file...")  
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    if file_path:
        print(f"Selected file: {file_path}")  
        try:
            with open(file_path, 'r') as file:
                symbols = [line.strip() for line in file.readlines() if line.strip()]

            if not symbols:
                messagebox.showwarning("Warning", "The file is empty or does not contain valid cryptocurrency symbols.")
                return

            data = []
            for symbol in symbols:
                crypto_data = fetch_cryptocurrency_data(symbol)
                if crypto_data:
                    data.append(crypto_data)

            if data:
                save_file(data)
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while processing the file: {e}")

def save_file(data):
    '''Function to write into excel file'''
    print("Saving file...")  
    try:
        file_name = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_name:
            print(f"Selected save location: {file_name}")  
            workbook = xlsxwriter.Workbook(file_name)
            worksheet = workbook.add_worksheet()

            # Column Headings
            headers = ['Name', 'Symbol', 'Current price', 'Market Cap', 'Total Volume', 'Price Change (24h)']
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)

            # Data recording
            for row, item in enumerate(data, start=1):
                worksheet.write(row, 0, item['Name'])
                worksheet.write(row, 1, item['Symbol'])
                worksheet.write(row, 2, item['Current price'])
                worksheet.write(row, 3, item['Market Cap'])
                worksheet.write(row, 4, item['Total Volume'])
                worksheet.write(row, 5, item['Price Change (24h)'])

            workbook.close()
            messagebox.showinfo("Successfully", f"The file was successfully saved as {file_name}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

#  GUI
root = tk.Tk()
root.title("Cryptocurrency Data Generator")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

label = tk.Label(frame, text="Upload file with cryptocurrency symbols (.txt)")
label.pack()

button = tk.Button(frame, text="Upload file", command=process_file)
button.pack()

root.mainloop()
