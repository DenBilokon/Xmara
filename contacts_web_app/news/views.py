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
    The home function is the main function of the news app. It renders
    the index.html template, which contains all of the information that
    is displayed on our home page.

    :param request: Get the data from the request object
    :return: The index
    :doc-author: Xmara
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
    which displays short war-related news articles from the tsn.ua website.

    :param request: Get the user's avatar
    :return: The news_war
    :doc-author: Xmara
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
    The news_war_show_one function is used to display a single news item from the TSN.ua website.
    It takes an id of a news item as an argument and returns the page with this particular news.

    :param request: Get information about the current request
    :param _id: Pass the id of a news item to the function
    :return: The news_item and news_details variables
    :doc-author: Xmara
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
    The news_prosport function is used to render the news_prosport.html template,
    which displays a list of short news from the prosport.ua website.

    :param request: Get the current user's avatar
    :return: The news_prosport
    :doc-author: Xmara
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
    the currency info from file and a list of short news items (title, date/time and image) using tsn_prosport_spider function.
    Then it looks for an item with such id in this list using next() function. If there is no such item in the list -
    it renders not found page template; if there is - it uses tsn_page_spider function to get detailed information about

    :param request: Get the request object
    :param _id: Get the news item with the same id from a list of short news items
    :return: A page with a detailed description of the news
    :doc-author: Xmara
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
    The war_statistic function is responsible for displaying the war statistic page.
    It takes a request as an argument and returns a render of the news/war_statistic.html template,
    which displays all of the information about wars that have been fought in this game.

    :param request: Get the user id from the request object
    :return: A page with a table of statistics on the war
    :doc-author: Xmara
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
    The when_bored function is a view that returns the bored.html template,
        which displays an activity to do when you're bored. The function also
        passes in the date and currency information as context.

    :param request: Get the user id from the request
    :return: The index
    :doc-author: Xmara
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
    The tsn_war_spider function scrapes the TSN.ua website for news articles about the war in Ukraine,
    and returns a list of dictionaries containing information about each article:
        - id (int) - unique identifier of an article;
        - data_src (str) - url to image;
        - href (str) - url to full text of an article;
        - title (str) – title of an article;
        and datetime(str): time when the news was published.

    :return: A list of dictionaries
    :doc-author: Xmara
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
    Each dictionary contains information about one article: its id, title, datetime and href.

    :return: A list of dictionaries
    :doc-author: Xmara
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
    The tsn_page_spider function takes in a url, img_link and news_date as arguments.
    It then makes a request to the url and parses the response using BeautifulSoup.
    The function then searches for an element with class 'l-page__main l-sheet l-sheet__gap .l-flex l-row .l-col
        l-col--xl l gap c article c article box' within that element it finds another element with class 'c card title'
        which is assigned to head content variable. It also finds an element with class 'span' within head content variable


    :param url: Pass the url of the page we want to scrape
    :param img_link: Pass the link of the image to be displayed with the news
    :param news_date: Pass the date of the news to tsn_page_spider function
    :return: A dictionary, but we need a list of dictionaries
    :doc-author: Xmara
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
    The war_stat_parse function takes the URL of a Russian Warship API and returns a dictionary with two keys:
        'war_stats' which contains the latest statistics for all ships in the game, and
        'war_increase' which contains an increase in stats from previous day.

    :return: A dictionary with two keys, war_stats and war_increase
    :doc-author: Xmara
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
    The currency_parse function takes the current date and uses it to query the PrivatBank API for currency exchange rates.
    The function returns a dictionary of currency exchange rates.

    :return: A dictionary with currencies
    :doc-author: Xmara
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
    The add_currency_to_file function takes the currency_parse function and writes it to a file.
    It then opens the file, dumps the data into json format, and closes it.

    :return: A dictionary of currency data
    :doc-author: Xmara
    """
    currency_dict = currency_parse()
    file_path = "currency_data.json"
    with open(file_path, "w") as file:
        json.dump(currency_dict, file, indent=4)


def read_currency_from_file():
    """
    The read_currency_from_file function reads the currency_data.json file and returns a dictionary of the data.

    :return: A dictionary
    :doc-author: Xmara
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
    the top 10 cryptocurrencies. The function uses the CoinAPI API to get this data.

    :return: A dictionary with the following structure:
    :doc-author: Xmara
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
    The add_crypto_currency_to_file function takes the crypto_currency_parse function and writes it to a file.
    The file is called cryptocurrency_data.json.

    :return: Nothing
    :doc-author: Xmara
    """
    crypto_currency_dict = crypto_currency_parse()
    file_path = "cryptocurrency_data.json"
    with open(file_path, "w") as file:
        json.dump(crypto_currency_dict, file, indent=4)


def read_crypto_currency_from_file():
    """
    The read_crypto_currency_from_file function reads the cryptocurrency_data.json file and returns a dictionary of
    the data in the file.

    :return: A dictionary
    :doc-author: Xmara
    """
    file_path = "cryptocurrency_data.json"
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("File not found")
        return None




