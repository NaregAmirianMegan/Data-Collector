from selenium import webdriver
from urllib.request import urlopen
import os, time

timeLag = 0.5 #Lag time to load full source code
preUrl = "https://www.google.com/search?q="
postUrl = "&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj50ti0zZ7ZAhWL6YMKHdt8B0UQ_AUICigB&biw=1536&bih=735"
continueCollecting = ""

#Add pluses in spaces in user input
def reformat(str):
    str = str.rstrip()
    stringList = (str.split(" "))
    return ("+").join(stringList)

#TODO: stop chrome from openning

def getImages(url, userInput, imageQuota):
    #Setup Chrome environment
    driver = webdriver.Chrome()
    driver.get(url)
    print("Loading images from Google Images . . .")
    pageStatusIndex = 0 

    #Get full page source to collect images
    while not(driver.find_element_by_id("smb").is_displayed()):
        driver.execute_script("window.scrollTo(0, "+str(pageStatusIndex*1000)+");")
        time.sleep(timeLag)
        pageStatusIndex = pageStatusIndex + 1

    driver.find_element_by_id("smb").click()

    while(pageStatusIndex < 50): #TODO: stop when at end of page
        driver.execute_script("window.scrollTo(0, "+str(pageStatusIndex*1000)+");")
        time.sleep(timeLag)
        pageStatusIndex = pageStatusIndex + 1

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
