# CodeGuard – Online Code Plagiarism Detection System

CodeGuard is a full-stack, final-year level project designed to intelligently detect code plagiarism. Unlike basic text-comparisons, CodeGuard uses a combination of Abstract Syntax Trees (AST) and Token Hashing to detect structural similarities, making it robust against variable renaming and code formatting changes.

## 🚀 Features

- **AST-Based Analysis**: Parses Python code into Abstract Syntax Trees, ignoring stylistic choices and focusing strictly on the code's logical structure.
- **Winnowing/K-Gram Hashing**: Generates hashes from tokenized code to detect similarities even if code segments are rearranged.
- **Interactive UI**: A stunning, dark-themed single-page application (SPA) with smooth animations and dynamic result visualization.
- **Multiple Input Methods**: Support for direct copy-pasting via `contenteditable` code boxes, or direct file uploads (`.py`, `.java`, `.cpp`, etc.).
- **Line Highlighting**: Dynamically highlights exactly which lines match between the two files.
- **Secure Processing**: Uploaded files are processed in memory or temporarily stored and immediately deleted after analysis.

---

## 📁 Project Structure

```
CodeGuard/
│
├── frontend/
│   └── index.html         # Full Single-Page UI (HTML, CSS, Vanilla JS)
│
├── backend/
│   ├── app.py             # Flask REST API Server
│   └── similarity.py      # Core AST and Hashing Algorithm Logic
│
├── uploads/               # Temporary directory for secure file handling
│
└── README.md              # Project Documentation
```

---

## ⚙️ Technologies Used

### Frontend
- **HTML5 & CSS3**: For structure and layout, utilizing CSS Grid/Flexbox and glassmorphism design.
- **Vanilla JavaScript (ES6)**: For DOM manipulation, animations (SVG progress bar), and API interaction using the Fetch API.

### Backend
- **Python 3**: Core language.
- **Flask & Flask-CORS**: Lightweight web framework to build the RESTful API and handle cross-origin requests.
- **`ast` Module**: Built-in Python library for parsing Abstract Syntax Trees.
- **`difflib` Module**: Used for sequence matching and extracting matched line indices.

---

## 🛠️ Setup & Execution Instructions

### 1. Start the Backend Server

You need Python installed on your system. Open your terminal or command prompt, navigate to the `backend` directory, and install the required dependencies:

```bash
cd CodeGuard/backend
pip install Flask flask-cors
```

Then, run the Flask application:

```bash
python app.py
```

You should see an output indicating the server is running on `http://localhost:5000`. Keep this terminal window open.

### 2. Open the Frontend UI

Simply navigate to the `frontend` directory and double-click the `index.html` file to open it in your default web browser (e.g., Chrome, Edge).

### 3. Run a Test

1. Scroll down to the **Live Analysis Engine** section.
2. You will see two pre-filled code boxes.
3. Click the **"Check Similarity (API Call)"** button.
4. The frontend will send the code to the Python backend. The backend will parse the AST and Hashes, compute the similarity, and return the exact matching lines.
5. The UI will animate to show the result and highlight the matching lines in red/orange!
6. Try modifying the variable names in the Python code and run it again—CodeGuard will still detect the similarity because the AST structure remains the same!

---

## 🧠 How the Algorithm Works (For Viva/Presentations)

1. **Input Reception**: The Flask API receives either raw strings or uploaded files via a `multipart/form-data` POST request.
2. **AST Normalization**: The `calculate_ast_similarity` function parses Python code into an AST. An `ast.NodeVisitor` walks through the tree and extracts only the structural node types (e.g., `FunctionDef`, `For`, `If`, `Assign`), completely ignoring what the variables are actually named.
3. **K-Gram Hashing**: To support non-Python code (or code that fails to parse due to syntax errors), the `calculate_hash_similarity` tokenizes the string into k-grams (chunks of $k$ tokens) and calculates the intersection over the union (Jaccard similarity).
4. **Combination**: The final similarity score is an average of the structural AST score and the text-based Hash score, providing a highly robust plagiarism metric.
5. **Highlighting**: `difflib.SequenceMatcher` is run line-by-line to extract the exact indices of matching blocks so the frontend can wrap them in `<mark>` tags.
