import os
import zipfile
import re
import shutil
from datetime import datetime
from pathlib import Path

# Fungsi untuk mendapatkan direktori dokumen Pyto
def get_pyto_documents_dir():
    """
    Mendapatkan direktori dokumen lokal Pyto.
    """
    try:
        # Path default ke direktori dokumen Pyto
        return Path.cwd()
    except Exception as e:
        print(f"Error mendapatkan direktori Pyto: {e}")
        return None

# Set path dasar
base_path = Path("/private/var/mobile/Library/Mobile Documents/com~apple~CloudDocs/SURCA/Function_Clean")

# Cek apakah base_path ada dan dapat diakses
if not base_path.exists():
    print(f"Path dasar tidak ditemukan: {base_path}")
    # Alternatif: Gunakan direktori lokal Pyto
    base_path = get_pyto_documents_dir() / "SURCA" / "Function_Clean"
    print(f"Menggunakan direktori lokal Pyto: {base_path}")
    if not base_path.exists():
        print(f"Direktori lokal Pyto juga tidak ditemukan: {base_path}")
        print("Pastikan direktori 'SURCA/Function_Clean' ada di Pyto Documents.")
        exit(1)

# Pastikan Pyto memiliki izin untuk mengakses direktori ini
if not os.access(base_path, os.R_OK | os.W_OK):
    print(f"Pyto tidak memiliki izin untuk mengakses direktori: {base_path}")
    print("Pastikan Pyto memiliki izin yang benar melalui pengaturan iOS.")
    exit(1)

# Ubah direktori kerja
try:
    os.chdir(base_path)
    print(f"Direktori kerja diubah ke: {base_path}")
except Exception as e:
    print(f"Gagal mengubah direktori kerja: {e}")
    exit(1)

# Pola untuk mencocokkan file zip dalam kedua bahasa
zip_patterns = [
    re.compile(r"^Chat WhatsApp dengan.*\.zip$", re.IGNORECASE),  # Bahasa Indonesia
    re.compile(r"^WhatsApp Chat with.*\.zip$", re.IGNORECASE)      # Bahasa Inggris
]

# Buat direktori untuk file yang diekstrak dengan tanggal dan waktu saat ini
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
extracted_folder_path = base_path / f"Extracted_WA_{current_time}"
try:
    extracted_folder_path.mkdir(parents=True, exist_ok=True)
    print(f"Direktori untuk file yang diekstrak dibuat: {extracted_folder_path}")
except Exception as e:
    print(f"Gagal membuat direktori untuk file yang diekstrak: {e}")
    exit(1)

# Definisikan fungsi untuk memangkas prefix
def trim_prefix(file_name):
    if file_name.startswith("Chat WhatsApp dengan "):
        return file_name.replace("Chat WhatsApp dengan ", "").replace(".zip", "").replace(".txt", "")
    elif file_name.startswith("WhatsApp Chat with "):
        return file_name.replace("WhatsApp Chat with ", "").replace(".zip", "").replace(".txt", "")
    return file_name.replace(".zip", "").replace(".txt", "")

# Iterasi melalui file di direktori dasar
for file_path in base_path.iterdir():
    if file_path.is_file():
        matched = False
        for zip_pattern in zip_patterns:
            if zip_pattern.match(file_path.name):
                matched = True
                # Ekstrak nama folder baru
                new_folder_name = trim_prefix(file_path.name)
                new_folder_path = base_path / new_folder_name
                try:
                    new_folder_path.mkdir(parents=True, exist_ok=True)
                    print(f"Direktori baru untuk ekstraksi dibuat: {new_folder_path}")
                except Exception as e:
                    print(f"Gagal membuat direktori baru {new_folder_path}: {e}")
                    continue

                # Ekstrak file zip
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(new_folder_path)
                    print(f"File zip diekstrak: {file_path.name} ke {new_folder_path}")
                except zipfile.BadZipFile:
                    print(f"File zip rusak atau tidak valid: {file_path.name}")
                    shutil.rmtree(new_folder_path)
                    continue
                except Exception as e:
                    print(f"Gagal mengekstrak {file_path.name}: {e}")
                    shutil.rmtree(new_folder_path)
                    continue

                # Ganti nama file txt di dalam folder yang diekstrak
                for extracted_file in new_folder_path.iterdir():
                    if extracted_file.is_file() and extracted_file.suffix.lower() == ".txt":
                        new_file_name = trim_prefix(extracted_file.name)
                        new_file_path = new_folder_path / new_file_name
                        try:
                            extracted_file.rename(new_file_path)
                            print(f"File {extracted_file.name} diubah menjadi {new_file_name}")
                        except Exception as e:
                            print(f"Gagal mengubah nama file {extracted_file.name}: {e}")

                # Pindahkan folder yang diekstrak ke direktori Extracted
                try:
                    shutil.move(str(new_folder_path), str(extracted_folder_path))
                    print(f"Folder {new_folder_path.name} dipindahkan ke {extracted_folder_path}")
                except Exception as e:
                    print(f"Gagal memindahkan folder {new_folder_path.name}: {e}")

        if not matched:
            print(f"File tidak cocok dengan pola zip: {file_path.name}")

# Buat folder baru untuk file zip mentah
raw_zip_folder = base_path / f"RAW_Extract_WA_{current_time}"
try:
    raw_zip_folder.mkdir(parents=True, exist_ok=True)
    print(f"Direktori untuk file zip mentah dibuat: {raw_zip_folder}")
except Exception as e:
    print(f"Gagal membuat direktori untuk file zip mentah: {e}")
    exit(1)

# Pindahkan semua file zip asli ke folder zip mentah
for file_path in base_path.iterdir():
    if file_path.is_file():
        for zip_pattern in zip_patterns:
            if zip_pattern.match(file_path.name):
                try:
                    shutil.move(str(file_path), str(raw_zip_folder))
                    print(f"File zip {file_path.name} dipindahkan ke {raw_zip_folder}")
                except Exception as e:
                    print(f"Gagal memindahkan file zip {file_path.name}: {e}")

# Bersihkan: Hapus folder yang diekstrak jika diperlukan
# (Komentari bagian ini jika Anda tidak ingin menghapus folder tertentu)
for folder_path in base_path.iterdir():
    if folder_path.is_dir() and (folder_path.name.startswith("Chat WhatsApp") or folder_path.name.startswith("WhatsApp Chat")):
        try:
            shutil.rmtree(folder_path)
            print(f"Folder {folder_path.name} dihapus.")
        except Exception as e:
            print(f"Gagal menghapus folder {folder_path.name}: {e}")

print("Skrip selesai dijalankan.")