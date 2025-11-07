import requests
from bs4 import BeautifulSoup
import bs4


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


def main():
    levelsUrl = "https://cdn.megamanmaker.com/levels/"  # Default landing page
    get_tag_results(levelsUrl)


if __name__ == "__main__":
    main()
