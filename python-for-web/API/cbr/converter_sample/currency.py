from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    url = 'http://cbr.ru/scripts/XML_daily.asp'

    def get_coefficient(soup, cur):
        current = soup.find('CharCode', text=cur)
        nominal = current.find_next_sibling('Nominal').string
        value = current.find_next_sibling('Value').string
        value = value.replace(',', '.')
        return Decimal(value) / Decimal(nominal)

    response = requests.get(url,
                            params={
                                'date_req': date,
                            })  # Использовать переданный requests
    soup = BeautifulSoup(response.content, "xml")
    coefficient_from = Decimal(1)  # value * coefficient to make RUR
    coefficient_to = Decimal(1)  # RUR * coefficient to make value
    if cur_from != "RUR":
        coefficient_from = get_coefficient(soup, cur_from)

    if cur_to != "RUR":
        coefficient_to = get_coefficient(soup, cur_to)

    return Decimal(amount * coefficient_from / coefficient_to).quantize(Decimal('.0001'))
