import requests
from bs4 import BeautifulSoup


def JankenJP_Kakeibo_Parser(data):
    url = "https://www.janken.jp/goods/jk_catalog_syosai.php?jan=" + data
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    
    # get descriptions
    descriptions = []
    tag_names = ["#gname", ".goodsval"]
    for tag_name in tag_names:
        elements = soup.select(tag_name)
        for element in elements:
            descriptions.append(element.get_text().replace('\n', '').replace('\r', '').replace(' ', ''))
    return descriptions


if __name__=="__main__":
    output = JankenJP_Kakeibo_Parser("4902750910454")
    print(output)