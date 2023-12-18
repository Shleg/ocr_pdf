import os


def delete_files_in_folder(folder_path):
    try:
        # Получаем список файлов в указанной папке
        files = os.listdir(folder_path)

        # Перебираем файлы и удаляем каждый
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

    except Exception as e:
        return print(f"Произошла ошибка: {e}")