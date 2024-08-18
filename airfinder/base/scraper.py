import statistics
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re
from .validations import validate_guests
import logging
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains



#Const
WEBSITE = "https://www.airbnb.com/"
#CSV_PATH = "/Users/shaharishay/Programing/Python/Web Scraping Bots/AirBnB"
DRIVER_PATH = "/Users/shaharishay/Programming/chromedriver-mac-arm64/chromedriver"

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Scraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15")
        # chrome_options.add_argument("--kiosk")
        # self.driver = webdriver.Chrome(options=chrome_options, executable_path=DRIVER_PATH)
        self.driver = webdriver.Chrome(options=chrome_options, executable_path=DRIVER_PATH)

    def scrape(self, city, in_date, out_date, adults, children, infants, pets):
        ids = []
        links = []
        titles = []
        prices = []
        ratings = []
        images = []

        success = False  # Flag to indicate if the attempt was successful

        ############DATA INSERTION############        
        #Open the website
        self.driver.get(WEBSITE)
        # self.driver.minimize_window()
        time.sleep(3)
        ############CITY INSERTION############
        #Select textbox
        try:
            city_textbox = self.driver.find_element(By.XPATH, '//input[@placeholder = "Search destinations"]')
            time.sleep(1)
        except:
            print("Error: Could not find search box")
            
            
        #Write to textbox    
        try:    
            city_textbox.clear()
            time.sleep(1)
            city_textbox.send_keys(city)
            time.sleep(1)
        except:
            print("Error: Could not type to search box")
            

        #Select city option
        try:
            city_option = self.driver.find_element(By.XPATH, '//div[@data-testid = "option-0"]')
            time.sleep(1)
        except:
            print("Error: Could not find city option")
            

        #Click city option
        try:
            city_option.click()
            time.sleep(1)
        except:
            print("Error: Could not click city option")
            

        ############DATES INSERTION############
        next_month_button = self.driver.find_element(By.XPATH, '//button[@aria-label = "Move forward to switch to the next month."]')
        previous_month_button = self.driver.find_element(By.XPATH, '//button[@aria-label = "Move backward to switch to the previous month."]')
        presentations = self.driver.find_elements(By.XPATH, '//table[@role="presentation"]')
        for presentation in presentations:
            all_buttons = presentation.find_elements(By.XPATH, "//div[@data-is-day-blocked]")
            for button in all_buttons:
                try:
                    # Assuming 'button' is a WebElement object
                    attributes = self.driver.execute_script(
                        'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', 
                        button)

                    print(attributes)
                    if button.get_attribute('data-testid') == f"calendar-day-{in_date}":
                        in_date_button = button
                        time.sleep(1)
                        if in_date_button.get_attribute("data-is-day-blocked") == "false":                        
                            success = True
                            break
                    elif button.get_attribute('data-testid') == f"{in_date}":
                        in_date_button = button
                        time.sleep(1)
                        if in_date_button.get_attribute("data-is-day-blocked") == "false":                        
                            success = True
                            break
                except:
                    pass
            if success:
                break

        while True:
            try:    
                in_date_button.click()
                time.sleep(1)
                break
            except:
                try:
                    next_month_button.click()
                    time.sleep(1)
                except:
                    pass    
            

        print("in-success:", success)
        if success == False:
            print("Error: Could not find check-in date")
            return [], [], [], [], [], []
            # attempt += 1
            # continue
            
        success = False #Flag to indicate if the attempt was successful
        #Select check-out date
        for presentation in presentations:
            for button in all_buttons:
                try:
                    # Assuming 'button' is a WebElement object
                    attributes = self.driver.execute_script(
                        'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', 
                        button)

                    print(attributes)
                    if button.get_attribute('data-testid') == f"calendar-day-{out_date}":
                        out_date_button = button
                        time.sleep(1)
                        if out_date_button.get_attribute("data-is-day-blocked") == "false":                        
                            success = True
                            break
                    elif button.get_attribute('data-testid') == f"{out_date}":
                        out_date_button = button
                        time.sleep(1)
                        if out_date_button.get_attribute("data-is-day-blocked") == "false":                        
                            success = True
                            break
                except:
                    pass
            if success:
                break

        while True:
            try:    
                out_date_button.click()
                time.sleep(1)
                break
            except:
                try:
                    next_month_button.click()
                    time.sleep(1)
                except:
                    pass

        print("out-success:", success)            
        if success == False:
            print("Error: Could not find check-out date")
            return [], [], [], [], [], []
            


        ############GUESTS INSERTION############
        try:
            guests_button = self.driver.find_element(By.XPATH,'//div[@class = "c111bvlt atm_9s_1txwivl atm_1eltean_1osqo2v c1gh7ier atm_am_1qhqiko dir dir-ltr"]/div[@class = "c1ddhymz atm_h_1h6ojuz atm_9s_1txwivl atm_gi_1n1ank9 atm_jb_idpfg4 atm_mk_h2mmj6 atm_vy_10bmcub cggll98 atm_am_1qhqiko dir dir-ltr"]/div[@data-testid = "structured-search-input-field-guests-button"]')
            guests_button.click()    
        except:
            print("Error: Could not find guests button")
            

        if validate_guests(adults):       
            for _ in range(adults):
                try:    
                    add_adults_button = self.driver.find_element(By.XPATH, '//div[@data-testid = "structured-search-input-field-guests-panel"]/div[@class = "g6e6z5i atm_l8_14br1z3 atm_vy_smdzip dir dir-ltr"]/div[@data-testid = "search-block-filter-stepper-row-adults"]/div[@id = "stepper-adults"]/button[@data-testid = "stepper-adults-increase-button"]')
                    add_adults_button.click()
                    time.sleep(1)
                except:
                    print("Error: Could not add adults")
                    


        if validate_guests(children):
            for _ in range(children):
                try:
                    add_children_button = self.driver.find_element(By.XPATH, '//div[@data-testid = "structured-search-input-field-guests-panel"]/div[@class = "g6e6z5i atm_l8_14br1z3 atm_vy_smdzip dir dir-ltr"]/div[@data-testid = "search-block-filter-stepper-row-children"]/div[@id = "stepper-children"]/button[@data-testid = "stepper-children-increase-button"]')
                    add_children_button.click()
                    time.sleep(1)
                except:
                    print("Error: Could not add children")
                    


        if validate_guests(infants):
            for _ in range(infants):
                try:
                    add_infants_button = self.driver.find_element(By.XPATH, '//div[@data-testid = "structured-search-input-field-guests-panel"]/div[@class = "g6e6z5i atm_l8_14br1z3 atm_vy_smdzip dir dir-ltr"]/div[@data-testid = "search-block-filter-stepper-row-infants"]/div[@id = "stepper-infants"]/button[@data-testid = "stepper-infants-increase-button"]')
                    add_infants_button.click()
                    time.sleep(1)
                except:
                    print("Error: Could not add infants")
                    


        if validate_guests(pets):
            for _ in range(pets):
                try:
                    add_pets_button = self.driver.find_element(By.XPATH, '//div[@data-testid = "structured-search-input-field-guests-panel"]/div[@class = "g6e6z5i atm_l8_14br1z3 atm_vy_smdzip dir dir-ltr"]/div[@data-testid = "search-block-filter-stepper-row-pets"]/div[@id = "stepper-pets"]/button[@data-testid = "stepper-pets-increase-button"]')
                    add_pets_button.click()
                    time.sleep(1)
                except:
                    print("Error: Could not add pets")
                    

        #########INITIATE SEARCH#########
        try:
            search_button = self.driver.find_element(By.XPATH, '//div[@class = "c111bvlt atm_9s_1txwivl atm_1eltean_1osqo2v c1gh7ier atm_am_1qhqiko dir dir-ltr"]//div[@class = "c1ddhymz atm_h_1h6ojuz atm_9s_1txwivl atm_gi_1n1ank9 atm_jb_idpfg4 atm_mk_h2mmj6 atm_vy_10bmcub cggll98 atm_am_1qhqiko dir dir-ltr"]/div[@class = "snd2ne0 atm_am_12336oc atm_gz_yjp0fh atm_ll_rdoju8 atm_mk_h2mmj6 atm_wq_qfx8er dir dir-ltr"]/button[@type= "button"]')
            search_button.click()
            time.sleep(1)
        except:
            print("Error: Could not click search button")
           

            
            
        #Pagination
        while True:       
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'lxml')

            #Get all listing
            try: 
                boxes = soup.find_all('div', attrs={'data-testid': 'card-container'})
            except:
                print("Error: Could not find any listings")

            for box in boxes:
                try:
                    id = box.find('a').get('target').split('_')[1]
                    ids.append(id)
                except:
                    ids.append("N/A")
                try:
                    link = box.find('a').get('href')
                    link = f'https://www.airbnb.com{link}'
                    links.append(link)  
                except:
                    links.append("N/A")

                try:
                    image = box.find('img', class_="itu7ddv atm_e2_idpfg4 atm_vy_idpfg4 atm_mk_stnw88 atm_e2_1osqo2v__1lzdix4 atm_vy_1osqo2v__1lzdix4 i1cqnm0r atm_jp_pyzg9w atm_jr_nyqth1 i1de1kle atm_vh_yfq0k3 dir dir-ltr").get('src')
                    images.append(image)
                except:
                    images.append("N/A")    

                #Get addtional info
                grid = box.find('div', class_= 'g1qv1ctd atm_u80d3j_1li1fea atm_c8_o7aogt atm_g3_8jkm7i c1v0rf5q atm_9s_11p5wf0 atm_cx_4wguik atm_dz_7esijk atm_e0_1lo05zz dir dir-ltr')
                try:
                    title = grid.find('div', attrs={'data-testid': 'listing-card-title'}).get_text()
                    titles.append(title)
                except:
                    titles.append("N/A")

                try:
                    price_pattern = r'<span class="_11jcbg2">(.*?)</span>'
                    price = re.search(price_pattern, str(box)).group(1)
                    price = price.split("\xa0")[0].replace("₪", "")
                    prices.append(float(price)) 
                except:
                    prices.append("N/A")

                try:
                    rating = grid.find('div', class_= "t1a9j9y7 atm_da_1ko3t4y atm_dm_kb7nvz atm_fg_h9n0ih dir dir-ltr").find('span', class_="r4a59j5 atm_h_1h6ojuz atm_9s_1txwivl atm_7l_jt7fhx atm_84_evh4rp atm_mk_h2mmj6 atm_mj_glywfm dir dir-ltr").find('span', attrs={'aria-hidden': 'true'}).get_text()
                    rating = rating.split("(")[0]
                    rating.replace(" ", "")
                    ratings.append(rating)
                except:
                    ratings.append("N/A")
        


            #Get next page
            try:
                next_page_button = self.driver.find_element(By.XPATH, '//a[@aria-label = "Next"]')
            except:
                print("Error: Could not find next page button")
                break

            try:
                next_page_button.click()
                time.sleep(1)
            except:
                break


        return ids, links, titles, prices, ratings, images

    def filter_listings(self, ids, links, titles, prices, ratings, images, threshold_percentage=110, min_listings=5):
        logging.info(f"Total listings before filtering: {len(ids)}")

        # Filter out non-float prices and handle ratings
        valid_listings = []
        for id, link, title, price, rating, image in zip(ids, links, titles, prices, ratings, images):
            if isinstance(price, float):
                # Convert rating to float if possible, otherwise keep as string
                try:
                    numeric_rating = float(rating)
                except ValueError:
                    numeric_rating = rating  # Keep "N/A" or "New" as is

                valid_listings.append((id, link, title, price, numeric_rating, image))

        if not valid_listings:
            logging.warning("No valid listings found")
            return [], [], [], [], [], []

        # Calculate average price
        valid_prices = [listing[3] for listing in valid_listings]
        average_price = statistics.mean(valid_prices)
        price_threshold = average_price * (threshold_percentage / 100)

        logging.info(f"Average price: {average_price}, Threshold: {price_threshold}")

        # Filter listings below threshold and with high ratings
        filtered_listings = [listing for listing in valid_listings if listing[3] < price_threshold and 
                            (isinstance(listing[4], float) and listing[4] > 4.5 or listing[4] in ["N/A", "New"])]

        # Sort listings by price high to low
        filtered_listings.sort(key=lambda x: x[3], reverse=True)

        # If not enough listings, take the top listings based on price
        if len(filtered_listings) < min_listings:
            filtered_listings = sorted(valid_listings, key=lambda x: x[3], reverse=True)[:min_listings]

        logging.info(f"Listings after filtering: {len(filtered_listings)}")

        # Unzip the filtered listings
        filtered_ids, filtered_links, filtered_titles, filtered_prices, filtered_ratings, filtered_images = zip(*filtered_listings)

        return list(filtered_ids), list(filtered_links), list(filtered_titles), list(filtered_prices), list(filtered_ratings), list(filtered_images)

    def compare_prices(self, link):
        self.driver.get(link)
        html = self.driver.page_source

        try:
            price_pattern = r'<span class="_11jcbg2">(.*?)</span>'
            price = re.search(price_pattern, str(html)).group(1)
            price = price.split("\xa0")[0].replace("₪", "")
            price = price.replace("&nbsp;", "")
        except:
            print("Error: Could not find price")
        
        if price:
            return float(price)    
        
        return None
            
    def __del__(self):
         if hasattr(self, 'driver'):
            self.driver.quit()



# scraper = Scraper()
# ids, links, titles, prices,ratings,images = scraper.scrape("Rome", "10/16/2024", "10/22/2024", 2, 0, 0, 0)

# f_ids, f_links, f_titles, f_prices, f_ratings, f_images = scraper.filter_listings(ids, links, titles, prices, ratings, images)
# print(f_prices)