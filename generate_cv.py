import os
import re
import subprocess
import sys

def main():
    # 1. Check if pandoc is installed
    try:
        subprocess.run(["pandoc", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("Pandoc is not installed. Attempting to install it via Homebrew...")
        try:
            subprocess.run(["brew", "install", "pandoc"], check=True)
        except Exception as e:
            print("Failed to install pandoc via brew. Please install pandoc manually (e.g. 'brew install pandoc') and run this script again.", file=sys.stderr)
            sys.exit(1)

    # 2. Read the readme.md
    readme_path = "readme.md"
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found in the current directory.", file=sys.stderr)
        sys.exit(1)

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 3. Rewrite relative project links to absolute github links
    # Matches: ](./projects/...) or ](projects/...)
    # Replaces with: ](https://github.com/defiveninth/cv/blob/main/projects/...)
    pattern = r'\]\(\.?/projects/(.*?)\)'
    replacement = r'](https://github.com/defiveninth/cv/blob/main/projects/\1)'
    updated_content = re.sub(pattern, replacement, content)

    # 4. Save to temporary markdown file
    temp_markdown_path = "temp_readme.md"
    with open(temp_markdown_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    # 5. Convert to DOCX using pandoc
    output_docx_path = "CV.docx"
    print(f"Generating {output_docx_path} from {readme_path}...")
    try:
        subprocess.run(["pandoc", temp_markdown_path, "-o", output_docx_path], check=True)
        print(f"Success! {output_docx_path} has been generated.")
    except subprocess.CalledProcessError as e:
        print(f"Error running pandoc: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Clean up temporary file
        if os.path.exists(temp_markdown_path):
            os.remove(temp_markdown_path)

if __name__ == "__main__":
    main()
