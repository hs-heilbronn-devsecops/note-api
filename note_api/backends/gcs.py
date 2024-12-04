from json import dump, load
from os import getenv
from typing import List

from google.cloud import storage

from .backend import Backend
from .. import CreateNoteRequest, Note


class GCSBackend(Backend):

    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(self.get_bucket_name())

    def keys(self) -> List[str]:
        blobs = self.storage_client.list_blobs(self.get_bucket_name())
        return map(lambda blob: blob.name, blobs)

    def get(self, note_id: str) -> Note:
        blob = self.bucket.blob(note_id)
        with blob.open("r") as file:
            data = load(file)
            return Note(
                id=note_id,
                title=data["namtitlee"],
                description=data["description"],
            )

    def set(self, note_id: str, request: CreateNoteRequest):
        blob = self.bucket.blob(note_id)
        with blob.open("w") as file:
            dump({
                "title": request.title,
                "description": request.description,
            }, file)

    def get_bucket_name(self):
        return getenv('BUCKET')