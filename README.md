# Dashfuel Take Home

## Local Development

Setup Python virtual environment:

pyenv virtualenv 3.13.1 dashfuel_takehome
echo 'dashfuel_takehome' > .python-version


Installing `mysqlclient` on Apple Silicon


brew install mysql-client pkg-config
export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
 

Install dependencies:

poetry install


Start MySQL database:

docker compose up db


Apply database migrations:

./manage.py migrate


Start the Django server:

./manage.py runserver


## API Endpoints

### Tanks

The API provides endpoints to manage fuel tanks and their volume measurements.

#### Tank Endpoints

**URL**: `/api/tanks/`

**Methods**:
- `GET` - List all tanks
- `POST` - Create a new tank
- `GET /{id}/` - Retrieve a specific tank
- `PUT /{id}/` - Update a tank
- `DELETE /{id}/` - Delete a tank

**Required Fields**:
- `name`: string (max length 255 characters)

#### Tank Volume Endpoints

**URL**: `/api/tank-volumes/`

**Methods**:
- `GET` - List all tank volume measurements
- `POST` - Create a new volume measurement
- `GET /{id}/` - Retrieve a specific volume measurement
- `PUT /{id}/` - Update a volume measurement
- `DELETE /{id}/` - Delete a volume measurement

**Required Fields**:
- `tank`: integer (foreign key to Tank)
- `volume`: float
- `created_at`: datetime (auto-generated)

### Average Sales

**URL**: `/api/average-sales/`

**Method**: `GET`

**Query Parameters**:
- `date` (required): Date in YYYY-MM-DD format
