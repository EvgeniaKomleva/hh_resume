import scrapy
import requests

def get_url(area, specialization, search_period, order_by):
    url = ['https://hh.ru/search/resume?clusters=True&area='+area+'&specialization='+specialization+'&order_by='+order_by+'&search_period='+search_period+'&logic=normal&pos=position%2Cworkplace_position&exp_period=last_year&exp_company_size=any&exp_industry=any&no_magic=False&st=resumeSearch&text=&fromSearch=true']
    #print(url)
    return url

def auth(username, password):
    s = requests.session()

    s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.79'})

    r = s.get('https://hh.ru').text

    x = r.find('name="_xsrf"') + 20
    _xsrf = r[x:x + 32]

    data = {'username': username,
            'password': password,
            'backUrl': 'https://hh.ru/',
            'remember': 'yes',
            'action': 'Войти',
            '_xsrf': _xsrf}
    r = s.post('https://hh.ru/account/login?backurl=%2F', data=data)
    #print(r.text)

class BlogSpider(scrapy.Spider):
    name = 'spider'
    area = str(input("Enter area number(null - all areas, 1 - Moscow, 2- St. Piterburg, 2019 -MO, more areas-+ https://api.hh.ru/areas): "))
    specialization = str(input("Enter specialization number (1 - IT, 17- sales, more-https://api.hh.ru/specializations): "))
    search_period = str(input("Enter search period (1- day,3- 3 days,7,30 - mounth,365): "))
    order_by = str(input("Order by (relevance, publication_time, salary_desc, salary_asc): "))
    auth_status = int(input("Do you whant login? (1-yes, null -no): "))
    if(auth_status == 1):
        username = str(input("Username: "))
        password = str(input("Password: "))
        auth(username, password)
    url = get_url(area,specialization,search_period, order_by)
    start_urls = get_url(area,specialization,search_period, order_by)#['https://hh.ru/search/resume?clusters=True&area=1&specialization=1&order_by=relevance&search_period=30&logic=normal&pos=position%2Cworkplace_position&exp_period=last_year&exp_company_size=any&exp_industry=any&no_magic=False&st=resumeSearch&text=&fromSearch=true']
    def parse(self, response):
        for resumes in response.css('.resume-search-item__content'):
            link = response.css('a.resume-search-item__name')
            title = resumes.css('::text').get()
            href = resumes.css('::attr(href)').get()
            last_work_plase = resumes.css('.resume-search-item__company-name::text').get()
            yield {
                'title': title,
                'href': href,
                'last_work_plase': last_work_plase,
            }

        for next_page in response.css('a.bloko-button'):
            yield response.follow(next_page, self.parse)