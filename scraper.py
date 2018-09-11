import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import requests
from bs4 import BeautifulSoup


def get_sitetext(url):
    """
        Get site text, strip html and js
        Returns: text w/o linebreaks
    """
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')

        # strip js
        for script in soup(["script", "style"]):
            script.decompose()

        return ' '.join(soup.get_text(' ').split())
    else:
        return False


def tokenize(text):
    """ """
    return [w for w in text.split()]


def word_frequency(tokens):
    """ """
    clean_tokens = tokens[:]
    for token in tokens:
        if token in stopwords.words('english'):
            clean_tokens.remove(token)
    return nltk.FreqDist(tokens)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description='Scrape a site, analyze text.')
    # p.add_argument('-c', '--config', dest='config_file', default='config.json', help='Set config file. Default: archiveTable.json.')
    p.add_argument('-u', '--url', required=True, help='URL of page to scrape')
    args = p.parse_args()

    if args.url:
        text = get_sitetext(args.url)
        tokens = tokenize(text)
        frequency = word_frequency(tokens)
        print(frequency.__dict__)
