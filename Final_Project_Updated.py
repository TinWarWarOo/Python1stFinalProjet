import requests 
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter 
from urllib3.util.retry import Retry
from requests.exceptions import ChunkedEncodingError, RequestException
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import time

def extract_page_list():
    default_url = "https://www.citymall.com.mm/citymall/my/c/id05011"

    url = default_url
    extracted_url_list = [default_url, ]
    while True:

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                   "AppleWebKit/537.36 (KHTML, like Gecko)"
                   "Chrome/120.0.0.0 Safari/537.36",
                   "Accept-Encoding":"identity"}

        session = requests.Session()
        retry = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]) 
        session.mount("https://", HTTPAdapter(max_retries=retry))

        response = session.get(url, headers=headers, timeout=30) 
        #print(response.status_code)

        bsObj = BeautifulSoup(response.text, "html5lib")

        next_link_tag = bsObj.find('a', class_ = 'page-link next')

        next_link_text = next_link_tag.get('href')

        if next_link_text != '#':
            next_link_part = next_link_text.split("/")[-1]
            next_link_url = default_url.replace('id05011', next_link_part)
            #print(next_link_url)
            url = next_link_url
            extracted_url_list.append(url)
            time.sleep(2)
        else:
            print("All pages are scraped.")
            break

 
    print(extracted_url_list)
    return extracted_url_list

def extract_product_name(tag):
    product_name_tag = dummy_tag.find('a', class_='name')
    # extract product's name using text attribute
    product_name = product_name_tag.text
    return product_name
    
def extract_product_price(tag,class_name,div_name):
    product_price_tag = dummy_tag.find(price_dives_name, class_=price_classes_name)
    # extract product's price using text attribute
    product_price = product_price_tag.text
    return product_price
   
product_name_list = [] # to store extracted product name
product_price_list = [] # to store extracted product price
   
def extract_product_name(tag):
    product_name_tag = tag.find('a', class_='name')
    # extract product's name using text attribute
    product_name = product_name_tag.text
    return product_name
    
def extract_product_price(tag,class_name,div_name):
    product_price_tag = tag.find(div_name, class_=class_name)
    # extract product's price using text attribute
    product_price = product_price_tag.text
    return product_price

def main():
    #product_name_list = [] # to store extracted product name
    #product_price_list = [] # to store extracted product price
    count = 1
    page_lists = extract_page_list()
    for page in page_lists:
        headers = { 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " 
                      "AppleWebKit/537.36 (KHTML, like Gecko) " 
                      "Chrome/120.0.0.0 Safari/537.36", 
        "Accept-Encoding": "identity" 
        }
        session = requests.Session()  
        retry = Retry( 
            total=5, 
            backoff_factor=1, 
            status_forcelist=[429, 500, 502, 503, 504] 
        )  
        url = page
        session.mount("https://", HTTPAdapter(max_retries=retry))  
        response = session.get(url, headers=headers, timeout=30) 
        bsObj = BeautifulSoup(response.text, "html5lib")
        main_tags = bsObj.find_all('div', class_='card-body')
        print("Num of tags: ", len(main_tags))   

        for dummy_tag in tqdm(main_tags):
            try:
                product_name2 =extract_product_name(dummy_tag)
                product_name_list.append(product_name2)
                
                price_classes = ['product-sale-price','product-price mt-1']
                price_dives = ['span','p']
                for price_classes_name in price_classes:
                    for price_dives_name in price_dives:
                        try:
                            product_price2 = extract_product_price(dummy_tag,price_classes_name,price_dives_name)
                            #remove unwanted char from the price
                            product_price2 = product_price2.replace("Ks","")
                            product_price2 = product_price2.replace(",","")
                            product_price2 = int(product_price2)
                            product_price_list.append(product_price2)
                        except:
                            continue  
                            count = count + 1
                            print(count)
            except:
                print(dummy_tag)
                raise
                break
    #print(product_name_list)
    #print(product_price_list)
    # Export data as an Excel file.

    data_dic = {"Product Name":product_name_list,
                "Product Price":product_price_list}

    # Create a dataframe
    df = pd.DataFrame(data_dic)

    # Create filename version
    time_str = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    df.to_excel("CityMall_" + time_str + ".xlsx", index=False)

    print("All steps are completed!")

if __name__=="__main__":
    main()