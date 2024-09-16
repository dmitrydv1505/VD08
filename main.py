# импортируем Flask и библиотеку Request
from flask import Flask, render_template, request, flash
import requests

# импортируем объект класса Flask
app = Flask(__name__)
# Необходим для использования flash сообщений
app.secret_key = 'your_secret_key_here'

# формируем путь и методы GET и POST
@app.route('/', methods=['GET', 'POST'])
# создаем функцию с переменной weather, где мы будем сохранять погоду
def index():
    weather = None
    news = None
    quote = None
    # формируем условия для проверки метода.
    # Форму мы пока не создавали, но нам из неё необходимо будет взять только город.
    if request.method == 'POST':
        # этот определенный город мы будем брать для запроса API
        city = request.form['city']
        # прописываем переменную, куда будет сохраняться результат и функцию weather с указанием города, который берем из формы
        weather = get_weather(city)
        news = get_news()
        quote = get_random_quote()
        # передаем информацию о погоде в index.html
    return render_template('index.html', weather=weather, news=news, quote=quote)

# в функции прописываем город, который мы будем вводить в форме
def get_weather(city):
    api_key = '96bb7245436072e41aa25ce4ad8b2296'
    # адрес, по которомы мы будем отправлять запрос. Не забываем указывать f строку.
    url = url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=30) # verify=False
        response.raise_for_status()  # Проверка на HTTP ошибки
        return response.json()
    except requests.exceptions.RequestException as e:
        flash(f"Ошибка при получении данных о погоде: {e}")
        return None

def get_news():
    api_key = '7a0245e24878485abc78dfa65dabae5a'
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    try:
        response = requests.get(url, timeout=30) #verify=False
        response.raise_for_status()
        return response.json().get('articles', [])
    except requests.exceptions.RequestException as e:
        flash(f"Ошибка при получении новостей: {e}")
        return []

def get_random_quote():
    url = "https://api.quotable.io/random"
    try:
        response = requests.get(url, timeout=30) # verify=False
        response.raise_for_status()
        return response.json().get('content', 'No quote available')
    except requests.exceptions.RequestException as e:
        flash(f"Ошибка при получении цитаты: {e}")
        return 'No quote available'

if __name__ == '__main__':
    app.run(debug=True)