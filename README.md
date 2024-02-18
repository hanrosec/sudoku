# Sudoku

## Endpointy

- / GET
- /game?diff=\<int\> GET
- /game/leaderboard
- /game/add_to_leaderboard POST
- /auth/login POST
- /auth/register POST

## Foldery

- .venv - środowisko wirtualne Pythona
- .vscode - konfiguracja VScode (można usunąć)
- instance - folder zawierający pliki związane z tą instancją serwisu
- sudoku
  - static - statyczne pliki (można zamienić na CDN)
  - templates - szablony stron
    - auth - szablony stron związanych z autoryzacją
  - test - folder ze skryptami testowymi

## TODO

1. Zrobić ładnego CSSa
2. Przy tworzeniu użytkownika dodać zabezpieczenie przed SQL injection
3. Dodać serwer CDN dla plików statycznych
4. Skonteneryzować projekt?
5. Zrobić konfigurację produkcyjną

## Uruchamianie

1. Za pierwszym uruchomieniem uruchom skrypt setup.bat (./scripts/setup.bat)
2. Aby uruchomić aplikację uruchom skrypt run.bat (./scripts/run.bat)
