# -*- coding: utf-8 -*-
from os import getenv
from typing import List

from redis import Redis
from .. import Note, CreateNoteRequest
from .backend import Backend


class RedisBackend(Backend):
    def __init__(
            self,
            redis=Redis(host=getenv('REDIS_HOST', 'localhost'),
                        port=6379, decode_responses=True)
    ) -> None:
        self.redis = redis

    def keys(self) -> List[str]:
        return self.redis.keys()

    def get(self, note_id: str) -> Note:
        task = self.redis.json().get(f'tasks:{note_id}')
        return Note(
            id=note_id,
            title=task['title'],
            description=task['description'],
        )

    def set(self, note_id: str, request: CreateNoteRequest):
        self.redis.json().set(f'tasks:{note_id}', '$', {
            'title': request.title,
            'description': request.description,
        })