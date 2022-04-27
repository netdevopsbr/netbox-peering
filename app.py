import requests
import re
import sys

url = 'https://ix.br/particip/sp'
img_url = '<img src="https://old.ix.br/images/ok.gif">'

control = []


def fetch_data():
    # Fetch data from ix-br and save to file
    try:
        data = requests.get(url)
        return data.text
    except:
        sys.exit(1)


def remove_element(text, elements):
    for element in elements:
        # Removing openning tag
        while re.search(f'<\s*{element}[^>]*>', text):
            text = re.sub(f'<\s*{element}[^>]*>', '', text)

        # Removing closing tag
        while re.search(f'<\/\s*{element}[^>]*>', text):
            text = re.sub(f'<\/\s*{element}[^>]*>', '', text)

    return text


def handle_row(row):
    # Split row content by td tag
    data_list = re.split('<\s*td[^>]*>', row)

    # Control variable
    new_list = []

    # Loop through data_list
    for data in data_list:

        # Remove element tags a and td
        element = remove_element(data, ['a', 'td']).strip()

        # If element has imagem, means that option is True
        if element == img_url:
            element = True

        # If no value was attributed, render element as False
        if element == '':
            element = False

        # Append to control variable
        new_list.append(element)

    # Put all data retrieved from row into a dict
    obj = {
        'asn': new_list[1],
        'nome': new_list[2],
        'atm': {
            'v4': new_list[3],
            'v6': new_list[4]
        },
        'transito': {
            'v4': new_list[5],
            'v6': new_list[6]
        },
        'transporte': {
            'l2': new_list[7],
            'cix': new_list[8]
        },
        'tipo': new_list[9]
    }

    print(obj)
    return obj


def scan_text():

    # Fetch data from https://ix.br/particip/sp
    text = fetch_data()

    # Get inner content of <center> tag
    center_div = re.findall('<center>.*</center>', text)

    if len(center_div) != 1:
        return

    center_div = center_div[0]

    # Get all tables from center_div and select the one that has actual data
    tables = center_div.split('</table>')
    data = tables[1]

    # Create list separating all table rows
    rows = data.split('</tr>')

    # Remove useless rows
    del rows[0:2]
    del rows[-1]

    # Loop through every of table
    for row in rows:

        # Remove all <tr> and </tr> tags
        row = remove_element(row, ['tr'])

        # Call function that returns dict with values from table row
        json = handle_row(row)

        # Append to control variable
        control.append(json)

    print(control)


scan_text()
