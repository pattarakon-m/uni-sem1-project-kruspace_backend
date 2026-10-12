# Requirement & Setup
- python3
- python3's flask
- sqlite3

```sh
python3 -m venv .venv
. ./.venv/bin/activate
pip3 install flask
```

# Run
```sh
python3 main.py
```

## Run with mockup data
```sh
cat sql/*.sql | sqlite3 database.db
cat test/create-teachers.sql | sqlite3 database.db
python3 main.py
```
