import requests
from bs4 import BeautifulSoup
import re
import csv

link = 'https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/'
r1 = requests.get(link)
soup1 = BeautifulSoup(r1.content, 'html.parser')
s1 = soup1.find('section', id='install-packages-in-a-virtual-environment-using-pip-and-venv')
s2 = s1.find_all('section')

# Write to CSV function with headers
def write_to_csv(file_name, data, headers):
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='*')
        writer.writerow(headers)  # Write headers
        writer.writerows(data)

rows = []
for j in s2:
    head = j.find('h2')
    if head:
        head = head.text.replace('#', '').strip()
    else:
        continue

    k = j.find_all('section')

    # If k contains elements
    if k:
        for l in k:
            suh = l.find('h3').text.replace('#', '').strip()
            o1 = l.find_all('div', class_='tab-set docutils container')
            for l in o1:
                s4 = l.text.split('Windows')
                unix = s4[0]
                unix1 = re.sub('\n+', ' | ', unix).replace(' | Unix/macOS | ', '').rstrip(' |')
                if len(s4) > 1:
                    windows = s4[1]
                    windows1 = re.sub('\n+', '|', windows).rstrip('|').lstrip('|')

                row = [head, suh, unix1]
                if len(s4) > 1:
                    row.append(windows1)
                rows.append(row)

    # If k doesn't contain elements
    else:
        suh = ''
        k = j.find_all('div', class_='tab-set docutils container')
        for tab_set in k:
            for p_tag in tab_set.find_all('p'):
                p_tag.extract()
            tab_set = tab_set.text.strip().split('Windows')
            unix = tab_set[0]
            unix1 = re.sub('\n+', ' | ', unix).replace('Unix/macOS | ', '').rstrip(' |')
            if len(tab_set) > 1:
                windows = tab_set[1]
                windows1 = re.sub('\n+', '|', windows).rstrip('|').lstrip('|')

            row = [head, suh, unix1]
            if len(tab_set) > 1:
                row.append(windows1)
            rows.append(row)

# Define headers
headers = ['Headings', 'Sub-Headings', 'Unix/macOS code', 'Windows code']

# Write to CSV with headers
write_to_csv('Assignment_Task1.csv', rows, headers)
