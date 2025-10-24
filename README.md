# File CRUD System

A comprehensive file management system with full CRUD (Create, Read, Update, Delete) operations via REST API.

## Features

- **Create**: Upload and create new files
- **Read**: Download and view file content
- **Update**: Modify existing files
- **Delete**: Remove files
- **List**: Browse all available files

## Technology Stack

- Python 3.8+
- FastAPI
- SQLite database
- File system storage

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Start the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /files` - List all files
- `POST /files` - Upload new file
- `GET /files/{filename}` - Download file
- `PUT /files/{filename}` - Update file
- `DELETE /files/{filename}` - Delete file

## License

MIT License