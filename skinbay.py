import requests
from bs4 import BeautifulSoup as bs
import logging
logging.basicConfig(filename='skinlog.txt', filemode='w')

#Skinbay API
api_key = 'SKINBAY API KEY HERE'
api_secret = 'SKINBAY API SECRET HERE'
API_URL = 'https://api.skinbay.com/v1/items'



class Item:
    def __init__(self, item):

        if item['steam_price']: # Many times skinbay returns None as the 'steam_price' so neglecting it
            self.suggested_price = float(item['steam_price'])
        else:
            self.suggested_price = 201

        self.name= item['market_hash_name']
        self.url = item['item_page']
        if item['quantity']>0:
            self.available = True
            self.price = float(item['min_price'])
            self.margin= round(self.suggested_price- self.price, 2)
            self.reduction= round((1- (self.price/self.suggested_price))*100, 2)
        else:
            # Not avaiable items will not be in the list now
            self.available= False
            self.price= 201
            self.margin = 0
            self.reduction = 24
            

        # self.image= get_image(url)
        # withdrawable_at= item['withdrawable_at']
        # price= float(item['price'])
        # self.available_in= withdrawable_at- datetime.timestamp(datetime.now())
        # if self.available_in< 0:
        # 	self.available= True
        
        
        

    def __str__(self):
        if self.available:
            return f"Name: {self.name}\nPrice: {self.price}\nSuggested Price: {self.suggested_price}\nReduction: {self.reduction}%\nAvailable Now!\nLink: {self.url}"
        else:
            return f"Name: {self.name}\nPrice: {self.price}\nSuggested Price: {self.suggested_price}\nReduction: {self.reduction}%\nNot yet available\n"

    def __lt__(self, other):
        return self.reduction < other.reduction
    def __gt__(self, other):
        return self.reduction > other.reduction


# def get_url(API_KEY, code):
# 	PER_PAGE= 480 # the number of items to retrieve. Either 30 or 480.
# 	return "https://bitskins.com/api/v1/get_inventory_on_sale/?api_key="+ API_KEY+"&code=" + code+ "&per_page="+ str(PER_PAGE)

# def get_image(url):
#     r = requests.get(url)
#     soup = bs(soup, r.text)


def get_data():
	r=requests.get(API_URL, auth=requests.auth.HTTPBasicAuth(api_key,api_secret))
	data = r.json()
	return data

def get_items():
    try:
        data = get_data()
        logging.info('Got data')
        if data:
            logging.info('get_items() got some data')
            items = []
            for item in data:
                tmp= Item(item)
                if tmp.reduction>=25 and tmp.price<=200 and tmp.price >=20:	# Minimum discount and maximum price to look for when grabbing items. Currently set at minimum discount of 25% with a minimum price of $20 and a maxmimum price of $200.
                    items.append(tmp)
                    logging.info(f'Appended {tmp}')
            return items
        else:
            raise Exception(data["errors"]["message"])
    except:
        raise Exception("Couldn't connect to Skinbay.")