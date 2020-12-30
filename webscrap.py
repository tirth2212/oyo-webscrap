import requests
from bs4 import BeautifulSoup
import pandas as pd 
oyo_url = 'https://www.oyorooms.com/hotels-in-bangalore/?page='
pageNum = 3
for page_num in range(1,pageNum):
    headers = { 
        "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding" : "gzip, deflate, br",
        "accept-language" : "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control" : "max-age=0",
        "cookie" : "_csrf=TiEgVpblY9UUZLS4r03DwckW; acc=IN; X-Location=georegion%3D104%2Ccountry_code%3DIN%2Cregion_code%3DMH%2Ccity%3DMUMBAI%2Clat%3D18.98%2Clong%3D72.83%2Ctimezone%3DGMT%2B5.50%2Ccontinent%3DAS%2Cthroughput%3Dvhigh%2Cbw%3D5000%2Casnum%3D55836%2Clocation_id%3D0; mab=aaf19c5c0d4048cdbdaa8f44842f19ac; appData=%7B%22userData%22%3A%7B%22isLoggedIn%22%3Afalse%7D%7D; token=dUxaRnA5NWJyWFlQYkpQNnEtemo6bzdvX01KLUNFbnRyS3hfdEgyLUE%3D; _uid=Not%20logged%20in; fingerprint2=18fabff44ff8162c98fdb1ad55ec18d0; _gcl_au=1.1.1218353456.1609304473; tvc_utm_source=(direct); tvc_utm_medium=(none); tvc_utm_campaign=(not set); tvc_utm_key=(not set); tvc_utm_content=(not set); AMP_TOKEN=%24NOT_FOUND; _ga=GA1.2.1473468547.1609304473; _gid=GA1.2.400701182.1609304473; _uetsid=0a27f5604a5c11eb8e0ecb444f78bb80; _uetvid=0a2824404a5c11ebbbe0e5b38ca3fbb9; expd=mww2%3A1%7CBnTc%3A0%7Cnear%3A0%7Cioab%3A0%7Cmhdp%3A1%7Cbcrp%3A1%7Cpwbs%3A1%7Cmwsb%3A0%7Cslin%3A1%7Chsdm%3A0%7Clpex%3A1%7Clphv%3A0%7Cdpcv%3A0%7Cgmab%3A0%7Curhe%3A0%7Cprdp%3A1%7Ccomp%3A1%7Csldw%3A1%7Cmdab%3A0%7Cnrmp%3A1%7Cnhyw%3A1%7Cwboi%3A1%7Csst%3A1%7Ctxwb%3A1%7Cpod2%3A1%7Clnhd%3A1%7Cppsi%3A0%7Cgcer%3A1%7Crecs%3A1%7Cgmbr%3A0%7Cyolo%3A1%7Crcta%3A0%7Ceopt%3A1; XSRF-TOKEN=gWVumG4K-b3-UDbMhOlzuRco-4PfRm443MzE; moe_uuid=d72ab4fe-3036-4d7f-8437-c84b6ebc0b8d",
        "sec-ch-ua-mobile" : "?0",
        "sec-fetch-dest" : "document",
        "sec-fetch-mode" : "navigate",
        "sec-fetch-site" : "none",
        "sec-fetch-user" : "?1",
        "upgrade-insecure-requests" : "1",
        "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    req = requests.get(oyo_url, headers=headers)
    content = req.content
    print(content)
    soup = BeautifulSoup(content,"html.parser")
    all_hotels = soup.find_all("div",{"class": "hotelCardListing"})
    scarped_info_list = []
    for hotel in all_hotels:
        hotel_dict = {}
        try:
            hotel_dict['name'] = hotel.find('h3',{'class': 'listingHotelDescription_hotelName'}).text
        except AttributeError:
            pass
        try:
            hotel_dict['address'] = hotel.find('span',{'itemprop': 'streetAddress'}).text
        except AttributeError:
            pass
        try:
            hotel_dict['price'] = hotel.find('span',{'class': 'listingPrice__finalPrice'}).text 
        except AttributeError:
            pass
        try:
            hotel_dict['ratings'] = hotel.find('span',{'class': 'hotelRating__ratingSummary'}).text 
        except AttributeError:
            pass
        parent_amenities_element = hotel.find('div',{'class': 'amenityWrapper'})
        amenities_list =[]
        for amenity in parent_amenities_element.find_all('div',{'class': 'amenityWrapper__amenity'}):
            amenities_list.append(amenity.find('span',{'class': 'd-body-sm'}).text.strip())
        hotel_dict['amenities'] = ', '.join(amenities_list[:-1])
        scarped_info_list.append(hotel_dict)
        #print(hotel_name,hotel_address,hotel_price,hotel_ratings, amenities_list)

    dataFrame = pd.DataFrame(scarped_info_list)
    dataFrame.to_csv('Oyo.csv')
