import feedparser
from feedgen.feed import FeedGenerator


def get_page(url, page=0):
    return feedparser.parse('{}?paged={}'.format(url, page))


def get_items(url, page=2):
    return get_page(url, page)['entries']


def add_entry(fg, entry):
    fe = fg.add_entry()
    fe.id(entry['link'])
    fe.title(entry['title'])
    fe.link(href=entry['link'])
    fe.author(entry['author_detail'])
    fe.published(entry['published'])
    fe.summary(entry['summary'])
    fe.content(entry['content'][0]['value'])
    fe.comments(entry['comments'])


def build_feed(url, filename):
    print('🌐Building {} from {}'.format(filename, url))

    fg = FeedGenerator()
    feed = feedparser.parse(url)

    fg.id(url)
    fg.title(feed['feed']['title'])
    fg.author(feed['entries'][0]['author_detail'])
    fg.link(href=feed['feed']['link'], rel='alternate')
    fg.subtitle(feed['feed']['subtitle'])
    fg.language('en')

    for entry in feed['entries']:
        add_entry(fg, entry)

    page = 2
    while feed:
        next_entries = get_items(url, page)
        if next_entries:
            print(f"\t📃 Adding page {page} with {len(next_entries)} entries")

            for entry in next_entries:
                add_entry(fg, entry)
            page += 1
        else:
            break

    fg.rss_file(filename)
    return


if __name__ == '__main__':
    build_feed('https://www.nomadicmatt.com/feed/', 'nomadicmatt.xml')
    build_feed('https://tynan.com/feed/', 'tynan.xml')
