import requests
from lxml import html
import os


class Model(object):
    def __repr__(self):
        classname = self.__class__.__name__
        properties = ('{} = ({})'.format(k, v)
                      for k, v in self.__dict__.items())
        return '\n< {}:\n {}\n>'.format(classname, '\n '.join(properties))


class Movie(Model):
    def __init__(self):
        self.title = ''
        self.crews = ''
        self.cover_url = ''
        self.link = ''
        self.ranking = 0
        self.score = 0
        self.comment_num = 0
        self.quote = ''


def log(*args, **kwargs):
    with open('top250_movies.txt', 'a', encoding='utf-8') as f:
        print(*args, file=f, **kwargs)


def cached_url(url, filename):
    path = os.path.join('cached_movies', filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return f.read()
    else:
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
        return r.content   


def movie_from_div(div):
    movie = Movie()
    movie.title = div.xpath('.//span[@class="title"]')[0].text
    movie.crews = div.xpath('.//div[@class="bd"]/p')[0].text
    movie.cover_url = div.xpath('.//div[@class="pic"]/a/img/@src')[0]
    movie.link = div.xpath('.//div[@class="hd"]/a/@href')[0]
    movie.ranking = div.xpath('.//div[@class="pic"]/em')[0].text
    movie.score = div.xpath('.//span[@class="rating_num"]')[0].text
    movie.comment_num = div.xpath('.//div[@class="star"]/span')[-1].text[:-3]
    try:
        movie.quote = div.xpath('.//span[@class="inq"]')[0].text
    except IndexError as e:
        movie.quote = '该电影没有描述'
    return movie 


def movie_from_url(url, filename):
    # 先把页面下载下来
    page = cached_url(url, filename)
    # 解析下载好的 html 页面
    root = html.fromstring(page)
    movie_divs = root.xpath('//div[@class="item"]')
    movies = [movie_from_div(div) for div in movie_divs]
    return movies


def download_img(url, name):
    r = requests.get(url)
    path = os.path.join('movie_covers', name)
    with open(path, 'wb') as f:
        f.write(r.content)


def save_covers(movies):
    for m in movies:
        download_img(m.cover_url, m.title + '.jpg')


def main():
    for i in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start={}'.format(i)
        filename = str(i) + '.html'
        movies = movie_from_url(url, filename)
        log(movies)
        save_covers(movies)


if __name__ == '__main__':
    main()
