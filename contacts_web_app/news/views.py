import json
from datetime import datetime, date

from users.views import currency_parse, weather_parse
import requests
import re

from bs4 import BeautifulSoup

from django.shortcuts import render

currency_info = currency_parse()
weather_info = weather_parse()


def home(request):
    return render(request, "news/index.html", context={'currency_info': currency_info,
                                                       'date': date.today().strftime('%d.%m.%Y'),
                                                       'weather_info': weather_info})


def news_war(request):
    short_news = tsn_war_spider()
    return render(request, "news/news_war.html", context={'short_news': short_news,
                                                          'currency_info': currency_info,
                                                          'weather_info': weather_info,
                                                          'date': date.today().strftime('%d.%m.%Y')})


def news_war_show_one(request, _id):
    short_news = tsn_war_spider()
    news_item = next((item for item in short_news if item['id'] == _id), None)
    if news_item:
        news_details = tsn_page_spider(news_item['href'], news_item['data_src'], news_item['datetime'])
        return render(request, 'news/one_news.html', context={'news_item': news_item,
                                                              'news_details': news_details,
                                                              'currency_info': currency_info,
                                                              'weather_info': weather_info,
                                                              'date': date.today().strftime('%d.%m.%Y')})
    else:
        return render(request, 'news/not_found.html')


def news_prosport(request):
    short_news = tsn_prosport_spider()
    return render(request, "news/news_prosport.html", context={'short_news': short_news,
                                                               'currency_info': currency_info,
                                                               'weather_info': weather_info,
                                                               'date': date.today().strftime('%d.%m.%Y')})


def news_prosport_show_one(request, _id):
    short_news = tsn_prosport_spider()
    news_item = next((item for item in short_news if item['id'] == _id), None)
    if news_item:
        news_details = tsn_page_spider(news_item['href'], news_item['data_src'], news_item['datetime'])
        return render(request, 'news/one_prosport_news.html', context={'news_item': news_item,
                                                                       'news_details': news_details,
                                                                       'currency_info': currency_info,
                                                                       'weather_info': weather_info,
                                                                       'date': date.today().strftime('%d.%m.%Y')})
    else:
        return render(request, 'news/not_found.html')


def war_statistic(request):
    war_stat = war_stat_parse()
    return render(request, "news/war_statistic.html", context={'war_statistic': war_stat,
                                                               'currency_info': currency_info,
                                                               'weather_info': weather_info,
                                                               'date': date.today().strftime('%d.%m.%Y')})


def tsn_war_spider():
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
    url = 'https://russianwarship.rip/api/v2/statistics/latest'
    war_data = {}
    response = requests.get(url)
    war_stats = json.loads(response.text).get('data').get('stats')
    war_increase = json.loads(response.text).get('data').get('increase')
    war_data['war_stats'] = war_stats
    war_data['war_increase'] = war_increase

    return war_data
