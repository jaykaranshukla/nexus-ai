# ✨ Nexus AI

A full-stack **Retrieval-Augmented Generation (RAG)** chatbot that answers questions strictly from your uploaded documents. Built with a **React 19 + Vite** frontend and a **FastAPI** backend, powered by **Google Gemini**, **LangChain**, and **ChromaDB Cloud**.

🔗 **Live Demo:** [frontend-bay-three-11.vercel.app](https://frontend-bay-three-11.vercel.app/)
🔗 **Backend API:** [nexus-ai-8xeo.onrender.com](https://nexus-ai-8xeo.onrender.com)

---

## 🧠 How It Works

1. **Upload** a PDF document via the API
2. The document is **split into chunks** and **embedded** using Google's Gemini embedding model
3. Embeddings are **stored in ChromaDB Cloud** (persistent vector database)
4. When you ask a question, the system **retrieves the most relevant chunks** via similarity search
5. **Google Gemini** generates an answer strictly based on the retrieved context

---

## 📁 Project Structure

```
chatbot-main/
├── backend/                  # FastAPI + LangChain RAG pipeline
│   ├── core_logic.py         # Ingestion, retrieval & generation logic
│   ├── main.py               # FastAPI server, CORS & API endpoints
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # API keys (not committed)
└── frontend/                 # React + Vite chat interface
    ├── src/
    │   ├── Components/       # Navbar, Body, Footer
    │   ├── App.jsx           # Main app, API integration
    │   └── main.jsx          # React entry point
    ├── index.html
    ├── vite.config.js
    └── package.json
```

---

## 🛠️ Tech Stack

| Layer            | Technology                              | Version  |
|------------------|------------------------------------------|----------|
| Frontend         | React                                   | v19      |
| Build Tool       | Vite                                    | v7       |
| Styling          | Tailwind CSS                            | v4       |
| Backend          | FastAPI                                 | v0.111   |
| AI Orchestration | LangChain                               | v0.3     |
| LLM              | Google Gemini                           | —        |
| Embeddings       | Google Gemini Embeddings                | —        |
| Vector Database  | ChromaDB Cloud                          | v1.1     |
| Deployment       | Vercel (frontend) + Render (backend)    | —        |

---

## ⚙️ Getting Started

### Prerequisites

- **Node.js** v18 or higher
- **Python** v3.10 or higher
- **Google Gemini API Key** — get one at [aistudio.google.com](https://aistudio.google.com/app/apikey)
- **ChromaDB Cloud account** — get one at [trychroma.com](https://www.trychroma.com/)

---

### 1. Clone the repository

```bash
git clone https://github.com/jaykaranshukla/nexus-ai.git
cd nexus-ai
```

---

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
CHROMA_HOST=api.trychroma.com
CHROMA_API_KEY=your_chromadb_cloud_api_key
CHROMA_TENANT=your_chromadb_tenant_id
CHROMA_DATABASE=your_chromadb_database_name
```

Start the backend server:

```bash
python -m uvicorn main:app --reload
```

Backend runs at `http://127.0.0.1:8000` locally
Interactive API docs at `http://127.0.0.1:8000/docs` locally

---

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

---

### 4. Upload a Document & Chat

1. Go to `https://nexus-ai-8xeo.onrender.com/docs`
2. Use the `/upload` endpoint to upload a PDF
3. Open the [live app](https://frontend-bay-three-11.vercel.app/) and ask questions about your document

---

## 🔌 API Endpoints

| Method | Endpoint  | Description                        |
|--------|-----------|------------------------------------|
| GET    | `/`       | Health check                       |
| POST   | `/chat`   | Send a message, get RAG response   |
| POST   | `/upload` | Upload a PDF to ingest into ChromaDB Cloud |

---

## 🧹 Linting

```bash
cd frontend
npm run lint
```

Uses **ESLint v9 flat config** with `eslint-plugin-react-hooks` and `eslint-plugin-react-refresh`.

---

## 📦 Build for Production

```bash
cd frontend
npm run build
```

Output goes to the `dist/` folder. Preview locally:

```bash
npm run preview
```

---

## 🌐 Deployment

### Frontend — Vercel

1. Push repo to GitHub
2. Import at [vercel.com/new](https://vercel.com/new)
3. Set root directory to `frontend`
4. Deploy — Vercel auto-detects Vite

### Backend — Render

1. Create a new **Web Service** on [render.com](https://render.com)
2. Connect your GitHub repo, set root directory to `backend`
3. Build command: `pip install -r requirements.txt`
4. Start command: `python -m uvicorn main:app --host 0.0.0.0 --port 10000`
5. Add these under **Environment Variables**:
   - `GOOGLE_API_KEY`
   - `CHROMA_HOST`
   - `CHROMA_API_KEY`
   - `CHROMA_TENANT`
   - `CHROMA_DATABASE`
   - `PYTHON_VERSION` = `3.11.9`

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push and open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
