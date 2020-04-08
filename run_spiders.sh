sleep 60
while :
do
    spiders=$(scrapy list)
    for spider in $spiders
    do
        if [ "${spider}" == "localhost" ]; then
            continue
        fi
        echo "[+] [$(date +"%Y-%m-%d %H:%M:%S")] ${spider}"
        scrapy crawl $spider
    done
    echo '[*] Done.wait 5 second'
    sleep 5
done

