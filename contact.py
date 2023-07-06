import requests
from bs4 import BeautifulSoup
import csv

ipf = open('new_leads0607.csv', 'r')

csv_reader = csv.reader(ipf)

cookies = {
    'ASP.NET_SessionId': 'jlzdftgfgpcaougko3jwiayt',
    '__utma': '185625580.116469391.1684556690.1684556690.1684556690.1',
    '__utmc': '185625580',
    '__utmz': '185625580.1684556690.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'ifShowHistory': 'false',
    '.ASPXANONYMOUS': 'WTm36WCHhMPjl71-8G15pamIKtke73bFm9KCGUWL-a06ghSGMFmGgV6yTaKU1yEpm6mUdHplNMu8EdlMHdDo5qTs8KFVDIYcyChYfG2Lz3y2EjnmogqYqp-KqqeOrC_1OOfH6a7g4tKdPrDH7IKn1w2',
    'Search_SearchOrganisation_gridRtoSearchResults': '100',
    '__utmb': '185625580.13.10.1684556690',
}

headers = {
    'authority': 'training.gov.au',
    'accept': 'text/html, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': 'ASP.NET_SessionId=jlzdftgfgpcaougko3jwiayt; __utma=185625580.116469391.1684556690.1684556690.1684556690.1; __utmc=185625580; __utmz=185625580.1684556690.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ifShowHistory=false; .ASPXANONYMOUS=WTm36WCHhMPjl71-8G15pamIKtke73bFm9KCGUWL-a06ghSGMFmGgV6yTaKU1yEpm6mUdHplNMu8EdlMHdDo5qTs8KFVDIYcyChYfG2Lz3y2EjnmogqYqp-KqqeOrC_1OOfH6a7g4tKdPrDH7IKn1w2; Search_SearchOrganisation_gridRtoSearchResults=100; __utmb=185625580.13.10.1684556690',
    'pragma': 'no-cache',
    'referer': 'https://training.gov.au/Organisation/Details/45892',
    'sec-ch-ua': '"Chromium";v="112", "Not_A Brand";v="24", "Opera GX";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'tabIndex': '2',
}

pairs = []
cnt = 0
for row in csv_reader:
    if cnt >= 0:
        try:
            id = row[0]
            url = row[1]
            if len(row) == 3:
                website = row[2]
            else:
                website = ''

            response = requests.get(
                f'https://training.gov.au/Organisation/AjaxDetailsLoadContacts/{id}',
                params=params,
                cookies=cookies,
                headers=headers,
            )

            soup = BeautifulSoup(response.text, 'lxml')
            outers = soup.findAll('div', class_="outer")
            for outer in outers:
                h2 = outer.find('h2', class_="legend").text.strip()

                headings = outer.findAll('div', class_="display-label")
                headingsText = [x.text.strip() for x in headings]

                details = outer.findAll('div', class_="display-field-no-width")
                detailsText = [x.text.strip() for x in details]

                pairs.append((['Legend', 'Url', 'Website'] + headingsText, [h2, url, website] + detailsText))
                print(cnt)
        except Exception as e:
            print(e)
    cnt += 1

# Combine all the headings into a single list and extract the unique headings
all_headings = list(set().union(*[pair[0] for pair in pairs]))

# Create a dictionary with unique headings as keys and empty lists as values
data_dict = {heading: [] for heading in all_headings}

# Populate the dictionary with values for each heading
for pair in pairs:
    headings, values = pair
    for heading in all_headings:
        if heading in headings:
            data_dict[heading].append(values[headings.index(heading)])
        else:
            data_dict[heading].append('')

# Convert the dictionary into a CSV file
csv_file = '0607_contacts.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)

    # Write the headings row
    writer.writerow(all_headings)

    # Write the values rows by iterating over the dictionary values
    num_rows = max(len(data_dict[heading]) for heading in all_headings)
    for i in range(num_rows): 
        try:
            writer.writerow([data_dict[heading][i] for heading in all_headings])
        except Exception as e:
            print(e)
ipf.close()