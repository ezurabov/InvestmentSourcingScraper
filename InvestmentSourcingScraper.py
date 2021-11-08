import time
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

def GetAttribute(elem):
    return elem.get_attribute('innerText')

def WriteToCSV(arr):
    if arr["Location"].strip().upper() == "CANADA" or arr["Location"].strip().upper() == "UNITED STATES":
    
        software = arr['Software'].strip()
        name = arr['Name'].strip()
        website = arr['Website'].strip()
        founded = arr['Founded'].strip()
        location = arr['Location'].strip()
        trueEmployees = arr['True Employees'].strip()
        linkedInEmployees = arr['LinkedIn Employees'].strip()
        with open('softwareLeadsListNS2.csv','a', newline='') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow([name, software, founded, website, location, linkedInEmployees, trueEmployees])

def ExtractData(page):
    newArr = {}
    try:
        newArr["Software"] = GetAttribute(page.find_element_by_class_name("ProductHeader__ProductHeading-sc-10fs9um-3"))
    except:
        newArr["Software"] = GetAttribute(page.find_element_by_class_name("ProductHeader__VendorSubheading-sc-10fs9um-2")).split(" ")[1]
    companyDetails = page.find_element_by_class_name("DeploymentSupportSection__CompanyDetailsContainer-z7uxeo-4").find_elements_by_class_name("ListItem__ListItemContainer-sc-1ejeqo-0")
    newArr["Name"] = GetAttribute(companyDetails[0])
    try:
        newArr["Website"] = GetAttribute(companyDetails[3])
    except:
        newArr["Website"] =""
    try:
        newArr["Founded"] = GetAttribute(companyDetails[2]).split(" ")[2]
    except:
        newArr["Founded"] = ""
    try:
        newArr["Location"] = GetAttribute(companyDetails[1]).split(" ")[2] + " " + GetAttribute(companyDetails[1]).split(" ")[3]
    except:
        try:
            newArr["Location"] = GetAttribute(companyDetails[3]).split(" ")[2]
        except:
            newArr["Location"] = ""
    #print(newArr["Location"] + newArr["Name"] + newArr["Software"])
    return newArr

def ExtractLinkedIn(arr):
    if arr["Location"].strip().upper() == "CANADA" or arr["Location"].strip().upper() == "UNITED STATES":
        linkedIn.get('https://www.google.com/')
        time.sleep(70)
        searchBox = linkedIn.find_element_by_name('q')
        searchBox.send_keys('site:linkedin.com/company/ AND ' + arr['Name'])
        searchBox.send_keys(Keys.RETURN)
        time.sleep(2)
        arr['True Employees'] = ""
        arr['LinkedIn Employees'] = ""

        try:
            result = linkedIn.find_elements_by_class_name('LC20lb')[0]
        
            if arr['Name'].upper() in GetAttribute(result).upper() or GetAttribute(result).upper() in arr['Name'].upper():
                result.click()
                time.sleep(2)
                try:
                    linkedIn.find_element_by_class_name("link-without-hover-visited").click()
                except:
                    pass
                time.sleep(2)
                try:
                    employeeInfo = GetAttribute(linkedIn.find_element_by_class_name("org-about-company-module__company-size-definition-text")).split(" ")[0]
                    arr['True Employees'] = employeeInfo
                except:
                    pass
                try:
                    employeeInfo = GetAttribute(linkedIn.find_element_by_class_name("org-page-details__employees-on-linkedin-count")).split(" ")[0]
                    arr['LinkedIn Employees'] = employeeInfo
                except:
                    pass
        except:
            pass

    return arr

def openMainPage():
    # Change URL depending on which category you want to scrape
    driver.get('https://www.capterra.com/network-security-software/')
    driver.implicitly_wait(1)
    while True:
        try:
            driver.implicitly_wait(1)
            temp1 = driver.find_element_by_class_name('HorizontalLayout__ShowMoreContainer-sc-15xb01e-2')
           # temp1 = driver.find_element_by_class_name('HorizontalLayout__ShowMoreContainer-sc-15xb01e-3')
            temp2 = temp1.find_element_by_class_name('Button__StyledButton-sc-2779at-0')
            temp2.click()
        except:
            try:
                driver.implicitly_wait(1)
                driver.find_element_by_class_name("ModalPopper__HeaderCloseButton-sc-1pwicnt-4").click()
            except:
                break;

with open('softwareLeadsListNS2.csv','a', newline='') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(["Company Name", "Software Name", "Founded", "Website", "Location", "LinkediIn Employees", "True Employees"])

# MUST CHANGE PATH AFTER INSTALLING chromedriver.exe
driver = webdriver.Chrome(executable_path=r'FILEPATH')
linkedIn = webdriver.Chrome(executable_path=r'FILEPATH')

openMainPage()
#temp1 = driver.find_element_by_class_name('HorizontalLayout__ProductsContainer-sc-15xb01e-2')
#companyBlocks = driver.find_elements_by_class_name("ProductCard__Root-sc-1aqkmbf-0")
companyBlocks = driver.find_element_by_class_name("nb-col-start-1").find_elements_by_class_name("nb-self-center")
#companyBlocks = driver.find_elements_by_class_name("mobile-listing-desc")
linkedIn.get('https://www.linkedin.com')

username = linkedIn.find_element_by_xpath('//*[@id="session_key"]')
# ENTER EMAIL HERE
username.send_keys('key')

password = linkedIn.find_element_by_xpath('//*[@id="session_password"]')
# ENTER PASSWORD HERE
password.send_keys("key")

log_in_button = linkedIn.find_element_by_class_name('sign-in-form__submit-button')
log_in_button.click()

companyLinks = []
for a in companyBlocks:
    #companyLinks.append(a.find_element_by_class_name("DesktopProductCard__ProductCardBody-v49nag-15").find_element_by_tag_name("a").get_attribute('href'))
    companyLinks.append(a.find_element_by_tag_name("a").get_attribute('href'))
   # print(a.find_element_by_tag_name("a").get_attribute('href'))
for i in companyLinks:
   # time.sleep(40)
    driver.get(i)
    WriteToCSV(ExtractLinkedIn(ExtractData(driver)))