# CLAUDE.md

This file provides guidance for AI assistants working with this repository.

## Project Overview

**historical-rss-feed** is a Python project that creates and maintains historical RSS feeds for blogs and podcasts. It scrapes content from websites that may not retain their full archive history and generates complete RSS/XML feed files that are served via GitHub's raw file hosting.

### Purpose

Some RSS feeds only show recent content (e.g., last 10 posts). This project:
1. Fetches paginated content from source websites
2. Compiles complete historical archives into RSS/XML format
3. Hosts the feeds via GitHub raw URLs for podcast apps and RSS readers

## Repository Structure

```
historical-rss-feed/
├── main.py              # Main script for blog RSS feeds (nomadicmatt, tynan)
├── cracked_podcast.py   # Specialized scraper for Cracked Podcast from Art19
├── Pipfile              # Python dependencies (pipenv)
├── Pipfile.lock         # Locked dependency versions
├── __init__.py          # Empty package init file
├── .github/
│   └── workflows/
│       └── save-xml.yml # GitHub Actions workflow (runs every 2 days)
└── *.xml                # Generated RSS feed files (output, checked into git)
```

### Key Files

| File | Description |
|------|-------------|
| `main.py` | Builds RSS feeds for WordPress blogs using pagination (`?paged=N`) |
| `cracked_podcast.py` | Scrapes Art19 API for The Cracked Podcast episodes |
| `cracked.xml` | Generated podcast feed for The Cracked Podcast |
| `nomadicmatt.xml` | Generated feed for nomadicmatt.com blog |
| `tynan.xml` | Generated feed for tynan.com blog |

## Development Setup

### Prerequisites

- Python 3.9
- pipenv

### Installation

```bash
# Install pipenv if not available
pip install pipenv

# Install dependencies
pipenv install --dev

# Activate virtual environment
pipenv shell
```

### Running the Scripts

```bash
# Generate blog feeds (nomadicmatt.xml, tynan.xml)
pipenv run python main.py

# Generate Cracked Podcast feed (cracked.xml)
pipenv run python cracked_podcast.py
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `feedparser` | Parse existing RSS feeds |
| `feedgen` | Generate new RSS/Atom feeds |
| `bs4` | HTML parsing (BeautifulSoup) |
| `requests` | HTTP requests for API calls |

## Architecture & Patterns

### main.py - Blog Feed Generator

- Uses `feedparser` to read the original RSS feed metadata
- Paginates through WordPress blog pages using `?paged=N` parameter
- Uses `feedgen` to construct a complete RSS feed with all historical entries
- Entry fields captured: id, title, link, author, published, summary, content, comments

### cracked_podcast.py - Podcast Scraper

- Directly calls Art19 API endpoints with custom headers
- Uses `CrackedPodcastItem` class to model episode data
- Generates iTunes-compatible podcast XML with proper namespaces
- Hard-coded to 3 pages (podcast is discontinued)

### XML Namespaces Used (Podcasts)

- `itunes:` - iTunes podcast extensions
- `atom:` - Atom syndication
- `content:` - RSS content module
- `art19:` - Art19 platform extensions
- `googleplay:` - Google Podcasts

## GitHub Actions Workflow

The workflow in `.github/workflows/save-xml.yml`:

- **Triggers**: Every 2 days (cron: `5 12 */2 * *`), on push to master, manual dispatch
- **Process**:
  1. Checkout repository
  2. Setup Python 3.9
  3. Install pipenv and dependencies
  4. Run `main.py`
  5. Commit and push any changes to XML files

**Note**: The workflow only runs `main.py`, not `cracked_podcast.py` (since the Cracked Podcast is discontinued).

## Important Conventions

### XML Files Are Output

The `*.xml` files are **generated output** and are committed to the repository. They serve as the hosted RSS feeds via GitHub raw URLs like:
```
https://raw.githubusercontent.com/androbwebb/historical-rss-feed/master/cracked.xml
```

### Error Handling

- `main.py` wraps feed building in try/except to continue if one feed fails
- Individual feed errors are printed but don't stop the entire process

### Character Encoding

- `cracked_podcast.py` manually escapes `&` to `&amp;` in titles and descriptions
- Uses CDATA sections for HTML content

## Adding New Feeds

### For WordPress Blogs (with pagination)

1. Add a new tuple to the list in `main.py:58`:
   ```python
   ['https://example.com/feed/', 'example.xml'],
   ```

2. Run the script to generate the XML file

### For Custom APIs/Scrapers

1. Create a new Python file following `cracked_podcast.py` pattern
2. Implement scraping logic with appropriate headers and pagination
3. Generate valid RSS/XML with proper namespaces
4. Add to workflow if automated updates are needed

## Testing

There are no automated tests in this repository. To verify changes:

1. Run the relevant Python script
2. Validate the generated XML is well-formed
3. Test the feed URL in an RSS reader or podcast app

## Common Issues

### Feed Pagination Stops Early

Some sites return empty pages differently. Check the `get_items()` return value handling in `main.py:43-51`.

### API Rate Limiting

The Art19 scraper uses specific headers to avoid blocks. If requests fail, check if headers need updating.

### XML Encoding Errors

Special characters in content must be properly escaped or wrapped in CDATA. Check the `to_xml()` method in `cracked_podcast.py`.
