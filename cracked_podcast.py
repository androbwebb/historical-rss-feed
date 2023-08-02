from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

def convert_date_format(date_str):
    # Convert the input string to a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Convert the datetime object to the desired output format
    formatted_date = date_obj.strftime("%a, %d %b %Y %H:%M:%S %z")

    return formatted_date


class CrackedPodcastItem:
    def __init__(self, data):
        self.guid = data.get('guid')
        self.id = data.get('id')
        self.description_plain = data.get('description_plain')
        self.description_html = data.get('description_html')
        self.title = data.get('title').replace('&', '&amp;')
        self.pub_date = data.get('pub_date')
        self.url = data.get('url')
        self.web_url = data.get('web_url')

    def to_xml(self):
        return f"""
            <item>
              <title>{self.title}</title>
              <description>
                <![CDATA[{self.description_html}]]>
              </description>
              <guid isPermaLink="false">{self.guid}</guid>
              <itunes:title>{self.title}</itunes:title>
              <itunes:episodeType>full</itunes:episodeType>
              <itunes:summary>{self.description_plain}</itunes:summary>
              <pubDate>{convert_date_format(self.pub_date)}</pubDate>
              <itunes:explicit>yes</itunes:explicit>
              <itunes:image href="https://content.production.cdn.art19.com/images/45/dc/e8/be/45dce8be-edd1-49ed-82a3-5efe662accbf/3b08a0384c4ae92a2ea996d027bbc5964c1763bf1cde978ac9efa208f58f0c9d07702e0aa152295eca574ee4c67c6e57e05068b423d517a4428f8fab143f28f2.jpeg"/>
              <enclosure url="{self.url}" type="audio/mpeg"/>
            </item>
        """


def scrape_feed(feed_url):
    pages = 3 # Hardcoded because the podcast is over, so we know how many
    items = []

    headers = {
        'authority': 'art19.com',
        'accept': 'application/vnd.art19.v0+json;q=0.9,application/json;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/vnd.art19.v0+json',
        'cookie': 'OptanonAlertBoxClosed=2023-08-01T21:07:28.987Z; OptanonConsent=isIABGlobal=false&datestamp=Wed+Aug+02+2023+15%3A15%3A17+GMT%2B0200+(Central+European+Summer+Time)&version=6.37.0&hosts=&landingPath=NotLandingPage&groups=C0002%3A1%2CC0001%3A1%2CC0003%3A1&geolocation=DE%3BBW&AwaitingReconsent=false',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://art19.com/shows/the-cracked-podcast?page=35',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
        'x-newrelic-id': 'Uw8FV1JaGwQJUVNXAgI=',
        'x-requested-with': 'XMLHttpRequest',
    }

    for page in range(1, pages + 1):
        page_url = f"{feed_url}&page%5Bnumber%5D={page}"
        print(f"🌐 Scraping {page_url}")
        response = requests.get(page_url, headers=headers)

        data = json.loads(response.text)

        for episode in data.get('episodes', []):
            guid = episode['rss_guid']
            id = episode['id']
            description_plain = episode['description_plain']
            description_html = episode['description']
            title = episode['title']
            pub_date = episode['created_at']

            url = f"https://rss.art19.com/episodes/{id}mp3"
            web_url = f"https://art19.com/shows/the-cracked-podcast/episodes/{id}"

            items.append(CrackedPodcastItem({
                'guid': guid,
                'id': id,
                'description_plain': description_plain,
                'description_html': description_html,
                'title': title,
                'pub_date': pub_date,
                'url': url,
                'web_url': web_url,
            }))

    with open("./cracked.xml", "w") as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:art19="https://art19.com/xmlns/rss-extensions/1.0" xmlns:googleplay="http://www.google.com/schemas/play-podcasts/1.0/" version="2.0">
  <channel>
    <title>The Cracked Podcast</title>
    <description>
      <![CDATA[<p>Facts, jokes, and more from the Internet’s leading comedy website, Cracked.com. Every week, host Alex Schmidt brings together comedians, authors, scientists, and Cracked staffers, to celebrate the awesome truth that being alive is more interesting than people think it is. Fill your week and your brain with hilarious, mind-blowing revelations that’ll make you the most interesting person in every room you’re in.</p>]]>
    </description>
    <managingEditor>podcasts@literally.media (Literally Media)</managingEditor>
    <copyright>© Literally Media LTD.</copyright>
    <generator>ART19</generator>
    <atom:link href="https://rss.art19.com/the-cracked-podcast" rel="self" type="application/rss+xml"/>
    <link>https://www.cracked.com/podcast/show-the-cracked-podcast/</link>
    <itunes:new-feed-url>https://rss.art19.com/the-cracked-podcast</itunes:new-feed-url>
    <itunes:owner>
      <itunes:name>Literally Media</itunes:name>
      <itunes:email>podcasts@literally.media</itunes:email>
    </itunes:owner>
    <itunes:author>Literally Media</itunes:author>
    <itunes:summary>
      <![CDATA[<p>Facts, jokes, and more from the Internet’s leading comedy website, Cracked.com. Every week, host Alex Schmidt brings together comedians, authors, scientists, and Cracked staffers, to celebrate the awesome truth that being alive is more interesting than people think it is. Fill your week and your brain with hilarious, mind-blowing revelations that’ll make you the most interesting person in every room you’re in.</p>]]>
    </itunes:summary>
    <language>en</language>
    <itunes:explicit>yes</itunes:explicit>
    <itunes:category text="Comedy">
      <itunes:category text="Comedy Interviews"/>
    </itunes:category>
    <itunes:type>episodic</itunes:type>
    <itunes:image href="https://content.production.cdn.art19.com/images/45/dc/e8/be/45dce8be-edd1-49ed-82a3-5efe662accbf/3b08a0384c4ae92a2ea996d027bbc5964c1763bf1cde978ac9efa208f58f0c9d07702e0aa152295eca574ee4c67c6e57e05068b423d517a4428f8fab143f28f2.jpeg"/>
    <image>
      <url>https://content.production.cdn.art19.com/images/45/dc/e8/be/45dce8be-edd1-49ed-82a3-5efe662accbf/3b08a0384c4ae92a2ea996d027bbc5964c1763bf1cde978ac9efa208f58f0c9d07702e0aa152295eca574ee4c67c6e57e05068b423d517a4428f8fab143f28f2.jpeg</url>
      <link>https://www.cracked.com/podcast/show-the-cracked-podcast/</link>
      <title>The Cracked Podcast</title>
    </image>

    {"".join([item.to_xml() for item in items])}
  </channel>
</rss>
                """)


if __name__ == "__main__":
    scrape_feed('https://art19.com/episodes?calendar_meta=true&page%5Bsize%5D=100&rss=true&series_id=12215a84-2d45-4e0c-8796-38dd47428008')