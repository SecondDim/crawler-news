while :
do
    spiders=$(scrapy list)
    for spider in $spiders
    do
        if [ "${spider}" == "localhost" ]; then
            continue
        fi
        echo "[+] ${spider}"
        scrapy crawl $spider
    done
    echo '[*] Done.wait 5 second'
    sleep 5
done

