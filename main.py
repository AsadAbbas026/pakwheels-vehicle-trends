import time
import numpy as np
import requests
import matplotlib.pyplot as plt
from numpy import double, sort
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

year_array = []
dictionary = {}
dictionary1 = {}

def fetch_soup(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'lxml')
        else:
            raise Exception(f"Fallback to Selenium due to status {response.status_code}")
    except:
        print(f"Using Selenium for URL: {url}")
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        return soup

def model(make, name, year, price):
    PRICE = []
    YEAR = []
    MILES = []
    for page in range(1, 3):
        url = f"https://www.pakwheels.com/used-cars/search/-/mk_{make}/md_{name}/pr_{price}_more/yr_{year}_Later/?page={page}"
        soup = fetch_soup(url)

        container = soup.find_all('div', class_='col-md-9 grid-style')
        for cars in container:
            try:
                car_name = cars.find('h3').text.strip()
                car_price = cars.find('div', class_='price-details generic-dark-grey').text.strip()
                car_info = cars.find('ul', class_='list-unstyled search-vehicle-info-2 fs13')
                car_details = car_info.find_all('li')

                mileage = car_details[1].text.strip()
                MILES.append(mileage)
                PRICE.append(car_price)
                YEAR.append(car_details[0].text.strip())
            except Exception as e:
                print(f"Error while parsing car entry: {e}")

        for x in range(len(PRICE)):
            try:
                if 'crore' in PRICE[x]:
                    PRICE[x] = double(PRICE[x].replace('PKR', '').replace(' ', '').replace('crore', '')) * 100
                else:
                    PRICE[x] = double(PRICE[x].replace('PKR', '').replace(' ', '').replace('lacs', ''))
            except:
                PRICE[x] = 0.0

        for y in range(len(MILES)):
            try:
                MILES[y] = int(MILES[y].replace(' ', '').replace(',', '').replace('km', ''))
            except:
                MILES[y] = 0.0

    for i in range(len(YEAR)):
        dictionary.setdefault(YEAR[i], []).append(MILES[i])
        dictionary1.setdefault(YEAR[i], []).append(MILES[i])

    year_array = sort(list(dictionary.keys()))

    avg_array = []
    for year in year_array:
        values = dictionary[year]
        avg_array.append(sum(values) / len(values))

    avg1_array = []
    for year in year_array:
        values = dictionary1[year]
        avg1_array.append(sum(values) / len(values))

    return year_array, avg_array, avg1_array

def min_max():
    year_array = sort(list(dictionary.keys()))
    min_array = []
    max_array = []
    for year in year_array:
        values = dictionary[year]
        min_array.append(min(values))
        max_array.append(max(values))
    return min_array, max_array, year_array

def parse_minmax():
    mini, maxi, year = min_max()
    x_point = np.array(year)
    plt.plot(x_point, mini, label='Minimum Mileage')
    plt.plot(x_point, maxi, label='Maximum Mileage')
    plt.title('Minimum & Maximum Mileage Over Years')
    plt.legend()
    plt.show()

def show_mileagedata(graphdata):
    for data in graphdata:
        plt.plot(data[0], data[1], label=f'{data[2]} {data[3]} Mileage', marker='x')
        plt.title(f'{data[2]} {data[3]} Mileage Data')
        plt.legend()
        plt.show()

def main():
    n = int(input('Enter number of cars to compare: '))
    comparison = []

    for _ in range(n):
        brand = input('Enter car brand: ')
        name = input('Enter model name: ')
        year = input('Minimum year model: ')
        price = input('Minimum price (in lacs): ')
        comparison.append((brand, name, year, price))

    mileage_graphdata = []

    for car in comparison:
        year_arr, avg_prices, mileage_vals = model(car[0], car[1], car[2], car[3])
        year_int = [int(x) for x in year_arr]

        plt.plot(year_int, avg_prices, label=f'{car[0]} {car[1]} Avg Price', marker='x')
        mileage_graphdata.append([year_int, mileage_vals, car[0], car[1]])

    plt.title('Average Car Prices Over Years')
    plt.legend()
    plt.show()

    show_mileagedata(mileage_graphdata)
    parse_minmax()

if __name__ == "__main__":
    main()
