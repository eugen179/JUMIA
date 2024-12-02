import requests
from bs4 import BeautifulSoup
import csv
url = "https://www.jumia.co.ke"  
try:
    response = requests.get(url)
    if response.status_code == 200:
        print("Website is accessible!")
    else:
        print(f"Failed to access website. Status code: {response.status_code}")
        exit()
except Exception as e:
    print(f"An error occurred: {e}")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

products = soup.find_all('article', {'class': 'prd'})
if not products:
    print("No products found on the homepage.")
    exit()

data = []
for product in products:
    try:
        name = product.find('h3', {'class': 'name'}).text.strip()  
    except:
        name = "N/A"
    
    try:
        price = product.find('div', {'class': 'prc'}).text.strip()
    except:
        price = "N/A"
    
    try:
        discount = product.find('div', {'class': 'tag _dsct'}).text.strip() if product.find('div', {'class': 'tag _dsct'}) else "0%"  
    except:
        discount = "0%"
    
    try:
        rating = product.find('div', {'class': 'stars'}).get('data-stars', '0') if product.find('div', {'class': 'stars'}) else "0" 
    except:
        rating = "0"
    
    try:
        reviews = product.find('div', {'class': 'rev'}).text.strip() if product.find('div', {'class': 'rev'}) else "0"  
    except:
        reviews = "0"

    data.append([name, price, discount, rating, reviews])


with open('jumia_products.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
   
    writer.writerow(["Product Name", "Price (Ksh)", "Discount (%)", "Rating (out of 5)", "Total Reviews"])

    writer.writerows(data)

print("Scraping completed! Data saved to 'jumia_products.csv'.")
