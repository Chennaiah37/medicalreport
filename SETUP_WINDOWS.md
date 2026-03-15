# How to Run MedReport AI on Windows

## Step 1 — Open the project folder in VS Code
File → Open Folder → select the MedReport folder

## Step 2 — Open terminal in VS Code
Press  Ctrl + `  (backtick key)

## Step 3 — Create virtual environment
```
python -m venv venv
```

## Step 4 — Activate it (REQUIRED every time)
```
venv\Scripts\activate
```
You should see (venv) appear at the start of the line.
If you get a red error about "scripts disabled", run this first:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating again.

## Step 5 — Install packages (first time only)
```
pip install -r requirements.txt
```

## Step 6 — Run the app
```
python -m streamlit run app.py
```

## Every time after that (already installed)
```
venv\Scripts\activate
python -m streamlit run app.py
```

## To stop the app
Press  Ctrl + C  in the terminal
