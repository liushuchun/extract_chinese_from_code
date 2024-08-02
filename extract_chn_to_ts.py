import os
import re
import json

def extract_chinese_strings_from_file(file_path):
    """
    Extracts Chinese strings from a given file.
    
    Args:
    file_path (str): Path to the file from which to extract Chinese strings.
    
    Returns:
    list: A list of Chinese strings found in the file.
    """
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
    chinese_strings = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            matches = chinese_pattern.findall(line)
            chinese_strings.extend(matches)
    
    return chinese_strings

def extract_chinese_strings_from_project(project_path):
    """
    Extracts Chinese strings from all files in a project directory.
    
    Args:
    project_path (str): Path to the project directory.
    
    Returns:
    dict: A dictionary where keys are file paths and values are lists of Chinese strings.
    """
    chinese_strings = {}
    
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.js') or file.endswith('.jsx') or file.endswith('.ts') or file.endswith('.tsx'):
                file_path = os.path.join(root, file)
                chinese_strings_in_file = extract_chinese_strings_from_file(file_path)
                if chinese_strings_in_file:
                    chinese_strings[file_path] = chinese_strings_in_file
    
    return chinese_strings

def generate_ts_file(chinese_strings, output_path):
    """
    Generates a TS file from a dictionary of Chinese strings.
    
    Args:
    chinese_strings (dict): A dictionary where keys are file paths and values are lists of Chinese strings.
    output_path (str): Path to the output TS file.
    """
    translations = {}
    index = 1
    
    for file_path, strings in chinese_strings.items():
        for string in strings:
            key = f'text_{index}'
            translations[key] = string
            index += 1
    
    with open(output_path, 'w', encoding='utf-8') as ts_file:
        ts_file.write('const translations = {\n')
        for key, value in translations.items():
            ts_file.write(f'  "{key}": "{value}",\n')
        ts_file.write('};\n')
        ts_file.write('\nexport default translations;\n')

def main():
    project_path = 'chinese-clothing'
    output_path = './translations.ts'
    
    chinese_strings = extract_chinese_strings_from_project(project_path)
    generate_ts_file(chinese_strings, output_path)
    print(f'Translations file generated at: {output_path}')

if __name__ == '__main__':
    main()
