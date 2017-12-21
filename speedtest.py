"This module calculates the network speed"
import sys
import time

import requests


def download_file(url):
    """Downloads the specified url and prints out the max speed, average speed and time elapsed 

    Arguments: 
        url {[string]} -- [the url of the file to download] """
    start = time.clock()
    request = requests.get(url, stream=True)
    size = int(request.headers.get('Content-Length'))
    downloaded = 0.0
    total_mbps = 0.0
    maximum_speed = 0.0
    total_chunks = 0.0

    if size is not None:
        for chunk in request.iter_content(1024 * 1024):
            downloaded += len(chunk)
            # Divide the progress bar in 50 chunks.
            done = 50 * downloaded / size
            # Calculate speed in megabytes per second.
            mbps = downloaded / (time.clock() - start) / (1024 * 1024)
            # Check if a new maximum speed is hit.
            maximum_speed = mbps if mbps > maximum_speed else maximum_speed
            total_chunks += 1
            total_mbps += mbps
            sys.stdout.write("\r[%s%s] %.2f MBps" %
                             ('=' * int(done), ' ' * int(50 - done), mbps))
        # Print result summary
        print("\nMaximum Speed: %.2f MBps" % (maximum_speed))
        print("Average Speed: %.2f MBps" % (total_mbps / total_chunks))
        print("Time Elapsed: %.2fs" % (time.clock() - start))
    else:
        print("Cannot calculate download speed")


def main():
    """Main entry point of script. If no url is specified as an argument, a default one is taken
    """
    if len(sys.argv) == 1:
        url = "https://go.microsoft.com/fwlink/?Linkid=850641"
    else:
        url = sys.argv[1]

    download_file(url)


if __name__ == "__main__":
    main()
