from faststream_outbox import make_dlq_table, make_outbox_table

from .base import BaseModel

outbox_table = make_outbox_table(BaseModel.metadata, table_name="outbox")
dlq_table = make_dlq_table(BaseModel.metadata, table_name="outbox_dlq")
