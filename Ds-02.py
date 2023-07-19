import requests
import pandas as pd
import lxml.html as lh
import matplotlib.pyplot as plt
import seaborn as sns

def get_data(urls):
    table = []

    for url in urls:
        page = requests.get(url)
        doc = lh.fromstring(page.content)
        table_row_element = doc.xpath('//tr')

        for i in range(1, 38):
            j = 0
            table_cols = []

            for elem in table_row_element[i]:
                j += 1
                elem_content = elem.text_content()

                if j == 1:
                    table_cols.append(elem_content)

                if j == 2:
                    table_cols.append(int(elem_content.replace(',', '')))
                    table.append(table_cols)
                    break

    df = pd.DataFrame(table, columns=['state', 'active cases','recovered', 'death'])
    return df

urls = ['https://www.mygov.in/covid-19/', 'https://www.ndtv.com/coronavirus/india-covid-19-tracker', 'https://www.mygov.in/corona-data/covid19-statewise-status/']
corona_data = get_data(urls)

# Bar graph
plt.figure(figsize=(12, 6))
sns.barplot(x='state', y='active cases', data=corona_data)
plt.title('Active COVID-19 Cases by State')
plt.xticks(rotation=90)
plt.show()

# Donut graph
labels = ['Active Cases', 'Recovered', 'Deaths']
sizes = [corona_data['active cases'].sum(), corona_data['recovered'].sum(), corona_data['death'].sum()]

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('COVID-19 Overall Distribution')
plt.show()
