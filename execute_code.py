import subprocess

def execute_code(code, language):
    """Executes the extracted code and returns output."""
    try:
        if language == "Python":
            result = subprocess.run(["python", "-c", code], capture_output=True, text=True, timeout=5)
        elif language == "Java":
            result = subprocess.run(["java", "-e", code], capture_output=True, text=True, timeout=5)
        elif language == "C":
            result = subprocess.run(["gcc", "-xc", "-"], input=code, capture_output=True, text=True, timeout=5)
        else:
            return "Language execution not supported."

        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return str(e)
