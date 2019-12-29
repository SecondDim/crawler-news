while :
do
    spiders=$(scrapy list)
    for spider in $spiders
    do
        echo $spider
        scrapy crawl $spider
    done
    echo '[*] Done.wait 5 min'
    sleep 5m
done

