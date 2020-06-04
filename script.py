import scrapy

class BlogSpider(scrapy.Spider):
    name = 'spider'
    start_urls = ['https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&logic=normal&no_magic=false&order_by=relevance&pos=full_text&text=&specialization=1']

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
        #проходимся по всем страницам
        for next_page in response.css('a.bloko-button'):
            yield response.follow(next_page, self.parse)