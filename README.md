# My Little Farma - SPA Setup

This is a Single Page Application (SPA) for pharmacy inventory management.

## Architecture

### Backend (Python/Flask)
- **Location**: `/backend/`
- **Main API**: `/backend/endpoints/app.py`
- **Database Scripts**: `/backend/scripts/database_manager.py`
- **Database**: SQLite database at `/backend/databases/inventory.db`

### Frontend (HTML/CSS/JavaScript)
- **Location**: `/frontend/`
- **Main Entry**: `/frontend/index.html`
- **Styles**: `/frontend/styles/main.css`
- **JavaScript**: 
  - `/frontend/js/router.js` - SPA routing
  - `/frontend/js/api.js` - API communication
  - `/frontend/js/app.js` - Main application logic
  - Individual page scripts in respective folders

## Running the Application

### Prerequisites
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Install Node.js dependencies
npm install
```

### Starting the Backend
```bash
python3 backend/endpoints/app.py
```
The API will be available at `http://localhost:5000`

### Starting the Frontend
```bash
npm run dev
```
The frontend will be available at `http://localhost:3000`

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/inventory` - Get all inventory items
- `POST /api/inventory` - Add new inventory item

## Features

- ✅ SPA routing with hash-based navigation
- ✅ REST API with Flask and CORS support
- ✅ SQLite database with inventory and users tables
- ✅ Responsive UI with modern CSS
- ✅ JavaScript API client for backend communication
- ✅ Home page with inventory management
- ✅ Login and signup pages (frontend only - auth endpoints to be implemented)

## Development

The application uses Vite as the frontend build tool and Flask as the backend framework. The frontend communicates with the backend via REST API calls.

To add new features:
1. Add API endpoints in `backend/endpoints/app.py`
2. Update database schema in `backend/scripts/database_manager.py`
3. Add frontend pages by creating new JS files and adding routes in `app.js`