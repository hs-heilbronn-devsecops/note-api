from projen.python import PythonProject

project = PythonProject(
    author_email="nicolas.byl@nexineer.io",
    author_name="Nicolas Byl",
    module_name="note_api",
    name="note-api",
    version="0.1.0",
    github=False,
    deps=[
        'fastapi',
        'google-cloud-storage',
        'redis',
        'uvicorn[standard]'
    ],
    dev_deps=[
        'attrs',
        'projen',
        'pylint',
        'pytest-cov',
        'pytest-xdist',
        'fakeredis[json]'
    ],
)

project.add_git_ignore('.idea')

dev_task = project.add_task('dev')
dev_task.exec('uvicorn note_api.main:app --reload')

project.synth()