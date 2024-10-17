# WeatherRoute

![Static Badge](https://img.shields.io/badge/Team-4-red)
  
WeatherRoute is a web-based application that predicts weather conditions along a travel route and offers real-time adjustments. Users input starting and ending points, and the application provides weather forecasts for each segment of their journey, recommending reroutes to avoid adverse weather. It can also suggest optimal departure times.

**Primary Audience**: Travelers and commuters who need to plan trips based on dynamic weather conditions.

**Problem Solved**: WeatherRoute helps users navigate safely by providing accurate, location-based forecasts and rerouting options to avoid severe weather, improving travel safety and efficiency.

**Technical Architecture**:
The application is a web app using JavaScript for the frontend, Python for backend logic, and integrates with weather and routing APIs. A cloud-based database manages user preferences, historical data, and route recommendations.

**Branch Naming Conventions**
To maintain clarity and organization in our repository, please follow these branch naming conventions:
 **Feature Branches**: Use `feature/<feature-name>` for new features. 
Example: `feature/user-authentication`  
This helps clearly indicate branches that are being used to develop new features for the application.

**Folder Structure**(CLICK EDIT FILE TO OPEN THIS IN THE FORMAT EASIER TO VIEW, MAKE SURE TO NOT COMMIT ANY CHANGES)
weather-map-app/
├── .git/                   # Git version control files
├── docs/                   # Documentation (if needed)
├── src/                    # Source code
│   ├── components/         # UI components for the frontend
│   ├── pages/              # Page components for different views
│   ├── services/           # API calls and backend services
│   ├── utils/              # Utility functions and helpers
│   ├── styles/             # CSS/SCSS files for styling
│   ├── main.py             # Main backend application file
├── public/                 # Public assets (like images and icons)
├── tests/                  # Test cases for both frontend and backend
├── .gitignore              # Files and folders to ignore in Git
├── README.md               # Project overview and instructions
└── requirements.txt        # Python dependencies for the backend
