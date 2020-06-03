from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

driver = webdriver.Chrome()
#setting options to open incognito window
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(chrome_options=chrome_options)


phone = '01772836280'
password = 'Mememe198$'
address = "Subidazar,Sylhet"
road = "Mirermoydan"


# Function to load webpage if it doesn't response in the first try.
# Or if the network diconnects it will keep reloading the page until network is connected and page is loaded.  
def load_page(url='https://www.google.com',error_element='//div[@class="error-code"]'):
    """"Tries to load the URL. If it finds error element by XPATH then it reloads the page.\nIf it doesn't finds the error element then it returns form the function.\n
    Requited imports:\n
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    """
    driver.get(url)
    while True:
        try:
            WebDriverWait(driver, .1).until(EC.presence_of_element_located((By.XPATH, error_element)))
        except TimeoutException:
            return
        driver.refresh()


#Function to load elements in a dynamically loading page
def load_elements(css_selector=".buy-button",page_ups=1,wait_max=20,time_to_wait=1):
    """
    Loads elements of a page by CSS class selector\nWaits for 20 seconds to load new items.\nCustomizable if needed.\n\n
    Requited imports:\n
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from time import sleep\n
    """
    old_elements_count = None
    new_elements_count = 0
    while new_elements_count != old_elements_count:
        elements = driver.find_elements_by_css_selector(css_selector)

        old_elements_count = new_elements_count #replacing old button count
        new_elements_count = len(elements) #getting new button count

        count = 0
        if old_elements_count==new_elements_count:
            for i in range(wait_max):
                elements = driver.find_elements_by_css_selector(css_selector)
                new_elements_count = len(elements) #getting new button count
                if not new_elements_count == old_elements_count:
                    count +=1
                    break
                if i==2:
                    for i in range(page_ups):
                        driver.find_element_by_tag_name('html').send_keys(Keys.PAGE_UP)
                    sleep(time_to_wait*2)
                sleep(time_to_wait*.5) #waits for .7 secs
        if count == wait_max:
            break
        
        #scrolling down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("found new",new_elements_count-old_elements_count,"elements")
        sleep(time_to_wait)
    
    return elements

def js_click(element):
    driver.execute_script("arguments[0].click();", element)



def login_from_login_page():
    load_page('https://evaly.com.bd/login.php')
    #entering phone number
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//button[text()="LOGIN"]')))
    num_field = driver.find_element_by_xpath('//input[@name="phone"]')
    num_field.send_keys(phone)
    #entering password
    pass_field = driver.find_element_by_xpath('//input[@name="password"]')
    pass_field.send_keys(password)
    #loging in
    login_btn = driver.find_element_by_xpath('//button[text()="LOGIN"]')
    login_btn.click()

def login_from_nav_bar(phone,password):
    #opening login menu
    login_svg = driver.find_element_by_xpath('//*[@d="M858.5 763.6a374 374 0 0 0-80.6-119.5 375.63 375.63 0 0 0-119.5-80.6c-.4-.2-.8-.3-1.2-.5C719.5 518 760 444.7 760 362c0-137-111-248-248-248S264 225 264 362c0 82.7 40.5 156 102.8 201.1-.4.2-.8.3-1.2.5-44.8 18.9-85 46-119.5 80.6a375.63 375.63 0 0 0-80.6 119.5A371.7 371.7 0 0 0 136 901.8a8 8 0 0 0 8 8.2h60c4.4 0 7.9-3.5 8-7.8 2-77.2 33-149.5 87.8-204.3 56.7-56.7 132-87.9 212.2-87.9s155.5 31.2 212.2 87.9C779 752.7 810 825 812 902.2c.1 4.4 3.6 7.8 8 7.8h60a8 8 0 0 0 8-8.2c-1-47.8-10.9-94.3-29.5-138.2zM512 534c-45.9 0-89.1-17.9-121.6-50.4S340 407.9 340 362c0-45.9 17.9-89.1 50.4-121.6S466.1 190 512 190s89.1 17.9 121.6 50.4S684 316.1 684 362c0 45.9-17.9 89.1-50.4 121.6S557.9 534 512 534z"]/ancestor::button')
    login_svg.click()
    #entering phone number
    num_field = driver.find_element_by_xpath("//label/input[@title='Phone number should be 11 digit number']")
    num_field.send_keys(phone)
    #entering password
    pass_field = driver.find_element_by_xpath("//label/input[@type='password']")
    pass_field.send_keys(password)
    #clicking login btn
    login_btn = driver.find_element_by_xpath('//button[text()="LOGIN"]')
    login_btn.click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="N"]')))

def get_active_campaigns():
    driver.find_element_by_tag_name('html').send_keys(Keys.HOME)
    
    burger_menu =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@class="text-2xl menu"]')))
    js_click(burger_menu)

    campaigns = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Campaigns"]')))
    js_click(campaigns)
    # campaigns.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href,"/campaign/")]//*[text()="Live now"]/ancestor::a')))
    live_campaigns_link = [campaign_link.get_attribute('href') for campaign_link in driver.find_elements_by_xpath('//a[contains(@href,"/campaign/")]//*[text()="Live now"]/ancestor::a')]
    return live_campaigns_link

def place_order(address,road):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@d="M922.9 701.9H327.4l29.9-60.9 496.8-.9c16.8 0 31.2-12 34.2-28.6l68.8-385.1c1.8-10.1-.9-20.5-7.5-28.4a34.99 34.99 0 0 0-26.6-12.5l-632-2.1-5.4-25.4c-3.4-16.2-18-28-34.6-28H96.5a35.3 35.3 0 1 0 0 70.6h125.9L246 312.8l58.1 281.3-74.8 122.1a34.96 34.96 0 0 0-3 36.8c6 11.9 18.1 19.4 31.5 19.4h62.8a102.43 102.43 0 0 0-20.6 61.7c0 56.6 46 102.6 102.6 102.6s102.6-46 102.6-102.6c0-22.3-7.4-44-20.6-61.7h161.1a102.43 102.43 0 0 0-20.6 61.7c0 56.6 46 102.6 102.6 102.6s102.6-46 102.6-102.6c0-22.3-7.4-44-20.6-61.7H923c19.4 0 35.3-15.8 35.3-35.3a35.42 35.42 0 0 0-35.4-35.2zM305.7 253l575.8 1.9-56.4 315.8-452.3.8L305.7 253zm96.9 612.7c-17.4 0-31.6-14.2-31.6-31.6 0-17.4 14.2-31.6 31.6-31.6s31.6 14.2 31.6 31.6a31.6 31.6 0 0 1-31.6 31.6zm325.1 0c-17.4 0-31.6-14.2-31.6-31.6 0-17.4 14.2-31.6 31.6-31.6s31.6 14.2 31.6 31.6a31.6 31.6 0 0 1-31.6 31.6z"]/ancestor::button')))
    curt = driver.find_element_by_xpath('//*[@d="M922.9 701.9H327.4l29.9-60.9 496.8-.9c16.8 0 31.2-12 34.2-28.6l68.8-385.1c1.8-10.1-.9-20.5-7.5-28.4a34.99 34.99 0 0 0-26.6-12.5l-632-2.1-5.4-25.4c-3.4-16.2-18-28-34.6-28H96.5a35.3 35.3 0 1 0 0 70.6h125.9L246 312.8l58.1 281.3-74.8 122.1a34.96 34.96 0 0 0-3 36.8c6 11.9 18.1 19.4 31.5 19.4h62.8a102.43 102.43 0 0 0-20.6 61.7c0 56.6 46 102.6 102.6 102.6s102.6-46 102.6-102.6c0-22.3-7.4-44-20.6-61.7h161.1a102.43 102.43 0 0 0-20.6 61.7c0 56.6 46 102.6 102.6 102.6s102.6-46 102.6-102.6c0-22.3-7.4-44-20.6-61.7H923c19.4 0 35.3-15.8 35.3-35.3a35.42 35.42 0 0 0-35.4-35.2zM305.7 253l575.8 1.9-56.4 315.8-452.3.8L305.7 253zm96.9 612.7c-17.4 0-31.6-14.2-31.6-31.6 0-17.4 14.2-31.6 31.6-31.6s31.6 14.2 31.6 31.6a31.6 31.6 0 0 1-31.6 31.6zm325.1 0c-17.4 0-31.6-14.2-31.6-31.6 0-17.4 14.2-31.6 31.6-31.6s31.6 14.2 31.6 31.6a31.6 31.6 0 0 1-31.6 31.6z"]/ancestor::button')
    js_click(curt)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Checkout"]/ancestor::button')))
    checkout = driver.find_element_by_xpath('//span[text()="Checkout"]/ancestor::button')
    js_click(checkout)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Confirm Payment"]')))
    confirm_payment_btn = driver.find_element_by_xpath('//button[text()="Confirm Payment"]')
    js_click(confirm_payment_btn)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchTextField"]')))
    address_field = driver.find_element_by_xpath('//*[@id="searchTextField"]')
    address_field.send_keys(address)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchTextField"]')))
    road_field = driver.find_element_by_xpath('//*[@id="additionalInfo"]')
    road_field.send_keys(road)

    terms = driver.find_element_by_xpath('//input[@type="checkbox"]')
    js_click(terms)

    final_confirm = driver.find_element_by_xpath('//button[text()="Confirm Order"]')
    js_click(final_confirm)
    
    sleep(4)
    driver.back()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//p[contains(@title," ")]/ancestor::div[contains(@class,"overflow-hidden bg-white")]')))





load_page('https://evaly.com.bd/')
driver.maximize_window()
login_from_nav_bar(phone,password)

#going to campaigns
for campaign in get_active_campaigns():
    load_page(campaign)

    #getting shops inside campaigns
    shops = [shop_link.get_attribute('href') for shop_link in driver.find_elements_by_xpath('//div[contains(@class,"campaign__Grid")]/a')]
    print(campaign)
    #going to shops
    for shop in shops:
        bought_procuct_titles = []
        load_page(shop)
        print(f"Going to shop {shop}")
        load_elements()
        titles =[elem.text for elem in driver.find_elements_by_xpath('//p[contains(@title," ")]')]

        reload_products = False
        if len(titles)>=15:
            reload_products = True

        product_cards = driver.find_elements_by_xpath('//p[contains(@title," ")]/ancestor::div[contains(@class,"overflow-hidden bg-white")]')
        order_no = 0
        #ordering products saperately
        for i in range(len(product_cards)):
            buy_button = product_cards[i].find_element_by_tag_name('button')
            title = product_cards[i].find_element_by_tag_name('p').text

            if title in titles:
                print(f"Ordering {title}")
                js_click(buy_button)
                place_order(address,road)
                titles.remove(title)
                order_no+=1
                product_cards = driver.find_elements_by_xpath('//p[contains(@title," ")]/ancestor::div[contains(@class,"overflow-hidden bg-white")]')
print("\nSuccessfuly orderd all the products form all the champaigns seperately")