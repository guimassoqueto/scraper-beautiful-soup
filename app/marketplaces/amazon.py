from bs4 import BeautifulSoup
import re
from app.utils.soup import get_soup


def get_product_name(soup: BeautifulSoup) -> str:
    product_name = soup.find(id="productTitle").text
    return product_name.strip()


def get_product_category(soup: BeautifulSoup) -> str:
    category_breadcombs = soup.find(id="wayfinding-breadcrumbs_container")
    main_category = category_breadcombs.find("span", class_="a-list-item").text

    return main_category.strip()


def get_product_image_url(soup: BeautifulSoup) -> str:
    image_tag = soup.find(id="landingImage").decode()
    regex = r"([\w\d\.\/\:\-]+.jpg)\":\[6\d{2},6\d{2}\]"
    image_url = re.search(regex, image_tag)

    assert image_url is not None, "please verify if the product image is beng captured correctly"
    assert image_url.group(1).startswith("https://") and image_url.group(
        1).endswith(".jpg"), "product image url is not being captured correctly"

    return str(image_url.group(1))


def get_product_prices(soup: BeautifulSoup) -> list:
    price_tag = soup.find(id="corePriceDisplay_desktop_feature_div").decode()
    regex = r"<span class=\"a-offscreen\">..(\d+),(\d+)<\/span>"
    prices = re.findall(regex, price_tag)

    # prices example: [(39, 90), (49, 99)]
    # where promotion price is 39.90
    # and original price is 49.99
    assert len(
        prices) == 2, "please verify whether the product prices are being captured correctly"
    return prices


def gen_product_prices_and_discount_dict(prices: list) -> dict:
    prod_price_discount_dict = {}

    # prices example: [(39, 90), (49, 99)]
    original_price = float(f"{prices[1][0]}.{prices[1][1]}")
    promotional_price = float(f"{prices[0][0]}.{prices[0][1]}")

    discont_total = round(original_price - promotional_price, 2)
    discount_pct = round(discont_total / original_price * 100)

    prod_price_discount_dict['original_price'] = original_price
    prod_price_discount_dict['promotional_price'] = promotional_price
    prod_price_discount_dict['discont_total'] = discont_total
    prod_price_discount_dict['discount_pct'] = discount_pct

    return prod_price_discount_dict


def generate_product_info_dict(product_url: str) -> dict:
    try:
        soup = get_soup(product_url)

        product_category = get_product_category(soup)
        product_name = get_product_name(soup)
        product_image = get_product_image_url(soup)
        product_prices = get_product_prices(soup)

        product_prices_dict = gen_product_prices_and_discount_dict(
            product_prices)

        product_info = {}
        product_info['product_category'] = product_category
        product_info['product_name'] = product_name
        product_info['product_image'] = product_image

        product_info.update(product_prices_dict)

        return product_info
    except Exception as e:
        # TODO: remove print and add logger
        print(e, {'product_url': product_url})
