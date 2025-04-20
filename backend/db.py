import duckdb
import os
import shutil
import bcrypt

DB_PATH = "/data/backup.db"
BACKUP_DIR = "/data/backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

def init_db():
    con = duckdb.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS backups (
            file_name TEXT,
            backup_path TEXT,
            original_path TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT
        )
    """)
    if con.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'").fetchone()[0] == 0:
        password = 'secret'
        hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        con.execute("INSERT INTO users VALUES (?, ?)", ('admin', hash_pw))
    con.close()

def save_backup(file_path):
    file_name = os.path.basename(file_path)
    backup_path = os.path.join(BACKUP_DIR, file_name)
    shutil.copy(file_path, backup_path)
    con = duckdb.connect(DB_PATH)
    con.execute("INSERT INTO backups VALUES (?, ?, ?)", (file_name, backup_path, file_path))
    con.close()

def restore_backup(file_name):
    con = duckdb.connect(DB_PATH)
    result = con.execute(
        "SELECT backup_path, original_path FROM backups WHERE file_name = ? ORDER BY timestamp DESC LIMIT 1",
        (file_name,)
    ).fetchone()
    con.close()
    if result:
        shutil.copy(result[0], result[1])
        return result[1]
    return None

def list_files():
    con = duckdb.connect(DB_PATH)
    results = con.execute("SELECT file_name, timestamp FROM backups ORDER BY timestamp DESC").fetchall()
    con.close()
    return [{"file_name": r[0], "timestamp": r[1]} for r in results]

def verify_user(username, password):
    con = duckdb.connect(DB_PATH)
    result = con.execute("SELECT password_hash FROM users WHERE username = ?", (username,)).fetchone()
    con.close()
    if result:
        return bcrypt.checkpw(password.encode(), result[0].encode())
    return False

def create_user(username, password):
    hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    con = duckdb.connect(DB_PATH)
    con.execute("INSERT INTO users VALUES (?, ?)", (username, hash_pw))
    con.close()
