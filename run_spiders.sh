spiders=$(scrapy list)
for spider in $spiders
do
    echo $spider
    scrapy crawl $spider
done
echo '[*] Done'
