import requests
from bs4 import BeautifulSoup
import mysql.connector
from sklearn.tree import DecisionTreeRegressor
url = "https://www.scrapethissite.com/pages/simple/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="countries"
)

cursor = conn.cursor()

country = soup.find_all("div", class_="country")

data_list = []

for c in country:
    name = c.find("h3", class_="country-name").text.strip()
    capital = c.find("span", class_="country-capital").text.strip()
    population = c.find("span", class_="country-population").text.strip()
    area = c.find("span", class_="country-area").text.strip()

    population = int(population.replace(",", ""))
    area = float(area)

    data_list.append((name, capital, population, area))

sql = """
INSERT IGNORE INTO country(cname, capital, population, area)
VALUES (%s, %s, %s, %s)
"""

cursor.executemany(sql, data_list)
conn.commit()

cursor.close()
conn.close()

print("✔ اطلاعات کشورها با موفقیت در MySQL ذخیره شد.")


cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="countries"
)

cursor = cnx.cursor()
x = []
y = []
query = "SELECT population, area FROM country"
cursor.execute(query)

for (population, area) in cursor:
    x.append([population])
    y.append(area)
cursor.close()
cnx.close()

clf = DecisionTreeRegressor()
clf.fit(x, y)

new_data = [[10000000]]
answer = clf.predict(new_data)

print("Predicted Area:", answer[0])

cursor.close()
cnx.close()



