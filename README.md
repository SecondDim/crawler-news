# Python Crawler for News

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Scrapy](https://img.shields.io/badge/scrapy-2.13.4-green)

A real-time news crawler built with Python and Scrapy, designed to fetch latest news from major Taiwan news websites.
使用 Python Scrapy 建置的台灣新聞網站即時爬蟲。

## Features

- **Real-time Crawling**: Fetches the latest news updates efficiently.
- **Multiple Sources**: Supports various major Taiwan news outlets.
- **Flexible Storage**: Supports saving data to Cassandra, MySQL, or JSON (via pipelines).
- **Extensible**: Easy to add new spiders for additional news sites.
- **Docker Support**: Ready-to-use Docker configuration for easy deployment.

## Supported News Sites

| News Site | Website | Status |
|-----------|---------|--------|
| 自由時報 (Liberty Times) | [Website](https://www.ltn.com.tw/) | ✅ Active |
| 東森新聞 (EBC) | [Website](https://news.ebc.net.tw/) | ✅ Active |
| 聯合新聞網 (UDN) | [Website](https://udn.com/news/index) | ✅ Active |
| 今日新聞 (NOWnews) | [Website](https://www.nownews.com/) | ✅ Active |
| ETtoday | [Website](https://www.ettoday.net/) | ✅ Active |
| 中時電子報 (China Times) | [Website](https://www.chinatimes.com/) | ✅ Active |
| TVBS | [Website](https://news.tvbs.com.tw/) | ✅ Active |
| 三立新聞網 (SETN) | [Website](https://www.setn.com/) | ✅ Active |
| 中央通訊社 (CNA) | [Website](https://www.cna.com.tw/) | ✅ Active |
| 巴哈姆特 (Gamer) | [Website](https://gnn.gamer.com.tw/) | 🚧 TODO |
| 風傳媒 (Storm) | [Website](https://www.storm.mg/) | 🚧 TODO |

## Requirements

- Python 3.9+
- Redis (for deduplication and queue management)
- Database (Optional): Cassandra or MySQL

## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/SecondDim/crawler-news.git
    cd crawler-news
    ```

2. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configuration**
    Copy the example settings file and configure your environment:

    ```bash
    cp crawler_news/settings.py.example crawler_news/settings.py
    ```

    Edit `crawler_news/settings.py` to set up your database connections (Redis, MySQL, Cassandra) and other preferences.

## Usage

### Run All Spiders

To run all spiders sequentially:

```bash
python app.py
# or
./run.sh
```

### Run a Single Spider

To run a specific spider (e.g., `ettoday`):

```bash
scrapy crawl ettoday
```

Available spiders: `chinatimes`, `cna`, `ebc`, `ettoday`, `libertytimes`, `nownews`, `setn`, `tvbs`, `udn`.

## Docker Deployment

You can run the crawler using Docker to avoid environment setup issues.

### Build Image

```bash
docker build . -t crawler_news
```

### Run with Docker Compose

```bash
# Start services (Crawler + Redis + DBs if configured)
docker-compose up -d

# Stop services
docker-compose down
```

### Run Manually

```bash
# Run without database (using local tmp/log folders)
docker run --rm -it -v $(pwd)/tmp:/src/tmp -v $(pwd)/log:/src/log crawler_news
```

## Project Structure

```text
crawler-news/
├── crawler_news/           # Main Scrapy project folder
│   ├── spiders/            # Spider definitions (one per news site)
│   ├── pipelines/          # Data processing pipelines (DB, JSON)
│   ├── extensions/         # Custom extensions (DB connectors)
│   ├── items.py            # Data models
│   └── settings.py         # Project configuration
├── docker/                 # Docker related files
├── app.py                  # Script to run all spiders
├── run.sh                  # Shell script entry point
├── requirements.txt        # Python dependencies
└── scrapy.cfg              # Scrapy deployment config
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.
