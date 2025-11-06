import time
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve


def check_valid_level_file(text: str, substring: str = ".."):
    return substring not in text


def get_tag_results(url: str, tag: str = "a"):
    """
    Get the content of all instances of a particular tag on a webpage
    :param url: The URL to grab content from
    :param tag: The HTML tag to search in the content of the page
    :return: All the files found in the folder in a structure of type bs4.element.ResultSet
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tag_results = soup.find_all(tag)
    return tag_results


# Default landing page
levelsUrl = "https://cdn.megamanmaker.com/levels/"
folderPath = "levels/"
sleepTime = 0.1
canSeeFolders = True
totalLevelsDownloaded = 0

print("=== MEGA MAN MAKER LEVEL BATCH DOWNLOADER ===\n"
      "=== Download all the levels in Mega Man Maker! ===\n")

while True:
    inputFolderChoice = input("Would you like to see the folder structure?\n"
                              "Enter Y/N: ")

    if inputFolderChoice.lower() == "y":
        # canSeeFolders set to True by default
        break
    elif inputFolderChoice.lower() == "n":
        canSeeFolders = False
        break
    else:
        print("Please enter a valid option\n")

print("\nFetching levels..."
      "\nPlease wait for about a minute...")

doubleDigitFolders = get_tag_results(levelsUrl)
for doubleDigit in doubleDigitFolders:
    if canSeeFolders:
        print("|--- " + doubleDigit.text)

    doubleDigitUrl = levelsUrl + doubleDigit.text
    quadrupleDigitFolders = get_tag_results(doubleDigitUrl)

    for quadrupleDigit in quadrupleDigitFolders:
        if canSeeFolders:
            print("   |--- " + quadrupleDigit.text)
        quadrupleDigitUrl = doubleDigitUrl + quadrupleDigit.text
        zippedLevelFiles = get_tag_results(quadrupleDigitUrl)

        for zippedLevelFile in zippedLevelFiles:
            zippedLevelFileUrl = quadrupleDigitUrl + zippedLevelFile.text

            # Printing the below message means level file downloaded successfully
            if canSeeFolders:
                print("      |--- " + zippedLevelFile.text)

            if check_valid_level_file(zippedLevelFileUrl):
                levelFileName = folderPath + zippedLevelFile.text

                # Save the level file in the specified folder
                urlretrieve(zippedLevelFileUrl, levelFileName)
                totalLevelsDownloaded += 1

                levelDownloadCountMessage = "Total downloaded levels: " + str(totalLevelsDownloaded)
                levelDownloadSuccessMessage = zippedLevelFile.text + " saved in 'levels' folder"

                if canSeeFolders:
                    print("\t\t\t" + levelDownloadSuccessMessage)
                    print("\t\t\t" + levelDownloadCountMessage)
                else:
                    print(levelDownloadSuccessMessage)
                    print(levelDownloadCountMessage)

                print("Total downloaded levels: " + str(totalLevelsDownloaded))

                # print(check_valid_level_file(zippedLevelFileUrl)))
                # print(zippedLevelFileUrl)

            # Sleep to not overload the server
            time.sleep(sleepTime)

print("Successfully downloaded all current Mega Man Maker levels!")
print("=== INSTRUCTIONS ===\n"
      "- Extract the .mmlv.gz file\n"
      "- Place the .mmlv file in your AppData\\Local\\MegaMaker\\Levels folder\n"
      "- Open Mega Maker\n"
      "- Go to your downloaded levels to see the level in-game!\n")
