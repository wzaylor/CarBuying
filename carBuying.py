import requests
import bs4
import re
import cPickle
import time
import numpy as np

# Define the car make class
class CarMake(object):
    def __init__(self, carMake, urls = None, cookies = None):
        self.cookies = cookies
        self.make = carMake
        for url in urls:
            self.getModelsKBB(carMake, url)

    def getModelsKBB(self, carMake, url):
        makeURL = url + '/' + urlize_word(carMake)
        html = fetch(makeURL, cookies=self.cookies)

        for model in html.find_all('a', class_='section-title'):
            modelName = filter(None, model.attrs['href'].split('/'))
            modelName = modelName[1]
            if modelName in ['Civic', 'civic']:
                car = CarModel(modelName, makeURL)

class CarModel(object):
    def __init__(self, modelName, makeURL, years = ['2011', '2012', '2013'], cookies = None):
        self.urlKBB = 'http://www.kbb.com'
        self.mileage = range(30000, 100000, 10000)
        self.name = modelName
        self.cookies = cookies
        self.data = {}
        self.getYearKBB(makeURL, years)

    def getYearKBB(self, makeURL, years):
        modelURL = makeURL + '/' + self.name
        html = fetch(modelURL, cookies=self.cookies)
        self.data['years'] = years
        for year in years:
            for link in html.find_all('a', class_='section-title'):
                if year in link.attrs['href']:
                    yearURL = self.urlKBB + link.attrs['href']
                    self.getStyleKBB(yearURL, year)
        return

    def getStyleKBB(self, yearURL, year, type = 'Sedan', condition = 'good'):
        self.data[str(year)] = {}
        link = self.getLink(yearURL,text = 'Buying this car?' )
        try:
            link = self.getLink(self.urlKBB + link, text = type)
        except:
            pass
        links = self.getLinks(self.urlKBB + link, className='right btn-main-cta')

        

        for link in links:
            style = str(self.getStyle(link))
            self.data[str(year)][style] = {}
            self.data[str(year)][style]['priceMin'] = np.zeros((len(self.mileage), 2))
            self.data[str(year)][style]['price'] = np.zeros((len(self.mileage), 2))
            self.data[str(year)][style]['priceMax'] = np.zeros((len(self.mileage), 2))
            self.data[str(year)][style]['priceMin'][:,0] = self.mileage
            self.data[str(year)][style]['price'][:,0] = self.mileage
            self.data[str(year)][style]['priceMax'][:,0] = self.mileage
            for i, mileage in enumerate(self.mileage):
                
                mileageURL = self.urlKBB + self.setMileage(link.attrs['href'], mileage)
                styleURL = mileageURL + '&condition=good&pricetype=retail'
                priceMin, price, priceMax = self.getPriceJavascript(styleURL)
                self.data[str(year)][style]['priceMin'][i,1] = priceMin
                self.data[str(year)][style]['price'][i,1] = price
                self.data[str(year)][style]['priceMax'][i,1] = priceMax

                print '***************************'
                print year, style, mileage
                print priceMin, price, priceMax
            break
            
        return

    def getStyle(self, link):
        text = link.previous_element.previous_element
        style = text.split('\r')[0]
        return style
    
    def getPrice(self, priceVar, text):
        priceText = priceVar + '":'
        price = text.split(priceText, 1)[1].rsplit('.0')[0]
        return float(price)

    def getPriceJavascript(self, URL):
        html = fetch(URL, cookies = self.cookies)
        script = html.find('script', type='text/javascript', language='javascript')
        scriptText = script.text.split('"fpp"', 1)[1]
        priceMin = self.getPrice('priceMin', scriptText)
        price = self.getPrice('price', scriptText)
        priceMax = self.getPrice('priceMax', scriptText)
        return priceMin, price, priceMax

    def setMileage(self, originalURL, mileage, condition = 'good'):
        def setCondition(URL, condition):
            splitURL = URL.split('options/',1)
            frontURL = splitURL[0]
            backURL = splitURL[1] + '&' + 'condition=' + condition
            return frontURL + backURL
        URL = setCondition(originalURL, condition)
        splitURL = URL.split('&mileage=',1)
        frontURL = splitURL[0]
        backURL = splitURL[1].rsplit('&')[1]
        mileageURL = frontURL + '&mileage=' + str(mileage) + '&' + backURL
        return mileageURL

    def getLink(self, currentURL, className = None, type = 'a', text = None):
        html = fetch(currentURL, cookies = self.cookies)
        if className != None:
            link = html.find(type, class_=className)
        elif text != None:
            link = html.find(type, text=text)
        return link.attrs['href']

    def getLinks(self, currentURL, className = None, type = 'a', text = None):
        html = fetch(currentURL, cookies = self.cookies)
        if className != None:
            links = html.find_all(type, class_=className)
        elif text != None:
            links = html.find_all(type, text=text)
        return links

# Utility functions
def fetch(url, cookies=None):
    #print('fetching: {}'.format(url))
    resp = requests.get(url, cookies=cookies)
    html = bs4.BeautifulSoup(resp.content)
    if html.find_all(re.compile('page not found', re.IGNORECASE)):
        raise PageNotFoundError
    return html

# Make 'word' safe to put in a URL
def urlize_word(word):
    return word.strip().replace(' ', '-').lower()

def pause():
    time.sleep(1)
    return

if __name__ == '__main__':
    cookies = {'ZipCode': '44146'}
    urls = ['http://www.kbb.com']
    #honda = CarMake('Honda', urls = urls, cookies = cookies)
    x = CarModel('Civic', 'http://www.kbb.com/honda/', cookies = cookies)

    with open('Civic.dat', mode = 'w') as file:
        cPickle.dump(x.data, file)