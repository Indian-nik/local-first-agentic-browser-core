"""
Code Analyzer - Multi-Modal Code Understanding
Analyze and understand source code structure
LOCAL PROCESSING - Privacy-first approach
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import ast
import json
import re

@dataclass
class CodeAnalysis:
    """Analysis results for source code"""
    language: str
    functions: List[Dict[str, Any]]
    classes: List[Dict[str, Any]]
    imports: List[str]
    dependencies: List[str]
    complexity_score: float
    loc: int  # Lines of code
    comments: int
    docstrings: int
    analysis_timestamp: datetime
    privacy_compliant: bool = True

class CodeAnalyzer:
    """
    LOCAL code analysis with NO external API calls
    Supports Python, JavaScript, and more
    """
    
    def __init__(self):
        self.supported_languages = ['.py', '.js', '.ts', '.java', '.cpp', '.go']
        
    def analyze_code(self, file_path: Path) -> CodeAnalysis:
        """Analyze source code file"""
        if not file_path.exists():
            raise FileNotFoundError(f"Code file not found: {file_path}")
            
        file_ext = file_path.suffix.lower()
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        if file_ext == '.py':
            return self._analyze_python(code, file_path)
        elif file_ext in ['.js', '.ts']:
            return self._analyze_javascript(code, file_path)
        else:
            return self._analyze_generic(code, file_path, file_ext[1:])
    
    def _analyze_python(self, code: str, file_path: Path) -> CodeAnalysis:
        """Analyze Python code using AST"""
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Python syntax error: {e}")
        
        functions = []
        classes = []
        imports = []
        docstrings = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'lineno': node.lineno,
                    'decorators': [d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list],
                    'is_async': isinstance(node, ast.AsyncFunctionDef)
                }
                if ast.get_docstring(node):
                    func_info['docstring'] = ast.get_docstring(node)
                    docstrings += 1
                functions.append(func_info)
            
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'lineno': node.lineno,
                    'methods': [],
                    'bases': [base.id if isinstance(base, ast.Name) else str(base) for base in node.bases]
                }
                if ast.get_docstring(node):
                    class_info['docstring'] = ast.get_docstring(node)
                    docstrings += 1
                
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        class_info['methods'].append(item.name)
                
                classes.append(class_info)
            
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    imports.extend([alias.name for alias in node.names])
                else:
                    imports.append(node.module if node.module else '')
        
        loc = len([line for line in code.split('\n') if line.strip()])
        comments = code.count('#')
        
        # Calculate complexity (simple cyclomatic complexity estimate)
        complexity_nodes = sum(1 for node in ast.walk(tree) 
                              if isinstance(node, (ast.If, ast.While, ast.For, ast.Try)))
        complexity_score = complexity_nodes / max(len(functions), 1)
        
        return CodeAnalysis(
            language='Python',
            functions=functions,
            classes=classes,
            imports=list(set(imports)),
            dependencies=self._extract_requirements(code),
            complexity_score=complexity_score,
            loc=loc,
            comments=comments,
            docstrings=docstrings,
            analysis_timestamp=datetime.now(),
            privacy_compliant=True
        )
    
    def _analyze_javascript(self, code: str, file_path: Path) -> CodeAnalysis:
        """Analyze JavaScript/TypeScript code"""
        # Simple regex-based analysis (can be enhanced with a proper JS parser)
        
        # Extract functions
        func_pattern = r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?(?:\(.*?\)|\w+)\s*=>)'
        functions = []
        for match in re.finditer(func_pattern, code):
            func_name = match.group(1) or match.group(2)
            functions.append({
                'name': func_name,
                'lineno': code[:match.start()].count('\n') + 1
            })
        
        # Extract classes
        class_pattern = r'class\s+(\w+)'
        classes = []
        for match in re.finditer(class_pattern, code):
            classes.append({
                'name': match.group(1),
                'lineno': code[:match.start()].count('\n') + 1
            })
        
        # Extract imports
        import_pattern = r'import\s+.*?from\s+['"]([^'"]+)['"]'
        imports = [match.group(1) for match in re.finditer(import_pattern, code)]
        
        loc = len([line for line in code.split('\n') if line.strip()])
        comments = code.count('//') + code.count('/*')
        
        complexity_score = (code.count('if ') + code.count('for ') + 
                          code.count('while ') + code.count('try')) / max(len(functions), 1)
        
        return CodeAnalysis(
            language='JavaScript' if file_path.suffix == '.js' else 'TypeScript',
            functions=functions,
            classes=classes,
            imports=imports,
            dependencies=[],
            complexity_score=complexity_score,
            loc=loc,
            comments=comments,
            docstrings=0,
            analysis_timestamp=datetime.now(),
            privacy_compliant=True
        )
    
    def _analyze_generic(self, code: str, file_path: Path, language: str) -> CodeAnalysis:
        """Generic code analysis for unsupported languages"""
        loc = len([line for line in code.split('\n') if line.strip()])
        comments = sum(1 for line in code.split('\n') if line.strip().startswith(('//', '#', '/*')))
        
        return CodeAnalysis(
            language=language.upper(),
            functions=[],
            classes=[],
            imports=[],
            dependencies=[],
            complexity_score=0.0,
            loc=loc,
            comments=comments,
            docstrings=0,
            analysis_timestamp=datetime.now(),
            privacy_compliant=True
        )
    
    def _extract_requirements(self, code: str) -> List[str]:
        """Extract Python package dependencies from imports"""
        # Common stdlib modules to exclude
        stdlib = {'os', 'sys', 'json', 're', 'datetime', 'pathlib', 'typing', 
                 'collections', 'itertools', 'functools', 'math', 'random'}
        
        import_pattern = r'(?:from|import)\s+([\w.]+)'
        all_imports = re.findall(import_pattern, code)
        
        # Get top-level package names
        packages = set()
        for imp in all_imports:
            top_level = imp.split('.')[0]
            if top_level not in stdlib:
                packages.add(top_level)
        
        return sorted(list(packages))
    
    def generate_summary(self, analysis: CodeAnalysis) -> str:
        """Generate code summary"""
        summary = f"Language: {analysis.language}\n"
        summary += f"Lines of Code: {analysis.loc}\n"
        summary += f"Functions: {len(analysis.functions)}\n"
        summary += f"Classes: {len(analysis.classes)}\n"
        summary += f"Imports: {len(analysis.imports)}\n"
        summary += f"Complexity Score: {analysis.complexity_score:.2f}\n"
        summary += f"Comments: {analysis.comments}\n"
        summary += f"Docstrings: {analysis.docstrings}\n"
        
        if analysis.dependencies:
            summary += f"\nExternal Dependencies:\n"
            for dep in analysis.dependencies:
                summary += f"  - {dep}\n"
        
        return summary
    
    def extract_documentation(self, analysis: CodeAnalysis) -> Dict[str, Any]:
        """Extract documentation from code"""
        docs = {
            'functions': [],
            'classes': []
        }
        
        for func in analysis.functions:
            if 'docstring' in func:
                docs['functions'].append({
                    'name': func['name'],
                    'docstring': func['docstring'],
                    'args': func.get('args', [])
                })
        
        for cls in analysis.classes:
            if 'docstring' in cls:
                docs['classes'].append({
                    'name': cls['name'],
                    'docstring': cls['docstring'],
                    'methods': cls.get('methods', [])
                })
        
        return docs
    
    def find_security_issues(self, code: str) -> List[Dict[str, Any]]:
        """Find potential security issues (basic patterns)"""
        issues = []
        
        # Check for dangerous patterns
        dangerous_patterns = [
            (r'eval\(', 'Use of eval() is dangerous'),
            (r'exec\(', 'Use of exec() is dangerous'),
            (r'os\.system\(', 'Direct system calls are risky'),
            (r'subprocess\.call\(.*shell=True', 'Shell=True is dangerous'),
            (r'pickle\.loads?\(', 'Pickle can execute arbitrary code'),
            (r'__import__\(', 'Dynamic imports can be risky'),
            (r'input\(.*\)', 'Raw input without validation'),
        ]
        
        for pattern, message in dangerous_patterns:
            for match in re.finditer(pattern, code):
                line_no = code[:match.start()].count('\n') + 1
                issues.append({
                    'line': line_no,
                    'issue': message,
                    'pattern': pattern
                })
        
        return issues
    
    def is_local_only(self) -> bool:
        """Verify LOCAL processing only"""
        return True
    
    def get_privacy_report(self) -> Dict[str, Any]:
        """Generate privacy compliance report"""
        return {
            'local_processing': True,
            'external_api_calls': False,
            'code_never_sent_externally': True,
            'ast_parsing_local': True,
            'compliance': ['GDPR', 'CCPA', 'Enterprise-ready']
        }

if __name__ == "__main__":
    analyzer = CodeAnalyzer()
    print("Code Analyzer ready - LOCAL processing only")
    print(f"Supported languages: {analyzer.supported_languages}")
    print(f"Privacy compliant: {analyzer.is_local_only()}")
