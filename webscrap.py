import requests
from bs4 import BeautifulSoup
import pandas as pd 
oyo_url = 'https://www.oyorooms.com/hotels-in-bangalore/?page='
pageNum = 3
for page_num in range(1,pageNum):
    req = requests.get(oyo_url)
    content = req.content
    print(content)
    soup = BeautifulSoup(content,"html.parser")
    all_hotels = soup.find_all("div",{"class": "hotelCardListing"})
    scarped_info_list = []
    for hotel in all_hotels:
        hotel_dict = {}
        hotel_dict['name'] = hotel.find('h3',{'class': 'listingHotelDescription_hotelName'}).text
        hotel_dict['address'] = hotel.find('span',{'itemprop': 'streetAddress'}).text
        hotel_dict['price'] = hotel.find('span',{'class': 'listingPrice__finalPrice'}).text 
        try:
            hotel_dict['ratings'] = hotel.find('span',{'class': 'hotelRating__ratingSummary'}).text 
        except AttributeError:
            pass
        parent_amenities_element = hotel.find('div',{'class': 'amenityWrapper'})
        amenities_list =[]
        for amenity in parent_amenities_element.findall('div',{'class': 'amenityWrapper__amenity'}):
            amenities_list.append(amenity.find('span',{'class': 'd-body-sm'}).text.strip())
        hotel_dict['amenities'] = ', '.join(amenities_list[:-1])
        scarped_info_list.append(hotel_dict)
        #print(hotel_name,hotel_address,hotel_price,hotel_ratings, amenities_list)

dataFrame = pd.DataFrame(scarped_info_list)
dataFrame.to_csv('Oyo.csv')