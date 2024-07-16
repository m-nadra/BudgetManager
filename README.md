# Budget Manager

This app is a simple Budget Manager. It was written in Python and use Flask to run.
All data are saved in data.db file which is handled by SQLAlchemy and SQLite.

## Installation
Clone the project

```bash
git clone https://github.com/m-nadra/BudgetManager.git
```

Go to the project directory

```bash
cd BudgetManager
```

Create virual environment
```bash
py -m venv .venv
```

Run virual environment
```bash
.venv\Scripts\activate
```

Install external libraries
```bash
pip install -r requirements.txt
```

## Run locally
Run virual environment
```bash
.venv\Scripts\activate
```

Start the app.py file
```bash
python src\app.py
```

## Running Tests
Test are written using pytest and can be find in tests directory.

Run virual environment
```bash
.venv\Scripts\activate
```

Run pytest
```bash
pytest
```

Run pytest with coverage
```bash
pytest --cov
```