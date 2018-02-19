from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from urllib.request import urlopen
import os, time

TIMELAG = 1 #Lag time to load full source code
preUrl = "https://www.google.com/search?q="
postUrl = "&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj50ti0zZ7ZAhWL6YMKHdt8B0UQ_AUICigB&biw=1536&bih=735"
continueCollecting = ""

#Add pluses in spaces in user input
def reformat(str):
    str = str.rstrip()
    stringList = (str.split(" "))
    return ("+").join(stringList)

def getImages(url, userInput, imageQuota):
    #Setup Firefox environment (change Firefox to chrome driver if you prefer chrome)
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(executable_path='geckodriver', firefox_options=options)

    #Get Google Images url with Selenium
    driver.get(url)
    print("Loading images from Google Images . . .")
    pageStatusIndex = 0

    #Get full page source to collect images
    while not(driver.find_element_by_id("smb").is_displayed()):
        driver.execute_script("window.scrollTo(0, "+str(pageStatusIndex*1000)+");")
        time.sleep(TIMELAG)
        pageStatusIndex = pageStatusIndex + 1

    driver.find_element_by_id("smb").click()

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True: 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(TIMELAG)
        pageStatusIndex = pageStatusIndex + 1
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    #Setup new directory name and locate images from source code
    newDir = './'+userInput
    images = driver.find_elements_by_css_selector("img.rg_ic")
    imgSources = []

    #Filter out null references and organize image sources
    for img in images:
        if(img.get_attribute('src') != None):
            imgSources.append(img.get_attribute('src'))

    #Check with user to create directory and download images
    if(imageQuota > len(images)):
        print("Could only find ", str(len(imgSources)), " images.")
        decision = input("Would you like to download "+str(len(imgSources))+" images into a directory called "+userInput+"? (Y/N)")
    else:
        print("Found ", str(len(imgSources)), "images.")
        decision = input("Would you like to download "+str(imageQuota)+" images into a directory called "+userInput+"? (Y/N)")

    #Download images to directory
    if(decision == "y" or decision == "Y"):

        print("Okay downloading images to directory")
        os.makedirs(newDir)
        num = 0
        for each in imgSources:
            if(num < imageQuota):
                num = num + 1
                print(num, ": " + each)
                f = open(newDir+'/pic'+str(num)+'.jpg','wb')
                f.write(urlopen(each).read())
                f.close()
            else:
                break
        print("Done")
    else:
        print("Okay Done")
        return

#CLI loop
while not(continueCollecting == "n" or continueCollecting == "N"):
    userInput = input("Image to collect: ")
    imageQuota = input("How many images of "+userInput+" would you like to collect? ")
    uInput = reformat(userInput)

    searchUrl = preUrl+uInput+postUrl

    print("Collecting "+str(imageQuota)+" images of "+userInput+"\nAt: "+searchUrl)

    getImages(searchUrl, uInput, int(imageQuota))
    continueCollecting = input("Would you like to continue collecting? (Y/N)")
