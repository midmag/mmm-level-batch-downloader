import os


def check_valid_level_file(text: str, substring: str = "..") -> str:
    return substring not in text


def count_files(path: str, ext: str) -> int:
    return sum(1 for file in os.listdir(path) if ext in file)


def find_game_version(levelId: int) -> str:
    """
    Find the Mega Man Maker major version that a level ID was uploaded in
    :param levelId: The level ID as an integer
    :return: The major version as a string (e.g. 1.0)
    """
    lastLevelUpdate0 = 155034
    lastLevelUpdate1 = 173349
    lastLevelUpdate2 = 201450
    lastLevelUpdate3 = 239790
    lastLevelUpdate4 = 306531
    lastLevelUpdate5 = 375784
    lastLevelUpdate6 = 450925
    lastLevelUpdate7 = 538463
    lastLevelUpdate8 = 569450
    lastLevelUpdate9 = 582667
    # lastLevelUpdate10 = 0

    if levelId > 0:
        if levelId <= lastLevelUpdate0:
            return "1.0"
        elif levelId <= lastLevelUpdate1:
            return "1.1"
        elif levelId <= lastLevelUpdate2:
            return "1.2"
        elif levelId <= lastLevelUpdate3:
            return "1.3"
        elif levelId <= lastLevelUpdate4:
            return "1.4"
        elif levelId <= lastLevelUpdate5:
            return "1.5"
        elif levelId <= lastLevelUpdate6:
            return "1.6"
        elif levelId <= lastLevelUpdate7:
            return "1.7"
        elif levelId <= lastLevelUpdate8:
            return "1.8"
        elif levelId <= lastLevelUpdate9:
            return "1.9"
        else:
            return "1.10"
