import os
import time
import bs4
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from datetime import datetime

# TODO[ ]: Add downloaded file size
# TODO[ ]: Add total size of all downloaded level files
# TODO[ ]: Display stats as a single updating message
# TODO[x]: Add time taken to download the level file
# TODO[X]: Add total program execution time after each level file
# TODO[X]: Add time taken for entire program execution
# TODO[X]: Find if file already exists
# TODO[X]: Skip downloading files that already exist


def check_valid_level_file(text: str, substring: str = "..") -> str:
    return substring not in text


def get_formatted_time(totalTime: float) -> str:
    """
    Calculate a formatted time in days, hours, minutes, and seconds
    :param totalTime: Total time (in seconds) to convert
    :return: Formatted time in 00d00h00m00s format
    """
    timeInDays, remainder = divmod(totalTime, 86400)
    timeInHours, remainder = divmod(remainder, 3600)
    timeInMinutes, timeInSeconds = divmod(remainder, 60)

    formattedTime = f"{int(timeInDays):02}d {int(timeInHours):02}h {int(timeInMinutes):02}m {int(timeInSeconds):02}s"

    return formattedTime


def get_tag_results(url: str, tag: str = "a") -> bs4.element.ResultSet:
    """
    Get the content of all instances of a particular tag on a webpage
    :param url: The URL to grab content from
    :param tag: The HTML tag to search in the content of the page
    :return: Each tag stored in a structure of type bs4.element.ResultSet
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tag_results = soup.find_all(tag)
    return tag_results


levelsUrl = "https://cdn.megamanmaker.com/levels/"  # Default landing page
folderPath = "levels/"  # Store downloaded level files in this path
sleepTime = 0.05
canSeeFolders = True
currentTime = datetime.now()
levelDownloadTime = 0  # In seconds
programStartTime = time.time()  # Start program time counter

# Track number of downloaded levels
totalLevelsDownloaded = 0
alreadyDownloadedLevels = 0
successfullyDownloadedLevels = 0

# Width of characters for stats display
characterCountWidth = 40
numberCountWidth = 6
totalMessageCountWidth = characterCountWidth + numberCountWidth

print("=== MEGA MAN MAKER LEVEL BATCH DOWNLOADER ===\n"
      "=== Download all the levels in Mega Man Maker! ===\n")

while True:
    inputFolderChoice = input("Would you like to see the whole folder structure?\n"
                              "Enter Y/N: ")

    if inputFolderChoice.lower() == "y":
        # canSeeFolders set to True by default
        break
    elif inputFolderChoice.lower() == "n":
        canSeeFolders = False
        break
    else:
        print("Please enter a valid option\n")

# Create folder path if it does not already exist
os.makedirs(folderPath, exist_ok=True)

print("\nFetching levels..."
      "\nPlease wait for about a minute...\n")

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

                # Display total downloaded level counts
                levelDownloadCountMessage = f"{'Total levels downloaded':<{characterCountWidth}} " \
                                            f"{str(totalLevelsDownloaded):<{numberCountWidth}}"
                levelSuccessfulDownloadCountMessage = f"{'Levels downloaded successfully':<{characterCountWidth}} " \
                                                      f"{str(successfullyDownloadedLevels):<{numberCountWidth}}"
                levelAlreadyDownloadedCountMessage = f"{'Already downloaded levels detected':<{characterCountWidth}} " \
                                                     f"{str(alreadyDownloadedLevels):<{numberCountWidth}}"

                # Only download if level file does not exist in the path
                if not os.path.exists(levelFileName):
                    # Find how long it takes to download the level
                    levelDownloadTimeStart = time.time()

                    # Save the level file in the specified folder
                    urlretrieve(zippedLevelFileUrl, levelFileName)

                    levelDownloadTimeEnd = time.time()
                    levelDownloadTime = levelDownloadTimeEnd - levelDownloadTimeStart
                    successfullyDownloadedLevels += 1
                    levelDownloadSuccessMessage = zippedLevelFile.text + " saved in 'levels' folder (downloaded " \
                                                                         "in " + str(levelDownloadTime) + " seconds)"

                    # Display message that level was downloaded successfully
                    if canSeeFolders:
                        print("\t\t\t" + levelDownloadSuccessMessage)
                    else:
                        print(levelDownloadSuccessMessage)

                else:
                    levelDownloadedAlreadyMessage = zippedLevelFile.text + " already exists in 'levels' folder"
                    alreadyDownloadedLevels += 1

                    # Display message that level already exists in the specified path
                    if canSeeFolders:
                        print("\t\t\t" + levelDownloadedAlreadyMessage)
                    else:
                        print(levelDownloadedAlreadyMessage)


                levelFileDoneTime = time.time()
                programExecutionTime = get_formatted_time(levelFileDoneTime - programStartTime)
                runtimeMessage = f"{'Runtime':<{characterCountWidth}} {programExecutionTime}\n"

                # Show total downloaded levels count
                # Includes both downloaded and already downloaded levels
                if canSeeFolders:
                    print(f"\n\t\t\t{'=== STATS ===':^{totalMessageCountWidth}}")
                    print("\t\t\t" + levelDownloadCountMessage)
                    print("\t\t\t" + levelSuccessfulDownloadCountMessage)
                    print("\t\t\t" + levelAlreadyDownloadedCountMessage)
                    print("\t\t\t" + runtimeMessage)
                else:
                    print(f"\n{'=== STATS ===':^{totalMessageCountWidth}}")
                    print(levelDownloadCountMessage)
                    print(levelSuccessfulDownloadCountMessage)
                    print(levelAlreadyDownloadedCountMessage)
                    print(runtimeMessage)

                # print(check_valid_level_file(zippedLevelFileUrl)))
                # print(zippedLevelFileUrl)

            # Sleep to not overload the server
            time.sleep(sleepTime)

print(f"Successfully downloaded all current Mega Man Maker levels as of {currentTime}!\n")
print("=== INSTRUCTIONS ===\n"
      "- Extract the .mmlv.gz file\n"
      "- Place the extracted .mmlv file in your AppData\\Local\\MegaMaker\\Levels folder\n"
      "- Open Mega Man Maker\n" 
      "- Go to your downloaded levels to see the level in-game!\n"
      "(The level will show up as its actual name in-game as in the level file data, not the level ID)\n")

# End program time counter
programEndTime = time.time()
programRunTime = get_formatted_time(programEndTime - programStartTime)

print(f"Ran for {programRunTime}")
