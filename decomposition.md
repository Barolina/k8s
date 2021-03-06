### Интернет  магазин шанс-видео.

Суть, есть  интернет магазн, шанс-видео, похоже что-то на поход в театр  на  премьеру, но  онлайн.

### Пользовательский  сценарий:
_____

**Есть** авторизованный  клиент

**И есть** интернет мазазин  "шанс-видео"

**И** клиент вводит в строке  поиска "Маузер"

**Тогда** появляется  список премьер, подходящий под   запрос  пользователя

**И** в  карточке  товара пользователь  видит:

- название  премьеры
- актеры
- описание
- цена  просмотра в театре
- цена просмотра онлайн
- скидка
- время  резервации
_____
**Когда** клиент нажимает на  карточку  товара

**Тогла** клиент переходит на страницу  с описание  премьеры
____
**Когда** клиент нажимает на добавить в  корзину

**Тогда** примьера добавляется в  корзину
____
**Когда** клиент переходит в  корзину

**Тогда** он  видит список всех своих пермьер
____
**Когда** клиент  нажимает кнопку Оформить  заказ

**Тогда** появляется   форма  формления  заказа, где он может  выбрат  время  резервации и срок
____
**Когда** клиент ввел данные  о сроке и времени резервации

**Тогда** появляется  форма  подтверждения списания   средств  со счета

**Или** появляется  форма  пополнения  баланса
_____
**Когда** пользователь подтвердил списание средств  со счета пользователя

**Тогда** примьера  доступна для  просмотра в личном   кабине, в  разделе мои премьеры

**И** приходит  письмо об  успешном приобретении  премьеры  и  описанем срока действаия
_____
**Когда**срок резервации подходит к  концу срока

**Тогда** приходит  письмо-напоминание о  завершении срока резервации
____

###  Общая схема взаимодействия сервисов
![geeral sheme](chancе-premiere.png)


### Cистемные действия

- Клиент  ищет премьеру по  выбранным параметрам
- Клиент получает подроную информацию о  премьере
- Клиент добавлет добавляет премьуре в корзину
- Клиент может отредактировать срок резервации  для просмотра
- Клиент может отредактировать список добавленных премьер в корзине
- Клиент проводит оплату резервации премьеры
- Приложение открывает премьеру для  просмотра в  личном кабинте, после успешной оплаты
- Клиент может изменить срок  резервации после оплаты

### Основные сервисы

- Клиенты
- Премьеры
- Корзина
- Уведомления

### Функциональное моделирование

![func_model_premier](func_model_premier.png)


### Описание  сервисов
____

#### Сервис примьер ( посути   наверное   сервис заказа)

**Название**

премьеры

**Запросы**

- поиск премьеры
  GET /api/v1/search/?q=Маузер
- получить стоимость  аренды  премьеры
  GET /api/v1/rent/:id=&period=
- информация  о  премьере
  GET /api/v1/premiere/:id
- просмотр  срока оставшей резервайии
  GET /api/v1/premiere/:id/term


**Команды**

- добавить преьеру в личный кабинет после успешной  оплаты
  POST /api/v1/rent/  {id: 'идентификатор премьеры', 'period': 12}

**Зависимости**

- очередь SendNotify, для публикации сообщений, отправки уведомлений (  успешной  резервации,  об окончании срока  резервации)   


**Вопросы**

- Что  использовать для поиска премьер (Elastic or  Shinx)? 
- Как   будет  храниться история  премьер,  использовать для   это какую  либо timseriesdb

______

##### Сервис биллинга

**Название**

биллинг

**Запросы**
- просмотр счета
  GET /api/v1/billing/amount/
- пополнить счет
  POST /api/v1/billing/fill {summ: сумма  пополнения}
- проверка  статтуса оплаты
  GET /api/v1/billing/status/:id
  
**Зависимости**

- очередь SendNotify,  для  публикации сообщении, отправки уведомлений ( о пополнении или  списания  средств) 

**Команды**

- списание  средств
  POST /api/v1/billing/withdraw/ {id: идентификатор премьеры,  summ: сумма  списания}

 
**Вопросы**

- Как  хранить историю списания?
- Предусмотруть  возможность отмены резервации, как вернуть  средства на счет?
- Что если клиент решит  изменить срок резервации?
- Как-то  нужно следить за идемпотентностью списания, что  если  списание  произошло, а  ответ  так  и  был  отправлен?

_____

#### Сервис уведомлений

**Название**

уведомление  клиентов об успешном  ( или нет ) выполнении  операций 

**Запросы**

- 

**Зависимости**

-  слушает  очередь  SendNotify, для  отправки уведомлений

**Команды**

- 

**Вопросы**

- Что  если  изменится способ уведомлений, если  к примеру  необходимо уведомлять  пользователя не  по почте, а по cms?

_____

#### Сервис авторизации и идентификации

**Название**

авотризация  и  идентифкация  пользователей, формирование  JWT токены с необходимой   информацией  о пользователе

**Запросы**

- получить   инфомацию  о пользователе
  GET /api/v1/users JWT 
- аутентификация
  POST /api/v1/login {email, password}
- авторизация 
  POST /api/v1/register {email, passowrd, lasta_name, first_name}
- логаут
  POST  /api/v1/logout JWT

**Команды**

- -

**Зависимости**

- очередь SendNotify,  для  публикации сообщении, отправки уведомлений ( о успешной  регистрации) 



