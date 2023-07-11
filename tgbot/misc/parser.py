from typing import Dict, List

import requests
from bs4 import BeautifulSoup


def parse(url: str, snils: str, sum_points: int, university: str) -> Dict | List:
    req = requests.get(url)
    req.encoding = 'utf-8'

    if req.status_code != 200:
        raise ValueError('The Service Denied Access')

    soup = BeautifulSoup(req.text, "html.parser")
    requested_data: dict = {}
    match university:
        case 'СПбГУ':
            requested_data = parse_spbgu(content=soup)
        case 'ПГНИУ':
            requested_data = parse_pgniu(content=soup)

    data = None
    if requested_data.get(snils):
        data = requested_data.get(snils)
    elif requested_data.get(snils) is None:
        data = [v for v in requested_data.values() if v["Sum Ege"] == sum_points]

    if data:
        return data
    else:
        raise ValueError("I couldn't find you in arbitrament list of this program and university")


def parse_spbgu(content: BeautifulSoup) -> Dict:
    json_obj = {}
    headers = [
        "Place", "Snils", "Concurs Type", "Priority",
        "Sum All", "Sum Ege", "Ex1", "Ex2", "Ex3",
        "Ind Ach", "Individual Achievements", "Dop Info"
    ]

    table_body = content.find(id='entry').find('tbody')
    for tr in table_body.findChildren('tr'):
        rows = []
        for td in BeautifulSoup(str(tr), "html.parser").findAll('td'):
            txt: str = td.text.strip()
            if txt.isdigit():
                txt: int = int(txt)
            rows.append(txt)

        if len(rows) >= 2:
            key = str(rows[1]).replace('-', '').replace(' ', '')
            json_obj[key] = {k: v for k, v in zip(headers, rows)}
        else:
            pass
    return json_obj


def parse_pgniu(content: BeautifulSoup) -> Dict:
    "Very crutch solution, sorry for it :'("
    json_obj = {}
    headers = [
        "Place", "Snils", "Original docs",
        "Ex1", "Ex2", "Ex3",
        "Ind Ach", "Sum Ege", "Priority",
    ]

    table = content.find("a", attrs={"name": "010302-13-11-67"}).parent.findAll("table")[0]
    kwota = ''
    for tr in table.findAll('tr')[1:]:
        rows = []
        for td in BeautifulSoup(str(tr), "html.parser").findAll('td'):
            txt: str = td.text.strip()
            if txt.isdigit():
                txt: int = int(txt)
            rows.append(txt)

        if len(rows) >= 2:
            if not json_obj.get(kwota):
                json_obj[kwota] = {}
            key = str(rows[1]).replace('-', '').replace(' ', '')
            json_obj[kwota][key] = {k: v for k, v in zip(headers, rows)}
        elif len(rows) == 1:
            kwota = rows[0]

    return json_obj['Общий конкурс']
