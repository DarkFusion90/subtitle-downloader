import requests
from bs4 import BeautifulSoup
import bs4
import zipapp

URL = 'https://subscene.com'


def initialize_script():
    q = 'Thor%3A%20Ragnarok'
    r = requests.get(URL + '/subtitles/title?q=%s&l=' % (q))
    soup = BeautifulSoup(r.content, 'html.parser')
    findSubtitle(soup)


def findSubtitle(soup):
    if noMatchingSubs(soup):
        print('No matching subs found. Please consider refining the keywords')
        return None

    search_results = list([soup.find('h2', {'class': 'exact'}), soup.find(
        'h2', {'class': 'close'}), soup.find('h2', {'class': 'popular'})])

    for result in search_results:
        if result == None:
            continue

        ul_tag = result.next_sibling
        while (ul_tag == '\n'):
            ul_tag = ul_tag.next_sibling

        div_result = ul_tag.find('div')
        subs_link = div_result.a['href']
        status = findSubsURL(subs_link)
        if status == True:
            break

def findSubsURL(url):
    r = requests.get(URL+url)
    soup = BeautifulSoup(r.content, 'html.parser')
    content_div = soup.find('div', {'class': ['content', 'clearfix']})
    subs_table = content_div.find('table')
    subs_table_body = subs_table.tbody
    subs_matching_language = find_subs_matching_lang(subs_table_body, 'English')
    downloadSubtitle(subs_matching_language)
    return True


def find_subs_matching_lang(table_body, lang):
    for tr_tag in table_body.find_all('tr'):
        td_tag = tr_tag.find('td', {'class': 'a1'})
        if td_tag == None:
            continue
        a_href_tag = td_tag.a
        subs_lang = a_href_tag.find('span', {'class': ['l', 'r', 'positive-icon']}).text
        subs_lang = subs_lang.strip()
        if subs_lang != lang:
            continue
        return a_href_tag['href']

def downloadSubtitle(subs_url):
    r = requests.get(URL + subs_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    download_div = soup.find('div', {'class':'download'})
    download_link = download_div.a['href']
    
    content = requests.get(URL + download_link).content
    with open('SUBS.zip', 'wb') as file:
        file.write(content)

def noMatchingSubs(soup):
    if soup.find('h2') == None:
        return True
    return soup.find('h2').text == 'No results found'


if __name__ == "__main__":
    initialize_script()
