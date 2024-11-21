import os

def save_project_structure_and_content(root_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Определяем уровень вложенности
            level = dirpath.replace(root_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            f.write(f'{indent}{os.path.basename(dirpath)}/\n')
            subindent = ' ' * 4 * (level + 1)
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                f.write(f'{subindent}{filename}\n')
                try:
                    with open(file_path, 'r', encoding='utf-8') as file_content:
                        content = file_content.read()
                    f.write(f'{subindent}{"-" * 40}\n')
                    f.write(f'{subindent}{content}\n')
                    f.write(f'{subindent}{"-" * 40}\n')
                except Exception as e:
                    f.write(f'{subindent}Не удалось прочитать файл: {e}\n')

if __name__ == "__main__":
    root_directory = './src'  # Укажите путь к корневой директории вашего проекта
    output_filename = 'project_structure_and_content.txt'
    save_project_structure_and_content(root_directory, output_filename)
    print(f'Структура проекта и содержимое файлов сохранены в {output_filename}')
