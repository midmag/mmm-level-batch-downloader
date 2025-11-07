import os
import time
from urllib.request import urlretrieve
from datetime import datetime
from packages.levels import find_game_version, count_files, check_valid_level_file
from packages.inputs import input_yes_or_no
from packages.times import get_formatted_time
from packages.html import get_tag_results

# Width of characters for stats display
statsMaxCharacterWidth = 40
# numberCountWidth = 6
# totalMessageCountWidth = characterCountWidth + numberCountWidth

levelsUrl = "https://cdn.megamanmaker.com/levels/"  # Default landing page
folderPath = "levels/"  # Store downloaded level files in this path
sleepTime = 0.3
latestSuccessfullyDownloadedLevelMessage = f"{'Latest successfully downloaded level':<{statsMaxCharacterWidth}} " \
                                           f"N/A"
latestAlreadyDownloadedLevelMessage = f"{'Latest already downloaded level':<{statsMaxCharacterWidth}} " \
                                           f"N/A"
levelDownloadTimeTakenMessage = f"{'Downloaded in ':<{statsMaxCharacterWidth}} N/A\n"
levelDownloadFinishedTimeMessage = f"{'Finished downloading at':<{statsMaxCharacterWidth}} N/A\n"

# Track number of downloaded levels
downloadedTotalLevels = count_files(folderPath, ".mmlv.gz")
downloadedAlreadyLevels = 0
downloadedSuccessfullyLevels = 0

levelDownloadTime = 0  # In seconds
currentTime = datetime.now()
programStartTime = time.time()  # Start program time counter

print("=== MEGA MAN MAKER LEVEL BATCH DOWNLOADER ===\n"
      "=== Download all the levels in Mega Man Maker! ===\n")

canSeeFolders = input_yes_or_no("Would you like to see the whole folder structure?")
print()

canSeeStats = input_yes_or_no("Would you like to see the stats after every level file?")
print()

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

            if canSeeFolders:
                print("      |--- " + zippedLevelFile.text)

            if check_valid_level_file(zippedLevelFileUrl):
                levelFileName = folderPath + zippedLevelFile.text

                # Find the version of Mega Man Maker in which the level was uploaded
                versionUploadedMessage = f"{'Game version uploaded':<{statsMaxCharacterWidth}} " \
                                            f"{find_game_version(int(zippedLevelFile.text[:-8]))}"

                # Display total downloaded level counts
                levelDownloadCountMessage = f"{'Total levels downloaded':<{statsMaxCharacterWidth}} " \
                                            f"{str(downloadedTotalLevels)}"
                levelSuccessfulDownloadCountMessage = f"{'Levels downloaded successfully':<{statsMaxCharacterWidth}} " \
                                                      f"{str(downloadedSuccessfullyLevels)}"
                levelAlreadyDownloadedCountMessage = f"{'Already downloaded levels detected':<{statsMaxCharacterWidth}} " \
                                                     f"{str(downloadedAlreadyLevels)}"

                # Only download if level file does not exist in the path
                if not os.path.exists(levelFileName):
                    isSuccessfullyDownloadedLevel = True

                    # Find how long it takes to download the level
                    latestSuccessfullyDownloadedLevelMessage = f"{'Latest successfully downloaded level':<{statsMaxCharacterWidth}} " \
                                                          f"{zippedLevelFile.text}"
                    levelDownloadTimeStart = time.time()

                    # Save the level file in the specified folder
                    urlretrieve(zippedLevelFileUrl, levelFileName)

                    # Level download finished
                    levelDownloadTimeEnd = time.time()
                    levelDownloadTime = levelDownloadTimeEnd - levelDownloadTimeStart
                    finishedLevelDownloadTime = datetime.now()

                    downloadedTotalLevels += 1
                    downloadedSuccessfullyLevels += 1
                    levelDownloadSuccessMessage = f"{zippedLevelFile.text} saved in '{folderPath}' folder\n"
                    levelDownloadTimeTakenMessage = f"{'Downloaded in ':<{statsMaxCharacterWidth}}" \
                                                       f"{finishedLevelDownloadTime:.3f}s\n"
                    levelDownloadFinishedTimeMessage = f"{'Finished downloading at':<{statsMaxCharacterWidth}}" \
                                                       f"{finishedLevelDownloadTime}\n"

                    # Display message that level was downloaded successfully
                    if canSeeFolders:
                        print("\t\t\t" + levelDownloadSuccessMessage)
                    else:
                        print(levelDownloadSuccessMessage)

                else:
                    isSuccessfullyDownloadedLevel = False
                    latestAlreadyDownloadedLevelMessage = f"{'Latest already downloaded level':<{statsMaxCharacterWidth}} " \
                                                          f"{zippedLevelFile.text}"
                    levelDownloadedAlreadyMessage = f"{zippedLevelFile.text} already exists in '{folderPath}' folder"
                    downloadedAlreadyLevels += 1

                    # Display message that level already exists in the specified path
                    if canSeeFolders:
                        print("\t\t\t" + levelDownloadedAlreadyMessage)
                    else:
                        print(levelDownloadedAlreadyMessage)

                levelFileDoneTime = time.time()
                programExecutionTime = get_formatted_time(levelFileDoneTime - programStartTime)
                runtimeMessage = f"{'Runtime':<{statsMaxCharacterWidth}} {programExecutionTime}\n"

                # Show level download stats
                # Includes both downloaded and already downloaded levels
                if canSeeFolders and canSeeStats:
                    print(f"\n\t\t\t{'=== STATS ===':^{statsMaxCharacterWidth}}")
                    print("\t\t\t" + levelDownloadCountMessage)
                    print("\t\t\t" + levelSuccessfulDownloadCountMessage)
                    print("\t\t\t" + levelAlreadyDownloadedCountMessage)
                    print("\t\t\t" + latestAlreadyDownloadedLevelMessage)
                    print("\t\t\t" + latestSuccessfullyDownloadedLevelMessage)
                    print("\t\t\t" + runtimeMessage)

                    if isSuccessfullyDownloadedLevel:
                        print("\t\t\t" + levelDownloadFinishedTimeMessage)
                        print("\t\t\t" + levelDownloadTimeTakenMessage)

                elif canSeeStats:
                    print(f"\n{'=== STATS ===':^{statsMaxCharacterWidth}}")
                    print(levelDownloadCountMessage)
                    print(levelSuccessfulDownloadCountMessage)
                    print(levelAlreadyDownloadedCountMessage)
                    print(latestAlreadyDownloadedLevelMessage)
                    print(latestSuccessfullyDownloadedLevelMessage)
                    print(runtimeMessage)

                    if isSuccessfullyDownloadedLevel:
                        print(levelDownloadFinishedTimeMessage)
                        print(levelDownloadTimeTakenMessage)

                # print(check_valid_level_file(zippedLevelFileUrl)))
                # print(zippedLevelFileUrl)

                # Sleep to not overload the server
                time.sleep(sleepTime)
            time.sleep(sleepTime)
        time.sleep(sleepTime)
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
