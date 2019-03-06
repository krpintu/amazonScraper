import csv
import ssl
import time
import requests
from bs4 import BeautifulSoup


class AmazonReviewScraper:
    
    # Ignore SSL certificate errors
    ssl._create_default_https_context = ssl._create_unverified_context

    csv_data = []

    csv_head = ["Rating", "Title", "Body", "Helpful Votes"]

    def __init__(self, url, start_page=1, end_page=None, sleeping_time=0, file_name="fetchfile.csv"):
        self.count_review=0
        self.file_name=file_name
        self.url = url
        self.url = self.set_url()
        self.product_name=""
        self.actual_product_rating=""
        self.start_page = int(start_page)
        self.check_file_status()

        if end_page is not None:
            self.end_page = int(end_page)
        else:
            self.end_page=None

        self.sleeping_time = sleeping_time
        print("Total number of page found: ", self.end_page)


    def filter_html_entity(self, text):
        return text.replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")

    # print->yes this will print the sleeping message
    def set_sleep_timer(self, print=None):
        sleep_time = int(self.sleeping_time)
        if print is not None:
            print("\nSleeping for " + str(sleep_time) + " seconds.")
        time.sleep(sleep_time)

    def set_url(self):
        self.url = self.url.split("/ref=")[0]
        #ref_part = '/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=1'
        ref_part = '/ref=cm_cr_arp_d_paging_btm_next_2?showViewpoints=1&pageNumber=1'

        # removing all extra staff after ref parameter if it exists in the url
        self.url = self.url.replace('/gp/','/dp/')
        url = self.url.split("?pd_rd_wg")
        if len(url) > 1:
            self.url = str(url[0]).replace('/dp/', '/product-reviews/')
        else:
            self.url = str(url[0]).replace('/dp/', '/product-reviews/')
        

        # adding extra parameter for receiving all comment
        self.url = self.url + ref_part

        # removing pageNumber parameter if it exists in the url
        url = self.url.split("&pageNumber")
        if len(url) > 1:
            self.url = url[0]
        else:
            self.url = url

        return self.url

    def set_start_page(self, start_page):
        url = self.url + "&pageNumber=" + str(start_page)
        return url

    def build_rating(self, review):
        return str(review).split("<span class=\"a-icon-alt\">")[1].split("</span>")[0].split(" ")[0]

    def build_title(self, review):
        return str(review).split("data-hook=\"review-title\"")[1].split("\">")[1].split("</a>")[0]

    def build_body(self, review):
        body = str(review).split("data-hook=\"review-body\">")[1].split("</span>")[0] + "\n"
        # to remove <br>, <br/> and </br>
        body = body.replace("<br>", ".").replace("<br/>", ".").replace("</br>", ".").strip()
        return body

    def build_votes(self, review):
        try:
            votes = str(review).split("data-hook=\"helpful-vote-statement\"")[1].split(">")[1].split("<")[
                0].strip().split()
            if votes[0] == "One":
                return "1"
            else:
                return votes[0]
        except:
            return "0"

    def display_detail_of_product(self):
        print("\nAbout Product")
        # Amazon blocks requests that don't come from browser. Hence need to mention user-agent
        user_agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        header = {'User-Agent': user_agent}

        url = self.url.replace('/product-reviews/', '/dp/')
        r = requests.get(url, headers=header)
        html = r.text
        soup = BeautifulSoup(html, 'html5lib')

        # finding name of product
        product_namex = soup.find("h1", class_="a-size-large a-spacing-none")
        product_namex = product_namex.find("span", class_="a-size-large").text
        self.product_name=product_namex.strip()
        print("Product Name: "+self.product_name+"\n")

        # finding detail of product
        product_detail = soup.find("ul", class_="a-unordered-list a-vertical a-spacing-none")
        product_detail = product_detail.find_all("span", class_="a-list-item")
        print("Product Detail")
        for id, detail in enumerate(product_detail[:len(product_detail)]):
            print((id + 1), ") ", detail.text.strip())

        # finding actual rating
        print("\nActual Rating by Customer")
        self.actual_product_rating = soup.find("span", class_="arp-rating-out-of-text a-color-base").text
        print("Rating: "+self.actual_product_rating.strip()+"\n")

    def get_actual_product_rating(self):
        return float(self.actual_product_rating.strip().split(" out of 5 stars")[0])

    def get_product_name(self):
        try:
            return self.product_name.strip()
        except:
            return ""

    def get_total_number_of_review(self):
        return self.count_review

    def scrape(self, return_value=False):
        start_page = self.start_page
        end_page = self.end_page
        csv_written=False

        self.csv_data.append(self.csv_head)
        print('Scraping started...')

        while True:

            try:
                url = self.set_start_page(start_page)
                print(url)
            except:
                print("URL is wrong. Please try again with the right URL.")
                exit()

            # Sleep because Amazon might block your IP if there are too many requests every second
            self.set_sleep_timer()

            print("Scraping page " + str(start_page))

            # Amazon blocks requests that don't come from browser. Hence need to mention user-agent
            user_agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
            header = {'User-Agent': user_agent}

            r = requests.get(url, headers=header)
            html = r.text

            # fatching comment and review part
            try:
                soup = BeautifulSoup(html, 'html5lib')
                reviews = soup.find_all("div", class_="a-section review")
                for review in reviews:
                    csv_body = []

                    # Star Rating
                    rating = self.build_rating(review)
                    csv_body.append(rating)

                    # Title
                    title = self.build_title(review)
                    csv_body.append(title)

                    # Body
                    body = self.build_body(review)
                    csv_body.append(self.filter_html_entity(body))
                    self.count_review += 1

                    # Helpful Votes
                    votes = self.build_votes(review)
                    csv_body.append(votes)
                    self.csv_data.append(csv_body)
            except:
                csv_written=True
                self.write_csv_scrape()
                break
                
            flagLastPage=False    
            reviews = soup.find_all("ul", class_="a-pagination")[-1]
            pagelist = reviews.find_all("li")

            # as soon it will find last page it will stop 
            if pagelist[-1].a is None:
                break
                
            start_page += 1
            
            
        if csv_written is False:
            self.write_csv_scrape()
            
        if return_value is True:
            return self.csv_data

    def check_file_status(self):
        import os
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def get_file_name(self):
        return self.file_name

    def write_csv_scrape(self):
        with open(self.file_name , 'w', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerows(self.csv_data)
