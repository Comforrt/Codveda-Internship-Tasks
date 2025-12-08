from bs4 import BeautifulSoup
import requests
import csv
import time


def store_csv(data):
    filename = "books_scrape.csv"

    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:  #utf-8 ensures that all special characters are saved correctly
#                 #newline="" : prevents the insertion of blank lines into the books_scrape

            # writer for writing dictionaries also DictWriter writes data from dictionary into csv
            writer = csv.DictWriter(file, fieldnames=["In Stock","Title","Price"])  #keys to expect inside each dictionary
            writer.writeheader()
            writer.writerows(data)

        #print("Saving...")
        #print(f"File has been successfully saved as: {filename}")

    except FileNotFoundError:
        print("Ooops!! File not found")
    except PermissionError:
        print("Ooops!! Access denied")
    except Exception as e:
        print(f"Ooops!! {e}")


def find_books():
    html_page = 1 #initialize
    results = []

    while True:
        url = f'https://books.toscrape.com/catalogue/page-{html_page}.html'
        try:
            response = requests.get(url, timeout=5)
        except requests.exceptions.RequestException:
            print("Connection error! check your connection please!")
            break

        if response.status_code != 200:  # if a page does not exist it stops the loop or even any other error
            break

        soup = BeautifulSoup(response.text, 'lxml')
        book = soup.find_all('ul', class_='nav nav-list')
        products = soup.find('div', class_='col-sm-8 col-md-9')
        my_books = products.find('ol', class_='row').text.replace(' ', '')
        products = soup.find('div', class_='col-sm-8 col-md-9')
        book_frame = products.find_all('article', class_='product_pod')

        if not book_frame:  # breaks the loop if the page does not consist of any products that's books
            break

        try:
            for books in book_frame: #looping through the list returned by the book_frame
                rating_tag = books.find("p", class_="star-rating")
                rating = rating_tag["class"][1]

                if rating == 'Five': # execute program only if the rating is upto 5 stars
                    in_stock = books.find('p', class_='instock availability').text.strip() # the strip method removes spaces to make output look clean
                    book_title = books.h3.a['title']
                    book_price = books.find('p', class_='price_color').text.strip()

                    print(in_stock)
                    print(f"Book Title : {book_title}")
                    print(f"Price : {book_price}")
                    print(" ")

                    results.append({
                        "In Stock": in_stock,
                        "Title": book_title,
                        "Price": book_price
                    })

        except Exception as e:
            print(f"{e} an error occurred")

        # increment page NUMBER (correct place)
        html_page += 1 #increment by 1

    # saving to the csv file after scraping all the pages
    store_csv(results)

find_books()

