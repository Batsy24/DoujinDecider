import random
import pygame
import requests
from bs4 import BeautifulSoup

pygame.init()


def get_newest_sauce():
    sauce_list = []
    url_ = 'https://nhentai.net'
    data_ = requests.get(url_).text
    hentai = BeautifulSoup(data_, 'lxml')
    lim_list = hentai.find_all('div', class_="container index-container")
    for f in lim_list:
        for g in f:
            for h in g:
                str_h = str(h)
                split_list = str_h.split()
                sauce_list.append(split_list)

    href = sauce_list[2][2]
    list_ = []
    for s in href:
        if s.isdigit():
            list_.append(s)

    strings = [str(integer) for integer in list_]
    a_string = "".join(strings)
    Sauce_limit = int(a_string)

    return Sauce_limit


limit = get_newest_sauce()


def get_sauce():
    sauce = random.randint(1, limit)
    print(sauce)
    url = f'https://nhentai.net/g/{sauce}/'
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'lxml')
    return soup, sauce


nhentai, sauce = get_sauce()


def get_info():
    date_uploaded = None
    language_list = []
    parody_list = []  # FINE ILL DO IT >:c
    tag_list = []

    hentai_info = nhentai.find_all('div', class_="tag-container field-name")

    for info in hentai_info:
        if "Parodies" in info.text:
            parody = info.find('span', class_="name").text
            parody_list.append(parody)

        if "Tags" in info.text:
            tags = info.find_all('span', class_="name")
            for t in tags:
                tag = t.text
                tag_list.append(tag)

        if "Languages" in info.text:
            languages = info.find_all('span', class_="name")
            for l in languages:
                language = l.text
                language_list.append(language)

        if "Uploaded" in info.text:
            date = info.time['datetime']
            date_uploaded = date[0:10]

    favorites = nhentai.find('span', class_="nobold").text
    favorite_count = favorites[1:-1]

    title = nhentai.find('span', class_="pretty").text

    return title, parody_list, tag_list, language_list, date_uploaded, favorite_count


def get_image():
    image_data = nhentai.find('img', class_="lazyload")
    image_link = image_data['data-src']
    image = requests.get(image_link).content
    with open('img/cover.jpg', 'wb+') as x:
        x.write(image)
    cover_img = pygame.image.load('img/cover.jpg')

    return cover_img


title, parodies, tags, language, date, fav = get_info()
print(f"""" title: {title},
Parodies: {parodies},
tags: {tags},
fav: {fav} """)
cover_ = get_image()

if len(parodies) < 1:
    parody = "nothing"
else:
    parody = parodies[-1]

# colors
grey = (40, 40, 40)
light_grey = (72, 72, 72)
white = (255, 255, 255)

win_size = (700, 500)
win = pygame.display.set_mode(win_size)
pygame.display.set_caption('Doujin Decider 3.0')
censor_logo = pygame.image.load('censor.png')

size = cover_.get_size()
if size[1] > size[0]:
    new_size = (270, 370)
elif size[0] > size[1]:
    new_size = (round(350 / 1.3), round(220 / 1.3))
elif size[0] == size[1]:
    new_size = (270, 270)
cover = pygame.transform.smoothscale(cover_, new_size)

click = False
alpha = 250
censor_conditional = True
eye_x, eye_y = 135, 180
pos = (30, 30)

if new_size == (round(350 / 1.3), round(220 / 1.3)):
    eye_y -= 100

while True:
    font = pygame.font.Font('Targa.ttf', 17)
    font_s = pygame.font.Font('Targa.ttf', 15)
    mx, my = pygame.mouse.get_pos()
    censor_rect = pygame.Rect(pos, new_size)
    if censor_rect.collidepoint((mx, my)):
        if click:
            alpha = 0
            censor_conditional = False

    click = False

    title_rect = pygame.Rect(320, 30, 350, 30)
    parody_rect = pygame.Rect(320, 80, 350, 30)
    tags_rect = pygame.Rect(320, 130, 350, 130)
    language_rect = pygame.Rect(30, 415, 200, 25)
    date_rect = pygame.Rect(30, 448, 200, 25)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True

        win.fill(grey)
        win.blit(cover, pos)

        pygame.draw.rect(win, light_grey, title_rect)
        pygame.draw.rect(win, light_grey, parody_rect)
        pygame.draw.rect(win, light_grey, tags_rect)
        pygame.draw.rect(win, light_grey, language_rect)
        pygame.draw.rect(win, light_grey, date_rect)

        title_text = font.render(f"Title: ", True, white)
        win.blit(title_text, (330, 33))

        parody_text = font.render(f"Parody of: ", True, white)
        win.blit(parody_text, (330, 83))

        tags_text = font.render(f"Tags: ", True, white)
        win.blit(tags_text, (330, 133))

        language_text = font.render(f"language: {language[-1]}", True, white)
        win.blit(language_text, (40, 417))

        date_text = font.render(f"Uploaded on {date}", True, white)
        win.blit(date_text, (40, 450))

        censor = pygame.Surface(new_size)
        censor.set_alpha(alpha)
        censor.fill((16, 16, 16))
        win.blit(censor, pos)

        if censor_conditional:
            win.blit(censor_logo, (eye_x, eye_y))

    pygame.display.update()
