import requests
import json
import ipywidgets as widgets
from IPython.core.display import display


def wylistuj_dostepne_waluty():
    url = 'http://api.nbp.pl/api/exchangerates/tables/c/?format=json'
    a = requests.get(url)
    dane = json.loads(a.text)
    dostepne_waluty = []
    waluty_dane = []
    for slownik in dane:
        waluty_dane.append(slownik['rates'])
    for lista in waluty_dane:
        for slo in lista:
            dostepne_waluty.append(slo['currency'])
    return dostepne_waluty


def symbol_dostepnej_waluty(waluta):
    url = 'http://api.nbp.pl/api/exchangerates/tables/c/?format=json'
    a = requests.get(url)
    dane = json.loads(a.text)
    waluty_dane = []
    for slownik in dane:
        waluty_dane.append(slownik['rates'])
    for lista in waluty_dane:
        for slo in lista:
            if slo['currency'] == waluta.lower():
                return slo['code']


def kup_walute(waluta, kwota):
    oznaczenie_waluty = symbol_dostepnej_waluty(waluta)
    url = 'http://api.nbp.pl/api/exchangerates/rates/c/{}/?format=json'.format(oznaczenie_waluty)
    a = requests.get(url)
    dane = json.loads(a.text)
    cena_zakupu = dane['rates'][0]['ask']
    return cena_zakupu * kwota


def sprzedaj_walute(waluta1, kwota1):
    oznaczenie_waluty = symbol_dostepnej_waluty(waluta1)
    url = 'http://api.nbp.pl/api/exchangerates/rates/c/{}/?format=json'.format(oznaczenie_waluty)
    a = requests.get(url)
    dane = json.loads(a.text)
    cena_sprzedazy = dane['rates'][0]['bid']
    return cena_sprzedazy * kwota1


przyciski_kupic_sprzedac = widgets.ToggleButtons(
    options=['KUPIĆ', 'SPRZEDAĆ'],
    description='Chcę: ',
    disabled=False,
    button_style='',  # 'success', 'info', 'warning', 'danger' or ''
    # tooltips=['Description of slow', 'Description of regular', 'Description of fast'],
    #     icons=['check'] * 2
)

wybor_waluty = widgets.Dropdown(
    options=wylistuj_dostepne_waluty(),
    # value='2',
    description='Waluta:',
    disabled=False,
)


wybor_kwoty = widgets.IntText(
    value=10,
    description='Kwota:',
    disabled=False
)


def wykonaj_na_klik():
    display(przyciski_kupic_sprzedac)
    if przyciski_kupic_sprzedac.value == 'KUPIĆ':
        display(wybor_waluty)
        display(wybor_kwoty)
        return kup_walute(wybor_waluty.value, wybor_kwoty.value)
    else:
        display(wybor_waluty)
        display(wybor_kwoty)
        return sprzedaj_walute(wybor_waluty.value, wybor_kwoty.value)
