# Kalkulator Kursów Walut

## Autor

**Ignacy Boczula**

## Opis
Prosty projekt aplikacji napisany w pythonie. Pozwala przeliczanie kwot pomiędzy różnymi walutami na podstawie kursów średnich udostępnianych przez Narodowy Bank Polski, które są na bierząco pobierane z API NBP. 

## Technologie
- `Python 3.x`
- biblioteka `requests` - do wykonywania zapytań HTTP do API NBP
- Moduł `json` - do parsowania i serializacji danych kursów
- Moduł `os` - do obsługi pliku cache
- `tkinter` i `tkinter.ttk` - do budowy interfejsu graficznego (GUI)

## Uruchomienie

1. Sklonuj repozytorium:
   
    ```sh
    git clone <adres repozytorium>
    cd <nazwa repozytorium>
    ```

2. Zainstaluj dependencje
    ```
    pip install -r requirements.txt
    ```

3. Uruchom grę
    ```
    python aplikacja_kursy.py
    ```
Po uruchomieniu aplikacja otworzy okno, w którym możesz:
-Wybrać walutę źródłową i docelową z listy
-Wpisać kwotę do przeliczenia
-Kliknąć przycisk `Oblicz`, aby zobaczyć wynik w wybranej walucie
-Kliknąć przycisk `Zakończ`, aby zamknąć aplikację
