# -*- coding: utf-8 -*-
from pydantic import BaseModel


class CreateNoteRequest(BaseModel):
    title: str
    description: str


class Note(CreateNoteRequest):
    id: str