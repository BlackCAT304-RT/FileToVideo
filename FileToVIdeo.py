#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FileToVideo v2.0

Original code by KorocheVolgin: https://github.com/KorocheVolgin/YouTube-Cloude/
UI and additional by BlackCAT304: https://github.com/BlackCAT304-RT/FileToVideo
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import sys
import os
import queue
import time
import webbrowser

try:
    import cv2
    import numpy as np
    import math
    import subprocess
    import tempfile
    import shutil
    import re
    BACKEND_AVAILABLE = True
except ImportError as _e:
    BACKEND_AVAILABLE = False
    _BACKEND_ERROR = str(_e)

# ─────────────────────────────────────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────────────────────────────────────

TRANSLATIONS = {
    'en': {
        'encode': 'Encode', 'decode': 'Decode', 'settings': 'Settings',
        'input_file': 'Input File:', 'output_file': 'Output File (MP4):',
        'output_folder': 'Output Folder:', 'browse': 'Browse...',
        'start_encode': 'Start Encoding', 'start_decode': 'Start Decoding',
        'clear_console': 'Clear', 'encryption_key': 'Encryption Key:',
        'no_key': '(leave empty to disable encryption)',
        'theme': 'Theme:', 'language': 'Language:',
        'theme_system': 'System', 'theme_dark': 'Dark', 'theme_light': 'Light',
        'console_label': 'Console Output:', 'ready': 'Ready',
        'encoding': 'Encoding...', 'decoding': 'Decoding...',
        'done': 'Done!', 'error': 'Error',
        'select_input': 'Select Input File',
        'select_output': 'Select Output File (MP4)',
        'select_folder': 'Select Output Folder',
        'load_key': 'Load key.txt',
        'video_files': 'Video Files', 'all_files': 'All Files',
        'encode_title': 'Encode File to Video',
        'decode_title': 'Decode Video to File',
        'settings_title': 'Settings',
        'show_key': 'Show', 'hide_key': 'Hide',
        'status': 'Status:',
    },
    'ru': {
        'encode': 'Кодировка', 'decode': 'Раскодировка', 'settings': 'Настройки',
        'input_file': 'Входной файл:', 'output_file': 'Выходной файл (MP4):',
        'output_folder': 'Папка вывода:', 'browse': 'Обзор...',
        'start_encode': 'Начать кодирование', 'start_decode': 'Начать декодирование',
        'clear_console': 'Очистить', 'encryption_key': 'Ключ шифрования:',
        'no_key': '(оставьте пустым для отключения шифрования)',
        'theme': 'Тема:', 'language': 'Язык:',
        'theme_system': 'Системная', 'theme_dark': 'Тёмная', 'theme_light': 'Светлая',
        'console_label': 'Вывод консоли:', 'ready': 'Готово',
        'encoding': 'Кодирование...', 'decoding': 'Декодирование...',
        'done': 'Завершено!', 'error': 'Ошибка',
        'select_input': 'Выберите входной файл',
        'select_output': 'Выберите выходной файл (MP4)',
        'select_folder': 'Выберите папку вывода',
        'load_key': 'Загрузить key.txt',
        'video_files': 'Видео файлы', 'all_files': 'Все файлы',
        'encode_title': 'Кодирование файла в видео',
        'decode_title': 'Декодирование видео в файл',
        'settings_title': 'Настройки',
        'show_key': 'Показать', 'hide_key': 'Скрыть',
        'status': 'Статус:',
    },
    'uk': {
        'encode': 'Кодування', 'decode': 'Декодування', 'settings': 'Налаштування',
        'input_file': 'Вхідний файл:', 'output_file': 'Вихідний файл (MP4):',
        'output_folder': 'Папка виводу:', 'browse': 'Огляд...',
        'start_encode': 'Почати кодування', 'start_decode': 'Почати декодування',
        'clear_console': 'Очистити', 'encryption_key': 'Ключ шифрування:',
        'no_key': '(залиште порожнім для вимкнення шифрування)',
        'theme': 'Тема:', 'language': 'Мова:',
        'theme_system': 'Системна', 'theme_dark': 'Темна', 'theme_light': 'Світла',
        'console_label': 'Вивід консолі:', 'ready': 'Готово',
        'encoding': 'Кодування...', 'decoding': 'Декодування...',
        'done': 'Завершено!', 'error': 'Помилка',
        'select_input': 'Виберіть вхідний файл',
        'select_output': 'Виберіть вихідний файл (MP4)',
        'select_folder': 'Виберіть папку виводу',
        'load_key': 'Завантажити key.txt',
        'video_files': 'Відео файли', 'all_files': 'Всі файли',
        'encode_title': 'Кодування файлу у відео',
        'decode_title': 'Декодування відео у файл',
        'settings_title': 'Налаштування',
        'show_key': 'Показати', 'hide_key': 'Сховати',
        'status': 'Статус:',
    },
    'de': {
        'encode': 'Kodieren', 'decode': 'Dekodieren', 'settings': 'Einstellungen',
        'input_file': 'Eingabedatei:', 'output_file': 'Ausgabedatei (MP4):',
        'output_folder': 'Ausgabeordner:', 'browse': 'Durchsuchen...',
        'start_encode': 'Kodierung starten', 'start_decode': 'Dekodierung starten',
        'clear_console': 'Leeren', 'encryption_key': 'Verschlüsselungsschlüssel:',
        'no_key': '(leer lassen zum Deaktivieren)',
        'theme': 'Thema:', 'language': 'Sprache:',
        'theme_system': 'System', 'theme_dark': 'Dunkel', 'theme_light': 'Hell',
        'console_label': 'Konsolenausgabe:', 'ready': 'Bereit',
        'encoding': 'Kodierung...', 'decoding': 'Dekodierung...',
        'done': 'Fertig!', 'error': 'Fehler',
        'select_input': 'Eingabedatei auswählen',
        'select_output': 'Ausgabedatei auswählen (MP4)',
        'select_folder': 'Ausgabeordner auswählen',
        'load_key': 'key.txt laden',
        'video_files': 'Videodateien', 'all_files': 'Alle Dateien',
        'encode_title': 'Datei in Video kodieren',
        'decode_title': 'Video in Datei dekodieren',
        'settings_title': 'Einstellungen',
        'show_key': 'Anzeigen', 'hide_key': 'Verbergen',
        'status': 'Status:',
    },
    'fr': {
        'encode': 'Encoder', 'decode': 'Décoder', 'settings': 'Paramètres',
        'input_file': "Fichier d'entrée:", 'output_file': 'Fichier de sortie (MP4):',
        'output_folder': 'Dossier de sortie:', 'browse': 'Parcourir...',
        'start_encode': "Démarrer l'encodage", 'start_decode': 'Démarrer le décodage',
        'clear_console': 'Effacer', 'encryption_key': 'Clé de chiffrement:',
        'no_key': '(laisser vide pour désactiver)',
        'theme': 'Thème:', 'language': 'Langue:',
        'theme_system': 'Système', 'theme_dark': 'Sombre', 'theme_light': 'Clair',
        'console_label': 'Sortie console:', 'ready': 'Prêt',
        'encoding': 'Encodage...', 'decoding': 'Décodage...',
        'done': 'Terminé!', 'error': 'Erreur',
        'select_input': "Sélectionner le fichier d'entrée",
        'select_output': 'Sélectionner le fichier de sortie (MP4)',
        'select_folder': 'Sélectionner le dossier de sortie',
        'load_key': 'Charger key.txt',
        'video_files': 'Fichiers vidéo', 'all_files': 'Tous les fichiers',
        'encode_title': 'Encoder Fichier en Vidéo',
        'decode_title': 'Décoder Vidéo en Fichier',
        'settings_title': 'Paramètres',
        'show_key': 'Afficher', 'hide_key': 'Masquer',
        'status': 'Statut:',
    },
    'es': {
        'encode': 'Codificar', 'decode': 'Decodificar', 'settings': 'Configuración',
        'input_file': 'Archivo de entrada:', 'output_file': 'Archivo de salida (MP4):',
        'output_folder': 'Carpeta de salida:', 'browse': 'Examinar...',
        'start_encode': 'Iniciar codificación', 'start_decode': 'Iniciar decodificación',
        'clear_console': 'Limpiar', 'encryption_key': 'Clave de cifrado:',
        'no_key': '(dejar vacío para desactivar)',
        'theme': 'Tema:', 'language': 'Idioma:',
        'theme_system': 'Sistema', 'theme_dark': 'Oscuro', 'theme_light': 'Claro',
        'console_label': 'Salida de consola:', 'ready': 'Listo',
        'encoding': 'Codificando...', 'decoding': 'Decodificando...',
        'done': '¡Completado!', 'error': 'Error',
        'select_input': 'Seleccionar archivo de entrada',
        'select_output': 'Seleccionar archivo de salida (MP4)',
        'select_folder': 'Seleccionar carpeta de salida',
        'load_key': 'Cargar key.txt',
        'video_files': 'Archivos de vídeo', 'all_files': 'Todos los archivos',
        'encode_title': 'Codificar Archivo en Vídeo',
        'decode_title': 'Decodificar Vídeo en Archivo',
        'settings_title': 'Configuración',
        'show_key': 'Mostrar', 'hide_key': 'Ocultar',
        'status': 'Estado:',
    },
    'pl': {
        'encode': 'Kodowanie', 'decode': 'Dekodowanie', 'settings': 'Ustawienia',
        'input_file': 'Plik wejściowy:', 'output_file': 'Plik wyjściowy (MP4):',
        'output_folder': 'Folder wyjściowy:', 'browse': 'Przeglądaj...',
        'start_encode': 'Rozpocznij kodowanie', 'start_decode': 'Rozpocznij dekodowanie',
        'clear_console': 'Wyczyść', 'encryption_key': 'Klucz szyfrowania:',
        'no_key': '(pozostaw puste aby wyłączyć)',
        'theme': 'Motyw:', 'language': 'Język:',
        'theme_system': 'Systemowy', 'theme_dark': 'Ciemny', 'theme_light': 'Jasny',
        'console_label': 'Wyjście konsoli:', 'ready': 'Gotowe',
        'encoding': 'Kodowanie...', 'decoding': 'Dekodowanie...',
        'done': 'Gotowe!', 'error': 'Błąd',
        'select_input': 'Wybierz plik wejściowy',
        'select_output': 'Wybierz plik wyjściowy (MP4)',
        'select_folder': 'Wybierz folder wyjściowy',
        'load_key': 'Wczytaj key.txt',
        'video_files': 'Pliki wideo', 'all_files': 'Wszystkie pliki',
        'encode_title': 'Zakoduj Plik do Wideo',
        'decode_title': 'Zdekoduj Wideo do Pliku',
        'settings_title': 'Ustawienia',
        'show_key': 'Pokaż', 'hide_key': 'Ukryj',
        'status': 'Status:',
    },
    'pt': {
        'encode': 'Codificar', 'decode': 'Decodificar', 'settings': 'Configurações',
        'input_file': 'Arquivo de entrada:', 'output_file': 'Arquivo de saída (MP4):',
        'output_folder': 'Pasta de saída:', 'browse': 'Procurar...',
        'start_encode': 'Iniciar codificação', 'start_decode': 'Iniciar decodificação',
        'clear_console': 'Limpar', 'encryption_key': 'Chave de criptografia:',
        'no_key': '(deixe vazio para desativar)',
        'theme': 'Tema:', 'language': 'Idioma:',
        'theme_system': 'Sistema', 'theme_dark': 'Escuro', 'theme_light': 'Claro',
        'console_label': 'Saída do console:', 'ready': 'Pronto',
        'encoding': 'Codificando...', 'decoding': 'Decodificando...',
        'done': 'Concluído!', 'error': 'Erro',
        'select_input': 'Selecionar arquivo de entrada',
        'select_output': 'Selecionar arquivo de saída (MP4)',
        'select_folder': 'Selecionar pasta de saída',
        'load_key': 'Carregar key.txt',
        'video_files': 'Arquivos de vídeo', 'all_files': 'Todos os arquivos',
        'encode_title': 'Codificar Arquivo em Vídeo',
        'decode_title': 'Decodificar Vídeo em Arquivo',
        'settings_title': 'Configurações',
        'show_key': 'Mostrar', 'hide_key': 'Ocultar',
        'status': 'Status:',
    },
    'it': {
        'encode': 'Codifica', 'decode': 'Decodifica', 'settings': 'Impostazioni',
        'input_file': 'File di input:', 'output_file': 'File di output (MP4):',
        'output_folder': 'Cartella di output:', 'browse': 'Sfoglia...',
        'start_encode': 'Avvia codifica', 'start_decode': 'Avvia decodifica',
        'clear_console': 'Pulisci', 'encryption_key': 'Chiave di cifratura:',
        'no_key': '(lascia vuoto per disabilitare)',
        'theme': 'Tema:', 'language': 'Lingua:',
        'theme_system': 'Sistema', 'theme_dark': 'Scuro', 'theme_light': 'Chiaro',
        'console_label': 'Output console:', 'ready': 'Pronto',
        'encoding': 'Codifica...', 'decoding': 'Decodifica...',
        'done': 'Completato!', 'error': 'Errore',
        'select_input': 'Seleziona file di input',
        'select_output': 'Seleziona file di output (MP4)',
        'select_folder': 'Seleziona cartella di output',
        'load_key': 'Carica key.txt',
        'video_files': 'File video', 'all_files': 'Tutti i file',
        'encode_title': 'Codifica File in Video',
        'decode_title': 'Decodifica Video in File',
        'settings_title': 'Impostazioni',
        'show_key': 'Mostra', 'hide_key': 'Nascondi',
        'status': 'Stato:',
    },
    'zh': {
        'encode': '编码', 'decode': '解码', 'settings': '设置',
        'input_file': '输入文件：', 'output_file': '输出文件（MP4）：',
        'output_folder': '输出文件夹：', 'browse': '浏览...',
        'start_encode': '开始编码', 'start_decode': '开始解码',
        'clear_console': '清除', 'encryption_key': '加密密钥：',
        'no_key': '（留空以禁用加密）',
        'theme': '主题：', 'language': '语言：',
        'theme_system': '系统', 'theme_dark': '深色', 'theme_light': '浅色',
        'console_label': '控制台输出：', 'ready': '就绪',
        'encoding': '编码中...', 'decoding': '解码中...',
        'done': '完成！', 'error': '错误',
        'select_input': '选择输入文件',
        'select_output': '选择输出文件（MP4）',
        'select_folder': '选择输出文件夹',
        'load_key': '加载 key.txt',
        'video_files': '视频文件', 'all_files': '所有文件',
        'encode_title': '编码 文件 → 视频',
        'decode_title': '解码 视频 → 文件',
        'settings_title': '设置',
        'show_key': '显示', 'hide_key': '隐藏',
        'status': '状态：',
    },
    'ja': {
        'encode': 'エンコード', 'decode': 'デコード', 'settings': '設定',
        'input_file': '入力ファイル：', 'output_file': '出力ファイル（MP4）：',
        'output_folder': '出力フォルダ：', 'browse': '参照...',
        'start_encode': 'エンコード開始', 'start_decode': 'デコード開始',
        'clear_console': 'クリア', 'encryption_key': '暗号化キー：',
        'no_key': '（空欄で暗号化を無効化）',
        'theme': 'テーマ：', 'language': '言語：',
        'theme_system': 'システム', 'theme_dark': 'ダーク', 'theme_light': 'ライト',
        'console_label': 'コンソール出力：', 'ready': '準備完了',
        'encoding': 'エンコード中...', 'decoding': 'デコード中...',
        'done': '完了！', 'error': 'エラー',
        'select_input': '入力ファイルを選択',
        'select_output': '出力ファイルを選択（MP4）',
        'select_folder': '出力フォルダを選択',
        'load_key': 'key.txt を読み込む',
        'video_files': '動画ファイル', 'all_files': 'すべてのファイル',
        'encode_title': 'ファイル → 動画 エンコード',
        'decode_title': '動画 → ファイル デコード',
        'settings_title': '設定',
        'show_key': '表示', 'hide_key': '非表示',
        'status': 'ステータス：',
    },
    'ko': {
        'encode': '인코드', 'decode': '디코드', 'settings': '설정',
        'input_file': '입력 파일:', 'output_file': '출력 파일 (MP4):',
        'output_folder': '출력 폴더:', 'browse': '찾아보기...',
        'start_encode': '인코딩 시작', 'start_decode': '디코딩 시작',
        'clear_console': '지우기', 'encryption_key': '암호화 키:',
        'no_key': '(비워두면 암호화 비활성화)',
        'theme': '테마:', 'language': '언어:',
        'theme_system': '시스템', 'theme_dark': '어두운', 'theme_light': '밝은',
        'console_label': '콘솔 출력:', 'ready': '준비',
        'encoding': '인코딩 중...', 'decoding': '디코딩 중...',
        'done': '완료!', 'error': '오류',
        'select_input': '입력 파일 선택',
        'select_output': '출력 파일 선택 (MP4)',
        'select_folder': '출력 폴더 선택',
        'load_key': 'key.txt 로드',
        'video_files': '비디오 파일', 'all_files': '모든 파일',
        'encode_title': '파일 → 비디오 인코드',
        'decode_title': '비디오 → 파일 디코드',
        'settings_title': '설정',
        'show_key': '표시', 'hide_key': '숨기기',
        'status': '상태:',
    },
}

LANGUAGE_NAMES = {
    'en': 'English', 'ru': 'Русский', 'uk': 'Українська',
    'de': 'Deutsch', 'fr': 'Français', 'es': 'Español',
    'pl': 'Polski', 'pt': 'Português', 'it': 'Italiano',
    'zh': '中文', 'ja': '日本語', 'ko': '한국어',
}
LANG_ORDER = ['en', 'ru', 'uk', 'de', 'fr', 'es', 'pl', 'pt', 'it', 'zh', 'ja', 'ko']

FOOTER_TEXT = (
    "Original code by KorocheVolgin: https://github.com/KorocheVolgin/YouTube-Cloude/    "
    "UI and additional by BlackCAT304: https://github.com/BlackCAT304-RT/FileToVideo"
)



# ─────────────────────────────────────────────────────────────────────────────
# BACKEND
# ─────────────────────────────────────────────────────────────────────────────

if BACKEND_AVAILABLE:
    class YouTubeEncoder:
        def __init__(self, key=None):
            self.width = 1920
            self.height = 1080
            self.fps = 6
            self.block_height = 16
            self.block_width = 24
            self.spacing = 4
            self.key = key
            self.use_encryption = key is not None
            self.colors = {
                '0000': (255, 0, 0),   '0001': (0, 255, 0),   '0010': (0, 0, 255),
                '0011': (255, 255, 0), '0100': (255, 0, 255), '0101': (0, 255, 255),
                '0110': (255, 128, 0), '0111': (128, 0, 255), '1000': (0, 128, 128),
                '1001': (128, 128, 0), '1010': (128, 0, 128), '1011': (0, 128, 0),
                '1100': (128, 0, 0),   '1101': (0, 0, 128),   '1110': (192, 192, 192),
                '1111': (255, 255, 255),
            }
            self.marker_size = 80
            self.blocks_x = (self.width - 2*self.marker_size) // (self.block_width + self.spacing)
            self.blocks_y = (self.height - 2*self.marker_size) // (self.block_height + self.spacing)
            self.blocks_per_region = self.blocks_x * self.blocks_y
            self.eof_bytes = ("█" * 64).encode('utf-8')
            print("=" * 60)
            print("ENCODER FileToVideo (6 FPS)")
            print("=" * 60)
            print(f"Grid: {self.blocks_x} x {self.blocks_y} blocks/region")
            print(f"Encryption: {'ON' if self.use_encryption else 'OFF'}")

        def _encrypt_data(self, data):
            if not self.use_encryption:
                return data
            kb = self.key.encode()
            return bytearray(b ^ kb[i % len(kb)] for i, b in enumerate(data))

        def _draw_markers(self, frame):
            ms = self.marker_size
            for x1, y1, x2, y2 in [
                (0, 0, ms, ms),
                (self.width - ms, 0, self.width, ms),
                (0, self.height - ms, ms, self.height),
                (self.width - ms, self.height - ms, self.width, self.height),
            ]:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), -1)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)
            return frame

        def _draw_block(self, frame, x, y, color):
            x1 = self.marker_size + x * (self.block_width + self.spacing)
            y1 = self.marker_size + y * (self.block_height + self.spacing)
            x2 = x1 + self.block_width
            y2 = y1 + self.block_height
            if x2 > self.width - self.marker_size or y2 > self.height - self.marker_size:
                return False
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 1)
            return True

        def _bits_to_color(self, bits):
            while len(bits) < 4:
                bits = '0' + bits
            return self.colors.get(bits, (255, 0, 0))

        def _data_to_blocks(self, data):
            bits = []
            for byte in data:
                for i in range(7, -1, -1):
                    bits.append(str((byte >> i) & 1))
            while len(bits) % 4 != 0:
                bits.append('0')
            return [''.join(bits[i:i+4]) for i in range(0, len(bits), 4)]

        def encode(self, input_file, output_file):
            with open(input_file, 'rb') as f:
                data = f.read()
            print(f"\nFile: {input_file}")
            print(f"Size: {len(data)} bytes")
            enc_data = self._encrypt_data(data) if self.use_encryption else data
            if self.use_encryption:
                print("Data encrypted")
            header = f"FILE:{os.path.basename(input_file)}:SIZE:{len(data)}|"
            print(f"Header: {header}")
            all_blocks = (
                self._data_to_blocks(header.encode('latin-1')) +
                self._data_to_blocks(enc_data) +
                self._data_to_blocks(self.eof_bytes)
            )
            print(f"Total blocks: {len(all_blocks)}")
            frames_needed = math.ceil(len(all_blocks) / self.blocks_per_region) + 5
            print(f"Frames needed: {frames_needed}")
            print(f"Duration: {frames_needed / self.fps:.1f}s")
            temp_dir = tempfile.mkdtemp()
            try:
                for frame_num in range(frames_needed - 5):
                    if frame_num % 10 == 0:
                        print(f"Frame {frame_num + 1}/{frames_needed}")
                    frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                    frame = self._draw_markers(frame)
                    start_idx = frame_num * self.blocks_per_region
                    end_idx = min(start_idx + self.blocks_per_region, len(all_blocks))
                    fb = all_blocks[start_idx:end_idx]
                    for rx, ry in [(0, 0), (self.blocks_x, 0), (0, self.blocks_y)]:
                        for idx, bits in enumerate(fb):
                            y = idx // self.blocks_x + ry
                            x = idx % self.blocks_x + rx
                            if x < self.blocks_x * 2 and y < self.blocks_y * 2:
                                self._draw_block(frame, x, y, self._bits_to_color(bits))
                    cv2.imwrite(os.path.join(temp_dir, f"frame_{frame_num:05d}.png"), frame)
                print("Creating guard frames...")
                for i in range(5):
                    fn = frames_needed - 5 + i
                    frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                    frame = self._draw_markers(frame)
                    for y in range(self.blocks_y * 2):
                        for x in range(self.blocks_x * 2):
                            self._draw_block(frame, x, y, (255, 0, 0))
                    cv2.imwrite(os.path.join(temp_dir, f"frame_{fn:05d}.png"), frame)
                print("Converting to MP4...")
                try:
                    subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
                    subprocess.run([
                        'ffmpeg', '-framerate', str(self.fps),
                        '-i', os.path.join(temp_dir, 'frame_%05d.png'),
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '23',
                        '-pix_fmt', 'yuv420p', '-an', '-movflags', '+faststart',
                        '-y', output_file
                    ], check=True, capture_output=True)
                    print("FFmpeg conversion successful")
                except Exception:
                    print("FFmpeg not available, using OpenCV...")
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(output_file, fourcc, self.fps, (self.width, self.height))
                    for fn in range(frames_needed):
                        fr = cv2.imread(os.path.join(temp_dir, f"frame_{fn:05d}.png"))
                        if fr is not None:
                            out.write(fr)
                    out.release()
            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)
                print("Temp files removed")
            if os.path.exists(output_file):
                sz = os.path.getsize(output_file)
                print(f"\nVideo saved: {output_file}")
                print(f"Size: {sz / 1024 / 1024:.2f} MB | Frames: {frames_needed} | Duration: {frames_needed / self.fps:.1f}s")
                return True
            return False


    class YouTubeDecoder:
        def __init__(self, key=None):
            self.width = 1920
            self.height = 1080
            self.block_height = 16
            self.block_width = 24
            self.spacing = 4
            self.marker_size = 80
            self.key = key
            self.colors = {
                '0000': (255, 0, 0),   '0001': (0, 255, 0),   '0010': (0, 0, 255),
                '0011': (255, 255, 0), '0100': (255, 0, 255), '0101': (0, 255, 255),
                '0110': (255, 128, 0), '0111': (128, 0, 255), '1000': (0, 128, 128),
                '1001': (128, 128, 0), '1010': (128, 0, 128), '1011': (0, 128, 0),
                '1100': (128, 0, 0),   '1101': (0, 0, 128),   '1110': (192, 192, 192),
                '1111': (255, 255, 255),
            }
            self.color_values = np.array(list(self.colors.values()), dtype=np.int32)
            self.color_keys = list(self.colors.keys())
            self.color_cache = {}
            self.cache_hits = 0
            self.cache_misses = 0
            self.blocks_x = (self.width - 2*self.marker_size) // (self.block_width + self.spacing)
            self.blocks_y = (self.height - 2*self.marker_size) // (self.block_height + self.spacing)
            self.blocks_per_region = self.blocks_x * self.blocks_y
            self._precompute_coords()
            print("=" * 60)
            print("DECODER FileToVideo")
            print("=" * 60)
            print(f"Grid: {self.blocks_x} x {self.blocks_y} blocks")
            print(f"Key: {'SET' if self.key else 'NONE'}")

        def _precompute_coords(self):
            self.block_coords = []
            for idx in range(self.blocks_per_region):
                y = idx // self.blocks_x
                x = idx % self.blocks_x
                if y < self.blocks_y:
                    cx = self.marker_size + x * (self.block_width + self.spacing) + self.block_width // 2
                    cy = self.marker_size + y * (self.block_height + self.spacing) + self.block_height // 2
                    self.block_coords.append((cx, cy))

        def _decrypt_data(self, data):
            if not self.key:
                return data
            kb = self.key.encode()
            return bytearray(b ^ kb[i % len(kb)] for i, b in enumerate(data))

        def _color_to_bits(self, color):
            key = (int(color[0]), int(color[1]), int(color[2]))
            if key in self.color_cache:
                self.cache_hits += 1
                return self.color_cache[key]
            self.cache_misses += 1
            if color[0] > 200 and color[1] < 50 and color[2] < 50:
                self.color_cache[key] = '0000'
                return '0000'
            arr = np.array([color[0], color[1], color[2]], dtype=np.int32)
            result = self.color_keys[np.argmin(np.sum((self.color_values - arr) ** 2, axis=1))]
            self.color_cache[key] = result
            return result

        def decode_frame(self, frame):
            if frame.shape[1] != self.width or frame.shape[0] != self.height:
                frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_NEAREST)
            h, w = frame.shape[:2]
            return [
                self._color_to_bits(frame[cy, cx]) if cx < w and cy < h else '0000'
                for cx, cy in self.block_coords
            ]

        def _blocks_to_bytes(self, blocks):
            bits = ''.join(blocks)
            result = bytearray()
            for i in range(0, len(bits) - 7, 8):
                bs = bits[i:i+8]
                if len(bs) == 8:
                    try:
                        result.append(int(bs, 2))
                    except Exception:
                        result.append(0)
            return result

        def _find_eof(self, data):
            eof = b'\xe2\x96\x88' * 64
            for i in range(len(data) - len(eof)):
                if data[i:i+len(eof)] == eof:
                    return i
            return -1

        def decode(self, video_file, output_dir='.'):
            print(f"\nDecoding: {video_file}")
            if not os.path.exists(video_file):
                print(f"File not found: {video_file}")
                return False
            cap = cv2.VideoCapture(video_file)
            if not cap.isOpened():
                print("Cannot open video")
                return False
            total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            print(f"Frames: {total} | FPS: {cap.get(cv2.CAP_PROP_FPS)} | "
                  f"Resolution: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
            self.cache_hits = self.cache_misses = 0
            t0 = time.time()
            all_blocks = []
            done = 0
            for fn in range(total):
                ret, frame = cap.read()
                if not ret:
                    break
                done += 1
                if fn % 50 == 0:
                    el = time.time() - t0
                    sp = done / el if el > 0 else 0
                    cr = self.cache_hits / max(1, self.cache_hits + self.cache_misses) * 100
                    print(f"  Progress: {fn}/{total} | {sp:.1f} fps | Cache: {cr:.1f}%")
                all_blocks.extend(self.decode_frame(frame))
            cap.release()
            el = time.time() - t0
            print(f"\n{len(all_blocks)} blocks in {el:.1f}s | {done} frames processed")
            data = self._blocks_to_bytes(all_blocks)
            print(f"Raw bytes: {len(data)}")
            eof_pos = self._find_eof(data)
            if eof_pos > 0:
                data = data[:eof_pos]
                print(f"EOF marker at position {eof_pos}")
            match = re.search(r'FILE:([^:]+):SIZE:(\d+)\|',
                              data[:1000].decode('latin-1', errors='ignore'))
            if match:
                filename = match.group(1)
                filesize = int(match.group(2))
                print(f"\nHeader found: {filename} ({filesize} bytes)")
                hb = match.group(0).encode('latin-1')
                hp = data.find(hb)
                if hp >= 0:
                    enc = data[hp + len(hb): hp + len(hb) + filesize]
                    fdata = self._decrypt_data(enc) if self.key else enc
                    if self.key:
                        print("Data decrypted")
                    out_path = os.path.join(output_dir, filename)
                    base, ext = os.path.splitext(filename)
                    n = 1
                    while os.path.exists(out_path):
                        out_path = os.path.join(output_dir, f"{base}_{n}{ext}")
                        n += 1
                    with open(out_path, 'wb') as f:
                        f.write(fdata)
                    print(f"\nFile restored: {out_path}")
                    print(f"Size: {len(fdata)} bytes" +
                          (" (matches original)" if len(fdata) == filesize else f" (expected {filesize})"))
                    return True
            else:
                print("Header not found")
            out_path = os.path.join(output_dir, "decoded_data.bin")
            with open(out_path, 'wb') as f:
                f.write(data)
            print(f"\nRaw data saved: {out_path}")
            return False


# ─────────────────────────────────────────────────────────────────────────────
# STDOUT → QUEUE
# ─────────────────────────────────────────────────────────────────────────────

class QueueStream:
    def __init__(self, q):
        self.q = q
    def write(self, text):
        if text:
            self.q.put(text)
    def flush(self):
        pass
    def isatty(self):
        return False


# ─────────────────────────────────────────────────────────────────────────────
# APPLICATION
# ─────────────────────────────────────────────────────────────────────────────

class FileToVideoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FileToVideo")
        self.root.geometry("740x520")
        self.root.minsize(560, 380)
        self.root.resizable(False, False)

        self.current_lang  = 'ru'
        self._key_visible  = False
        self.is_running    = False
        self.active_tab    = 'encode'

        self.con_queue = queue.Queue()

        self.enc_in_var  = tk.StringVar()
        self.enc_out_var = tk.StringVar()
        self.dec_in_var  = tk.StringVar()
        self.dec_out_var = tk.StringVar()
        self.key_var     = tk.StringVar()
        self.lang_var    = tk.StringVar(value=LANGUAGE_NAMES['ru'])

        self.display_to_code = {LANGUAGE_NAMES[c]: c for c in LANG_ORDER}

        self._load_icon()
        self._build_ui()
        self._apply_language()
        self._show_tab('encode')

        self.root.after(100, self._drain_queue)

        self.root.mainloop()

    # ── helpers ───────────────────────────────────────────────────────────────

    def _load_icon(self):
        try:
            ico = os.path.join('DATA', 'ico.ico')
            if os.path.exists(ico):
                self.root.iconbitmap(ico)
        except Exception:
            pass

    def t(self, key):
        return TRANSLATIONS.get(self.current_lang, TRANSLATIONS['en']).get(
            key, TRANSLATIONS['en'].get(key, key))


    # ── build ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Tab bar at the top
        self.tab_bar = tk.Frame(self.root, relief='flat', bd=0)
        self.tab_bar.grid(row=0, column=0, sticky='ew', padx=2, pady=(4, 0))

        self._tab_btns = {}
        for name in ('encode', 'decode', 'settings'):
            b = tk.Button(self.tab_bar, command=lambda n=name: self._show_tab(n))
            b.pack(side='left', padx=2, pady=2)
            self._tab_btns[name] = b

        # Plain 1px separator (themeable)
        self.tab_sep = tk.Frame(self.root, height=1, bd=0)
        self.tab_sep.grid(row=0, column=0, sticky='sew')

        # Vertical paned: content on top, console on bottom
        self.paned = tk.PanedWindow(self.root, orient=tk.VERTICAL,
                                     sashwidth=5, sashrelief='flat', relief='flat')
        self.paned.grid(row=1, column=0, sticky='nsew', padx=2, pady=2)

        self.content_host = tk.Frame(self.paned)
        self.paned.add(self.content_host, minsize=140, stretch='always')
        self.content_host.columnconfigure(0, weight=1)
        self.content_host.rowconfigure(0, weight=1)

        self.con_host = tk.Frame(self.paned)
        self.paned.add(self.con_host, minsize=80, stretch='always')

        # Tabs (stacked)
        self._tabs = {}
        self._tabs['encode']   = self._build_encode_tab()
        self._tabs['decode']   = self._build_decode_tab()
        self._tabs['settings'] = self._build_settings_tab()

        for f in self._tabs.values():
            f.place(in_=self.content_host, relwidth=1, relheight=1)

        self._build_console()
        self._build_footer()

        self.root.update_idletasks()
        self.root.after(60, lambda: self.paned.sash_place(0, 0, 210))

    # ── encode tab ────────────────────────────────────────────────────────────

    def _build_encode_tab(self):
        f = tk.Frame(self.content_host)
        f.columnconfigure(1, weight=1)

        self.enc_in_lbl = tk.Label(f)
        self.enc_in_lbl.grid(row=0, column=0, sticky='w', padx=(8, 4), pady=(8, 2))
        self.enc_in_entry = tk.Entry(f, textvariable=self.enc_in_var)
        self.enc_in_entry.grid(row=0, column=1, sticky='ew', pady=(8, 2))
        self.enc_in_btn = tk.Button(f, command=self._browse_enc_in)
        self.enc_in_btn.grid(row=0, column=2, padx=(4, 8), pady=(8, 2))

        self.enc_out_lbl = tk.Label(f)
        self.enc_out_lbl.grid(row=1, column=0, sticky='w', padx=(8, 4), pady=2)
        self.enc_out_entry = tk.Entry(f, textvariable=self.enc_out_var)
        self.enc_out_entry.grid(row=1, column=1, sticky='ew', pady=2)
        self.enc_out_btn = tk.Button(f, command=self._browse_enc_out)
        self.enc_out_btn.grid(row=1, column=2, padx=(4, 8), pady=2)

        self.enc_key_lbl = tk.Label(f)
        self.enc_key_lbl.grid(row=2, column=0, sticky='w', padx=(8, 4), pady=2)

        kf = tk.Frame(f)
        kf.grid(row=2, column=1, sticky='ew', pady=2)
        kf.columnconfigure(0, weight=1)
        self.enc_key_entry = tk.Entry(kf, textvariable=self.key_var, show='*')
        self.enc_key_entry.grid(row=0, column=0, sticky='ew')
        self.enc_key_note = tk.Label(kf, font=('TkDefaultFont', 7))
        self.enc_key_note.grid(row=1, column=0, sticky='w')

        kb = tk.Frame(f)
        kb.grid(row=2, column=2, padx=(4, 8), pady=2)
        self.enc_show_btn = tk.Button(kb, width=6, command=self._toggle_key)
        self.enc_show_btn.pack(side='left', padx=(0, 2))
        self.enc_load_btn = tk.Button(kb, command=self._load_key_file)
        self.enc_load_btn.pack(side='left')

        sf = tk.Frame(f)
        sf.grid(row=3, column=0, columnspan=3, sticky='w', padx=8, pady=(8, 6))
        self.enc_start_btn = tk.Button(sf, command=self._start_encode)
        self.enc_start_btn.pack(side='left', padx=(0, 10))
        self.enc_status_lbl = tk.Label(sf, font=('TkDefaultFont', 8))
        self.enc_status_lbl.pack(side='left')
        self.enc_status_val = tk.Label(sf, font=('TkDefaultFont', 8))
        self.enc_status_val.pack(side='left')

        return f

    # ── decode tab ────────────────────────────────────────────────────────────

    def _build_decode_tab(self):
        f = tk.Frame(self.content_host)
        f.columnconfigure(1, weight=1)

        self.dec_in_lbl = tk.Label(f)
        self.dec_in_lbl.grid(row=0, column=0, sticky='w', padx=(8, 4), pady=(8, 2))
        self.dec_in_entry = tk.Entry(f, textvariable=self.dec_in_var)
        self.dec_in_entry.grid(row=0, column=1, sticky='ew', pady=(8, 2))
        self.dec_in_btn = tk.Button(f, command=self._browse_dec_in)
        self.dec_in_btn.grid(row=0, column=2, padx=(4, 8), pady=(8, 2))

        self.dec_out_lbl = tk.Label(f)
        self.dec_out_lbl.grid(row=1, column=0, sticky='w', padx=(8, 4), pady=2)
        self.dec_out_entry = tk.Entry(f, textvariable=self.dec_out_var)
        self.dec_out_entry.grid(row=1, column=1, sticky='ew', pady=2)
        self.dec_out_btn = tk.Button(f, command=self._browse_dec_out)
        self.dec_out_btn.grid(row=1, column=2, padx=(4, 8), pady=2)

        self.dec_key_lbl = tk.Label(f)
        self.dec_key_lbl.grid(row=2, column=0, sticky='w', padx=(8, 4), pady=2)

        kf2 = tk.Frame(f)
        kf2.grid(row=2, column=1, sticky='ew', pady=2)
        kf2.columnconfigure(0, weight=1)
        self.dec_key_entry = tk.Entry(kf2, textvariable=self.key_var, show='*')
        self.dec_key_entry.grid(row=0, column=0, sticky='ew')
        self.dec_key_note = tk.Label(kf2, font=('TkDefaultFont', 7))
        self.dec_key_note.grid(row=1, column=0, sticky='w')

        kb2 = tk.Frame(f)
        kb2.grid(row=2, column=2, padx=(4, 8), pady=2)
        self.dec_show_btn = tk.Button(kb2, width=6, command=self._toggle_key)
        self.dec_show_btn.pack(side='left', padx=(0, 2))
        self.dec_load_btn = tk.Button(kb2, command=self._load_key_file)
        self.dec_load_btn.pack(side='left')

        sf2 = tk.Frame(f)
        sf2.grid(row=3, column=0, columnspan=3, sticky='w', padx=8, pady=(8, 6))
        self.dec_start_btn = tk.Button(sf2, command=self._start_decode)
        self.dec_start_btn.pack(side='left', padx=(0, 10))
        self.dec_status_lbl = tk.Label(sf2, font=('TkDefaultFont', 8))
        self.dec_status_lbl.pack(side='left')
        self.dec_status_val = tk.Label(sf2, font=('TkDefaultFont', 8))
        self.dec_status_val.pack(side='left')

        return f

    # ── settings tab ──────────────────────────────────────────────────────────

    def _build_settings_tab(self):
        f = tk.Frame(self.content_host)

        self.set_lang_lbl = tk.Label(f)
        self.set_lang_lbl.grid(row=0, column=0, sticky='w', padx=(8, 6), pady=(10, 4))

        lang_names = [LANGUAGE_NAMES[c] for c in LANG_ORDER]
        self.lang_menu = tk.OptionMenu(f, self.lang_var, *lang_names,
                                        command=self._on_lang_change)
        self.lang_menu.grid(row=0, column=1, sticky='w', pady=(10, 4))

        return f

    # ── console ───────────────────────────────────────────────────────────────

    def _build_console(self):
        self.con_host.columnconfigure(0, weight=1)
        self.con_host.rowconfigure(1, weight=1)

        bar = tk.Frame(self.con_host)
        bar.grid(row=0, column=0, columnspan=2, sticky='ew')
        bar.columnconfigure(0, weight=1)
        self.con_lbl = tk.Label(bar, font=('TkDefaultFont', 8, 'bold'), anchor='w')
        self.con_lbl.grid(row=0, column=0, padx=4, pady=1, sticky='w')
        self.con_clear_btn = tk.Button(bar, command=self._clear_console)
        self.con_clear_btn.grid(row=0, column=1, padx=4, pady=1)

        self.con_text = tk.Text(
            self.con_host, font=('Courier', 9),
            wrap=tk.WORD, state='disabled', relief='sunken', bd=1
        )
        self.con_text.grid(row=1, column=0, sticky='nsew')

        self.con_sb = tk.Scrollbar(self.con_host, command=self.con_text.yview)
        self.con_sb.grid(row=1, column=1, sticky='ns')
        self.con_text.config(yscrollcommand=self.con_sb.set)

    # ── footer ────────────────────────────────────────────────────────────────

    def _build_footer(self):
        self.footer = tk.Frame(self.root, relief='sunken', bd=1)
        self.footer.grid(row=2, column=0, sticky='ew')

        tk.Label(self.footer, text='Original code by KorocheVolgin: ',
                  font=('TkDefaultFont', 7)).pack(side='left', padx=(6, 0), pady=2)

        lnk1 = tk.Label(self.footer,
                         text='https://github.com/KorocheVolgin/YouTube-Cloude/',
                         font=('TkDefaultFont', 7, 'underline'),
                         cursor='hand2')
        lnk1.pack(side='left', pady=2)
        lnk1.bind('<Button-1>', lambda e: webbrowser.open('https://github.com/KorocheVolgin/YouTube-Cloude/'))
        self._footer_link1 = lnk1

        tk.Label(self.footer, text='    UI and additional by BlackCAT304: ',
                  font=('TkDefaultFont', 7)).pack(side='left', pady=2)

        lnk2 = tk.Label(self.footer,
                         text='https://github.com/BlackCAT304-RT/FileToVideo',
                         font=('TkDefaultFont', 7, 'underline'),
                         cursor='hand2')
        lnk2.pack(side='left', pady=2)
        lnk2.bind('<Button-1>', lambda e: webbrowser.open('https://github.com/BlackCAT304-RT/FileToVideo'))
        self._footer_link2 = lnk2

    # ── tabs ──────────────────────────────────────────────────────────────────

    def _show_tab(self, name):
        self.active_tab = name
        for n, f in self._tabs.items():
            f.lift() if n == name else f.lower()
        self._refresh_tab_btns()

    def _refresh_tab_btns(self):
        for name, btn in self._tab_btns.items():
            btn.config(relief='sunken' if name == self.active_tab else 'raised')

    # ── browse ────────────────────────────────────────────────────────────────

    def _browse_enc_in(self):
        p = filedialog.askopenfilename(title=self.t('select_input'))
        if p:
            self.enc_in_var.set(p)
            if not self.enc_out_var.get():
                self.enc_out_var.set(os.path.splitext(p)[0] + '_encoded.mp4')

    def _browse_enc_out(self):
        p = filedialog.asksaveasfilename(
            title=self.t('select_output'), defaultextension='.mp4',
            filetypes=[(self.t('video_files'), '*.mp4'), (self.t('all_files'), '*.*')])
        if p:
            self.enc_out_var.set(p)

    def _browse_dec_in(self):
        p = filedialog.askopenfilename(
            title=self.t('select_input'),
            filetypes=[(self.t('video_files'), '*.mp4 *.avi *.mkv'), (self.t('all_files'), '*.*')])
        if p:
            self.dec_in_var.set(p)
            if not self.dec_out_var.get():
                self.dec_out_var.set(os.path.dirname(p))

    def _browse_dec_out(self):
        p = filedialog.askdirectory(title=self.t('select_folder'))
        if p:
            self.dec_out_var.set(p)

    def _toggle_key(self):
        self._key_visible = not self._key_visible
        show = '' if self._key_visible else '*'
        self.enc_key_entry.config(show=show)
        self.dec_key_entry.config(show=show)
        lbl = self.t('hide_key') if self._key_visible else self.t('show_key')
        self.enc_show_btn.config(text=lbl)
        self.dec_show_btn.config(text=lbl)

    def _load_key_file(self):
        p = filedialog.askopenfilename(
            title='Select key file',
            filetypes=[('Text files', '*.txt'), ('All files', '*.*')])
        if p:
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    self.key_var.set(f.read().strip())
                self._log(f"Key loaded from {p}\n")
            except Exception as e:
                self._log(f"Key load error: {e}\n")

    # ── operations ────────────────────────────────────────────────────────────

    def _start_encode(self):
        if self.is_running:
            return
        if not BACKEND_AVAILABLE:
            msg = f"Backend not available — {_BACKEND_ERROR}"
            self._log(f"ERROR: {msg}\n")
            messagebox.showerror("FileToVideo", msg)
            return
        inp = self.enc_in_var.get().strip()
        out = self.enc_out_var.get().strip()
        if not inp:
            self._log("ERROR: No input file selected\n")
            messagebox.showwarning("FileToVideo", self.t('select_input'))
            return
        if not out:
            out = os.path.splitext(inp)[0] + '_encoded.mp4'
            self.enc_out_var.set(out)
        self._set_busy(True, 'encoding')
        threading.Thread(
            target=self._run_encode,
            args=(inp, out, self.key_var.get().strip() or None),
            daemon=True
        ).start()

    def _run_encode(self, inp, out, key):
        old, sys.stdout = sys.stdout, QueueStream(self.con_queue)
        ok = False
        try:
            ok = YouTubeEncoder(key).encode(inp, out)
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            sys.stdout = old
            self.root.after(0, lambda: self._set_busy(False, 'done' if ok else 'error'))

    def _start_decode(self):
        if self.is_running:
            return
        if not BACKEND_AVAILABLE:
            msg = f"Backend not available — {_BACKEND_ERROR}"
            self._log(f"ERROR: {msg}\n")
            messagebox.showerror("FileToVideo", msg)
            return
        inp = self.dec_in_var.get().strip()
        if not inp:
            self._log("ERROR: No input file selected\n")
            messagebox.showwarning("FileToVideo", self.t('select_input'))
            return
        self._set_busy(True, 'decoding')
        threading.Thread(
            target=self._run_decode,
            args=(inp, self.dec_out_var.get().strip() or '.', self.key_var.get().strip() or None),
            daemon=True
        ).start()

    def _run_decode(self, inp, out, key):
        old, sys.stdout = sys.stdout, QueueStream(self.con_queue)
        ok = False
        try:
            ok = YouTubeDecoder(key).decode(inp, out)
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            sys.stdout = old
            self.root.after(0, lambda: self._set_busy(False, 'done' if ok else 'error'))

    def _set_busy(self, busy, status='ready'):
        self.is_running = busy
        state = 'disabled' if busy else 'normal'
        self.enc_start_btn.config(state=state)
        self.dec_start_btn.config(state=state)
        txt = self.t(status)
        self.enc_status_val.config(text=txt)
        self.dec_status_val.config(text=txt)
        if not busy:
            self._load_icon()  # Re-apply icon after subprocess/thread resets it

    # ── console ───────────────────────────────────────────────────────────────

    def _drain_queue(self):
        try:
            while True:
                self._log(self.con_queue.get_nowait())
        except queue.Empty:
            pass
        self.root.after(100, self._drain_queue)

    def _log(self, text):
        self.con_text.config(state='normal')
        self.con_text.insert('end', text)
        self.con_text.tag_remove('sel', '1.0', 'end')
        self.con_text.see('end')
        self.con_text.config(state='disabled')

    def _clear_console(self):
        self.con_text.config(state='normal')
        self.con_text.delete('1.0', 'end')
        self.con_text.config(state='disabled')

    # ── language ──────────────────────────────────────────────────────────────

    def _on_lang_change(self, display_name):
        self.current_lang = self.display_to_code.get(display_name, 'en')
        self._apply_language()

    def _apply_language(self):
        for name, btn in self._tab_btns.items():
            btn.config(text=self.t(name))

        self.enc_in_lbl.config(text=self.t('input_file'))
        self.enc_out_lbl.config(text=self.t('output_file'))
        self.enc_key_lbl.config(text=self.t('encryption_key'))
        self.enc_key_note.config(text=self.t('no_key'))
        self.enc_in_btn.config(text=self.t('browse'))
        self.enc_out_btn.config(text=self.t('browse'))
        self.enc_show_btn.config(text=self.t('hide_key') if self._key_visible else self.t('show_key'))
        self.enc_load_btn.config(text=self.t('load_key'))
        self.enc_start_btn.config(text=self.t('start_encode'))
        self.enc_status_lbl.config(text=self.t('status') + ' ')
        self.enc_status_val.config(text=self.t('ready'))

        self.dec_in_lbl.config(text=self.t('input_file'))
        self.dec_out_lbl.config(text=self.t('output_folder'))
        self.dec_key_lbl.config(text=self.t('encryption_key'))
        self.dec_key_note.config(text=self.t('no_key'))
        self.dec_in_btn.config(text=self.t('browse'))
        self.dec_out_btn.config(text=self.t('browse'))
        self.dec_show_btn.config(text=self.t('hide_key') if self._key_visible else self.t('show_key'))
        self.dec_load_btn.config(text=self.t('load_key'))
        self.dec_start_btn.config(text=self.t('start_decode'))
        self.dec_status_lbl.config(text=self.t('status') + ' ')
        self.dec_status_val.config(text=self.t('ready'))

        self.set_lang_lbl.config(text=self.t('language'))

        self.con_lbl.config(text=self.t('console_label'))
        self.con_clear_btn.config(text=self.t('clear_console'))

        self._refresh_tab_btns()


# ─────────────────────────────────────────────────────────────────────────────

def main():
    FileToVideoApp()


if __name__ == '__main__':
    main()
