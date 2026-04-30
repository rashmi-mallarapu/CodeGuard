import ast
import difflib

class ASTNormalizer(ast.NodeVisitor):
    def __init__(self):
        self.structure = []
    
    def generic_visit(self, node):
        self.structure.append(type(node).__name__)
        super().generic_visit(node)

def calculate_ast_similarity(code1, code2):
    try:
        tree1 = ast.parse(code1)
        tree2 = ast.parse(code2)
        
        norm1 = ASTNormalizer()
        norm1.visit(tree1)
        
        norm2 = ASTNormalizer()
        norm2.visit(tree2)
        
        sm = difflib.SequenceMatcher(None, norm1.structure, norm2.structure)
        return sm.ratio() * 100
    except SyntaxError:
        # Fallback if not valid Python code (e.g., C++ or Java)
        return calculate_hash_similarity(code1, code2)

def calculate_hash_similarity(code1, code2, k=5):
    """Basic k-gram token hashing to detect structural similarity ignoring formatting"""
    def get_kgrams(text, k):
        words = text.split()
        return set(' '.join(words[i:i+k]) for i in range(len(words) - k + 1))
    
    kgrams1 = get_kgrams(code1, k)
    kgrams2 = get_kgrams(code2, k)
    
    if not kgrams1 or not kgrams2:
        return 0.0
    
    intersection = kgrams1.intersection(kgrams2)
    union = kgrams1.union(kgrams2)
    
    return (len(intersection) / len(union)) * 100 if union else 0.0

def get_matching_lines(code1, code2):
    lines1 = code1.splitlines()
    lines2 = code2.splitlines()
    
    sm = difflib.SequenceMatcher(None, lines1, lines2)
    matches1 = set()
    matches2 = set()
    
    for match in sm.get_matching_blocks():
        if match.size > 0:
            for i in range(match.size):
                # Only highlight lines that actually contain code, ignore blank lines
                if lines1[match.a + i].strip() and lines2[match.b + i].strip(): 
                    matches1.add(match.a + i)
                    matches2.add(match.b + i)
                    
    return list(matches1), list(matches2)

def analyze_similarity(code1, code2):
    ast_sim = calculate_ast_similarity(code1, code2)
    hash_sim = calculate_hash_similarity(code1, code2)
    
    # Combine both methods for robust detection
    final_sim = (ast_sim + hash_sim) / 2
    
    matches1, matches2 = get_matching_lines(code1, code2)
    
    risk = "Low"
    if final_sim > 70:
        risk = "High"
    elif final_sim > 30:
        risk = "Medium"
        
    return {
        "similarity": round(final_sim, 2),
        "risk": risk,
        "matches_file1": matches1,
        "matches_file2": matches2
    }
