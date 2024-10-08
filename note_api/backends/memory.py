from typing import Dict, List

from .backend import Backend
from .. import CreateNoteRequest, Note


class MemoryBackend(Backend):

    def __init__(self):
        self.tasks: Dict[str, Note] = {}

    def keys(self) -> List[str]:
        return self.tasks.keys()

    def get(self, note_id: str) -> Note:
        return self.tasks[note_id]

    def set(self, note_id: str, request: CreateNoteRequest):
        self.tasks[note_id] = Note(
            id=note_id,
            title=request.title,
            description=request.description
        )