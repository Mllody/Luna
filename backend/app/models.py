from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base



# --- 1. UŻYTKOWNICY ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    role = Column(String(20), default="operator")  # "admin" lub "operator"
    created_at = Column(DateTime, default=datetime.utcnow)

    executions = relationship("Execution", back_populates="user")


# --- 2. ZADANIA (pojedyncze skrypty) ---
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)  # python / vbs / bat
    path = Column(String(300), nullable=False)
    parameters = Column(Text, nullable=True)
    enabled = Column(Boolean, default=True)
    owner = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    executions = relationship("Execution", back_populates="task")


# --- 3. PROCESY (graficzne połączenia zadań) ---
class Process(Base):
    __tablename__ = "processes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    graph_json = Column(Text, nullable=True)  # zapis połączeń z React Flow
    version = Column(String(20), default="1.0")
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# --- 4. KOLEJKA ZADAŃ ---
class Queue(Base):
    __tablename__ = "queue"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    process_id = Column(Integer, ForeignKey("processes.id"), nullable=True)
    requested_by = Column(String(50), nullable=False)
    status = Column(String(20), default="WAITING")  # WAITING / RUNNING / OK / ERROR
    priority = Column(Integer, default=3)
    payload_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    log_path = Column(String(300), nullable=True)


# --- 5. HISTORIA WYKONAŃ ---
class Execution(Base):
    __tablename__ = "executions"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(20), default="OK")  # OK / ERROR
    duration_ms = Column(Integer, nullable=True)
    log_path = Column(String(300), nullable=True)
    triggered_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="executions")
    user = relationship("User", back_populates="executions")
