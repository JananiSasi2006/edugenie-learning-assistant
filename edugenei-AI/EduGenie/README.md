# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a FastAPI web application with a responsive HTML/CSS/JavaScript frontend. It provides:
- Question answering (`POST /qa`)
- Concept explanations (`POST /explain`)
- Three-question multiple-choice quizzes with answer checking (`POST /quiz`)
- Passage summarization (`POST /summarize`)
- Personalized learning recommendations (`POST /learn/recommendations`)

The application follows the uploaded project document's module structure. It uses Google Gemini through the current `google-genai` SDK. The document names Gemini 1.5 Pro; the default here is configurable as `gemini-2.5-flash` because older model availability may vary by account. The local LaMini explanation model is optional and is not downloaded unless explicitly enabled.

## Requirements
- Python 3.10 or later
- A Google AI Studio API key for live Gemini responses
- VS Code (recommended)

## Setup in VS Code (Windows PowerShell)

1. Extract the project ZIP and open the `EduGenie` folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt terminal and run:
   `.\.venv\Scripts\activate.bat`

4. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env`, then edit `.env` and set your key:

   ```env
   GEMINI_API_KEY=your_actual_key_here
   GEMINI_MODEL=gemini-2.5-flash
   EXPLANATION_PROVIDER=gemini
   ```

   Get a key from Google AI Studio. Never commit `.env` or share your key publicly.

6. Start the app from the project root:

   ```powershell
   uvicorn main:app --reload
   ```

7. Open `http://127.0.0.1:8000` in your browser.
8. API documentation is available at `http://127.0.0.1:8000/docs`.

## macOS / Linux setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add GEMINI_API_KEY
uvicorn main:app --reload
```

## Test the application

- In the web UI, choose each of the five tools and submit a question, concept, passage, or topic.
- Test service health: open `http://127.0.0.1:8000/health`.
- Open `/docs` and try each POST endpoint with a JSON body such as:

  ```json
  {
    "text": "Which is the largest ocean?",
    "level": "Beginner"
  }
  ```

- Quiz endpoint returns a JSON object with exactly three questions, four options each, a zero-based `answer` index, and an explanation. The frontend lets the learner select options and check the score.

## Optional local explanation model

The project document proposes `LaMini-Flan-T5-783M` for local concept explanation. This can require several GB of disk space and additional PyTorch dependencies. Install the optional dependencies:

```bash
pip install transformers torch
```

Then set in `.env`:

```env
EXPLANATION_PROVIDER=local
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The model weights download on first use. For most beginner setups, leave `EXPLANATION_PROVIDER=gemini`.

## Troubleshooting

- `GEMINI_API_KEY is not configured`: check `.env` is in the same folder as `main.py`, the variable is spelled exactly, then restart Uvicorn.
- `ModuleNotFoundError`: activate `.venv` and run `pip install -r requirements.txt`.
- Port 8000 is busy: run `uvicorn main:app --reload --port 8001` and open port 8001.
- Gemini model/API errors: confirm the API key is valid, the selected model is available to your account, and your network/API quota is working.
- Keep `.env` private. Do not put the API key in frontend HTML or JavaScript.
