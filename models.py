from sqlmodel import SQLModel, Field

# --- TASKS MODELS ---
class TaskBase(SQLModel):
    title: str = Field(min_length=2, index=True)
    completed: bool = False

class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: str | None = None
    completed: bool | None = None

# --- USER MODELS (ΝΕΑ ΠΡΟΣΘΗΚΗ) ---
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str # Εδώ αποθηκεύεται ΜΟΝΟ ο κρυπτογραφημένος κωδικός!

class UserCreate(SQLModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=6)

class UserPublic(SQLModel):
    id: int
    username: str