
---

# Agrimax

Agrimax is a comprehensive Crop Recommendation and Field Management System designed to empower farmers with data-driven decisions for better crop yield and farm management. It integrates soil health analysis, weather forecasting, and crop recommendation to help users make informed agricultural choices.

---
## Features

- **Crop Recommendation:** Suggests the best crops to grow based on soil nutrients, environmental factors, and local weather data.
- **Soil Health Analysis:** Evaluates soil health and provides actionable suggestions to improve fertility and productivity.
- **Weather Forecasting:** Offers real-time weather insights for better planning.
- **Farm Management:** Tracks farm history, crop rotations, and nutrient usage for optimized farming practices.
- **User-Friendly Interface:** A web interface designed for ease of use by farmers.

---
## Technologies Used

- **Frontend:** HTML, CSS, JavaScript (Tailwind CSS for styling)
- **Backend:** Python (Django Framework)
- **Database:** SQLite / PostgreSQL
- **APIs:** Weather API integration for real-time forecasting
- **AI/ML:** Machine learning models for crop recommendation and soil analysis

---
## Dependencies

This project relies on the following Python packages and modules:

- **Core Libraries:**
  - numpy
  - pandas
  - datetime
  - os
  - json
  - pathlib
  - time

- **Data Science and Machine Learning:**
  - sklearn (datasets: make_classification, preprocessing: MinMaxScaler)
  - joblib

- **Visualization:**
  - matplotlib.pyplot
  - seaborn

- **Web Framework and Utilities:**
  - django.conf (settings)

- **Geolocation and Requests:**
  - requests
  - geopy (exc, geocoders: Geocodio, GoogleV3, Nominatim, OpenCage)

- **Custom Modules:**
  - get_coordinates (get_latitude_longitude)

- **Configuration Parsing:**
  - configparser

### Dependency Graph
![dependency-graph](./AgriMax/dep_graph.png)

---
## Installation

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.8 or higher
- pip (Python package installer)
- Node.js (optional, for frontend builds)

### Clone the Repository
```bash
git clone https://github.com/skye-cyber/Agrimax.git
cd Agrimax
```

### Backend Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run database migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup (Optional)
If you're working on the frontend, navigate to the `frontend` folder and install dependencies:
```bash
cd frontend
npm install
```

To build the frontend:
```bash
npm run build
```

---
## Usage
1. Access the application locally at [http://localhost:8000](http://localhost:8000).
2. Register or log in to start using the features.
3. Input soil data, weather parameters, or manage farm details to receive recommendations.

---
## Contributing
We welcome contributions to make Agrimax even better! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Added new feature"
   ```
4. Push to your forked repository:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request in the original repository.

---
## License
This project is licensed under the GNU GPL Version 3. See the LICENSE file for more details. See the [LICENSE](LICENSE) file for details.

---
## Contact
For questions, feedback, or support, feel free to reach out:
- **Email:** [swskye17@gmail.com](mailto:swskye17@gmail.com)
- **GitHub:** [skye-cyber](https://github.com/skye-cyber)

---

Thank you for choosing Agrimax! Together, let's make farming smarter and more efficient.
