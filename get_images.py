from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, urlretrieve
import os

def reformat(str):
    str = str.rstrip()
    stringList = (str.split(" "))
    return ("+").join(stringList)

def soupify(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    return BeautifulSoup(html, "lxml")


def getImages(url, userInput):
    newDir = './'+userInput
    os.makedirs(newDir)
    bsoup = soupify(url)
    btags = [img for img in bsoup.findAll('img')]
    print("Found ", str(len(btags)), "images.")
    decision = input("Would you like to download these images into a directory called "+userInput+"? Y/N")
    if(decision == "y" or decision == "y"):
        print("Okay downloading images to directory")
        image_links = [each.get('src') for each in btags]
        num = 0
        for each in image_links:
            num = num + 1
            f = open(newDir+'/pic'+str(num)+'.jpg','wb')
            f.write(urlopen(each).read())
            f.close()
        print("Done")
    else:
        print("Okay Done")
        return

userInput = input("Image to collect: ")
uInput = reformat(userInput)

searchUrl = "https://www.google.com/search?q="+uInput+"&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj50ti0zZ7ZAhWL6YMKHdt8B0UQ_AUICigB&biw=1536&bih=735"

print("Collecting images of "+userInput+"\nAt: "+searchUrl)

getImages(searchUrl, uInput)
