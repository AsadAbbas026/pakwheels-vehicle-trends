from bs4 import BeautifulSoup
from matplotlib import markers
import requests
import matplotlib.pyplot as plt
import numpy as np
from numpy import double, sort

year_array = []
dictionary = {}
dictionary1 = {}

def model(make, name, year, price):
    PRICE = []
    YEAR = []
    MILES = []
    for page in range(1, 3):
        url = "https://www.pakwheels.com/used-cars/search/-/mk_" + make + "/md_" + name + "/pr_"+ price + "_more/yr_" + year + "_Later/?page="+str(page)
        pakwheels = requests.get(url).content
        soup = BeautifulSoup(pakwheels, 'lxml')

        container = soup.find_all('div', class_ = 'col-md-9 grid-style')
        for cars in container:

            car_name = cars.find('h3').text.replace('\n', '')
            car_price = cars.find('div', class_ = 'price-details generic-dark-grey').text.replace('\n','')
            car_info = cars.find('ul', class_ = 'list-unstyled search-vehicle-info-2 fs13')
            car_details = car_info.find_all('li')

            mileage = car_details[1]
            MILES.append(mileage.text)
            PRICE.append(car_price)
            YEAR.append(car_info.find('li').text)
        for x in range(len(PRICE)):
            try:
                if 'crore' in PRICE[x]:
                    PRICE[x] = double(PRICE[x].replace('PKR', '').replace(' ', '').replace('crore', '')) * 100
                else:
                    PRICE[x] = PRICE[x].replace('PKR', '').replace(' ', '').replace('lacs', '')
                    PRICE[x] = double(PRICE[x])
            except:
                PRICE[x] = double(PRICE[x])
        for y in range(len(MILES)):
            try:
                MILES[y] = int(MILES[y].replace(' ', '').replace(',', '').replace('km', ''))
            except:
                MILES[y] = double(MILES[y])
    index = 0
    for per_year in YEAR:
        if per_year not in dictionary:
            dictionary[per_year] = [MILES[index]]
        if per_year in dictionary:
            dictionary[per_year].append(MILES[index])
        index+=1
    index = 0
    for per_year in YEAR:
        if per_year not in dictionary1:
            dictionary1[per_year] = [MILES[index]]
        if per_year in dictionary1:
            dictionary1[per_year].append(MILES[index])
        index+=1

    year_array = dictionary.keys()
    year_array = list(year_array)
    year_array = sort(year_array)

    avg_array = []
    for year in year_array:
        values = dictionary[year]
        this_sum = 0
        for value in values:
            this_sum+=value

        this_avg = this_sum/len(values)
        avg_array.append(this_avg)

    avg1_array = []
    for year in year_array:
        values = dictionary1[year]
        this_sum = 0
        for value in values:
            this_sum+=value

        this_avg = this_sum/len(values)
        avg_array.append(this_avg)


    return year_array, avg_array, avg1_array

def min_max():
    year_array = dictionary.keys()
    year_array = list(year_array)
    year_array = sort(year_array)
    min_array = []
    max_array = []
    for year in year_array:
        values = dictionary[year]

        mini = min(values)
        maxi = max(values)
        min_array.append(mini)
        max_array.append(maxi)

    return min_array, max_array, year_array

def parse_minmax():
    mini, maxi, year = min_max()
    x_point = np.array(year)
    minimum_vals = np.array(mini)
    maximum_vals = np.array(maxi)

    plt.plot(x_point, minimum_vals, label = 'Minimum Values')
    plt.plot(x_point, maximum_vals, label = 'Maximum Values')
    plt.title('Minimum & Maximum Values')
    plt.legend()
    plt.show()

def show_mileagedata(graphdata):
    for data in graphdata:
        plt.plot(data[0], data[1], label = data[2]+ ' ' +data[3], marker = 'x', markerfacecolor = 'blue')
        plt.title(data[2]+' '+data[3]+' Mileage Data')
        plt.show()

def main():
    n = int(input('Enter the execution time: '))
    i = 1
    brand1 = []
    carname1 = []
    Year = []
    Price = []
    comparison  = []
    mileage_graphdata = []
    while i <= n:
        brand = input('Enter any car brand: ')
        carname = input('Car Name of the perticular brand: ')
        Price1 = input('Price of the Perticular Car: ')
        YearModel = input('Year Model of the Car: ')
        comparison.append((brand, carname, YearModel, Price1))
        brand1.append(brand)
        carname1.append(carname)
        Price.append(Price1)
        Year.append(YearModel)
        i += 1
    for car in comparison:
        year1, avg1, mileage_array = model(car[0], car[1], car[2], car[3])
        year1 = [int(x) for x in year1]
        
        x_point = np.array(year1)
        y_point = np.array(avg1)
        y1_point = np.array(mileage_array)
        mileage_graphdata.append([x_point, y1_point, car[0], car[1]])
        plt.plot(x_point, y_point, label = car[0]+ ' ' +car[1], marker = 'x', markerfacecolor = 'blue')

    plt.legend()

    plt.title('Average Prices')
    plt.show()

    show_mileagedata(mileage_graphdata)

    parse_minmax()

main()