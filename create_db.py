import requests, re
from bs4 import BeautifulSoup


# f2 = open("anime_records_2.sql", "w")

# opening a file in write mode
f_1 = open("name.txt", "w")
f_2 = open("description.txt", "w")
f_3 = open("score.txt", "w")
f_4 = open("end_date.txt", "w")
f_5 = open("image_url.txt", "w")
# traverse paragraphs from soup
f_1.close()
f_2.close()
f_3.close()
f_4.close()
f_5.close()


def add_db(first, finish , url, name):
    for i in range(50*first, 50*finish, 50):
        url_1 = url
        urls = f'{url}&show={i}'
        grab = requests.session().get(urls)
        if i == 0:
            grab = requests.session().get(url_1)
        soup = BeautifulSoup(grab.text, 'html.parser')
        
        for j in range(50):
            check = True

            try:
                link = soup.find_all("tr")[j+9]
            except:
                check = False
            #name
            try:
                data = link.find("strong")
                data = str(data)
                data = data.replace('<strong>', '')
                data = data.replace('</strong>', '')
                data = data.replace('"', '')
                data = data.replace("'", '')
                with open("name.txt", "a") as order_text:
                    order_text.write(f'{i+j}:{data}/n')
                # f_1.write(f'{i+j}:{data}')
                # f_1.write("\n")
                data_1 = f', "{data}"'
            except:
                check = False
            
            #content
            try:
                data = link.find("div", {'class':'pt4'})
                data = str(data)
                data = data.replace('<div class="pt4">', '')
                data = data.replace('</div>', '')
                data = data.replace('"', '')
                data = data.replace("'", '')
                if 'read more.' in data:
                    index_1 = data.index('...')
                    data = data[:index_1+1]
                with open("description.txt", "a") as order_text:
                    order_text.write(f'{i+j}:{data}/n')
                # f_2.write(f'{i+j}:{data}')
                # f_2.write("\n")
                data_2 = f', "{data}"'
            except:
                check = False

            #score
            try:
                data = link.find("td", {'class':f'borderClass ac bgColor0', 'width':'50'})
                if data == None:
                    data = link.find("td", {'class':f'borderClass ac bgColor1', 'width':'50'})
                    data = str(data)
                    data = data.replace(f'<td class="borderClass ac bgColor1" width="50">', '')
                else:
                    data = str(data)
                    data = data.replace(f'<td class="borderClass ac bgColor0" width="50">', '')
                data = data[5:]
                data = data.replace('  </td>', '')
                data = data.strip()
                data = data.replace('"', '')
                data = data.replace("'", '')
                with open("score.txt", "a") as order_text:
                    order_text.write(f'{i+j}:{data}/n')
                # f_3.write(f'{i+j}:{data}')
                # f_3.write("\n")
                data_3 = f', {data}'
            except:
                check = False

            #end_date
            try:
                data = link.find("td", {'class':'borderClass ac bgColor0', 'width':'80'})
                if data == None:
                    data = link.find("td", {'class':f'borderClass ac bgColor1', 'width':'80'})
                    data = str(data)
                    data = data.replace(f'<td class="borderClass ac bgColor1" width="80">', '')
                else:
                    data = str(data)
                    data = data.replace(f'<td class="borderClass ac bgColor0" width="80">', '')
                data = data[5:]
                data = data.replace('  </td>', '')
                data = data.replace('"', '')
                data = data.replace("'", '')
                data = data.strip()
                (m,d,y) = data.split("-")
                if '?' in y:
                    y = '00'
                if '?' in m:
                    m = '01'
                if '?' in d:
                    d = '01'
                y_2 = 20
                if int(y) > 23:
                    y_2 = 19
                data = f'{y_2}{y}-{m}-{d}'
                with open("end_date.txt", "a") as order_text:
                    order_text.write(f'{i+j}:{data[:-1]}/n')
                # f_4.write(f'{i+j}:{data[:-1]}')
                # f_4.write("\n")
                data_4 = f', "{data}"'
            except:
                check = False
            
            #image_url
            try:
                data = link.find("img", {'width':'50', 'height':'70'})
                data = str(data)
                index_1 = data.index('data-src="')
                index_2 = data.index('data-srcset=')
                data = data[index_1:index_2-2]
                data = data.replace('data-src="', '')
                data = data.replace('"', '')
                data = data.replace("'", '')
                index_3 = data.index('/r/')
                data = data.replace(data[index_3:index_3+8], '')
                with open("image_url.txt", "a") as order_text:
                    order_text.write(f'{i+j}:{data}/n')
                # f_5.write(f'{i+j}:{data}')
                # f_5.write("\n")
                data_5 = f', "{data}"'
            except:
                check = False

            
            # print(check)

            if check:
                with open(name, "a") as order_text:
                    order_text.write(f'  ( {i+j+1}')
                    order_text.write(data_1)
                    order_text.write(data_2)
                    order_text.write(data_3)
                    order_text.write(data_4)
                    order_text.write(data_5)
                    order_text.write('),')
                    order_text.write("\n")
            # if check and i > 5000:
            #     f2.write(f'  ( {i+j+1}')
            #     f2.write(data_1)
            #     f2.write(data_2)
            #     f2.write(data_3)
            #     f2.write(data_4)
            #     # f2.write(f', {0}')
            #     f2.write(data_5)
            #     f2.write('),')
            #     f2.write("\n")


# f_1.close()
# f_2.close()
# f_3.close()
# f_4.close()
# f_5.close()
# f.close()
# f2.close()


last_page = 167

# with open("anime_records.sql", "w") as f:
#     f.write("insert into\n")
#     f.write("  anime_anime (id, name, summery, myanimelist_score, released_date, image_url)\n")
#     f.write("values\n")
# add_db(0, 90, "https://myanimelist.net/anime.php?cat=anime&q=&type=0&score=6&status=0&p=0&r=0&sm=0&sd=0&sy=1990&em=0&ed=0&ey=2023&c%5B0%5D=a&c%5B1%5D=b&c%5B2%5D=c&c%5B3%5D=e&c%5B4%5D=f&genre_ex%5B0%5D=28&genre_ex%5B1%5D=12&genre_ex%5B2%5D=50", "anime_records.sql")


# f2 = open("anime_records_2.sql", "w")
# f2.write("insert into\n")
# f2.write("  anime_anime (id, name, summery, myanimelist_score, released_date, image_url)\n")
# f2.write("values\n")
# f2.close()
# add_db(90, 167, "https://myanimelist.net/anime.php?cat=anime&q=&type=0&score=6&status=0&p=0&r=0&sm=0&sd=0&sy=1990&em=0&ed=0&ey=2023&c%5B0%5D=a&c%5B1%5D=b&c%5B2%5D=c&c%5B3%5D=e&c%5B4%5D=f&genre_ex%5B0%5D=28&genre_ex%5B1%5D=12&genre_ex%5B2%5D=50", "anime_records_2.sql")


    
