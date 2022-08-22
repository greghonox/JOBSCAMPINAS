from requests import get
from datetime import datetime
from bs4 import BeautifulSoup
from re import search, findall
from argparse import ArgumentParser
from concurrent import futures
from queue import Queue



TAM_COL = 150

class JobCampinas:
    
    def __init__(self) -> None:
        self.occupations: list = []
        self.args: ArgumentParser = self.get_parse()        
        self.url: str = 'https://empregacampinas.com.br/categoria/vaga/'
        
    def __call__(self):
        self.print('START CRAWLER')        
        self.print(f'ARGS RECEIVE: {self.args}')
        self.load = '/?s=' + self.args.l if self.args.l else ''
            
        for page in range(self.args.i, self.args.f):
            self.url = f'https://empregacampinas.com.br/categoria/vaga/page/{page}' + self.load
            pages = self.get_link_page()
            urls = self.extract_url(pages)
            
            self.queue = Queue()
            for page in urls:
                self.queue.put(page)
                
            self.run()
            self.print('-' * TAM_COL)
            print('\n')
            
    def run(self) -> None:
        works = []
        with futures.ThreadPoolExecutor(max_workers=self.args.t) as pool:
            for work in range(self.args.t):
                works.append(pool.submit(self.extract_jobs_pages, work))
            futures.wait(works, return_when='ALL_COMPLETED')
            self.print('-' * TAM_COL)
            self.print_jobs(works)
            
    def print_jobs(self, jobs: list) -> None:
        reges_items = {'email': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', 
                       'interested': 'aos\scuidados[\s|\w|\d]+'}
        for job in futures.as_completed(jobs):
            job = job.result()
            if not job:
                continue
            job = job[0]
            self.print('-' * TAM_COL)
            self.print(job)
            for reg in reges_items.items():
                regex = ', '.join(findall(reg[1], job))
                self.print(f'{reg[0]}: {regex}', 3)
        
    def get_link_page(self) -> list:
        html = self.get_html(self.url)
        return self.get_parse_html(html.text, ('a', {'class': 'thumbnail'}))

    def extract_jobs_pages(self, th) -> list:
        jobs = []
        while not self.queue.empty():
            url = self.queue.get()
            self.print(f'Jobs thread:{th} title: {url[1]}')
            if job:=self.get_job_page(url[0]):
                if job.text not in self.occupations:
                    fmt = '\n'.join([x.text for x in job.findAll('p')])
                    jobs.append(fmt)
                    self.occupations.append(fmt)
        return jobs
            
    @classmethod
    def get_html(cls, url: str) -> get:
        response = get(url)
        cls.print(f'GET {url}', 2)
        assert response.status_code == 200, 'page cannout response!'
        return response

    @classmethod
    def get_job_page(cls, url) -> BeautifulSoup:
        html = cls.get_html(url)
        return cls.get_parse_html(html.text, ('div', {'class': 'postie-post'}), types='find')

    @classmethod        
    def extract_url(cls, pages: list) -> list:
        cases_ignore = ['Página.*', 'Interage.*', 'Criação.*', 'Barini.*', 'Emprega.*', 'Wezen.*']
        l = lambda x: search('|'.join(cases_ignore), x, 2)
        urls = [(url.get('href'), url.get('title')) for url in pages \
            if url.get('title') and not l(url.get('title'))]
        cls.print(f'GET LEN {len(urls)} PAGES')
        return urls
                
    @classmethod
    def get_parse_html(cls, htmls: str, parse: dict, types: str='findAll') -> list:
        html = BeautifulSoup(htmls, 'lxml')
        return html.findAll(*parse) if types == 'findAll' else html.find(*parse)
        
    @classmethod
    def get_parse(cls) -> ArgumentParser.parse_args:
        parser = ArgumentParser()
        parser.add_argument('-t', help='number the thread in pages', type=int, default=1)
        parser.add_argument('-l', help='what is load expected?', type=str)
        parser.add_argument('-i', help='page init', type=int, default=1)
        parser.add_argument('-f', help='page final', type=int, default=99)
        args = parser.parse_args()
        return args
    
    @classmethod
    def extract_html(cls, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, 'lxml')
    
    @classmethod
    def print(cls, msg: str, tip: int=1) -> None:
        tips = {1: ':AVISO:', 2: ':ATENCAO:', 3: ':ERROR:'}
        fmt = f"{datetime.now().strftime('%d-%m-%Y %H:%M')} {tips[tip]} {msg}"
        colors = {
                    1: f"\033[94m{msg}\033[0;0m",
                    2: f"\033[93m{msg}\033[0;0m",
                    3: f"\033[1;35m{msg}\033[0;0m",
                    4: f"\033[91m{msg}\033[0;0m",
                }        
        print(colors.get(tip).format(fmt))
        
JobCampinas()()