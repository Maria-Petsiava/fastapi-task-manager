from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from models import Task, TaskCreate, TaskUpdate
from security import get_current_user
from models import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# CREATE (POST /tasks/)
@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, session: Session = Depends(get_session)):
    # Μετατρέπουμε το TaskCreate σε πίνακα Task
    db_task = Task.model_validate(task_data)
    session.add(db_task)      # Προσθήκη στη βάση
    session.commit()          # Αποθήκευση (Save)
    session.refresh(db_task)  # Ανανέωση για να πάρουμε το νέο ID που έδωσε η βάση
    return db_task

# READ ALL (GET /tasks/)
@router.get("/", response_model=list[Task])
def get_all_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return tasks

# READ ONE (GET /tasks/{task_id})
@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Η εργασία δεν βρέθηκε.")
    return task

# UPDATE (PUT /tasks/{task_id})
@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskUpdate, session: Session = Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Η εργασία δεν βρέθηκε.")
    
    # Ενημερώνουμε μόνο τα πεδία που έστειλε ο χρήστης
    hero_data = task_data.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(hero_data)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

# DELETE (DELETE /tasks/{task_id})
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user) # <--- ΚΛΕΙΔΩΜΕΝΟ!
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Η εργασία δεν βρέθηκε.")
    session.delete(task)
    session.commit()
    return