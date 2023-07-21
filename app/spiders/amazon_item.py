from app.helpers.utils.regex_replacer import regex_replacer
from bs4 import BeautifulSoup
from bs4.element import Tag
from pydantic import BaseModel
import re
import json


class Product(BaseModel):
    id: str
    title: str
    image_url: str
    category: str
    price: float
    previous_price: float
    discount: int
    reviews: int
    free_shipping: str





def get_title(soup: BeautifulSoup):
    title = soup.find(id='productTitle')
    if title: return regex_replacer(title.get_text().strip())
    return "Not Defined"


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
            set([txt.strip().replace("'", "''") for txt in inner_text if txt.strip() != ""])
        )
    return "Not Defined"


def get_free_shipping(soup: BeautifulSoup) -> str:
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


def convert_price_to_number(price_string: str) -> float:
    price = re.search("[\d\,\.]+", price_string)
    return float(price.group().replace(".", "").replace(",", "."))


def loop_price_selectors(element: Tag):
    """
    Com o element selecionado e existente, roda um loop nos possíveis seletores
    que podem possuir o preço, e se esse seletor existir, retorna o conteúdo (innerText)
    do seletor.
    """
    possible_price_selectors = ["span.a-offscreen"]
    for selector in possible_price_selectors:
        has_content = element.select(selector)
        if has_content:
            return has_content[0].text
    return None


def get_biggest_image(element: Tag):
    images = element.get('data-a-dynamic-image', None)
    if images:
        images = list(json.loads(images).keys())
        return images[-1]
    return None


def get_image_url(soup: BeautifulSoup) -> str:
    #v1
    image_element = soup.find('img', {'class': 'a-dynamic-image'})
    if image_element:
        image_url = image_element.get('data-old-hires', None)
        if image_url: return image_url
    del image_element
    
    # v2
    image_element = soup.find(id='landingImage')
    if image_element:
        image_url = image_element.get('data-old-hires', None)
        if image_url: return image_url
    del image_element
    
    # v3
    image_element = soup.find(id='landingImage')
    if image_element: 
        image_url = get_biggest_image(image_element)
        if image_url: return image_url
        
    # livros físicos
    image_element = soup.find(id='ebooksImgBlkFront')
    if image_element: 
        image_url = get_biggest_image(image_element)
        if image_url: return image_url
    del image_element
    
    # livros físicos v2
    image_element = soup.find(id='imgBlkFront')
    if image_element: 
        image_url = get_biggest_image(image_element)
        if image_url: return image_url
    del image_element
    
    return 'https://raw.githubusercontent.com/guimassoqueto/mocks/main/images/404.webp'


def get_price(soup: BeautifulSoup) -> float:
    price_container_element = soup.find(id="corePrice_feature_div")
    if price_container_element:
        price = loop_price_selectors(price_container_element)
        if price:
            return convert_price_to_number(price)
    del price_container_element

    # no caso de livros, #corePrice_feature_div existe, mas não contem dados relevantes, o elemento a ser capturado é outro
    book_price = soup.find(id="price")
    if book_price:
        return convert_price_to_number(book_price.text)
    del book_price

    # para ebooks kindle, o processo é semelhante ao de livros
    ebook_price = soup.find(id="kindle-price")
    if ebook_price:
        return convert_price_to_number(ebook_price.text)

    return 0.0


def get_previous_price(soup: BeautifulSoup):
    basis_price_element = soup.find('span', {'class': 'basisPrice'})
    if basis_price_element:
        previous_price = basis_price_element.find('span', {'class': 'a-offscreen'})
        if previous_price: return convert_price_to_number(previous_price.text)
    del basis_price_element
    
    # ebooks
    basis_price_element = soup.find(id='digital-list-price')
    if basis_price_element: return convert_price_to_number(basis_price_element.text)
    del basis_price_element
    
    # livros físicos
    basis_price_element = soup.find(id='listPrice')
    if basis_price_element: return convert_price_to_number(basis_price_element.text)
    del basis_price_element
    
    # ração em tabela
    basis_price_element = soup.find('span', {'class': 'a-price a-text-price a-size-base'})
    if basis_price_element: 
        previous_price = basis_price_element.find('span', {'class': 'a-offscreen'})
        if previous_price: return convert_price_to_number(previous_price.text)
    del basis_price_element
    
    return None


def convert_discount_to_number(discount_string: str) -> int:
    discount = re.search("\d{1,2}%", discount_string)
    return int(discount.group().replace("%", ""))


def get_discount(soup: BeautifulSoup) -> int:
    discount_basic_element = soup.find("span", {"class": "savingPriceOverride"})
    if discount_basic_element:
        return convert_discount_to_number(discount_basic_element.text)
    del discount_basic_element

    # livros fisicos
    book_discount = soup.find(id="savingsPercentage")
    if book_discount:
        return convert_discount_to_number(book_discount.text)
    del book_discount

    # ebooks
    ebook_discount = soup.select("p.ebooks-price-savings")
    if ebook_discount:
        return convert_discount_to_number(ebook_discount[0].text)
    del ebook_discount

    # preços e descontos em <table>
    table_discount = soup.select(
        "tr td.a-span12.a-color-price.a-size-base span.a-color-price"
    )
    if table_discount:
        return convert_discount_to_number(table_discount[0].text)

    return 0


def get_item(pid: str, soup: BeautifulSoup) -> dict:
    item = Product(**{
        "id": pid,
        "title": get_title(soup),
        "image_url": get_image_url(soup),
        "category": get_category(soup),
        "reviews": get_reviews(soup),
        "free_shipping": get_free_shipping(soup),
        "price": get_price(soup),
        "previous_price": get_previous_price(soup),
        "discount":get_discount(soup)
    })

    return dict(item)
