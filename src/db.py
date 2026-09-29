import sqlite3
from pathlib import Path
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/"data"/"projects.db"
SCHEMA=ROOT/"database"/"schema.sql"

def conn():
    DB.parent.mkdir(exist_ok=True)
    c=sqlite3.connect(DB)
    c.row_factory=sqlite3.Row
    return c

def init_db():
    with conn() as c:
        c.executescript(SCHEMA.read_text())
        if c.execute("SELECT COUNT(*) FROM projects").fetchone()[0]==0:
            now=datetime.now(timezone.utc).isoformat()
            for i in range(1,11):
                c.execute("INSERT INTO projects(name,budget,status,created_at) VALUES(?,?,?,?)",(f"Demo Project {i}",100000*i,"active",now))
                pid=c.execute("SELECT last_insert_rowid()").fetchone()[0]
                for a in range(1,7):
                    c.execute("INSERT INTO activities(project_id,name,planned_days,progress,risk_signal,delay_days,delayed) VALUES(?,?,?,?,?,?,?)",(pid,f"Activity {a}",10,min(.55+a*.05,1),0,0,0))
            c.commit()

def list_projects():
    with conn() as c:
        return [dict(x) for x in c.execute("SELECT p.*,COALESCE(AVG(a.progress),0) progress,SUM(CASE WHEN a.delayed=1 THEN 1 ELSE 0 END) delayed_activities FROM projects p LEFT JOIN activities a ON a.project_id=p.id GROUP BY p.id ORDER BY p.id").fetchall()]

def create_project(name,budget):
    with conn() as c:
        cur=c.execute("INSERT INTO projects(name,budget,status,created_at) VALUES(?,?,?,?)",(name,budget,"active",datetime.now(timezone.utc).isoformat()))
        c.commit()
        return cur.lastrowid

def create_activity(pid,name,planned_days,progress,risk_signal):
    with conn() as c:
        cur=c.execute("INSERT INTO activities(project_id,name,planned_days,progress,risk_signal,delay_days,delayed) VALUES(?,?,?,?,?,?,?)",(pid,name,planned_days,progress,risk_signal,0,0))
        c.commit()
        return cur.lastrowid

def get_activity(aid):
    with conn() as c:
        row=c.execute("SELECT * FROM activities WHERE id=?",(aid,)).fetchone()
        return dict(row) if row else None

def update_progress(aid,progress):
    with conn() as c:
        c.execute("UPDATE activities SET progress=? WHERE id=?",(progress,aid))
        c.commit()
