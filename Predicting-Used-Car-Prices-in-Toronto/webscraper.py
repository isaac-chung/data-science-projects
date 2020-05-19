from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np

def scrape(front_url, back_url='' ,num=[], to_file='out.csv'):
'''
    front_url (str): url of website to be scraped. Starts with 'https://'.
    back_url (str, optional): url trailing the page/results count.
    num (list of int, optional): list of integers for page/results count. E.g. [100,200,300] or [0,1,2,3].
    to_file (str,optional): the output csv will be saved to this file name.
'''

    # Autotrader, used sedans
    cars=[]
    prices=[]
    mileages=[]

    # create list of urls to be loped through
    if num == [] and back_url == '':
        url_list = [front_url]
    else:
        url_list = ["{}{}{}".format(front_url,str(page),back_url) for page in num]

    # psuedo headers for the psuedo browser access
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    for url in url_list:
        response = requests.get(url, timeout=5, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # the following is very specific to the website
        for a in soup.findAll('div', attrs={'class':'newSRPDesign'}):
            # add any interested attributes here
            name=a.find('span', attrs={'itemprop':'itemOffered'})
            price=a.find('span', attrs={'class':'price-amount'})
            mileage=a.find('div', attrs={'class':'kms'})
            cars.append(name.text.strip())
            prices.append(price.text)
            mileages.append(mileage.text.strip())

    # save our scraped data
    df = pd.DataFrame({'Cars':cars,'Price':prices,'Mileage':mileages}) 
    df.to_csv(to_file, index=False, encoding='utf-8')
    
    print('Scrape successful!')
    return True


if '__name__' == '__main__':
    
    #backup front page
    base_url = 'https://www.autotrader.ca/cars/on/toronto/?rcp=100&rcs=0&srt=3&prx=50&prv=Ontario&loc=M5S%202P9&body=Sedan&hprc=True&wcp=True&sts=Used&adtype=Private&showcpo=1&scpty=5%20seats&inMarket=advancedSearch'
    front_url = 'https://www.autotrader.ca/cars/on/toronto/?rcp=100&rcs='
    back_url = '&srt=3&prx=50&prv=Ontario&loc=M5S%202P9&body=Sedan&hprc=True&wcp=True&sts=Used&adtype=Private&showcpo=1&scpty=5%20seats&inMarket=advancedSearch' 
    
    #the search contains 15 pages
    num = np.arange(15)*100
    
    scrape(front_url,back_url,num,to_file='autotrader.csv')
    