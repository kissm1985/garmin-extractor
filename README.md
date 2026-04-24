# garmin-extractor

Garmin Venu SQ2 adat-exportáló és Google Drive feltöltő eszköz.

## Funkciók

- lekérdezi az elmúlt 30 nap Garmin Connect adatait
- JSON struktúrába normalizálja
- feltölti Google Drive-ba a `Garmin Daily Data/<timestamp>/` almappába
- manuálisan indítható webes felületről
- lokális tesztekkel validálható

## Telepítés

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Google Drive előkészítés

1. Google Cloud Console-ban engedélyezd a Google Drive API-t.
2. Hozz létre Service Accountot.
3. Töltsd le a JSON kulcsot `service_account.json` néven.
4. A Google Drive-ban hozz létre vagy használd a `Garmin Daily Data` mappát.
5. Oszd meg ezt a mappát a Service Account e-mail címével.

## Manuális indítás webes felületről

```bash
python src/app.py
```

Majd nyisd meg:

```text
http://localhost:5000
```

## Parancssoros futtatás

```bash
python src/extractor.py
```

## Tesztelés

```bash
python -m unittest discover -s tests
```

## GitHub Secrets

Ne tegyél fel jelszót vagy service account JSON-t a repóba. Használj `.env` fájlt lokálisan vagy GitHub Secrets-et automatizáláshoz.
