translations = {
    "ru": {
        "dir_error": "Ошибка: Нет доступа к директории",
        "size_error": "Ошибка при подсчете: {error}",
        "generic_error": "Ошибка: {error}",
        "total": "Всего: {dirs} папок, {files} файлов",
        "total_with_size": "Всего: {dirs} папок, {files} файлов. Общий вес директории: {size}",
        "DIR": "ПАПКА",
        "FILE": "ФАЙЛ"
    },
    "en": {
        "dir_error": "Error: No access to directory",
        "size_error": "Error during size calculation: {error}",
        "generic_error": "Error: {error}",
        "total": "Total: {dirs} folders, {files} files",
        "total_with_size": "Total: {dirs} folders, {files} files. Directory total size: {size}",
        "DIR": "DIR",
        "FILE": "FILE"
    }
}

def get_translation(key, lang="en", **kwargs):
    return translations.get(lang, translations["en"])[key].format(**kwargs)