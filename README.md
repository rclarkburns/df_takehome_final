# Dashfuel Take Home

## Local Development

Setup Python virtual environment:
```shell
pyenv virtualenv 3.13.1 dashfuel_takehome
echo 'dashfuel_takehome' > .python-version
```

Installing `mysqlclient` on Apple Silicon

```shell
brew install mysql-client pkg-config
export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
```

Install dependencies:
```shell
poetry install
```

Start MySQL database:
```shell
docker compose up db
```

Apply database migrations:
```shell
./manage.py migrate
```

Start the Django server:
```shell
./manage.py runserver
```

## API Endpoints

### Tanks

The API provides endpoints to manage fuel tanks and their volume measurements.

#### Tank Endpoints
- `GET /api/tanks/` - List all tanks
- `POST /api/tanks/` - Create a new tank
- `GET /api/tanks/{id}/` - Retrieve a specific tank
- `PUT /api/tanks/{id}/` - Update a tank
- `DELETE /api/tanks/{id}/` - Delete a tank

Required fields:
- `name`: string (max length 255 characters)

#### Tank Volume Endpoints
- `GET /api/tank-volumes/` - List all tank volume measurements
- `POST /api/tank-volumes/` - Create a new volume measurement
- `GET /api/tank-volumes/{id}/` - Retrieve a specific volume measurement
- `PUT /api/tank-volumes/{id}/` - Update a volume measurement
- `DELETE /api/tank-volumes/{id}/` - Delete a volume measurement

Required fields:
- `tank`: integer (foreign key to Tank)
- `volume`: float
- `created_at`: datetime (auto-generated)

### Example Usage

Create a new tank:
POST /api/tanks/
```json
{
    "name": "Tank 1"
}
```
POST /api/tank-volumes/
Record a volume measurement:
```json
{
    "tank": 1,
    "volume": 500.5
}
```
