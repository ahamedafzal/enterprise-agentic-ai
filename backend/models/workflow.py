import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query        = Column(Text, nullable=False)
    status       = Column(String(20), default="pending")
    created_at   = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    result       = Column(JSONB, nullable=True)
    metadata_    = Column("metadata", JSONB, nullable=True)

class AgentLog(Base):
    __tablename__ = "agent_logs"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_run_id = Column(UUID(as_uuid=True), ForeignKey("workflow_runs.id"))
    agent_name      = Column(String(100))
    action          = Column(Text)
    input           = Column(JSONB)
    output          = Column(JSONB)
    tokens_used     = Column(Integer)
    latency_ms      = Column(Integer)
    created_at      = Column(DateTime, default=datetime.utcnow)

class Document(Base):
    __tablename__ = "documents"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename    = Column(String(255))
    file_type   = Column(String(50))
    chroma_id   = Column(String(255))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    metadata_   = Column("metadata", JSONB, nullable=True)