from note_api.model import CreateNoteRequest, Note
from note_api.backends import MemoryBackend
from note_api.main import create_note, get_note, get_notes


def test_save_and_get_item():
    backend = MemoryBackend()
    id = create_note(CreateNoteRequest(
        title='Test Note',
        description='Demo Note',
    ), backend)
    assert get_note(id, backend) == Note(title='Test Note', description='Demo Note', id=id)


def test_save_and_get_items():
    backend = MemoryBackend()
    create_note(CreateNoteRequest(
        title='Test Note',
        description='Demo Note',
    ), backend)
    create_note(CreateNoteRequest(
        title='Test Note 2',
        description='Demo Note 2',
    ), backend)
    notes = get_notes(backend)
    assert len(notes) == 2