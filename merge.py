import os

def create_markdown_from_directory(root_directory, output_markdown):
    """
    Walks through a directory and subdirectories, extracting code from all files
    and creating a markdown file that consolidates all the code.

    Parameters:
    root_directory (str): The root directory to traverse.
    output_markdown (str): The path to the output markdown file.
    """
    with open(output_markdown, 'w', encoding='utf-8') as markdown_file:
        # Write header to markdown file
        markdown_file.write("# Consolidated Code\n\n")

        for dirpath, _, filenames in os.walk(root_directory):
            if '/virtual/' in dirpath:
                continue

            for filename in filenames:
                file_path = os.path.join(dirpath, filename)

                # Skip files that are not code (you can customize this filter)
                if not filename.endswith(('.py', '.js', '.html', '.css', '.java', '.cpp', '.txt')):
                    continue

                markdown_file.write(f"## File: {file_path}\n\n```")

                try:
                    with open(file_path, 'r', encoding='utf-8') as code_file:
                        markdown_file.write(code_file.read())
                except Exception as e:
                    markdown_file.write(f"Error reading file: {e}")

                markdown_file.write("\n````\n\n")

if __name__ == "__main__":
    root_dir = "/workspaces/automate-career"  # Replace with your root directory path
    output_file = "output.md"  # Replace with your desired output file path

    create_markdown_from_directory(root_dir, output_file)
    print(f"Markdown file created at {output_file}")
