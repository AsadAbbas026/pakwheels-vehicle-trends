
from bs4 import BeautifulSoup
from matplotlib import markers
import requests
import matplotlib.pyplot as plt
import numpy as np
from numpy import double, sort

year_array = []
dictionary = {}
dictionary1 = {}

def model(brand, carname, year, Sprice, Eprice):
    data = []
    data1 = []
    miles_array = []
    for i in range(1, 3):
        url = "https://www.pakwheels.com/used-cars/search/-/mk_" + brand + "/md_" + carname + "/pr_"+ Sprice + "_"+ Eprice+ "/yr_" + year + "_Later/?page="+str(i)
        #url = 'https://www.pakwheels.com/used-cars/search/-/pr_200000_more/yr_2000_Later/?page=2'
        pakwheels = requests.get(url).content

        soup = BeautifulSoup(pakwheels, 'lxml')
        container = soup.find_all('div', class_ = 'col-md-9 grid-style')

        for cars in container:
            car_name = cars.find('h3').text.replace('\n', '')
            car_price = cars.find('div', class_ = 'price-details generic-dark-grey').text.replace('\n','')
            car_info = cars.find('ul', class_ = 'list-unstyled search-vehicle-info-2 fs13')
            car_details =  car_info.find_all('li')
            mileage = car_details[1]
            print(mileage.text)
            data1.append(car_info.find('li').text)
            data.append(car_price)
            miles_array.append(mileage.text)
        #    print(miles_array)
        for x in range(len(data)):
            try:
                if 'crore' in data[x]:
                    data[x] = double(data[x].replace('PKR', '').replace(' ', '').replace("crore","")) *100
                else:
                    data[x] = data[x].replace('PKR', '').replace(' ', '').replace('lacs', '')
                    data[x] = double(data[x])
            except:
                data[x] = double(data[x])
        for y in range(len(miles_array)):
            try:
                miles_array[y] = int(miles_array[y].replace(' ', '').replace(',', '').replace('km', ''))
            except:
                miles_array[y] = double(miles_array[y])
    index = 0
    for per_year in data1:
        if per_year not in dictionary:
            dictionary[per_year] = [data[index]]
        if per_year in dictionary:
            dictionary[per_year].append(data[index])
        index+=1
    # print(dictionary)
    index = 0
    for per_year in data1:
        if per_year not in dictionary1:
            dictionary1[per_year] = [miles_array[index]]
        if per_year in dictionary1:
            dictionary1[per_year].append(miles_array[index])
        index+=1


    year_array = dictionary.keys()
    year_array = list(year_array)
    year_array = sort(year_array)
    print(year_array)
    avg_array =[]
    for year in year_array:
        values = dictionary[year]
        print(values)    
        this_sum = 0
        for value in values:
            this_sum+= value
        this_avg = this_sum/len(values)
        avg_array.append(this_avg)
    
    avg1_array =[]
    for year in year_array:
        values = dictionary1[year]
        print(values)    
        this_sum = 0
        for value in values:
            this_sum+= value
        this_avg1 = this_sum/len(values)
        avg1_array.append(this_avg1)

    return year_array, avg_array, avg1_array


def min_max():
    year_array = dictionary.keys()
    year_array = list(year_array)
    year_array = sort(year_array)
    min_array = []
    max_array = []
    for year in year_array:
        values = dictionary[year]
        print(values)
        mini = min(values)
        maxi = max(values)
        min_array.append(mini)
        max_array.append(maxi)
       # print('Minimum value ' + year + ': '+ str(mini))
       # print('Maximum value ' + year + ': '+ str(maxi))
    
#    print('Minimum values: ',min_array)
#    print('Maximum values: ',max_array)
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
    #return maximum_vals, minimum_vals, year
def show_mileagedata(graphdata):
    for data in graphdata:
        plt.plot(data[0], data[1], label = data[2]+ ' ' +data[3], marker = 'x', markerfacecolor = 'blue')
        plt.title(data[2]+' '+data[3]+' Mileage Data')
        plt.show()
def main():
    n = int(input("Enter the execution time: "))
    i = 1
    brand1 = []
    carname1 = []
    Year = []
    Price_Start = []
    Price_End = []
    comparison  = []
    graph_values = []
    mileage_graphdata = []
    while i <= n:
        brand = input('Enter any car brand: ')
        carname = input('Car Name of the perticular brand: ')
        Start_Price = input('Starting Price Range of the Perticular Car: ')
        End_Price = input('Ending Price Range of the Perticular Car: ')
        YearModel = input('Year Model of the Car: ')
        comparison.append((brand, carname, YearModel, Start_Price, End_Price))
        brand1.append(brand)
        carname1.append(carname)
        Price_Start.append(Start_Price)
        Price_End.append(End_Price)
        Year.append(YearModel)
        i += 1
    for car in comparison:
        year1, avg1, avg_mileage  = model(car[0], car[1], car[2], car[3], car[4])
        print(year1)
        print(avg1)
        year1 = [int(x) for x in year1]
        x_point = np.array(year1)
        y_point = np.array(avg1)
        y1_point = np.array(avg_mileage)
        print(car)
        mileage_graphdata.append([x_point, y1_point, car[0], car[1]])
        plt.plot(x_point, y_point, label = car[0]+ ' ' +car[1], marker = 'x', markerfacecolor = 'blue')

    
    plt.legend()
    plt.title('Average prices')
    plt.show()
    show_mileagedata(mileage_graphdata)
    parse_minmax()
main()