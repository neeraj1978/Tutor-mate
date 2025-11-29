# TutorMate: AI-Powered Intelligent Tutoring System 🎓🤖

**TutorMate** is a next-generation AI tutoring platform designed to provide personalized, adaptive, and engaging learning experiences. It leverages advanced Large Language Models (Google Gemini) to act as a smart tutor that understands, diagnoses, explains, and quizzes students just like a human teacher would.

![TutorMate Banner](https://via.placeholder.com/1200x400?text=TutorMate+AI+Learning+Platform)

## 🚀 Key Features

*   **🧠 Cognitive Diagnosis:** Automatically identifies a student's weak areas through quiz responses and interaction patterns.
*   **💬 Socratic Chat Agent:** A conversational AI that guides students to answers rather than just giving them away, using Socratic questioning techniques.
*   **📊 Smart Dashboard:** Visualizes learning progress, recent sessions, and performance stats with interactive charts.
*   **🎮 Gamified Learning:** "Daily Challenge" mode with cooldowns and rewards to build a daily learning habit.
*   **📝 Adaptive Practice:** Generates custom practice sets tailored specifically to the student's identified weak concepts.
*   **📈 Progress Tracking:** Monitors improvement over time and generates detailed teacher-style summary reports.

## 🛠️ Technology Stack

### Backend
*   **Framework:** FastAPI (Python) - High-performance, easy-to-use web framework.
*   **AI Engine:** Google Gemini (via `google-generativeai`) - Powers the core intelligence.
*   **Database:** SQLite - Lightweight and efficient for local data storage.
*   **Agents:** Custom-built AI agents for specific tasks (Diagnosis, Explanation, Quiz, Chat).

### Frontend
*   **Framework:** React 19 (Vite) - Fast and modern UI development.
*   **Styling:** Tailwind CSS - Utility-first CSS for rapid and beautiful design.
*   **Animations:** Framer Motion - Smooth and engaging UI transitions.
*   **Charts:** Recharts - Data visualization for the dashboard.
*   **Icons:** Lucide React - Clean and consistent iconography.

## 📂 Project Structure

```
TutorMate/
├── agents/                 # AI Agents logic (Chat, Diagnostic, etc.)
├── tools/                  # Helper tools (Memory, Database, Math Solver)
├── frontend/               # React frontend application
├── data/                   # Data storage
├── api.py                  # Main FastAPI backend entry point
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## ⚡ Getting Started

### Prerequisites
*   Python 3.10+
*   Node.js 18+
*   Google Gemini API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/neeraj1978/Tutor-mate.git
    cd Tutor-mate
    ```

2.  **Backend Setup:**
    ```bash
    # Create virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    # Install dependencies
    pip install -r requirements.txt

    # Set up environment variables
    # Create a .env file and add your GOOGLE_API_KEY
    ```

3.  **Frontend Setup:**
    ```bash
    cd frontend
    npm install
    ```

### Running the Application

1.  **Start Backend:**
    ```bash
    # From root directory
    python api.py
    ```
    Backend runs on `http://localhost:8000`

2.  **Start Frontend:**
    ```bash
    # From frontend directory
    npm run dev
    ```
    Frontend runs on `http://localhost:5173`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.
