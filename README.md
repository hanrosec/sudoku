# Sudoku

## Endpointy

- / GET
- /game?diff=\<int\> GET
- /game/leaderboard
- /game/add_to_leaderboard POST
- /auth/login POST
- /auth/register POST

## Foldery

- sudoku
  - static - statyczne pliki (można zamienić na CDN)
  - templates - szablony stron
    - auth - szablony stron związanych z autoryzacją

## TODO

- [ ] Zrobić ładnego CSSa
- [x] Przy tworzeniu użytkownika dodać zabezpieczenie przed SQL injection
- [ ] Dodać serwer CDN dla plików statycznych
- [x] Skonteneryzować projekt?
- [ ] Zrobić konfigurację produkcyjną

## Uruchamianie

1. Za pierwszym uruchomieniem uruchom skrypt setup.bat (./scripts/setup.bat)
2. Aby uruchomić aplikację uruchom skrypt run.bat (./scripts/run.bat)
