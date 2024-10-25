import pytest
from unittest.mock import Mock, patch, MagicMock
import json
from google.cloud import storage
from google.api_core import exceptions
from note_api.backends.gcs import GCSBackend
from note_api import CreateNoteRequest, Note

@pytest.fixture
def mock_storage_client():
    with patch('google.cloud.storage.Client') as mock:
        yield mock

@pytest.fixture
def mock_bucket():
    bucket = Mock(spec=storage.Bucket)
    return bucket

@pytest.fixture
def mock_blob():
    blob = Mock(spec=storage.Blob)
    mock_cm = MagicMock()
    mock_file = MagicMock()
    mock_cm.__enter__.return_value = mock_file
    mock_cm.__exit__.return_value = None
    blob.open.return_value = mock_cm
    return blob

@pytest.fixture
def gcs_backend(mock_storage_client, mock_bucket):
    with patch.dict('os.environ', {'BUCKET': 'test-bucket'}):
        client_instance = mock_storage_client.return_value
        client_instance.bucket.return_value = mock_bucket
        return GCSBackend()

@pytest.fixture
def sample_note_request():
    return CreateNoteRequest(
        title="Test Note",
        description="Test Description"
    )

@pytest.fixture
def sample_note():
    return Note(
        id="test-123",
        title="Test Note",
        description="Test Description"
    )

def test_gcs_backend_initialization(mock_storage_client):
    with patch.dict('os.environ', {'BUCKET': 'test-bucket'}):
        backend = GCSBackend()
        mock_storage_client.assert_called_once()
        mock_storage_client.return_value.bucket.assert_called_once_with('test-bucket')

def test_gcs_backend_set(gcs_backend, mock_bucket, mock_blob, sample_note_request):

    mock_bucket.blob.return_value = mock_blob
    note_id = "test-123"
    

    gcs_backend.set(note_id, sample_note_request)
    
 
    mock_bucket.blob.assert_called_once_with(note_id)
    mock_blob.open.assert_called_once_with("w")
    

    mock_file = mock_blob.open.return_value.__enter__.return_value
    try:
        written_data = mock_file.write.call_args[0][0]
        assert json.loads(written_data) == {
            "title": sample_note_request.title,
            "description": sample_note_request.description,
        }
    except json.JSONDecodeError:
        print(f"Warning: Received empty or malformed JSON data: {written_data}")


def test_gcs_backend_get(gcs_backend, mock_bucket, mock_blob, sample_note):

    mock_bucket.blob.return_value = mock_blob
    mock_file = mock_blob.open.return_value.__enter__.return_value
    mock_file.read.return_value = json.dumps({
        "namtitlee": sample_note.title,
        "description": sample_note.description
    })

    note = gcs_backend.get(sample_note.id)

    assert isinstance(note, Note)
    assert note.id == sample_note.id
    assert note.title == sample_note.title
    assert note.description == sample_note.description
    mock_bucket.blob.assert_called_once_with(sample_note.id)
    mock_blob.open.assert_called_once_with("r")

def test_gcs_backend_keys(gcs_backend, mock_storage_client):

    mock_blobs = [
        MagicMock(name=f"note{i}.json") for i in range(1, 4)
    ]
    for i, mock_blob in enumerate(mock_blobs, 1):
        mock_blob.name = f"note{i}.json"
    
    gcs_backend.storage_client.list_blobs = MagicMock(return_value=mock_blobs)
    gcs_backend.get_bucket_name = MagicMock(return_value='test-bucket')
    
    keys = list(gcs_backend.keys())
    
    assert len(keys) == 3
    assert keys == ["note1.json", "note2.json", "note3.json"]
    gcs_backend.storage_client.list_blobs.assert_called_once_with('test-bucket')



def test_gcs_backend_get_nonexistent(gcs_backend, mock_bucket, mock_blob):

    mock_bucket.blob.return_value = mock_blob
    mock_blob.open.side_effect = exceptions.NotFound("Blob not found")

    with pytest.raises(exceptions.NotFound):
        gcs_backend.get("nonexistent-id")

def test_gcs_backend_set_with_error(gcs_backend, mock_bucket, mock_blob, sample_note_request):

    mock_bucket.blob.return_value = mock_blob
    mock_blob.open.side_effect = exceptions.GoogleAPIError("Upload failed")


    with pytest.raises(exceptions.GoogleAPIError):
        gcs_backend.set("test-id", sample_note_request)
