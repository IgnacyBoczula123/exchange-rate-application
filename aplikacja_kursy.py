import os
import json
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

CACHE_FILE = 'nbp_rates.json'
API_URL = 'http://api.nbp.pl/api/exchangerates/tables/A?format=json'

class CurrencyConverter:
    """
    Aplikacja GUI do przeliczania walut na podstawie kursów z NBP.
    Aplikacja pobiera najnowsze kursy z internetu i zapisuje je lokalnie,
    aby działać również w trybie offline.
    """
    def __init__(self, master):
        """
        Inicjalizuje obiekt CurrencyConverter.

        - Ustawia tytuł i rozmiar głównego okna.
        - Ładuje kursy walut (online lub z cache).
        - Tworzy wszystkie widżety GUI.

        Args:
            master (tk.Tk): Główne okno aplikacji.
        """
        self.master = master
        self.master.title('Kalkulator kursów walut')
        self.master.geometry('600x300')

        # Wczytywanie kursów walut
        self.rates = self.load_rates()
        self.currencies = ['PLN złoty polski'] + sorted([i['code'] + ' ' + i['currency'] for i in self.rates])

        # Tworzenie interfejsu
        self.create_widgets()

    def load_rates(self):
        """
        Pobiera kursy walut z API NBP lub z pliku cache, jeśli brak dostępu do internetu.

        Returns:
            list: Lista słowników z polami 'code', 'currency', 'mid'.
        """
        try:
            response = requests.get(API_URL, timeout=5)
            response.raise_for_status()
            data = response.json()[0]['rates']

            # Zapis do pliku cache
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f)

            return data
        except Exception:
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                messagebox.showerror('Błąd','Nie można pobrać kursów, a brak pliku cache.')
                self.master.destroy()
                return []

    def create_widgets(self):
        """
        Tworzy i rozmieszcza wszystkie widżety w oknie aplikacji:
        - Etykiety i pola wyboru waluty źródłowej i docelowej
        - Pole do wpisania kwoty
        - Pole do wyświetlenia wyniku
        - Przyciski 'Oblicz' i 'Zakończ'
        """
        # Waluta źródłowa
        tk.Label(
            self.master,
            text='Waluta źródłowa:'
        ).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.src_currency = ttk.Combobox(
            self.master,
            values=self.currencies,
            state='readonly',
            width=40
        )
        self.src_currency.current(0)
        self.src_currency.grid(row=0, column=1, padx=5, pady=5)

        # Waluta docelowa
        tk.Label(
            self.master,
            text='Waluta docelowa:'
        ).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.dst_currency = ttk.Combobox(
            self.master,
            values=self.currencies,
            state='readonly',
            width=40
        )
        self.dst_currency.current(0)
        self.dst_currency.grid(row=1, column=1, padx=5, pady=5)

        # Pole na kwotę
        tk.Label(
            self.master,
            text='Kwota:'
        ).grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.amount_var = tk.StringVar()
        tk.Entry(
            self.master,
            textvariable=self.amount_var
        ).grid(row=2, column=1, padx=5, pady=5)

        # Pole na wynik
        tk.Label(
            self.master,
            text='Wynik:'
        ).grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.result_var = tk.StringVar()
        tk.Entry(
            self.master,
            textvariable=self.result_var,
            state='readonly'
        ).grid(row=3, column=1, padx=5, pady=5)

        # Ramka na przyciski
        btn_frame = tk.Frame(self.master)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(
            btn_frame,
            text='Oblicz',
            command=self.convert
        ).pack(side='left', padx=5)
        tk.Button(
            btn_frame,
            text='Zakończ',
            command=self.master.quit
        ).pack(side='left', padx=5)

    def get_rate(self, code):
        """
        Zwraca kurs średni (mid) dla podanej waluty.

        Args:
            code (str): Ciąg w formacie '<kod> <nazwa waluty>' lub 'PLN złoty polski'.

        Returns:
            float: Kurs waluty w PLN lub None, jeśli nie znaleziono.
        """
        if code == 'PLN złoty polski':
            return 1.0
        for i in self.rates:
            if i['code'] + ' ' + i['currency'] == code:
                return i['mid']
        return None

    def convert(self):
        """
        Przelicza wprowadzoną kwotę z waluty źródłowej na docelową.
        Wynik jest wyświetlany w polu wynikowym lub wyświetlany jest komunikat błędu.
        """
        try:
            source = self.src_currency.get()
            destination = self.dst_currency.get()
            amount_str = self.amount_var.get().strip()
            if not amount_str:
                self.result_var.set('nie podano kwoty')
                return
            #czy to liczba
            try:
                amount = float(amount_str.replace(',', '.'))
            except ValueError:
                self.result_var.set('kwota musi być liczbą')
                return
            if amount <= 0:
                self.result_var.set('kwota musi być dodatnia')
                return
            # Konwersja walut
            rate_src = self.get_rate(source)
            rate_dst = self.get_rate(destination)
            if rate_src is None or rate_dst is None:
                raise ValueError('Nieznany kod waluty')

            # Konwersja: źródłowa -> PLN -> docelowa
            amount_pln = amount * rate_src
            result = amount_pln / rate_dst
            currency_code = destination.split()[0]
            self.result_var.set(f"{result:.4f} {currency_code}")
        except Exception as e:
            messagebox.showerror('Błąd',f'Nieprawidłowe dane: {e}')



root = tk.Tk()
app = CurrencyConverter(root)
root.mainloop()
