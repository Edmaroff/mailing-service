<img src="https://img.shields.io/badge/python-3.12-blue" alt="Python version"/> <img src="https://img.shields.io/badge/django-5.1-blue" alt="Django Version"/> <img src="https://img.shields.io/badge/Django%20REST%20framework-3.15-blue" alt="Django REST Framework Version"/>
<h1>Mailing Service</h1>

<h2>Описание</h2>
<p>
Mailing Service — это API для управления рассылками сообщений. Проект позволяет создавать рассылки, 
фильтровать клиентов по заданным критериям и отправлять сообщения 
выбранным пользователям. После создания рассылки система проверяет, наступило ли время запуска рассылки, если да, то сообщения отправляются клиентам автоматически. 
Если запуск запланирован на будущее, отправка сообщений начнется автоматически в указанное время. 
<p>


<h2>Функциональность</h2>
<ul>
  <li>Создание, просмотр и управление рассылками
  </li>
  <li>Фильтрация клиентов по коду оператора и тегам
  </li>
  <li>Автоматический запуск рассылки по расписанию
  </li>
  <li>Асинхронная отправка сообщений с помощью Celery и Redis
  </li>
  <li>Мониторинг задач через Flower
  </li>
</ul>



<details>
  <summary><h2>Технологии</h2></summary>
    <ul>
      <li>Django</li>
      <li>Django REST framework</li>
      <li>PostgreSQL</li>
      <li>Celery</li>
      <li>Redis</li>
      <li>Flower</li>
    </ul>
</details>

<h2><a href="https://edmaroff-dev.postman.co/workspace/mailing-service~42b42e35-a59e-4ecb-90b1-639ee7e13700/collection/25907870-daf7daf9-7413-486d-bca7-054388310a19?action=share&creator=25907870&active-environment=25907870-8a2f88a9-d11a-40ed-99e8-c1c3a104c28f">API коллекция (Postman)</a></h2>


<h2>Запуск проекта с Docker</h2>


<ol>
  <li>Клонируйте репозиторий:
    <pre><code>git clone https://github.com/Edmaroff/mailing-service</code></pre>
  </li>
  <li>Перейдите в директорию проекта:
    <pre><code>cd mailing-service</code></pre>
  </li>
  <li>Создайте и заполните файл <code>.env</code> по шаблону <code>.env.template</code></li>
  <li>Выполните сборку и запуск контейнеров:
    <pre><code>docker-compose up --build</code></pre>
  </li>
</ol>

<h2>Дополнительная информация</h2>

<ul>
  <li>При первом запуске автоматически создаются тестовые данные (фикстуры) и суперпользователь с логином <code>admin</code> и паролем <code>admin</code> для доступа к административной панели Django.</li>
  <li><strong>Django API</strong> будет доступен по адресу: <a href="http://localhost:8000" target="_blank">http://localhost:8000</a></li>
  <li><strong>Flower</strong> для мониторинга задач Celery будет доступен по адресу: <a href="http://localhost:5555" target="_blank">http://localhost:5555</a></li>
</ul>
