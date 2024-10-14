from fakeredis import FakeStrictRedis

from note_api.model import CreateNoteRequest, Note
from note_api.backends import RedisBackend
from note_api.main import create_note, get_note, get_notes

def test_save_and_get_item():
    redis = FakeStrictRedis()
    backend = RedisBackend(redis)
    id = 'test12345'
    backend.set(id, CreateNoteRequest(
        title='Test Note',
        description='Demo Note',
    ))
    assert backend.get(id) == Note(title='Test Note', description='Demo Note', id=id)


def test_save_and_get_items():
    redis = FakeStrictRedis()
    backend = RedisBackend(redis)
    create_note(CreateNoteRequest(
        title='Test Note',
        description='Demo Note',
    ), backend)
    create_note(CreateNoteRequest(
        title='Test Note 2',
        description='Demo Note 2',
    ), backend)
    keys = backend.keys()
    assert len(keys) == 2