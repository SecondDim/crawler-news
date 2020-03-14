'''
https://github.com/codelucas/newspaper

pip3 install newspaper3k
'''

import sys

from newspaper import Article

try:
    URL = sys.argv[1]
except IndexError:
    print('[X] please enter url')
    sys.exit(0)

print('[*] url: %s' % URL)

print('[F] ----- download & parse -----')
ARTICLE = Article(URL, language='zh')
ARTICLE.download()
ARTICLE.parse()

print('[*] authors: %s' % ARTICLE.authors)
print('[*] publish_date: %s' % ARTICLE.publish_date)
print('[*] text: %s' % ARTICLE.text)
print('[*] top_image: %s' % ARTICLE.top_image)
print('[*] movies: %s' % ARTICLE.movies)

ARTICLE.nlp()
print('[F] ----- article.nlp() -----')
print('[*] keywords: %s' % ARTICLE.keywords)
print('[*] summary: %s' % ARTICLE.summary)
