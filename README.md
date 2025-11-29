# TutorMate: AI Teacher Assistant

**TutorMate** is a multi-agent educational intelligence system designed to help underperforming students by diagnosing their weak concepts, generating personalized practice, scheduling revision sessions, and tracking long-term progress.

Built with **Google Vertex AI** and **Gemini**.

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents for diagnosis, practice generation, explanation, and tracking.
- **Deep Diagnosis**: Goes beyond right/wrong to identify *why* a student missed a concept.
- **Personalized Practice**: Generates new questions tailored to specific weaknesses.
- **Long-term Memory**: Tracks student mastery over time using a persistent Memory Bank.
- **Teacher Summaries**: Generates human-readable reports for educators.

## 📂 Repository Structure

```
TutorMate/
│
├── agents/                 # AI Agents
│   ├── ingest_agent.py     # Data ingestion
│   ├── diagnostic_agent.py # Gemini-powered diagnosis
│   ├── practice_agent.py   # Practice generation
│   ├── explanation_agent.py# Concept explanation
│   ├── quiz_runner.py      # Grading logic
│   ├── progress_tracker.py # Mastery tracking
│   ├── scheduler_agent.py  # Spaced repetition scheduler
│   └── teacher_summary_agent.py # Report generation
│
├── tools/                  # Helper Tools
│   ├── memory_bank.py      # SQLite database interface
│   ├── math_solver.py      # SymPy math validation
│   ├── content_retriever.py# Search tool (placeholder)
│   └── notification.py     # Notification tool
│
├── prompts/                # LLM Prompts
├── data/                   # Sample Data
├── notebooks/              # Demo & Evaluation Notebooks
├── run_demo.py             # Main orchestration script
├── deploy.sh               # Deployment script
└── requirements.txt        # Dependencies
```

## 🛠️ Setup & Usage

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set API Key**:
    ```bash
    export GOOGLE_API_KEY="your-gemini-api-key"
    ```

3.  **Run the Demo**:
    ```bash
    python run_demo.py
    ```

4.  **Run Notebooks**:
    Open `notebooks/demo.ipynb` in Jupyter/Colab.

## 🤖 Agent Workflow

1.  **Ingest**: Parses quiz data and student responses.
2.  **Diagnose**: `DiagnosticAgent` identifies weak concepts and misconceptions.
3.  **Explain**: `ExplanationAgent` provides targeted explanations.
4.  **Practice**: `PracticeAgent` generates a new set of questions.
5.  **Track**: `ProgressTracker` updates the `MemoryBank`.
6.  **Schedule**: `SchedulerAgent` plans the next session.
7.  **Report**: `TeacherSummaryAgent` informs the teacher.

## ☁️ Deployment (Vertex AI)

Use the included `deploy.sh` script to containerize and deploy the agents to Google Vertex AI Agent Engine.

```bash
./deploy.sh
```

## 📝 Evaluation

See `notebooks/evaluation.ipynb` for metrics on agent performance and accuracy.
