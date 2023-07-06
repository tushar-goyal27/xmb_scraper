import requests
import csv

f = open('0607_org.csv', 'a', newline='')

csv_writer = csv.writer(f)

cookies = {
    '__utmz': '185625580.1684556690.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'Search_SearchOrganisation_gridRtoSearchResults': '100',
    '.ASPXANONYMOUS': 'WVv-7KCEblsoAq5_DUzT9JAmRFkmI6khLgxCmCLbPOQjHwoRZ09iVjmW_A-uA9o3t_hGn7Kck8ChZsgGvgbeKx5pFLTuPy-qvDdx8YDC7565F0n9R6yUSWB2d3eN0x73CTJzaUAdhLJbTQw53W9kRA2',
    'ASP.NET_SessionId': 'vvj3pwcunwmexhn5naqq2tij',
    '__utma': '185625580.116469391.1684556690.1684641461.1688622152.7',
    '__utmc': '185625580',
    '__utmt': '1',
    'ifShowHistory': 'false',
    '__utmb': '185625580.4.10.1688622152',
}

headers = {
    'authority': 'training.gov.au',
    'accept': 'text/plain, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': '__utmz=185625580.1684556690.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Search_SearchOrganisation_gridRtoSearchResults=100; .ASPXANONYMOUS=WVv-7KCEblsoAq5_DUzT9JAmRFkmI6khLgxCmCLbPOQjHwoRZ09iVjmW_A-uA9o3t_hGn7Kck8ChZsgGvgbeKx5pFLTuPy-qvDdx8YDC7565F0n9R6yUSWB2d3eN0x73CTJzaUAdhLJbTQw53W9kRA2; ASP.NET_SessionId=vvj3pwcunwmexhn5naqq2tij; __utma=185625580.116469391.1684556690.1684641461.1688622152.7; __utmc=185625580; __utmt=1; ifShowHistory=false; __utmb=185625580.4.10.1688622152',
    'origin': 'https://training.gov.au',
    'pragma': 'no-cache',
    'referer': 'https://training.gov.au/Search/SearchOrganisation?Name=&IncludeUnregisteredRtos=false&IncludeNotRtos=false&AdvancedSearch=true&JavaScriptEnabled=true&orgSearchByNameSubmit=Search',
    'sec-ch-ua': '"Opera GX";v="99", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'implicitNrtScope': 'True',
    'includeUnregisteredRtosForScopeSearch': 'True',
    'includeUnregisteredRtos': 'False',
    'includeNotRtos': 'False',
    'orgSearchByNameSubmit': 'Search',
    'AdvancedSearch': 'true',
    'JavaScriptEnabled': 'true',
}

for j in range(1, 42):
    print(j)
    data = {
        'page': f'{j}',
        'size': '100',
        'orderBy': 'LegalPersonName-asc',
        'groupBy': '',
        'filter': '',
    }

    response = requests.post(
        'https://training.gov.au/Search/AjaxGetOrganisations',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )

    res = response.json()
    org_list = res['data']

    for i in org_list:
        org_id = i['OrganisationId']
        code = i['Codes']
        url = 'https://training.gov.au/Organisation/Details/' + code
        if len(i['WebAddresses']):
            website = i['WebAddresses'][0]
        else:
            website = ''
        csv_writer.writerow([org_id, url, website])

f.close()
