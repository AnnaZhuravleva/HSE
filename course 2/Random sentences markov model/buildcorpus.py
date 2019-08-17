import re
import urllib.request
import html.parser
import html

commonUrl = 'https://ling.hse.ru/news/'


def download_page(pageUrl):
    req = urllib.request.Request(pageUrl)
    with urllib.request.urlopen(req) as page:
        html_text = page.read().decode('utf-8', 'ignore')
    return html_text


def get_news_links(Source_HTML):
    numbers = re.findall('href="https://ling.hse.ru/news/([0123456789]+).html"', Source_HTML)
    urls = []
    for number in numbers:
        urls.append('https://ling.hse.ru/news/' + number + '.html')
    print(urls)
    return urls


def get_news_text(Source_HTML):
    text = re.findall('<div class="lead-in">(.*?)<style type="text/css">', Source_HTML.replace('\n','').replace('\r',''))
    text = tegs_cleaning(''.join(text))
    return text


def tegs_cleaning(html_text):
    regTag = re.compile('<.*?>', re.DOTALL)
    regScript = re.compile(u'<script.*?</script>', re.DOTALL)
    regComment = re.compile('<!--.*?-->', re.DOTALL)
    clean = regScript.sub('', html_text)
    clean = regComment.sub("", clean)
    clean = regTag.sub("", clean)
    clean = html.unescape(clean)
    return clean


if __name__ == '__main__':
    with open('news.txt', 'w', encoding='utf-8') as f:
        for i in range(1, 47):
            page_url = 'https://ling.hse.ru/news/page' + str(i) + '.html'
            urls = get_news_links(download_page(page_url))
            for url in urls:
                try:
                    f.write(get_news_text(download_page(url)))
                    f.write('\n')
                except:
                    pass