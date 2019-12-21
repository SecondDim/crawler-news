'''
https://github.com/codelucas/newspaper

pip3 install newspaper3k
'''

from newspaper import Article

import sys

try:
    url = sys.argv[1]
except IndexError:
    print('[X] please enter url')
    sys.exit(0)

print('[*] url: %s' % url)

print('[F] ----- download & parse -----')
article = Article(url, language='zh')
article.download()
article.parse()

print('[*] authors: %s' % article.authors)
print('[*] publish_date: %s' % article.publish_date)
print('[*] text: %s' % article.text)
print('[*] top_image: %s' % article.top_image)
print('[*] movies: %s' % article.movies)

article.nlp()
print('[F] ----- article.nlp() -----')
print('[*] keywords: %s' % article.keywords)
print('[*] summary: %s' % article.summary)
