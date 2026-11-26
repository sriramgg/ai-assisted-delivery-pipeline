import os, sqlite3
from contextlib import closing
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
app = FastAPI(title='Release Tracker')
class Task(BaseModel):
    title: str = Field(min_length=1,max_length=120)
    done: bool = False

def db():
    conn=sqlite3.connect(os.getenv('DB_PATH','tasks.db'))
    conn.row_factory=sqlite3.Row
    conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL)')
    return conn
@app.get('/health')
def health():
    with closing(db()) as c: c.execute('SELECT 1')
    return {'status':'ok'}
@app.get('/')
def home(): return FileResponse(Path(__file__).with_name('index.html'))
@app.get('/api/tasks')
def list_tasks():
    with closing(db()) as c: return [dict(r) for r in c.execute('SELECT * FROM tasks ORDER BY id')]
@app.post('/api/tasks',status_code=201)
def create(task:Task):
    with closing(db()) as c, c:
        cur=c.execute('INSERT INTO tasks(title,done) VALUES (?,?)',(task.title,task.done))
        return {'id':cur.lastrowid,**task.model_dump()}
@app.put('/api/tasks/{task_id}')
def update(task_id:int,task:Task):
    with closing(db()) as c,c:
        if not c.execute('UPDATE tasks SET title=?,done=? WHERE id=?',(task.title,task.done,task_id)).rowcount: raise HTTPException(404,'Task not found')
        return {'id':task_id,**task.model_dump()}
@app.delete('/api/tasks/{task_id}',status_code=204)
def delete(task_id:int):
    with closing(db()) as c,c:
        if not c.execute('DELETE FROM tasks WHERE id=?',(task_id,)).rowcount: raise HTTPException(404,'Task not found')
