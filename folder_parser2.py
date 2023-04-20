import shutil
import os
import argparse
from pathlib import Path
from normalize import normalize

images = []
video = []
audio = []
documents = []
archives = []
others = []

dict_extension = {
    'images': ['JPEG', 'JPG', 'PNG', 'SVG', 'GIF'],
    'video': ['AVI', 'MP4', 'MOV', 'MKV'],
    'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'archives': ['ZIP', 'GZ', 'TAR'],
    'others': []
}

folders = []
extensions = set() #всі розширення
unknown = set()


def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def scan(folder: Path):
    for item in folder.iterdir():
        if item.is_dir() and item.name not in ('images', 'audio' 'video', 'documents', 'archives'):
            folders.append(item)
            scan(item)
            continue
        ext = get_extension(item)
        full_name = folder / item.name
        category = 'others'
        new_path = f'{new}\\{category}\\'
        Path(f'{new}\\{category}\\').mkdir(exist_ok=True, parents=True)
        for k, v in dict_extension.items():
            if ext in v:
                category = k
                new_path = f'{new}\\{category}\\'
                Path(f'{new}\\{category}\\').mkdir(exist_ok=True, parents=True)
        if category == 'images':
            images.append(full_name.name)
            extensions.add(ext)
            os.replace(full_name, Path(new_path+normalize(full_name.name)))
        elif category == 'video':
            video.append(full_name.name)
            extensions.add(ext)
            os.replace(full_name, Path(new_path + normalize(full_name.name)))
        elif category == 'audio':
            audio.append(full_name.name)
            extensions.add(ext)
            os.replace(full_name, Path(new_path + normalize(full_name.name)))
        elif category == 'documents':
            documents.append(full_name.name)
            extensions.add(ext)
            os.replace(full_name, Path(new_path + normalize(full_name.name)))
        elif category == 'archives':
            archives.append(full_name.name)
            extensions.add(ext)
            new_path = f'{new}\\{category}\\{normalize(full_name.name.replace(full_name.suffix, ""))}\\'
            Path(new_path).mkdir(exist_ok=True, parents=True)
            os.replace(full_name, Path(new_path + normalize(full_name.name)))
            try:
                shutil.unpack_archive(f'{new}\\{category}\\{normalize(full_name.name.replace(full_name.suffix, ""))}\\{normalize(full_name.name)}', Path(f'{new}\\{category}\\{normalize(full_name.name.replace(full_name.suffix, ""))}'))
                os.remove(Path(f'{new}\\{category}\\{normalize(full_name.name.replace(full_name.suffix, ""))}\\{normalize(full_name.name)}'))
            except shutil.ReadError:
                print(f"Cant't extract the file {full_name.name}")
                return None
        elif category == 'others':
            others.append(full_name.name)
            unknown.add(ext)
            os.replace(full_name, Path(new_path + normalize(full_name.name)))


def delete_folder(folder_to_delete: Path) -> None:
    for folder in folders[::-1]:
        try:
            os.rmdir(folder)
        except OSError:
            print(f"Sorry, we can't delete the folder: {folder}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sorting file')
    parser.add_argument('--source', required=True)
    parser.add_argument('--new', default='Sort_folder')
    args = vars(parser.parse_args())
    source = args.get('source')
    new = args.get('new')

    scan(Path(source))
    delete_folder(Path(source))

    print(f'Start in folder: {source}')
    print(f'extension: \n {extensions}')
    print(f'unknown: \n {unknown}')
    print(f'folders: {folders}')
    print(f'images:\n  {images}\n ')
    print(f'video:\n  {video}\n ')
    print(f'audio:\n  {audio}\n ')
    print(f'documents:\n  {documents}\n ')
    print(f'archives:\n  {archives}\n ')
    print(f'others:\n  {others}\n ')

#python folder_parser2.py --source General --new New


