# Music Fun Beats

Music Fun Beats to projekt zaliczeniowy kursu PythonPro.

Aplikacja jest backendem internetowego sklepu muzycznego umożliwiającego
zarządzanie katalogiem albumów, obsługę użytkowników, koszyka i zamówień.

Projekt wykorzystuje REST API, JWT, GraphQL, PostgreSQL, Redis, Celery,
Docker oraz automatyczne testy i CI.

---

## Główne funkcjonalności

- rejestracja i logowanie użytkowników,
- uwierzytelnianie JWT,
- odświeżanie tokenów,
- wylogowanie z blacklistowaniem refresh tokena,
- pobieranie danych zalogowanego użytkownika,
- katalog albumów muzycznych,
- artyści, gatunki, wydawnictwa i formaty muzyczne,
- obsługa stanów magazynowych,
- obsługa edycji limitowanych,
- limity zakupu,
- koszyk użytkownika,
- składanie zamówień,
- zachowanie historycznej ceny i nazwy produktu w zamówieniu,
- generowanie kodu płatności,
- automatyczne zmniejszanie stanu magazynowego,
- walidacja dostępności produktów podczas checkoutu,
- powiadomienia użytkownika,
- Django Signals po rejestracji,
- asynchroniczne zadania Celery,
- cache katalogu albumów w Redis,
- cykliczna kontrola niskiego stanu magazynowego,
- REST API,
- GraphQL API,
- panel Django Admin,
- testy automatyczne,
- GitHub Actions,
- pre-commit.

---

## Technologie

### Backend

- Python
- Django
- Django REST Framework
- Simple JWT
- Strawberry GraphQL

### Baza danych i cache

- PostgreSQL
- Redis

### Zadania asynchroniczne

- Celery
- Celery Beat
- Redis jako broker i backend wyników

### Konteneryzacja

- Docker
- Docker Compose

### Testy i automatyzacja

- pytest
- pytest-django
- pytest-mock
- GitHub Actions
- pre-commit

---

## Architektura projektu

Projekt został podzielony na kilka aplikacji Django:

```text
music-fun-beats
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── celery.py
│
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── signals.py
│
├── products/
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── views.py
│   ├── tasks.py
│   └── graphql_schema.py
│
├── orders/
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── views.py
│   └── tasks.py
│
├── notifications/
│   ├── models.py
│   └── admin.py
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

Logika biznesowa została oddzielona od warstwy API poprzez moduły
`services.py`.

---

## Modele domenowe

### Users

Projekt wykorzystuje własny model użytkownika oparty o Django
`AbstractUser`.

Adres e-mail jest unikalny.

### Products

Katalog muzyczny składa się z modeli:

- `Artist`
- `Genre`
- `Label`
- `MusicFormat`
- `Album`

Album posiada między innymi:

- tytuł,
- artystę,
- gatunki,
- wydawnictwo,
- format,
- rok wydania,
- cenę,
- stan magazynowy,
- informację o aktywności,
- informację o edycji limitowanej,
- opcjonalny limit zakupu.

### Orders

System zamówień wykorzystuje:

- `Cart`
- `CartItem`
- `Order`
- `OrderItem`

Podczas checkoutu cena oraz tytuł albumu są kopiowane do `OrderItem`,
dzięki czemu późniejsza zmiana katalogu produktów nie zmienia historii
złożonego zamówienia.

### Notifications

Model `Notification` przechowuje powiadomienia użytkowników.

Obsługiwane są między innymi:

- powiadomienie powitalne po utworzeniu konta,
- powiadomienie po utworzeniu zamówienia.

---

## Logika biznesowa

Jednym z najważniejszych elementów projektu jest własna logika obsługi
zakupu.

Przed dodaniem albumu do koszyka oraz przed utworzeniem zamówienia
sprawdzane są między innymi:

- poprawność ilości,
- aktywność produktu,
- dostępny stan magazynowy,
- limit zakupu edycji limitowanej.

Checkout wykonywany jest wewnątrz transakcji bazodanowej.

Przy tworzeniu zamówienia:

1. blokowany jest koszyk użytkownika,
2. ponownie sprawdzany jest stan magazynowy,
3. tworzony jest obiekt `Order`,
4. tworzone są pozycje `OrderItem`,
5. zachowywana jest historyczna cena produktu,
6. zmniejszany jest stan magazynowy,
7. obliczana jest całkowita wartość zamówienia,
8. koszyk zostaje wyczyszczony,
9. po zatwierdzeniu transakcji uruchamiane jest zadanie Celery.

Do wysłania zadania Celery wykorzystywany jest:

```python
transaction.on_commit(...)
```

Dzięki temu powiadomienie nie jest wykonywane, jeżeli transakcja
zamówienia zakończy się rollbackiem.

---

## REST API

Bazowy adres aplikacji lokalnej:

```text
http://127.0.0.1:8000/
```

### Users

| Metoda | Endpoint | Opis |
|---|---|---|
| POST | `/api/users/register/` | rejestracja |
| POST | `/api/users/login/` | uzyskanie tokenów JWT |
| POST | `/api/users/token/refresh/` | odświeżenie access tokena |
| POST | `/api/users/logout/` | wylogowanie |
| GET | `/api/users/me/` | dane zalogowanego użytkownika |

### Products

Albumy są dostępne pod:

```text
/api/products/albums/
```

Pojedynczy album:

```text
/api/products/albums/<id>/
```

### Cart i Orders

| Metoda | Endpoint | Opis |
|---|---|---|
| GET | `/api/orders/cart/` | pobranie koszyka |
| POST | `/api/orders/cart/items/` | dodanie albumu do koszyka |
| POST | `/api/orders/checkout/` | utworzenie zamówienia |
| GET | `/api/orders/` | lista zamówień użytkownika |
| GET | `/api/orders/<id>/` | szczegóły zamówienia |

Endpointy wymagające autoryzacji korzystają z tokena JWT:

```text
Authorization: Bearer <access_token>
```

---

## GraphQL

Projekt posiada również API GraphQL przygotowane przy użyciu Strawberry.

Endpoint:

```text
/graphql/
```

GraphQL umożliwia pobieranie danych katalogu albumów.

---

## Django Admin

Panel administracyjny znajduje się pod adresem:

```text
/admin/
```

Panel umożliwia zarządzanie między innymi:

- użytkownikami,
- albumami,
- artystami,
- gatunkami,
- wydawnictwami,
- formatami muzycznymi,
- koszykami,
- zamówieniami,
- pozycjami zamówień,
- powiadomieniami.

Panel wykorzystuje wyszukiwanie, filtry, pola autocomplete, widoki inline
oraz pola tylko do odczytu.

---

## Redis

Redis pełni kilka niezależnych funkcji.

```text
Redis DB 0 -> Celery broker
Redis DB 1 -> Django cache
Redis DB 2 -> Celery result backend
```

Lista albumów jest cache'owana, aby ograniczyć liczbę zapytań do bazy
danych.

---

## Celery

Projekt posiada dwa osobne workery Celery.

### Orders worker

Obsługuje kolejkę:

```text
orders
```

Przeznaczony jest między innymi do zadań związanych z zamówieniami i
kontrolą magazynu.

### Notifications worker

Obsługuje kolejkę:

```text
notifications
```

Przetwarza zadania związane z powiadomieniami.

### Celery Beat

Celery Beat cyklicznie uruchamia zadanie kontrolujące niski stan
magazynowy.

Architektura:

```text
                    Redis
                      │
          ┌───────────┴───────────┐
          │                       │
     queue: orders       queue: notifications
          │                       │
  celery_orders          celery_notifications
          │
     Celery Beat
```

---

## Django Signals

Po utworzeniu nowego użytkownika wykonywany jest sygnał Django
`post_save`.

Signal automatycznie tworzy powitalne powiadomienie.

Schemat:

```text
User.objects.create(...)
        │
        ▼
post_save
        │
        ▼
users.signals
        │
        ▼
Notification
```

---

## Uruchomienie lokalne

### 1. Utworzenie środowiska wirtualnego

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalacja zależności

```powershell
python -m pip install -r requirements.txt
```

### 3. Konfiguracja środowiska

Na podstawie przykładowego pliku:

```powershell
Copy-Item .env.example .env
```

Należy uzupełnić własne wartości zmiennych środowiskowych.

Pliku `.env` zawierającego dane lokalne i sekrety nie należy commitować
do repozytorium.

### 4. Migracje

```powershell
python manage.py migrate
```

### 5. Uruchomienie serwera

```powershell
python manage.py runserver
```

Aplikacja będzie dostępna pod:

```text
http://127.0.0.1:8000/
```

---

## Uruchomienie przez Docker Compose

Projekt można uruchomić razem z PostgreSQL, Redis i Celery:

```powershell
docker compose up --build
```

Docker Compose uruchamia:

```text
db
redis
web
celery_orders
celery_notifications
celery_beat
```

Aplikacja dostępna jest pod:

```text
http://127.0.0.1:8000/
```

Sprawdzenie kontenerów:

```powershell
docker compose ps
```

Zatrzymanie środowiska:

```powershell
docker compose down
```

Usunięcie również wolumenu PostgreSQL:

```powershell
docker compose down -v
```

---

## PostgreSQL

W środowisku Docker aplikacja korzysta z PostgreSQL 16.

Kontener bazy posiada healthcheck, dzięki czemu serwer Django uruchamia
się dopiero po uzyskaniu gotowości bazy danych.

Dane PostgreSQL przechowywane są w wolumenie:

```text
postgres_data
```

---

## Testy

Projekt wykorzystuje `pytest`.

Uruchomienie:

```powershell
python -m pytest -q
```

Aktualny zestaw:

```text
20 passed
```

Testowane są między innymi:

- serializery,
- REST API,
- dodawanie produktów do koszyka,
- walidacja stanów magazynowych,
- limity edycji limitowanych,
- checkout,
- zachowanie historycznej ceny,
- GraphQL,
- Redis cache,
- zadania Celery,
- Django Signals,
- tworzenie powiadomień,
- zabezpieczenie przed duplikacją powiadomień,
- planowanie taska Celery po commit transakcji.

---

## Mockowanie

Projekt wykorzystuje `pytest-mock`.

Przykładem jest test planowania zadania Celery, w którym wywołanie:

```python
send_order_notification.delay(...)
```

jest zastępowane mockiem.

Dzięki temu test może sprawdzić integrację aplikacji z Celery bez
uruchamiania prawdziwego workera.

---

## GitHub Actions

Repozytorium posiada workflow CI uruchamiany dla zmian związanych z
gałęziami:

```text
main
develop
```

Workflow wykonuje między innymi:

```text
instalacja zależności
        ↓
python manage.py check
        ↓
pytest
```

Pull Request może zostać zweryfikowany automatycznie przed scaleniem.

---

## Pre-commit

Projekt wykorzystuje również `pre-commit`.

Przed lokalnym commitem uruchamiane są testy:

```powershell
pre-commit run --all-files
```

Pozwala to wykrywać błędy przed wysłaniem kodu do repozytorium.

---

## Git workflow

W projekcie wykorzystywane są gałęzie:

```text
main
develop
feature/*
```

Schemat pracy:

```text
feature/*
    ↓
develop
    ↓
main
```

Zmiany są integrowane poprzez Pull Requesty.

---

## Bezpieczeństwo

Projekt wykorzystuje JWT do uwierzytelniania użytkowników.

Poufne ustawienia aplikacji są przechowywane w zmiennych środowiskowych,
a lokalny plik `.env` nie jest przechowywany w repozytorium.

---

## Status projektu

Projekt obejmuje aktualnie:

- REST API,
- JWT,
- własną logikę biznesową,
- PostgreSQL,
- Redis,
- cache,
- Celery,
- dwie kolejki Celery,
- dwóch workerów,
- Celery Beat,
- Django Signals,
- system powiadomień,
- GraphQL,
- Docker i Docker Compose,
- panel Django Admin,
- pytest,
- pytest-mock,
- GitHub Actions,
- pre-commit.

---

## Autor

Bartosz Wypych

Projekt zaliczeniowy kursu PythonPro.