import bs4
from bs4 import BeautifulSoup
import json

text2 = """ {
  "header": {
    "Заголовок": "Акт приема передачи.doc",
    "Вид/подвид": "Акт",
    "Автор документа": "Новикова С.П.",
    "Примечание к документу": "Требуется утверждение",
    "Срок выполнения": "09.03.2023 16:38:33"
  },


  "signer": "Сидоров М.О.",
  "buttons": {
    "Задача №5": {
      "file": {
        "name": "failik",
        "format": "pdf",
        "required": true
      },
      "comment": {
        "name": "my_comment",
        "required": true
      }
    },
    "Отказать": {
      "comment": {
        "name": "my_comment",
        "required": true
      }
    },
    "Поставить на контроль": {
      "category": {
        "name": "cat",
        "variants": {
          "one": {
            "code": "one",
            "name": "один",
            "checked": false
          },
          "two": {
            "code": "two",
            "name": "два",
            "checked": false
          }
        }
      }
    }
  }
}

"""

text = """ 
{"header":{"Заголовок":"Акт приема передачи.doc","Вид/подвид":"Акт","Автор документа":"Новикова С.П.","Примечание к документу":"Требуется утверждение","Срок выполнения":"09.03.2023 16:38:33"},"concordants":[["Иванов И.И","Согласовано","-","02.04.2023"],["Петров П.П.","Отказано","Все переделать!","06.03.2023"]],"signer":"Сидоров М.О.","buttons":{"Задача №5":{"file":{"name":"failik","format":"pdf","required":true},"comment":{"name":"my_comment","required":true}},"Отказать":{"comment":{"name":"my_comment","required":true}},"Поставить на контроль":{"category":{"name":"cat","variants":{"one":{"code":"one","name":"один","checked":false},"two":{"code":"two","name":"два","checked":false}}}}}}
"""

class RenderHTML:

    def __init__(self, context):
        self.context = context

    @staticmethod
    def create_table_td(soup, border, class_, width):

        table = soup.new_tag("table")
        table['class'] = class_
        table['style'] = 'margin:0; padding:0; border-collapse: collapse;'
        table['border'] = border
        table['cellpadding'] = '5'
        table['width'] = width

        tbody = soup.new_tag("tbody")
        tr = soup.new_tag("tr")

        table.append(tbody)
        tbody.append(tr)

        return table, tr

    @staticmethod
    def create_logo(soup):
        """ Создаем контейнер с логотипом """

        div_logo = soup.new_tag("div")
        img_logo = soup.new_tag("img", alt="Логотип")
        img_logo['src'] = 'https://im.wampi.ru/2023/04/10/png-transparent-flower-garden-logo-petal-flower-leaf-logo-plant-stem-thumbnail.png'
        img_logo['style'] = 'height:36px; width:36px'
        div_logo.append(img_logo)

        return div_logo

    @staticmethod
    def create_tr_link(soup):
        """ Создаем строку-ссылку на задачу """

        tr = soup.new_tag("tr")
        td = soup.new_tag("td", colspan='2')
        div = soup.new_tag("div")
        div[
            'style'] = """padding: 10px; background-color: #5ac37d; text-align:center; color:white; text-decoration: underline; font-weight: bold """
        a = soup.new_tag("a")
        a['style'] = "color:white"
        a['class'] = "header"
        a['href'] = "task_link"

        tr.append(td)
        td.append(div)
        div.append(a)
        a.append('task_name')

        return tr

    @staticmethod
    def create_tr_attention(soup):
        """ Выводим предупреждение о конфиденциальности, если требуется """

        tr = soup.new_tag("tr")
        td = soup.new_tag("td", colspan='2')
        div = soup.new_tag("div")
        div[
            'style'] = "padding: 10px; background-color: red; text-align:center; color:white; font-weight: bold"
        text = """ 
              Внимание! Документ ограниченного доступа! \n
              Запрещается пересылка сотрудникам, не допущенным к просмотру \n
              данной информации, и пересылка по незащищенным каналам связи! \n
        """
        tr.append(td)
        td.append(div)
        div.append(text)

        return tr

    @staticmethod
    def create_trs_description(soup, context):
        """ Заполняем ['Заголовок', 'Вид/подвид', 'Автор документа' ... ]"""

        tr_outer = soup.new_tag("tr")

        for key, value in context['header'].items():
            tr = soup.new_tag("tr")

            td_30 = soup.new_tag("td", width="30%")
            td_30.append(key)
            tr.append(td_30)

            td_70 = soup.new_tag("td", width="70%")
            td_70.append(value)
            tr.append(td_70)

            tr_outer.append(tr)

        return tr_outer

    @staticmethod
    def create_trs_concordants(soup, context):
        """ Заполняем таблицу согласующих """

        tr_outer = soup.new_tag("tr")

        headers = ['Согласующий', 'Решение', 'Замечания', 'Срок исполнения']
        tr_th = soup.new_tag("tr")
        for i in range(len(headers)):
            th = soup.new_tag("th")
            th.append(headers[i])
            tr_th.append(th)
        tr_outer.append(tr_th)

        for item in context['concordants']:

            tr = soup.new_tag("tr")
            for i in range(len(item)):
                td = soup.new_tag("td")
                td.append(item[i])
                tr.append(td)
            tr_outer.append(tr)

        return tr_outer

    @staticmethod
    def create_tr_signer(soup, context):
        """ Заполняем таблицу подписантов """

        tr_signer = soup.new_tag("tr")

        th_30 = soup.new_tag("th", width="30%")
        th_30.append('Подписант')
        tr_signer.append(th_30)

        td_70 = soup.new_tag("td", width="70%")
        td_70.append(context['signer'])
        tr_signer.append(td_70)

        return tr_signer


def render_table_second(message):

    render = RenderHTML(message)

    print(message)

    soup = BeautifulSoup('<p></p>', 'html.parser')

    # <!-- внешняя таблица -->
    table_outer, tr_outer = render.create_table_td(soup, '0', "outer", '800px')
    td_outer = soup.new_tag("td", align="center")
    td_outer['class'] = 'td_outer'
    tr_outer.append(td_outer)

    # <!-- Логотип Fortum -->
    div_logo = render.create_logo(soup)
    td_outer.append(div_logo)

    # <!-- средняя таблица -->
    table_middle, tr_middle = render.create_table_td(soup, '0', "middle",
                                                     '100%')
    td_middle = soup.new_tag("td", align="center")
    td_middle['class'] = 'td_middle'
    tr_middle.append(td_middle)
    td_outer.append(table_middle)

    table_t1, tr_t1 = render.create_table_td(soup, '1', "t1", '100%')
    td_middle.append(table_t1)

    # <!-- Ссылка на задачу (зеленая) -->
    tr_link = render.create_tr_link(soup)
    tr_t1.append(tr_link)

    # <!-- КОнфиденциально (красное) -->
    if 'confidential' in message.keys():
        tr_attention = render.create_tr_attention(soup)
        tr_t1.append(tr_attention)

    # <!-- Заголовок, Подвид ... -->
    trs_description = render.create_trs_description(soup, message)
    tr_t1.append(trs_description)
    p1 = soup.new_tag("p")
    td_middle.append(p1)

    # <!-- Согласующие -->
    if 'concordants' in message:
        table_t2, tr_t2 = render.create_table_td(soup, '1', "t2", '100%')
        td_middle.append(table_t2)

        tr_conc = render.create_trs_concordants(soup, message)
        tr_t2.append(tr_conc)
        p2 = soup.new_tag("p")
        td_middle.append(p2)

    # <!-- Подписант -->
    if 'signer' in message:
        table_t3, tr_t3 = render.create_table_td(soup, '1', "t3", '100%')
        td_middle.append(table_t3)

        tr_signer = render.create_tr_signer(soup, message)
        tr_t3.append(tr_signer)
        p3 = soup.new_tag("p")
        td_middle.append(p3)

    return str(table_outer)


message = json.loads(text)
print(render_table_second(message))
