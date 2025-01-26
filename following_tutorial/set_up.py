###https://www.byperth.com/2018/04/25/guide-web-scraping-101-what-you-need-to-know-and-how-to-scrape-with-python-selenium-webdriver/
from selenium import webdriver # allow launching browser
from selenium.webdriver.chrome.service import Service #handles chromedriver service
from selenium.webdriver.common.by import By # allow search with parameters
from selenium.webdriver.support.ui import WebDriverWait # allow waiting for page to load
from selenium.webdriver.support import expected_conditions as EC # determine whether the web page has loaded
from selenium.common.exceptions import TimeoutException # handling timeout situation
import pandas as pd

chromedriver_path = "/Users/sallydavies/Downloads/chromedriver-mac-arm64/chromedriver"

#prepare the code for easily opening a new browser window
driver_option = webdriver.ChromeOptions()
driver_option.add_argument("--incognito")

def create_webdriver():
    try:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=driver_option)
        return driver
    except Exception as error:
        print(f"Error initialising ChromeDrive: {error}")
        return None


#open the browser
browser = create_webdriver()
if browser:
    try:
        browser.get("https://github.com/collections/machine-learning")
        print("Page title", browser.title)
        #find all project titles
        projects = browser.find_elements(By.XPATH, "//h1[@class='h3 lh-condensed']")
        #create a dictionary to store the project data 
        project_list = {}
        #loop through the projects
        for proj in projects:
            proj_name = proj.text # Project name
            proj_url = proj.find_element(By.XPATH, "a").get_attribute("href") # Project URL
            #add project name and URL to the dictionary 
            project_list[proj_name] = proj_url

        #convert the dictionary to a DataFrame    
        project_df = pd.DataFrame.from_dict(project_list, orient = "index", columns=["project_url"])
        project_df["project_name"] = project_df.index
        project_df = project_df.reset_index(drop=True)      
            
        # Export project dataframe to CSV
        project_df.to_csv("project_list.csv", index=False)
        print("Project list saved to project_list.csv")
    except Exception as error:
        print(f"Error during browser operation: {error}")
    finally:
        browser.quit
else:
    print("Failed to initialise WebDriver")






# Extract information for each project
