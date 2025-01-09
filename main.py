import asyncio
from bs4 import BeautifulSoup
import json
import requests


class HymnsScrapper:

    def __init__(self):
        # Categories of hymns to scrape
        self.categories = [
            "001-100", "101-200", "201-300", "301-400", "401-500", "501-600",
            "601-700"
        ]
        self.main_url = "https://sdahymnals.com/Hymnal/category/"
        self.hymns = []

    async def fetch(self, url: str):
        # Fetch the content of a URL asynchronously
        resp = await asyncio.to_thread(requests.get, url)
        if resp.ok:
            print(f"Fetched {url} successfully")
            return resp.content
        else:
            print(f"Failed to fetch URL: {url}")
            return None

    async def get_hymn(self, url: str):
        # Scrape hymn details from a given URL
        html = await self.fetch(url)
        if not html:
            return

        soup = BeautifulSoup(html, "html.parser")

        # Extract the main container and hymn content
        main_cont = soup.find("div", class_="main-container")
        verse_table = main_cont.find("table")

        # Extract the hymn category
        category_table = soup.find('div',
                                   class_='post-categories').find('table')
        category = category_table.find('a').text

        # Parse verses and refrain
        verses = []
        refrain = ""
        for p in verse_table.find_all("p"):
            verse = p.text
            v_split = verse.split("\n", 1)

            if verse:
                if v_split[0] == "Refrain":
                    refrain = v_split[-1]
                else:
                    verses.append(v_split[-1])

        # Compile hymn details
        hymn_info = self.get_hymn_info(url)
        hymn = {"refrain": refrain, "verses": verses, "category": category}
        hymn.update(hymn_info)

        print(f"Finished hymn {hymn['number']}")
        self.hymns.append(hymn)

    def get_hymn_info(self, hym_url: str) -> dict:
        # Extract hymn number and title from the URL
        hymn_info = hym_url[:-1].split("/")[-1]
        hymn_info = hymn_info.replace("-", " ")
        hymn_num, hymn_title = hymn_info.split(" ", 1)
        return {"number": hymn_num, "title": hymn_title}

    def generate_page_url(self, main_url: str, category: str,
                          page: int) -> str:
        # Generate the URL for a specific page in a category
        if page <= 1:
            return f"{main_url}{category}/"
        return f"{main_url}{category}/page/{page}/"

    async def run(self):
        try:
            tasks = []
            for category in self.categories:
                for page in range(1, 11):
                    # Generate and fetch category page
                    url = self.generate_page_url(self.main_url, category, page)
                    html = await self.fetch(url)
                    if not html:
                        continue

                    soup = BeautifulSoup(html, "html.parser")
                    hymns_link_divs = soup.find_all("div", class_="readMore")

                    # Extract links to individual hymns
                    hymn_links = [
                        div.find("a").get("href") for div in hymns_link_divs
                    ]

                    # Create async tasks for each hymn
                    for hymn_url in hymn_links:
                        task = asyncio.create_task(self.get_hymn(hymn_url))
                        tasks.append(task)

            # Run all tasks concurrently
            await asyncio.gather(*tasks)

            # Save scraped hymns to a JSON file
            with open("hymns.json", "w") as f:
                json.dump(self.hymns, f, indent=4)
        except asyncio.CancelledError:
            # Handle script interruption and save collected data
            print("Process interrupted. Saving progress...")
            with open("hymns.json", "w") as f:
                json.dump(self.hymns, f, indent=4)


if __name__ == "__main__":
    # Instantiate and run the scrapper
    scrapper = HymnsScrapper()
    asyncio.run(scrapper.run())

# import asyncio
# from bs4 import BeautifulSoup
# import json
# import requests
#
#
# class HymnsScrapper:
#
#     def __init__(self):
#         self.categories = [
#             "001-100", "101-200", "201-300", "301-400", "401-500", "501-600",
#             "601-700"
#         ]
#         self.main_url = "https://sdahymnals.com/Hymnal/category/"
#         self.hymns = []
#
#     async def fetch(self, url: str):
#         resp = await asyncio.to_thread(requests.get, url)
#         if resp.ok:
#             print(f"Fetched {url} successfully")
#             return resp.content
#         else:
#             print(f"Failed to fetch URL: {url}")
#             return None
#
#     async def get_hymn(self, url: str):
#         html = await self.fetch(url)
#         if not html:
#             return
#
#         soup = BeautifulSoup(html, "html.parser")
#         main_cont = soup.find("div", class_="main-container")
#         verse_table = main_cont.find("table")
#
#         category_table = soup.find('div',
#                                    class_='post-categories').find('table')
#         category = category_table.find('a').text
#
#         verses = []
#         refrain = ""
#         for p in verse_table.find_all("p"):
#             verse = p.text
#             v_split = verse.split("\n", 1)
#
#             if verse:
#                 if v_split[0] == "Refrain":
#                     refrain = v_split[-1]
#                 else:
#                     verses.append(v_split[-1])
#
#         hymn_info = self.get_hymn_info(url)
#         hymn = {"refrain": refrain, "verses": verses, "category": category}
#         hymn.update(hymn_info)
#
#         print(f"Finished hymn {hymn['number']}")
#         self.hymns.append(hymn)
#
#     def get_hymn_info(self, hym_url: str) -> dict:
#         hymn_info = hym_url[:-1].split("/")[-1]
#         hymn_info = hymn_info.replace("-", " ")
#         hymn_num, hymn_title = hymn_info.split(" ", 1)
#         return {"number": hymn_num, "title": hymn_title}
#
#     def generate_page_url(self, main_url: str, category: str,
#                           page: int) -> str:
#         if page <= 1:
#             return f"{main_url}{category}/"
#         return f"{main_url}{category}/page/{page}/"
#
#     async def run(self):
#         try:
#             tasks = []
#             for category in self.categories:
#                 for page in range(1, 11):
#                     url = self.generate_page_url(self.main_url, category, page)
#                     html = await self.fetch(url)
#                     if not html:
#                         continue
#
#                     soup = BeautifulSoup(html, "html.parser")
#                     hymns_link_divs = soup.find_all("div", class_="readMore")
#                     hymn_links = [
#                         div.find("a").get("href") for div in hymns_link_divs
#                     ]
#
#                     for hymn_url in hymn_links:
#                         task = asyncio.create_task(self.get_hymn(hymn_url))
#
#                         tasks.append(task)
#
#             await asyncio.gather(*tasks)
#
#             with open("hymns.json", "w") as f:
#                 json.dump(self.hymns, f, indent=4)
#         except asyncio.CancelledError:
#             print("wow")
#             with open("hymns.json", "w") as f:
#                 json.dump(self.hymns, f, indent=4)
#
#
# if __name__ == "__main__":
#     scrapper = HymnsScrapper()
#     asyncio.run(scrapper.run())
