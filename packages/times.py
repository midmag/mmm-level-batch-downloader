def get_formatted_time(totalTime: float) -> str:
    """
    Calculate a formatted time in days, hours, minutes, seconds, and milliseconds
    :param totalTime: Total time (in seconds) to convert
    :return: Formatted time in 00d 00h 00m 00s 000ms format
    """
    timeInDays, remainder = divmod(totalTime, 86400)
    timeInHours, remainder = divmod(remainder, 3600)
    timeInMinutes, timeInSeconds = divmod(remainder, 60)
    timeInMilliseconds = (totalTime - (int(totalTime))) * 1000

    formattedTime = f"{int(timeInDays):02}d {int(timeInHours):02}h {int(timeInMinutes):02}m " \
                    f"{int(timeInSeconds):02}s {int(timeInMilliseconds):03}ms"

    return formattedTime


def main():
    import time

    startTime = time.time()
    time.sleep(3.3)
    endTime = time.time()

    print("Run time: " + get_formatted_time(endTime - startTime))
    print(endTime - startTime)


if __name__ == "__main__":
    main()
