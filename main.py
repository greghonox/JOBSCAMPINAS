from requests import get
from datetime import datetime
from bs4 import BeautifulSoup
from argparse import ArgumentParser

class JobCampinas:
    
    def __init__(self) -> None:
        self.url = 'https://empregacampinas.com.br/categoria/vaga/'
        self.occupations: list = []
        self.args = self.get_parse()
        
    def __call__(self):
        self.print('START CRAWLER')        
        self.print(f'ARGS RECEIVE: {self.args}')
        if self.args.l:
            self.url.replace('/categoria/vaga/', '/?' + self.args.l)
        html = self.get_html()
        parse = self.get_parse_html(html.text, ['div', {'class': 'col-lg-12'}])
            
    @classmethod
    def get_parse_html(cls, html: str, parse: dict) -> list:
        list_parse = []
        for tag in parse:
            html = BeautifulSoup(html, 'lxml')
            list_parse.append(html.findAll(tag))
        return list_parse
            
    def get_html(self) -> get:
        response = get(self.url)
        assert response.status_code == 200, 'page cannout response!'
        return response
    
    def get_parse(self) -> ArgumentParser.parse_args:
        parser = ArgumentParser()
        parser.add_argument('-t', help='number the thread in pages', type=int, default=1)
        parser.add_argument('-l', help='what is load expected?', type=str)
        args = parser.parse_args()
        return args
    
    def extract_html(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, 'lxml')
    
    def print(self, msg: str, tip: int=1) -> None:
        tips = {1: ':AVISO:', 2: ':ERROR:', 3: ':ATENCAO:'}
        fmt = f"{datetime.now().strftime('%D-%M-%Y %H:%M')} {tips[tip]} {msg}"
        print(msg)
        
JobCampinas()()