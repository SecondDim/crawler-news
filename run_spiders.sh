sleep 10
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
    echo '[*] Done.wait 300 second'
    sleep 300
done

