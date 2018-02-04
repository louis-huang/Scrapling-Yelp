# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 14:24:41 2017

@author: afu
"""
from bs4 import BeautifulSoup
import requests
import csv 
import time

result_number = 0
while True:
    
    url = 'https://www.yelp.com/search?find_desc=Restaurants&start={}&l=p:IL:Chicago::The_Loop'
    page_url = url.format(result_number)
    
    with open('loop_restaurants.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(['resaturant_name','Review_number','Stars','price_range','Address'])
        time.sleep(10)
        r = requests.get(page_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        restaurant_tags = soup.find_all('li', 'regular-search-result')
        if len(restaurant_tags) == 0:
            break

        for restaurant in restaurant_tags:
            
            name_a = restaurant.find('a', 'biz-name')
            name = ''
            if name_a.find('span') is not None:
                name = name_a.find('span').string
           
            review_number_span = restaurant.find('span', 'review-count')
            review_number = ''
            if review_number_span is not None:
                review_number = review_number_span.string
                
            star_div = restaurant.find('div', 'i-stars')
            star = star_div.get('title')
            if star is None:
                star = ''
            
            price_range_span = restaurant.find('span', 'price-range')
            price_range = ''
            if price_range_span is not None:
                price_range = price_range_span.string.count('S')
                
            address_tag = restaurant.find('address')
            address = ''
            if address_tag is not None:
                address_strings = address_tag.strings
                address_list = [string.strip() for string in address_strings]
                address = ' '.join(address_list)
                
            writer.writerow([name, review_number, star, price_range, address])
        result_number += 10 # result_number = result_numer + 10

f.close()
