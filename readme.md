# Amazon Review Scraper
This is a simple python library that scrapes reviews from amazon.com and writes it into a csv file.



## Usage
1. Instantiating the object: ```scraper = AmazonReviewScraper.AmazonReviewScraper(url, start_page=1, end_page=None, sleeping_time=0, file_name="fetchfile.csv")```

   * ```url```: In the product's page, scroll down to the end of the reviews and click **see all reviews**. Click on that and copy the ```url```. This ```url``` is your first parameter. 
   	Example: ```https://www.amazon.in/Samsung-Galaxy-J4-Blue-Offer/dp/B07DG9384L/ref=sr_1_4?ie=UTF8&qid=1551862000&sr=8-4&keywords=samsung+j7+prime```
   	
   * ```start page```: This is the second parameter. Mention the page from which you want to scrape.

   * ```end page```: This is the third parameter. Mention at what page the scraper has to stop scraping and by Default value is None.

   * ```sleeping_time(in seconds)```: This is the 4th argument. Amazon might block your IP if it receives too many requests every second. To prevent that, you can mention ```sleeping_time``` (in seconds). The scraper will wait anywhere from ```0``` to the ```sleeping_time``` before scraping every page. If you don't want to wait before scraping every page, give the value as **0**.

   * ```file_name```: This is the 5th argument. Here we provide the name of the file in which we can save file scrape data. By default file name is fetchfile.csv.Here you have to provide .csv extension.

2. Call the ``` scrape(self, return_value=False)``` method: ```scraper.scrape()```.to perform scrape of the website. there is 1 parameter in this function that is return value.
if we pass True as parameter then it will directly return the scrape value to 'scraper' object.


3. Write to CSV using ```write_csv()``` method: ```scraper.write_csv()```
to write csv. As by default it automatic save the csv file as 'fetchfile.csv'

## Example Code

```
from AmazonReviewScraper import AmazonReviewScraper

url = input("Enter URL: ")
start_page = input("Enter Start Page Number: ")
end_page = input("Enter End Page Number: ")
sleeping_time = input("Enter sleeping time rangein second: ")
file_name = "samsungj7.csv"

scraper = amazon_review_scraper.amazon_review_scraper(url, start_page, end_page, sleeping_time,file_name)
scraper.scrape()
```