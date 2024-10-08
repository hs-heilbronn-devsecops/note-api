# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from note_api import Note, CreateNoteRequest


class Backend(ABC):

    @abstractmethod
    def keys(self) -> List[str]:
        pass

    @abstractmethod
    def get(self, note_id: str) -> Note:
        pass

    @abstractmethod
    def set(self, note_id: str, request: CreateNoteRequest):
        pass