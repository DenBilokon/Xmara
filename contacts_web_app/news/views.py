import json
from datetime import datetime

from users.views import date_today
from contacts_web_app.settings import CRYPTO_API_KEY
import requests
import re

from bs4 import BeautifulSoup

from django.shortcuts import render

from users.models import Avatar


def home(request):
    """
    The home function is the main view of the website. It renders a template
        with information about currency and crypto-currency rates, as well as
        news articles from various sources.
    
    :param request: Get the request object
    :return: A rendered template
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    currency_info = read_currency_from_file()
    crypto_currency_info = read_crypto_currency_from_file()
    return render(request, "news/index.html", context={'currency_info': currency_info,
                                                       'crypto_currency_info': crypto_currency_info,
                                                       'date': date_today,
                                                       'avatar': avatar})


def news_war(request):
    """
    The news_war function is a view that renders the news_war.html template,
        which displays the short war news from tsn.ua website.
    
    :param request: Pass the request object to the view
    :return: The news_war
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    short_news = tsn_war_spider()
    currency_info = read_currency_from_file()
    return render(request, "news/news_war.html", context={'short_news': short_news,
                                                          'currency_info': currency_info,
                                                          'date': date_today,
                                                          'avatar': avatar})


def news_war_show_one(request, _id):
    """
    The news_war_show_one function is used to render the one_news.html template, which displays a single news item
    from the TSN website. The function takes in an id parameter and uses it to find a matching news item from the list of
    shortened news items returned by tsn_war_spider(). If there is no match, then not_found.html will be rendered instead.
    
    :param request: Get the information about the current user
    :param _id: Get the news item from the list of short news
    :return: A response object
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    currency_info = read_currency_from_file()
    short_news = tsn_war_spider()
    news_item = next((item for item in short_news if item['id'] == _id), None)
    if news_item:
        news_details = tsn_page_spider(news_item['href'], news_item['data_src'], news_item['datetime'])
        return render(request, 'news/one_news.html', context={'news_item': news_item,
                                                              'news_details': news_details,
                                                              'currency_info': currency_info,
                                                              'date': date_today,
                                                              'avatar': avatar})
    else:
        return render(request, 'news/not_found.html')


def news_prosport(request):
    """
    The news_prosport function is responsible for rendering the news_prosport.html template,
    which displays a list of short news from the prosport.ua website.
    
    :param request: Get the request object, which contains information about the current web request
    :return: A page with the news_prosport
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    currency_info = read_currency_from_file()
    short_news = tsn_prosport_spider()
    return render(request, "news/news_prosport.html", context={'short_news': short_news,
                                                               'currency_info': currency_info,
                                                               'date': date_today,
                                                               'avatar': avatar})


def news_prosport_show_one(request, _id):
    """
    The news_prosport_show_one function is used to show one news item from the Prosport website.
        It takes a request and an id as arguments, then it gets the avatar of the user who made this request,
        reads currency info from file, gets short news list from tsn_prosport_spider function and finds a news item with 
        given id in this list. If such an item exists it calls tsn_page_spider function to get detailed information about 
        this particular article and renders one_prosport_news template with all necessary data.
    
    :param request: Get the request object, which contains information about the current http request
    :param _id: Identify the news item in the database
    :return: The news_item, which is a dictionary
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    currency_info = read_currency_from_file()
    short_news = tsn_prosport_spider()
    news_item = next((item for item in short_news if item['id'] == _id), None)
    if news_item:
        news_details = tsn_page_spider(news_item['href'], news_item['data_src'], news_item['datetime'])
        return render(request, 'news/one_prosport_news.html', context={'news_item': news_item,
                                                                       'news_details': news_details,
                                                                       'currency_info': currency_info,
                                                                       'date': date_today,
                                                                       'avatar': avatar})
    else:
        return render(request, 'news/not_found.html')


def war_statistic(request):
    """
    The war_statistic function is responsible for parsing the war_statistic.txt file and displaying it on the page.
    
    :param request: Get the current user
    :return: The war_statistic
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    currency_info = read_currency_from_file()
    war_stat = war_stat_parse()
    return render(request, "news/war_statistic.html", context={'war_statistic': war_stat,
                                                               'currency_info': currency_info,
                                                               'date': date_today,
                                                               'avatar': avatar})


def when_bored(request):
    """
    The when_bored function is a view that returns the bored.html template, which displays an activity to do when bored.
    
    :param request: Pass the request object to the view
    :return: A rendered template
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    url = "https://www.boredapi.com/api/activity/"
    response = requests.get(url).json()
    currency_info = read_currency_from_file()
    crypto_currency_info = read_crypto_currency_from_file()
    return render(request, 'news/index.html', context={'bored': response,
                                                       'currency_info': currency_info,
                                                       'crypto_currency_info': crypto_currency_info,
                                                       'date': date_today,
                                                       'avatar': avatar})


def tsn_war_spider():
    """
    The tsn_war_spider function scrapes the TSN.ua website for news articles related to the war in Ukraine, and returns a list of dictionaries containing information about each article.
    
    :return: A list of dictionaries
    :doc-author: Trelent
    """
    base_url = 'https://tsn.ua/ato'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    element = soup.select(
        '.l-page__main.l-sheet.l-sheet__gap .l-flex.l-row .l-gap.l-col.l-col--xl .c-section .l-col.l-col--sm.l-gap')

    news_list = []

    for article in element:
        news_dict = {}

        link = article.find('a', class_='c-card__link')
        id_match = re.search(r'\d+', link['href']) if link else None
        news_dict['id'] = int(id_match.group(0)) if id_match else None

        img = article.find('img', class_='c-card__embed__img')
        news_dict['data_src'] = img['data-src'] if img else None

        link = article.find('a', class_='c-card__link')
        news_dict['href'] = link['href'] if link else None

        title = article.find('h3', class_='c-card__title')
        news_dict['title'] = title.text.strip() if title else None

        time = article.find('time', datetime=True)
        if time:
            datetime_str = time['datetime']
            datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")
            formatted_datetime = datetime_obj.strftime("%H:%M %d.%m.%Y")
            news_dict['datetime'] = formatted_datetime
        else:
            news_dict['datetime'] = None

        if news_dict['id']:
            news_list.append(news_dict)

    return news_list


def tsn_prosport_spider():
    """
    The tsn_prosport_spider function scrapes the TSN Prosport news page and returns a list of dictionaries.
    Each dictionary contains information about one article:
        - href (str): link to the article;
        - id (int): unique identifier of an article;
        - data_src (str): link to the image on the main page; 
        - title (str): title of an article;
        - datetime(str) : time when an article was published.
    
    :return: A list of dictionaries
    :doc-author: Trelent
    """
    base_url = 'https://tsn.ua/prosport'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    element = soup.select(
        '.l-page__main.l-sheet .l-sheet__gap .c-section.u-divider--t .l-row.l-flex.u-hide--sdmd .l-col.l-col--xs.l-gap')

    news_list = []

    for article in element:
        link = article.find('a', class_='c-card__link')

        news_dict = {}
        news_dict['href'] = link['href'] if link else None

        id_match = link['href'].split('/')[-1].split('-')[-1].split('.')[0] if news_dict['href'] else None
        news_dict['id'] = int(id_match) if id_match else None

        img = article.find('img', class_='c-card__embed__img')
        news_dict['data_src'] = img['data-src'] if img else None

        title = article.find('h3', class_='c-card__title')
        news_dict['title'] = title.text.strip() if title else None

        time = article.find('time', datetime=True)
        if time:
            datetime_str = time['datetime']
            datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")
            formatted_datetime = datetime_obj.strftime("%H:%M %d.%m.%Y")
            news_dict['datetime'] = formatted_datetime
        else:
            news_dict['datetime'] = None

        if news_dict['id']:
            news_list.append(news_dict)

    return news_list


def tsn_page_spider(url, img_link, news_date):
    """
    The tsn_page_spider function takes in a url, img_link and news_date as parameters.
    It then makes a request to the url and parses the response using BeautifulSoup.
    The function then searches for all elements with class 'l-page__main l-sheet l-sheet__gap .l-flex l-row .l-col 
        l-col--xl l-gap .carticle carticle__box' within the soup object. It iterates through each of these elements, 
        creating an empty dictionary called one_news_dict on each iteration. The function then searches for
    
    :param url: Pass the url of the page to be scraped
    :param img_link: Pass the image link to the tsn_page_spider function
    :param news_date: Pass the date of the news to tsn_page_spider function
    :return: A single dictionary
    :doc-author: Trelent
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    element = soup.select(
        '.l-page__main.l-sheet.l-sheet__gap .l-flex.l-row .l-col.l-col--xl.l-gap .c-article .c-article__box')

    for article in element:
        one_news_dict = {}

        head_content = article.find('h1', class_='c-card__title')
        span = head_content.find('span') if head_content else None
        one_news_dict['head_content'] = span.text.strip() if span else None

        content = article.find('div', class_='c-article__body')
        cleaned_content = content.text

        read_more_index = cleaned_content.find('Читайте також:')
        if read_more_index != -1:
            cleaned_content = cleaned_content[:read_more_index]

        one_news_dict['content'] = cleaned_content if cleaned_content else None

        one_news_dict['src_img'] = img_link
        one_news_dict['news_date'] = news_date

        return one_news_dict


def war_stat_parse():
    """
    The war_stat_parse function takes the URL of a JSON file and returns a dictionary with two keys:
        war_stats - A list of dictionaries containing the statistics for each ship type.
        war_increase - A list of dictionaries containing the increase in statistics for each ship type.
    
    :return: A dictionary with two keys: war_stats and war_increase
    :doc-author: Trelent
    """
    url = 'https://russianwarship.rip/api/v2/statistics/latest'
    war_data = {}
    response = requests.get(url)
    war_stats = json.loads(response.text).get('data').get('stats')
    war_increase = json.loads(response.text).get('data').get('increase')
    war_data['war_stats'] = war_stats
    war_data['war_increase'] = war_increase

    return war_data


def currency_parse():
    """
    The currency_parse function takes the date_today variable and uses it to query the PrivatBank API.
    The response is then parsed into a dictionary with currency names as keys and exchange rates as values.
    
    :return: A dictionary
    :doc-author: Trelent
    """
    url = f"https://api.privatbank.ua/p24api/exchange_rates?date={date_today}"
    response = requests.get(url)
    currency_data = json.loads(response.text).get('exchangeRate')
    currency_dict = {"currency_USD": currency_data[23],
                     "currency_EUR": currency_data[8],
                     "currency_GBP": currency_data[9],
                     "currency_PLN": currency_data[17],
                     "currency_CZK": currency_data[6],
                     "currency_JPY": currency_data[13],
                     "currency_MDL": currency_data[15],
                     "currency_CHF": currency_data[4],
                     "currency_CAD": currency_data[3],
                     "currency_DKK": currency_data[7]
                     }

    return currency_dict


def add_currency_to_file():
    """
    The add_currency_to_file function takes the currency_dict dictionary and writes it to a file called 'currency_data.json'
    
    :return: A dictionary of currencies and their values
    :doc-author: Trelent
    """
    currency_dict = currency_parse()
    file_path = "currency_data.json"
    with open(file_path, "w") as file:
        json.dump(currency_dict, file, indent=4)


def read_currency_from_file():
    """
    The read_currency_from_file function reads the currency_data.json file and returns a dictionary of the data.
    
    :return: A dictionary
    :doc-author: Trelent
    """
    file_path = "currency_data.json"
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("File not found")
        return None


def crypto_currency_parse():
    """
    The crypto_currency_parse function takes no arguments and returns a dictionary of the current exchange rates for 
    the top 10 cryptocurrencies. The function uses the CoinAPI API to get the data, which is then parsed into a dictionary 
    with each cryptocurrency as a key and its exchange rate as its value.
    
    :return: A dictionary
    :doc-author: Trelent
    """
    cryptocurrencies_list = ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'SOL', 'MATIC', 'TRX', 'LTC']
    crypto_dict = {}
    for i in cryptocurrencies_list:
        url = f'https://rest.coinapi.io/v1/exchangerate/{i}/USD'
        api_key = CRYPTO_API_KEY
        headers = {"X-CoinAPI-Key": api_key}
        response = requests.get(url, headers=headers).json()
        if response:
            crypto_dict[i] = round(response.get('rate'), 4)

    return crypto_dict


def add_crypto_currency_to_file():
    """
    The add_crypto_currency_to_file function takes the crypto_currency_dict dictionary and writes it to a file called cryptocurrency_data.json
    
    :return: None
    :doc-author: Trelent
    """
    crypto_currency_dict = crypto_currency_parse()
    file_path = "cryptocurrency_data.json"
    with open(file_path, "w") as file:
        json.dump(crypto_currency_dict, file, indent=4)


def read_crypto_currency_from_file():
    """
    The read_crypto_currency_from_file function reads the cryptocurrency_data.json file and returns a dictionary of 
    cryptocurrency data.
    
    :return: A dictionary
    :doc-author: Trelent
    """
    file_path = "cryptocurrency_data.json"
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("File not found")
        return None




