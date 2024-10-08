from projen.python import PythonProject

project = PythonProject(
    author_email="nicolas.byl@nexineer.io",
    author_name="Nicolas Byl",
    module_name="note_api",
    name="note-api",
    version="0.1.0",
)

project.synth()