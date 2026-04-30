from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from similarity import analyze_similarity

app = Flask(__name__)
# Enable CORS so the frontend running on a different port/file can access this API
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/analyze', methods=['POST'])
def analyze():
    code1 = ""
    code2 = ""

    # Priority 1: Check if text was pasted directly into the form
    if 'code1' in request.form and 'code2' in request.form:
        if request.form['code1'].strip() and request.form['code2'].strip():
            code1 = request.form['code1']
            code2 = request.form['code2']
    
    # Priority 2: Check for uploaded files
    if not code1 and not code2:
        if 'file1' in request.files and 'file2' in request.files:
            file1 = request.files['file1']
            file2 = request.files['file2']
            if file1.filename != '' and file2.filename != '':
                # Save temporarily to demonstrate secure handling
                path1 = os.path.join(UPLOAD_FOLDER, file1.filename)
                path2 = os.path.join(UPLOAD_FOLDER, file2.filename)
                file1.save(path1)
                file2.save(path2)
                
                with open(path1, 'r', encoding='utf-8') as f:
                    code1 = f.read()
                with open(path2, 'r', encoding='utf-8') as f:
                    code2 = f.read()
                    
                # Delete files immediately after reading to avoid permanent storage
                os.remove(path1)
                os.remove(path2)
            
    if not code1.strip() or not code2.strip():
        return jsonify({"error": "Both code inputs or valid files are required."}), 400
        
    try:
        # Run our core similarity algorithms
        result = analyze_similarity(code1, code2)
        return jsonify(result)
    except Exception as e:
        print("Error during analysis:", e)
        return jsonify({"error": "An error occurred during analysis.", "details": str(e)}), 500

if __name__ == '__main__':
    print("CodeGuard Backend starting on http://localhost:5000...")
    app.run(debug=True, port=5000)
