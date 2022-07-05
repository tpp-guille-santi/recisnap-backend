from contextvars import ContextVar

trace_id: ContextVar[str] = ContextVar("global_context", default='no-trace-id')
