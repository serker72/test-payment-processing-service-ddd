from faststream_outbox.fastapi import OutboxRouter

from src.infrastructure.database.models.outbox import dlq_table, outbox_table
from src.infrastructure.database.sessions.engine import engine

outbox_router = OutboxRouter(engine, outbox_table=outbox_table, dlq_table=dlq_table)
