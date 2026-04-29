"""
File encoding detection and conversion module.
"""
import chardet

def detect_encoding(file_path: str) -> str:
    """Return the most likely encoding of a text file."""
    with open(file_path, 'rb') as f:
        raw = f.read()
    result = chardet.detect(raw)
    return result['encoding']

def convert_encoding(input_path: str, output_path: str,
                     from_enc: str = None, to_enc: str = 'utf-8') -> bool:
    """Convert text file from one encoding to another."""
    try:
        if from_enc is None:
            from_enc = detect_encoding(input_path)
        with open(input_path, 'r', encoding=from_enc) as f:
            content = f.read()
        with open(output_path, 'w', encoding=to_enc) as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Encoding conversion failed: {e}")
        return False
