import re

def detect_language(code):
    """Detects the programming language of the extracted code."""
    if "import" in code or "def " in code:
        return "Python"
    elif "public class" in code or "System.out.println" in code:
        return "Java"
    elif "#include <" in code or "int main()" in code:
        return "C"
    elif "function " in code or "console.log" in code:
        return "JavaScript"
    else:
        return "Unknown"
