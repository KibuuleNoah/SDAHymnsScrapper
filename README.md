# SDAHymnsScrapper

`SDAHymnsScrapper` is an asynchronous Python application designed to scrape hymns from the [SDA Hymnal](https://sdahymnals.com) website. It collects hymn data, including titles, numbers, categories, verses, and refrains, and saves the information in a structured JSON file.

## Features

- Scrapes hymns across various categories (`001-700`).
- Retrieves hymn titles, numbers, categories, verses, and refrains.
- Handles multiple pages and hymn links dynamically.
- Saves the scraped data into a JSON file (`hymns.json`) for further use.

## Requirements

Before running the script, make sure you have the following installed:

- Python 3.8+
- Required Python libraries:
  - `asyncio`
  - `beautifulsoup4`
  - `requests`

You can install the required libraries using pip:

```bash
pip install beautifulsoup4 requests
```

## How It Works

1. **Initialization**: The class initializes with predefined categories and the base URL for the hymnal website.
2. **Fetching Data**: Asynchronous requests are used to fetch hymn data from the website, including verses, refrains, and categories.
3. **Parsing Hymn Data**: BeautifulSoup is used to parse the HTML content and extract meaningful data such as verses and categories.
4. **Saving Data**: All the scraped data is saved in a JSON file (`hymns.json`) for easy access and reuse.

## Usage

1. Clone or download the script to your local environment.

```bash
git clone https://github.com/KibuuleNoah/SDAHymnsScrapper.git
```

2. Cd to the folder

```bash
cd SDAHymnsScrapper
```

3. Run the script using Python:

```bash
python main.py
```

4. Once the script finishes execution, you will find the scraped data in a file named `hymns.json` in the same directory.

## File Structure

The JSON output (`hymns.json`) will have the following structure:

```json
[
    {
        "number": "1",
        "title": "Hymn Title",
        "category": "Category Name",
        "verses": [
            "Verse 1 text",
            "Verse 2 text"
        ],
        "refrain": "Refrain text"
    },
    ...
]
```

## Key Methods

- `fetch(url: str)`: Asynchronously fetches the content of a given URL.
- `get_hymn(url: str)`: Scrapes the hymn details (title, verses, refrain, etc.) from the hymn page.
- `generate_page_url(main_url: str, category: str, page: int)`: Generates paginated URLs for the given category.
- `run()`: Orchestrates the scraping process and saves the data into a JSON file.

## Notes

- The script is designed to scrape up to 10 pages per category, but this can be adjusted in the `run` method.
- The script handles failed requests gracefully and skips invalid URLs.
- If the script is interrupted, it will save the collected data before exiting.

## License

This project is open-source and available under the [MIT License](https://github.com/KibuuleNoah/SDAHymnsScrapper?tab=MIT-1-ov-file#). Feel free to modify and use it as needed.
