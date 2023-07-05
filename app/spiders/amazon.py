from bs4 import BeautifulSoup
from requests import get
import re


def get_soup(pid: str, header: dict) -> BeautifulSoup:
    url = f"https://amazon.com.br/dp/{pid}"
    page = get(url, headers=header)
    assert page.status_code == 200, "Status Code must be 200"
    return BeautifulSoup(page.content, "html.parser")


def get_title(soup: BeautifulSoup):
    assert soup.title.string is not None, "title must not be None"
    return re.sub(r"[^a-zA-Z0-9_\s\.]", "", soup.title.string)


def get_reviews(soup: BeautifulSoup):
    title = soup.find(id="acrCustomerReviewText")
    if title is None:
        return 0
    reviews = re.search("^[\d*\.]+", title.get_text())
    if not reviews:
        return 0
    return int(reviews.group().replace(".", ""))


def get_category(soup: BeautifulSoup, delimiter: str = " > "):
    element = soup.find(id="wayfinding-breadcrumbs_container")
    if element is None:
        return "Not Defined"
    element = str(element)
    inner_text = re.findall(r">\n([\s/\n\w]+)<", element)
    if inner_text:
        return delimiter.join(
            set([txt.strip() for txt in inner_text if txt.strip() != ""])
        )
    return "Not Defined"


def get_is_prime(soup: BeautifulSoup) -> str:
    prime_div = soup.find(id="primeSavingsUpsellCaption_feature_div")
    if prime_div is not None:
        return "true"

    prime_div = soup.select(
        "div.tabular-buybox-text:nth-child(4) div:nth-child(1) span:nth-child(1)"
    )
    if prime_div:
        prime_div = prime_div[0].text
        if "amazon" in prime_div.strip().lower():
            return "true"

    prime_div = soup.select(
        "div#mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE span"
    )
    if prime_div:
        prime_div = prime_div[0].text
        if "grátis" in prime_div.strip().lower():
            return "true"

    return "false"


def get_item(pid: str, header: dict) -> dict:
    item = {}
    item["id"] = pid
    soup = get_soup(pid, header)
    item["title"] = get_title(soup)
    item["category"] = get_category(soup)
    item["reviews"] = get_reviews(soup)
    item["is_prime"] = get_is_prime(soup)
    return item
