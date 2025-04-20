from nicegui import ui
import requests

BACKEND_URL = "http://backend:5000"
session = {}

main_view = ui.column().classes("w-full items-center")

def login():
    username = session.get('username_input').value
    password = session.get('password_input').value
    r = requests.get(f"{BACKEND_URL}/list", auth=(username, password))
    if r.ok:
        session['auth'] = (username, password)
        session['logged_in'] = True
        show_dashboard()
    else:
        ui.notify("Login failed", color='negative')

def show_login():
    main_view.clear()
    with main_view:
        ui.label("Login").classes("text-2xl font-bold")
        session['username_input'] = ui.input('Username').props('outlined')
        session['password_input'] = ui.input('Password', password=True).props('outlined')
        ui.button('Login', on_click=login)

def backup_file():
    file_path = session['backup_input'].value
    r = requests.post(f"{BACKEND_URL}/backup", json={'file_path': file_path}, auth=session['auth'])
    if r.ok:
        ui.notify('Backup successful')
        refresh()
    else:
        ui.notify('Backup failed', color='negative')

def restore_file():
    file_name = session['restore_input'].value
    r = requests.post(f"{BACKEND_URL}/restore", json={'file_name': file_name}, auth=session['auth'])
    if r.ok:
        ui.notify('Restored successfully')
    else:
        ui.notify('Restore failed', color='negative')

def refresh():
    r = requests.get(f"{BACKEND_URL}/list", auth=session['auth'])
    if r.ok:
        session['table'].rows = r.json()

def show_dashboard():
    main_view.clear()
    with main_view:
        ui.label(f"Welcome, {session['auth'][0]}").classes("text-xl font-bold")

        with ui.row():
            session['backup_input'] = ui.input('Path to file').props('outlined')
            ui.button('Backup', on_click=backup_file)

        with ui.row():
            session['restore_input'] = ui.input('File name to restore').props('outlined')
            ui.button('Restore', on_click=restore_file)

        session['table'] = ui.table(columns=[
            {'name': 'file_name', 'label': 'File Name', 'field': 'file_name'},
            {'name': 'timestamp', 'label': 'Timestamp', 'field': 'timestamp'},
        ], rows=[], row_key='file_name')

        ui.button("Refresh List", on_click=refresh)
        refresh()

show_login()
ui.run(host="0.0.0.0", port=8080)
