from enum import Enum, unique


@unique
class Status(Enum):
    IDLE = 'idle'
    RUNNING = 'running'
    COMPLETE = 'complete'
    FAILED = 'failed'
