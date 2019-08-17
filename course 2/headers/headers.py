import urllib.request
import re


def main():
    req = urllib.request.Request('https://magazines.gorky.media/ural')
    with urllib.request.urlopen(req) as response:
       html = response.read().decode('utf-8')
    titles = re.findall('<p>(Номер .*)<.p>', html)
    with open('Заголовки.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(titles))


if __name__ == '__main__':
    main()
