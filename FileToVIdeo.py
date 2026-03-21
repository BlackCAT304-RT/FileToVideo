#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FileToVideo v2.1

Original code by KorocheVolgin: https://github.com/KorocheVolgin/YouTube-Cloude/
UI and additional by BlackCAT304: https://github.com/BlackCAT304-RT/FileToVideo
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import sys
import os
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
        'encryption_key': 'Encryption Key:',
        'no_key': '(leave empty to disable encryption)',
        'theme': 'Theme:', 'language': 'Language:',
        'theme_system': 'System', 'theme_dark': 'Dark', 'theme_light': 'Light',
        'ready': 'Ready',
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
        # stats labels
        'stat_elapsed':   'Elapsed:',
        'stat_remaining': 'Remaining:',
        'stat_frame':     'Frame:',
        'stat_blocks':    'Blocks/frame:',
        'stat_blocksize': 'Block size:',
        'stat_filesize':  'File size:',
        'stat_grid':      'Grid:',
        'stat_fps':       'FPS:',
        'stat_encrypt':   'Encryption:',
        'stat_on':        'ON',
        'stat_off':       'OFF',
        # completion dialog
        'done_title':     'Completed!',
        'done_encode':    'Encoding finished in {t}.\n\nOutput: {out}\nSize: {sz}\nFrames: {fr}\nDuration: {dur}',
        'done_decode':    'Decoding finished in {t}.\n\nOutput: {out}\nFrames processed: {fr}',
        'err_title':      'Error',
        'err_encode':     'Encoding failed after {t}.',
        'err_decode':     'Decoding failed after {t}.',
    },
    'ru': {
        'encode': 'Кодировка', 'decode': 'Раскодировка', 'settings': 'Настройки',
        'input_file': 'Входной файл:', 'output_file': 'Выходной файл (MP4):',
        'output_folder': 'Папка вывода:', 'browse': 'Обзор...',
        'start_encode': 'Начать кодирование', 'start_decode': 'Начать декодирование',
        'encryption_key': 'Ключ шифрования:',
        'no_key': '(оставьте пустым для отключения шифрования)',
        'theme': 'Тема:', 'language': 'Язык:',
        'theme_system': 'Системная', 'theme_dark': 'Тёмная', 'theme_light': 'Светлая',
        'ready': 'Готово',
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
        'stat_elapsed':   'Прошло:',
        'stat_remaining': 'Осталось:',
        'stat_frame':     'Кадр:',
        'stat_blocks':    'Блоков/кадр:',
        'stat_blocksize': 'Размер блока:',
        'stat_filesize':  'Размер файла:',
        'stat_grid':      'Сетка:',
        'stat_fps':       'FPS:',
        'stat_encrypt':   'Шифрование:',
        'stat_on':        'ВКЛ',
        'stat_off':       'ВЫКЛ',
        'done_title':     'Завершено!',
        'done_encode':    'Кодирование завершено за {t}.\n\nФайл: {out}\nРазмер: {sz}\nКадров: {fr}\nДлительность: {dur}',
        'done_decode':    'Декодирование завершено за {t}.\n\nФайл: {out}\nОбработано кадров: {fr}',
        'err_title':      'Ошибка',
        'err_encode':     'Кодирование завершилось с ошибкой за {t}.',
        'err_decode':     'Декодирование завершилось с ошибкой за {t}.',
    },
    'uk': {
        'encode': 'Кодування', 'decode': 'Декодування', 'settings': 'Налаштування',
        'input_file': 'Вхідний файл:', 'output_file': 'Вихідний файл (MP4):',
        'output_folder': 'Папка виводу:', 'browse': 'Огляд...',
        'start_encode': 'Почати кодування', 'start_decode': 'Почати декодування',
        'encryption_key': 'Ключ шифрування:',
        'no_key': '(залиште порожнім для вимкнення шифрування)',
        'theme': 'Тема:', 'language': 'Мова:',
        'theme_system': 'Системна', 'theme_dark': 'Темна', 'theme_light': 'Світла',
        'ready': 'Готово',
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
        'stat_elapsed':   'Минуло:',
        'stat_remaining': 'Залишилось:',
        'stat_frame':     'Кадр:',
        'stat_blocks':    'Блоків/кадр:',
        'stat_blocksize': 'Розмір блоку:',
        'stat_filesize':  'Розмір файлу:',
        'stat_grid':      'Сітка:',
        'stat_fps':       'FPS:',
        'stat_encrypt':   'Шифрування:',
        'stat_on':        'УВМ',
        'stat_off':       'ВИМК',
        'done_title':     'Завершено!',
        'done_encode':    'Кодування завершено за {t}.\n\nФайл: {out}\nРозмір: {sz}\nКадрів: {fr}\nТривалість: {dur}',
        'done_decode':    'Декодування завершено за {t}.\n\nФайл: {out}\nОброблено кадрів: {fr}',
        'err_title':      'Помилка',
        'err_encode':     'Кодування завершилося з помилкою за {t}.',
        'err_decode':     'Декодування завершилося з помилкою за {t}.',
    },
    'de': {
        'encode': 'Kodieren', 'decode': 'Dekodieren', 'settings': 'Einstellungen',
        'input_file': 'Eingabedatei:', 'output_file': 'Ausgabedatei (MP4):',
        'output_folder': 'Ausgabeordner:', 'browse': 'Durchsuchen...',
        'start_encode': 'Kodierung starten', 'start_decode': 'Dekodierung starten',
        'encryption_key': 'Verschlüsselungsschlüssel:',
        'no_key': '(leer lassen zum Deaktivieren)',
        'theme': 'Thema:', 'language': 'Sprache:',
        'theme_system': 'System', 'theme_dark': 'Dunkel', 'theme_light': 'Hell',
        'ready': 'Bereit',
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
        'stat_elapsed':   'Vergangen:',
        'stat_remaining': 'Verbleibend:',
        'stat_frame':     'Frame:',
        'stat_blocks':    'Blöcke/Frame:',
        'stat_blocksize': 'Blockgröße:',
        'stat_filesize':  'Dateigröße:',
        'stat_grid':      'Gitter:',
        'stat_fps':       'FPS:',
        'stat_encrypt':   'Verschlüsselung:',
        'stat_on':        'AN',
        'stat_off':       'AUS',
        'done_title':     'Abgeschlossen!',
        'done_encode':    'Kodierung abgeschlossen in {t}.\n\nDatei: {out}\nGröße: {sz}\nFrames: {fr}\nDauer: {dur}',
        'done_decode':    'Dekodierung abgeschlossen in {t}.\n\nDatei: {out}\nFrames verarbeitet: {fr}',
        'err_title':      'Fehler',
        'err_encode':     'Kodierung fehlgeschlagen nach {t}.',
        'err_decode':     'Dekodierung fehlgeschlagen nach {t}.',
    },
    'fr': {
        'encode': 'Encoder', 'decode': 'Décoder', 'settings': 'Paramètres',
        'input_file': "Fichier d'entrée:", 'output_file': 'Fichier de sortie (MP4):',
        'output_folder': 'Dossier de sortie:', 'browse': 'Parcourir...',
        'start_encode': "Démarrer l'encodage", 'start_decode': 'Démarrer le décodage',
        'encryption_key': 'Clé de chiffrement:',
        'no_key': '(laisser vide pour désactiver)',
        'theme': 'Thème:', 'language': 'Langue:',
        'theme_system': 'Système', 'theme_dark': 'Sombre', 'theme_light': 'Clair',
        'ready': 'Prêt',
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
        'stat_elapsed':   'Écoulé:',
        'stat_remaining': 'Restant:',
        'stat_frame':     'Image:',
        'stat_blocks':    'Blocs/image:',
        'stat_blocksize': 'Taille bloc:',
        'stat_filesize':  'Taille fichier:',
        'stat_grid':      'Grille:',
        'stat_fps':       'FPS:',
        'stat_encrypt':   'Chiffrement:',
        'stat_on':        'OUI',
        'stat_off':       'NON',
        'done_title':     'Terminé!',
        'done_encode':    'Encodage terminé en {t}.\n\nFichier: {out}\nTaille: {sz}\nImages: {fr}\nDurée: {dur}',
        'done_decode':    'Décodage terminé en {t}.\n\nFichier: {out}\nImages traitées: {fr}',
        'err_title':      'Erreur',
        'err_encode':     'Encodage échoué après {t}.',
        'err_decode':     'Décodage échoué après {t}.',
    },
    'es': {
        'encode': 'Codificar', 'decode': 'Decodificar', 'settings': 'Configuración',
        'input_file': 'Archivo de entrada:', 'output_file': 'Archivo de salida (MP4):',
        'output_folder': 'Carpeta de salida:', 'browse': 'Examinar...',
        'start_encode': 'Iniciar codificación', 'start_decode': 'Iniciar decodificación',
        'encryption_key': 'Clave de cifrado:',
        'no_key': '(dejar vacío para desactivar)',
        'theme': 'Tema:', 'language': 'Idioma:',
        'theme_system': 'Sistema', 'theme_dark': 'Oscuro', 'theme_light': 'Claro',
        'ready': 'Listo',
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
        'stat_elapsed':   'Transcurrido:',
        'stat_remaining': 'Restante:',
        'stat_frame':     'Fotograma:',
        'stat_blocks':    'Bloques/fotograma:',
        'stat_blocksize': 'Tamaño bloque:',
        'stat_filesize':  'Tamaño archivo:',
        'stat_grid':      'Cuadrícula:',
        'stat_fps':       'FPS:',
        'stat_encrypt':   'Cifrado:',
        'stat_on':        'SÍ',
        'stat_off':       'NO',
        'done_title':     '¡Completado!',
        'done_encode':    'Codificación completada en {t}.\n\nArchivo: {out}\nTamaño: {sz}\nFotogramas: {fr}\nDuración: {dur}',
        'done_decode':    'Decodificación completada en {t}.\n\nArchivo: {out}\nFotogramas procesados: {fr}',
        'err_title':      'Error',
        'err_encode':     'Codificación fallida tras {t}.',
        'err_decode':     'Decodificación fallida tras {t}.',
    },
    'pl': {
        'encode': 'Kodowanie', 'decode': 'Dekodowanie', 'settings': 'Ustawienia',
        'input_file': 'Plik wejściowy:', 'output_file': 'Plik wyjściowy (MP4):',
        'output_folder': 'Folder wyjściowy:', 'browse': 'Przeglądaj...',
        'start_encode': 'Rozpocznij kodowanie', 'start_decode': 'Rozpocznij dekodowanie',
        'encryption_key': 'Klucz szyfrowania:',
        'no_key': '(pozostaw puste aby wyłączyć)',
        'theme': 'Motyw:', 'language': 'Język:',
        'theme_system': 'Systemowy', 'theme_dark': 'Ciemny', 'theme_light': 'Jasny',
        'ready': 'Gotowe',
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
        'stat_elapsed':   'Upłynęło:',
        'stat_remaining': 'Pozostało:',
        'stat_frame':     'Klatka:',
        'stat_blocks':    'Bloki/klatka:',
        'stat_blocksize': 'Rozmiar bloku:',
        'stat_filesize':  'Rozmiar pliku:',
        'stat_grid':      'Siatka:',
        'stat_fps':       'FPS:',
        'stat_encrypt':   'Szyfrowanie:',
        'stat_on':        'WŁ',
        'stat_off':       'WYŁ',
        'done_title':     'Gotowe!',
        'done_encode':    'Kodowanie zakończone w {t}.\n\nPlik: {out}\nRozmiar: {sz}\nKlatki: {fr}\nCzas trwania: {dur}',
        'done_decode':    'Dekodowanie zakończone w {t}.\n\nPlik: {out}\nPrzetworzone klatki: {fr}',
        'err_title':      'Błąd',
        'err_encode':     'Kodowanie nieudane po {t}.',
        'err_decode':     'Dekodowanie nieudane po {t}.',
    },
    'pt': {
        'encode': 'Codificar', 'decode': 'Decodificar', 'settings': 'Configurações',
        'input_file': 'Arquivo de entrada:', 'output_file': 'Arquivo de saída (MP4):',
        'output_folder': 'Pasta de saída:', 'browse': 'Procurar...',
        'start_encode': 'Iniciar codificação', 'start_decode': 'Iniciar decodificação',
        'encryption_key': 'Chave de criptografia:',
        'no_key': '(deixe vazio para desativar)',
        'theme': 'Tema:', 'language': 'Idioma:',
        'theme_system': 'Sistema', 'theme_dark': 'Escuro', 'theme_light': 'Claro',
        'ready': 'Pronto',
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
        'stat_elapsed':   'Decorrido:',
        'stat_remaining': 'Restante:',
        'stat_frame':     'Quadro:',
        'stat_blocks':    'Blocos/quadro:',
        'stat_blocksize': 'Tamanho bloco:',
        'stat_filesize':  'Tamanho arquivo:',
        'stat_grid':      'Grade:',
        'stat_fps':       'FPS:',
        'stat_encrypt':   'Criptografia:',
        'stat_on':        'SIM',
        'stat_off':       'NÃO',
        'done_title':     'Concluído!',
        'done_encode':    'Codificação concluída em {t}.\n\nArquivo: {out}\nTamanho: {sz}\nQuadros: {fr}\nDuração: {dur}',
        'done_decode':    'Decodificação concluída em {t}.\n\nArquivo: {out}\nQuadros processados: {fr}',
        'err_title':      'Erro',
        'err_encode':     'Codificação falhou após {t}.',
        'err_decode':     'Decodificação falhou após {t}.',
    },
    'it': {
        'encode': 'Codifica', 'decode': 'Decodifica', 'settings': 'Impostazioni',
        'input_file': 'File di input:', 'output_file': 'File di output (MP4):',
        'output_folder': 'Cartella di output:', 'browse': 'Sfoglia...',
        'start_encode': 'Avvia codifica', 'start_decode': 'Avvia decodifica',
        'encryption_key': 'Chiave di cifratura:',
        'no_key': '(lascia vuoto per disabilitare)',
        'theme': 'Tema:', 'language': 'Lingua:',
        'theme_system': 'Sistema', 'theme_dark': 'Scuro', 'theme_light': 'Chiaro',
        'ready': 'Pronto',
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
        'stat_elapsed':   'Trascorso:',
        'stat_remaining': 'Rimanente:',
        'stat_frame':     'Frame:',
        'stat_blocks':    'Blocchi/frame:',
        'stat_blocksize': 'Dim. blocco:',
        'stat_filesize':  'Dim. file:',
        'stat_grid':      'Griglia:',
        'stat_fps':       'FPS:',
        'stat_encrypt':   'Cifratura:',
        'stat_on':        'SÌ',
        'stat_off':       'NO',
        'done_title':     'Completato!',
        'done_encode':    'Codifica completata in {t}.\n\nFile: {out}\nDimensione: {sz}\nFrame: {fr}\nDurata: {dur}',
        'done_decode':    'Decodifica completata in {t}.\n\nFile: {out}\nFrame elaborati: {fr}',
        'err_title':      'Errore',
        'err_encode':     'Codifica fallita dopo {t}.',
        'err_decode':     'Decodifica fallita dopo {t}.',
    },
    'zh': {
        'encode': '编码', 'decode': '解码', 'settings': '设置',
        'input_file': '输入文件：', 'output_file': '输出文件（MP4）：',
        'output_folder': '输出文件夹：', 'browse': '浏览...',
        'start_encode': '开始编码', 'start_decode': '开始解码',
        'encryption_key': '加密密钥：',
        'no_key': '（留空以禁用加密）',
        'theme': '主题：', 'language': '语言：',
        'theme_system': '系统', 'theme_dark': '深色', 'theme_light': '浅色',
        'ready': '就绪',
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
        'stat_elapsed':   '已用时：',
        'stat_remaining': '剩余：',
        'stat_frame':     '帧：',
        'stat_blocks':    '块/帧：',
        'stat_blocksize': '块大小：',
        'stat_filesize':  '文件大小：',
        'stat_grid':      '网格：',
        'stat_fps':       '帧率：',
        'stat_encrypt':   '加密：',
        'stat_on':        '开',
        'stat_off':       '关',
        'done_title':     '完成！',
        'done_encode':    '编码完成，用时 {t}。\n\n文件：{out}\n大小：{sz}\n帧数：{fr}\n时长：{dur}',
        'done_decode':    '解码完成，用时 {t}。\n\n文件：{out}\n处理帧数：{fr}',
        'err_title':      '错误',
        'err_encode':     '编码失败，用时 {t}。',
        'err_decode':     '解码失败，用时 {t}。',
    },
    'ja': {
        'encode': 'エンコード', 'decode': 'デコード', 'settings': '設定',
        'input_file': '入力ファイル：', 'output_file': '出力ファイル（MP4）：',
        'output_folder': '出力フォルダ：', 'browse': '参照...',
        'start_encode': 'エンコード開始', 'start_decode': 'デコード開始',
        'encryption_key': '暗号化キー：',
        'no_key': '（空欄で暗号化を無効化）',
        'theme': 'テーマ：', 'language': '言語：',
        'theme_system': 'システム', 'theme_dark': 'ダーク', 'theme_light': 'ライト',
        'ready': '準備完了',
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
        'stat_elapsed':   '経過：',
        'stat_remaining': '残り：',
        'stat_frame':     'フレーム：',
        'stat_blocks':    'ブロック/フレーム：',
        'stat_blocksize': 'ブロックサイズ：',
        'stat_filesize':  'ファイルサイズ：',
        'stat_grid':      'グリッド：',
        'stat_fps':       'FPS：',
        'stat_encrypt':   '暗号化：',
        'stat_on':        'ON',
        'stat_off':       'OFF',
        'done_title':     '完了！',
        'done_encode':    'エンコード完了（{t}）。\n\nファイル：{out}\nサイズ：{sz}\nフレーム：{fr}\n長さ：{dur}',
        'done_decode':    'デコード完了（{t}）。\n\nファイル：{out}\n処理フレーム：{fr}',
        'err_title':      'エラー',
        'err_encode':     'エンコード失敗（{t}）。',
        'err_decode':     'デコード失敗（{t}）。',
    },
    'ko': {
        'encode': '인코드', 'decode': '디코드', 'settings': '설정',
        'input_file': '입력 파일:', 'output_file': '출력 파일 (MP4):',
        'output_folder': '출력 폴더:', 'browse': '찾아보기...',
        'start_encode': '인코딩 시작', 'start_decode': '디코딩 시작',
        'encryption_key': '암호화 키:',
        'no_key': '(비워두면 암호화 비활성화)',
        'theme': '테마:', 'language': '언어:',
        'theme_system': '시스템', 'theme_dark': '어두운', 'theme_light': '밝은',
        'ready': '준비',
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
        'stat_elapsed':   '경과:',
        'stat_remaining': '남은 시간:',
        'stat_frame':     '프레임:',
        'stat_blocks':    '블록/프레임:',
        'stat_blocksize': '블록 크기:',
        'stat_filesize':  '파일 크기:',
        'stat_grid':      '격자:',
        'stat_fps':       'FPS:',
        'stat_encrypt':   '암호화:',
        'stat_on':        'ON',
        'stat_off':       'OFF',
        'done_title':     '완료!',
        'done_encode':    '인코딩 완료 ({t}).\n\n파일: {out}\n크기: {sz}\n프레임: {fr}\n길이: {dur}',
        'done_decode':    '디코딩 완료 ({t}).\n\n파일: {out}\n처리된 프레임: {fr}',
        'err_title':      '오류',
        'err_encode':     '인코딩 실패 ({t}).',
        'err_decode':     '디코딩 실패 ({t}).',
    },
}

LANGUAGE_NAMES = {
    'en': 'English', 'ru': 'Русский', 'uk': 'Українська',
    'de': 'Deutsch', 'fr': 'Français', 'es': 'Español',
    'pl': 'Polski', 'pt': 'Português', 'it': 'Italiano',
    'zh': '中文', 'ja': '日本語', 'ko': '한국어',
}
LANG_ORDER = ['en', 'ru', 'uk', 'de', 'fr', 'es', 'pl', 'pt', 'it', 'zh', 'ja', 'ko']


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
            self.blocks_x = (self.width - 2 * self.marker_size) // (self.block_width + self.spacing)
            self.blocks_y = (self.height - 2 * self.marker_size) // (self.block_height + self.spacing)
            self.blocks_per_region = self.blocks_x * self.blocks_y
            self.eof_bytes = ("█" * 64).encode('utf-8')

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
            return [''.join(bits[i:i + 4]) for i in range(0, len(bits), 4)]

        def encode(self, input_file, output_file, progress_callback=None):
            with open(input_file, 'rb') as f:
                data = f.read()
            enc_data = self._encrypt_data(data) if self.use_encryption else data
            header = f"FILE:{os.path.basename(input_file)}:SIZE:{len(data)}|"
            all_blocks = (
                self._data_to_blocks(header.encode('latin-1')) +
                self._data_to_blocks(enc_data) +
                self._data_to_blocks(self.eof_bytes)
            )
            data_frames = math.ceil(len(all_blocks) / self.blocks_per_region)
            frames_needed = data_frames + 5
            temp_dir = tempfile.mkdtemp()
            try:
                for frame_num in range(data_frames):
                    if progress_callback:
                        progress_callback(frame_num + 1, frames_needed)
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

                for i in range(5):
                    fn = data_frames + i
                    frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                    frame = self._draw_markers(frame)
                    for y in range(self.blocks_y * 2):
                        for x in range(self.blocks_x * 2):
                            self._draw_block(frame, x, y, (255, 0, 0))
                    cv2.imwrite(os.path.join(temp_dir, f"frame_{fn:05d}.png"), frame)

                if progress_callback:
                    progress_callback(frames_needed, frames_needed)

                try:
                    subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
                    subprocess.run([
                        'ffmpeg', '-framerate', str(self.fps),
                        '-i', os.path.join(temp_dir, 'frame_%05d.png'),
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '23',
                        '-pix_fmt', 'yuv420p', '-an', '-movflags', '+faststart',
                        '-y', output_file
                    ], check=True, capture_output=True)
                except Exception:
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(output_file, fourcc, self.fps, (self.width, self.height))
                    for fn in range(frames_needed):
                        fr = cv2.imread(os.path.join(temp_dir, f"frame_{fn:05d}.png"))
                        if fr is not None:
                            out.write(fr)
                    out.release()
            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)

            if os.path.exists(output_file):
                return True, frames_needed
            return False, frames_needed


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
            self.blocks_x = (self.width - 2 * self.marker_size) // (self.block_width + self.spacing)
            self.blocks_y = (self.height - 2 * self.marker_size) // (self.block_height + self.spacing)
            self.blocks_per_region = self.blocks_x * self.blocks_y
            self._precompute_coords()

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
                return self.color_cache[key]
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
                bs = bits[i:i + 8]
                if len(bs) == 8:
                    try:
                        result.append(int(bs, 2))
                    except Exception:
                        result.append(0)
            return result

        def _find_eof(self, data):
            eof = b'\xe2\x96\x88' * 64
            for i in range(len(data) - len(eof)):
                if data[i:i + len(eof)] == eof:
                    return i
            return -1

        def decode(self, video_file, output_dir='.', progress_callback=None):
            if not os.path.exists(video_file):
                return False, 0, None
            cap = cv2.VideoCapture(video_file)
            if not cap.isOpened():
                return False, 0, None
            total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            all_blocks = []
            done = 0
            for fn in range(total):
                ret, frame = cap.read()
                if not ret:
                    break
                done += 1
                if progress_callback:
                    progress_callback(fn + 1, total)
                all_blocks.extend(self.decode_frame(frame))
            cap.release()
            data = self._blocks_to_bytes(all_blocks)
            eof_pos = self._find_eof(data)
            if eof_pos > 0:
                data = data[:eof_pos]
            match = re.search(r'FILE:([^:]+):SIZE:(\d+)\|',
                              data[:1000].decode('latin-1', errors='ignore'))
            out_path = None
            if match:
                filename = match.group(1)
                filesize = int(match.group(2))
                hb = match.group(0).encode('latin-1')
                hp = data.find(hb)
                if hp >= 0:
                    enc = data[hp + len(hb): hp + len(hb) + filesize]
                    fdata = self._decrypt_data(enc) if self.key else enc
                    out_path = os.path.join(output_dir, filename)
                    base, ext = os.path.splitext(filename)
                    n = 1
                    while os.path.exists(out_path):
                        out_path = os.path.join(output_dir, f"{base}_{n}{ext}")
                        n += 1
                    with open(out_path, 'wb') as f:
                        f.write(fdata)
                    return True, done, out_path
            out_path = os.path.join(output_dir, "decoded_data.bin")
            with open(out_path, 'wb') as f:
                f.write(data)
            return False, done, out_path


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def fmt_time(seconds):
    """Format seconds as MM:SS or HH:MM:SS."""
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def fmt_size(nbytes):
    """Human-readable file size."""
    if nbytes < 1024:
        return f"{nbytes} B"
    elif nbytes < 1024 ** 2:
        return f"{nbytes / 1024:.1f} KB"
    elif nbytes < 1024 ** 3:
        return f"{nbytes / 1024 ** 2:.2f} MB"
    return f"{nbytes / 1024 ** 3:.2f} GB"


# ─────────────────────────────────────────────────────────────────────────────
# APPLICATION
# ─────────────────────────────────────────────────────────────────────────────

class FileToVideoApp:
    # ── static encoder params (match YouTubeEncoder defaults) ────────────────
    _BLOCK_W = 24
    _BLOCK_H = 16
    _SPACING = 4
    _MARKER  = 80
    _FPS     = 6
    _VW, _VH = 1920, 1080

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FileToVideo")
        self.root.geometry("660x420")
        self.root.minsize(520, 360)
        self.root.resizable(False, False)

        self.current_lang = 'ru'
        self._key_visible = False
        self.is_running   = False
        self.active_tab   = 'encode'

        # task state
        self._start_time   = None
        self._timer_id     = None
        self._cur_frame    = 0
        self._tot_frames   = 0
        self._active_mode  = None   # 'encode' | 'decode'

        # computed grid info (constant)
        bx = (self._VW - 2 * self._MARKER) // (self._BLOCK_W + self._SPACING)
        by = (self._VH - 2 * self._MARKER) // (self._BLOCK_H + self._SPACING)
        self._grid_str  = f"{bx} × {by}"
        self._bpf_str   = str(bx * by)
        self._bsize_str = f"{self._BLOCK_W}×{self._BLOCK_H} px"

        # string vars
        self.enc_in_var  = tk.StringVar()
        self.enc_out_var = tk.StringVar()
        self.dec_in_var  = tk.StringVar()
        self.dec_out_var = tk.StringVar()
        self.key_var     = tk.StringVar()
        self.lang_var    = tk.StringVar(value=LANGUAGE_NAMES['ru'])

        self.enc_progress_var = tk.DoubleVar(value=0.0)
        self.dec_progress_var = tk.DoubleVar(value=0.0)

        # dynamic stat StringVars
        self.enc_elapsed_var   = tk.StringVar(value="--:--")
        self.enc_remaining_var = tk.StringVar(value="--:--")
        self.enc_frame_var     = tk.StringVar(value="—")
        self.enc_filesize_var  = tk.StringVar(value="—")
        self.enc_encrypt_var   = tk.StringVar(value="—")

        self.dec_elapsed_var   = tk.StringVar(value="--:--")
        self.dec_remaining_var = tk.StringVar(value="--:--")
        self.dec_frame_var     = tk.StringVar(value="—")
        self.dec_encrypt_var   = tk.StringVar(value="—")

        self.display_to_code = {LANGUAGE_NAMES[c]: c for c in LANG_ORDER}

        self._load_icon()
        self._build_ui()
        self._apply_language()
        self._show_tab('encode')

        self.root.mainloop()

    # ── icon ──────────────────────────────────────────────────────────────────

    def _load_icon(self):
        try:
            base = os.path.dirname(os.path.abspath(__file__))
            ico = os.path.join(base, 'DATA', 'ico.ico')
            if os.path.exists(ico):
                self.root.iconbitmap(ico)
        except Exception:
            pass

    def t(self, key):
        return TRANSLATIONS.get(self.current_lang, TRANSLATIONS['en']).get(
            key, TRANSLATIONS['en'].get(key, key))

    # ── live timer (called from main thread via after()) ──────────────────────

    def _tick(self):
        if not self.is_running:
            return
        elapsed = time.time() - self._start_time
        ef = fmt_time(elapsed)

        # estimate remaining
        rf = "—"
        if self._tot_frames > 0 and self._cur_frame > 0:
            rate = self._cur_frame / elapsed
            rem  = (self._tot_frames - self._cur_frame) / rate
            rf   = "~" + fmt_time(rem)

        fstr = f"{self._cur_frame} / {self._tot_frames}" if self._tot_frames else "—"

        if self._active_mode == 'encode':
            self.enc_elapsed_var.set(ef)
            self.enc_remaining_var.set(rf)
            self.enc_frame_var.set(fstr)
        else:
            self.dec_elapsed_var.set(ef)
            self.dec_remaining_var.set(rf)
            self.dec_frame_var.set(fstr)

        self._timer_id = self.root.after(500, self._tick)

    def _start_timer(self, mode):
        self._active_mode = mode
        self._start_time  = time.time()
        self._cur_frame   = 0
        self._tot_frames  = 0
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
        self._timer_id = self.root.after(500, self._tick)

    def _stop_timer(self):
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None

    # ── progress callbacks (safe from worker thread) ──────────────────────────

    def _make_enc_progress_cb(self):
        def cb(current, total):
            pct = (current / total * 100.0) if total > 0 else 0.0
            self._cur_frame  = current
            self._tot_frames = total
            self.root.after(0, lambda p=pct: self.enc_progress_var.set(p))
        return cb

    def _make_dec_progress_cb(self):
        def cb(current, total):
            pct = (current / total * 100.0) if total > 0 else 0.0
            self._cur_frame  = current
            self._tot_frames = total
            self.root.after(0, lambda p=pct: self.dec_progress_var.set(p))
        return cb

    # ── build ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Tab bar
        self.tab_bar = tk.Frame(self.root, relief='flat', bd=0)
        self.tab_bar.grid(row=0, column=0, sticky='ew', padx=2, pady=(4, 0))

        self._tab_btns = {}
        for name in ('encode', 'decode', 'settings'):
            b = tk.Button(self.tab_bar, command=lambda n=name: self._show_tab(n))
            b.pack(side='left', padx=2, pady=2)
            self._tab_btns[name] = b

        # Content area
        self.content_host = tk.Frame(self.root)
        self.content_host.grid(row=1, column=0, sticky='nsew', padx=4, pady=4)
        self.content_host.columnconfigure(0, weight=1)
        self.content_host.rowconfigure(0, weight=1)

        self._tabs = {}
        self._tabs['encode']   = self._build_encode_tab()
        self._tabs['decode']   = self._build_decode_tab()
        self._tabs['settings'] = self._build_settings_tab()

        for f in self._tabs.values():
            f.place(in_=self.content_host, relwidth=1, relheight=1)

        self._build_footer()

    # ── encode tab ────────────────────────────────────────────────────────────

    def _build_encode_tab(self):
        f = tk.Frame(self.content_host)
        f.columnconfigure(1, weight=1)

        # Input file
        self.enc_in_lbl = tk.Label(f)
        self.enc_in_lbl.grid(row=0, column=0, sticky='w', padx=(8, 4), pady=(10, 3))
        tk.Entry(f, textvariable=self.enc_in_var).grid(row=0, column=1, sticky='ew', pady=(10, 3))
        self.enc_in_btn = tk.Button(f, command=self._browse_enc_in)
        self.enc_in_btn.grid(row=0, column=2, padx=(4, 8), pady=(10, 3))

        # Output file
        self.enc_out_lbl = tk.Label(f)
        self.enc_out_lbl.grid(row=1, column=0, sticky='w', padx=(8, 4), pady=3)
        tk.Entry(f, textvariable=self.enc_out_var).grid(row=1, column=1, sticky='ew', pady=3)
        self.enc_out_btn = tk.Button(f, command=self._browse_enc_out)
        self.enc_out_btn.grid(row=1, column=2, padx=(4, 8), pady=3)

        # Encryption key
        self.enc_key_lbl = tk.Label(f)
        self.enc_key_lbl.grid(row=2, column=0, sticky='w', padx=(8, 4), pady=3)
        kf = tk.Frame(f)
        kf.grid(row=2, column=1, sticky='ew', pady=3)
        kf.columnconfigure(0, weight=1)
        self.enc_key_entry = tk.Entry(kf, textvariable=self.key_var, show='*')
        self.enc_key_entry.grid(row=0, column=0, sticky='ew')
        self.enc_key_note = tk.Label(kf, font=('TkDefaultFont', 7))
        self.enc_key_note.grid(row=1, column=0, sticky='w')
        kb = tk.Frame(f)
        kb.grid(row=2, column=2, padx=(4, 8), pady=3)
        self.enc_show_btn = tk.Button(kb, width=6, command=self._toggle_key)
        self.enc_show_btn.pack(side='left', padx=(0, 2))
        self.enc_load_btn = tk.Button(kb, command=self._load_key_file)
        self.enc_load_btn.pack(side='left')

        # Start + status
        sf = tk.Frame(f)
        sf.grid(row=3, column=0, columnspan=3, sticky='w', padx=8, pady=(8, 2))
        self.enc_start_btn = tk.Button(sf, command=self._start_encode)
        self.enc_start_btn.pack(side='left', padx=(0, 10))
        self.enc_status_lbl = tk.Label(sf, font=('TkDefaultFont', 8))
        self.enc_status_lbl.pack(side='left')
        self.enc_status_val = tk.Label(sf, font=('TkDefaultFont', 8))
        self.enc_status_val.pack(side='left')

        # Progress bar
        self.enc_progress = ttk.Progressbar(
            f, variable=self.enc_progress_var, maximum=100,
            mode='determinate', length=300)
        self.enc_progress.grid(row=4, column=0, columnspan=3,
                               sticky='ew', padx=8, pady=(2, 4))

        # ── Stats panel ──────────────────────────────────────────────────────
        sf2 = tk.LabelFrame(f, padx=6, pady=4)
        sf2.grid(row=5, column=0, columnspan=3, sticky='ew', padx=8, pady=(0, 8))
        sf2.columnconfigure(1, weight=1)
        sf2.columnconfigure(3, weight=1)
        self._enc_stat_frame = sf2

        def _slbl(parent, r, c, tvar):
            """Stat label pair: bold key + value."""
            lbl = tk.Label(parent, anchor='e', font=('TkDefaultFont', 8, 'bold'))
            lbl.grid(row=r, column=c, sticky='e', padx=(4, 2))
            val = tk.Label(parent, textvariable=tvar, anchor='w',
                           font=('TkDefaultFont', 8))
            val.grid(row=r, column=c + 1, sticky='w', padx=(0, 10))
            return lbl

        _sv = tk.StringVar(value=f"{self._BLOCK_W}×{self._BLOCK_H} px")
        _gv = tk.StringVar(value=self._grid_str)
        _bv = tk.StringVar(value=self._bpf_str)
        _fv = tk.StringVar(value=f"{self._FPS}")

        self._enc_lbl_elapsed   = _slbl(sf2, 0, 0, self.enc_elapsed_var)
        self._enc_lbl_remaining = _slbl(sf2, 0, 2, self.enc_remaining_var)
        self._enc_lbl_frame     = _slbl(sf2, 1, 0, self.enc_frame_var)
        self._enc_lbl_filesize  = _slbl(sf2, 1, 2, self.enc_filesize_var)
        self._enc_lbl_blocksize = _slbl(sf2, 2, 0, _sv)
        self._enc_lbl_grid      = _slbl(sf2, 2, 2, _gv)
        self._enc_lbl_blocks    = _slbl(sf2, 3, 0, _bv)
        self._enc_lbl_fps       = _slbl(sf2, 3, 2, _fv)
        self._enc_lbl_encrypt   = _slbl(sf2, 4, 0, self.enc_encrypt_var)

        # keep fixed vars for re-labelling
        self._enc_sv_fixed = [_sv, _gv, _bv, _fv]
        return f

    # ── decode tab ────────────────────────────────────────────────────────────

    def _build_decode_tab(self):
        f = tk.Frame(self.content_host)
        f.columnconfigure(1, weight=1)

        self.dec_in_lbl = tk.Label(f)
        self.dec_in_lbl.grid(row=0, column=0, sticky='w', padx=(8, 4), pady=(10, 3))
        tk.Entry(f, textvariable=self.dec_in_var).grid(row=0, column=1, sticky='ew', pady=(10, 3))
        self.dec_in_btn = tk.Button(f, command=self._browse_dec_in)
        self.dec_in_btn.grid(row=0, column=2, padx=(4, 8), pady=(10, 3))

        self.dec_out_lbl = tk.Label(f)
        self.dec_out_lbl.grid(row=1, column=0, sticky='w', padx=(8, 4), pady=3)
        tk.Entry(f, textvariable=self.dec_out_var).grid(row=1, column=1, sticky='ew', pady=3)
        self.dec_out_btn = tk.Button(f, command=self._browse_dec_out)
        self.dec_out_btn.grid(row=1, column=2, padx=(4, 8), pady=3)

        self.dec_key_lbl = tk.Label(f)
        self.dec_key_lbl.grid(row=2, column=0, sticky='w', padx=(8, 4), pady=3)
        kf2 = tk.Frame(f)
        kf2.grid(row=2, column=1, sticky='ew', pady=3)
        kf2.columnconfigure(0, weight=1)
        self.dec_key_entry = tk.Entry(kf2, textvariable=self.key_var, show='*')
        self.dec_key_entry.grid(row=0, column=0, sticky='ew')
        self.dec_key_note = tk.Label(kf2, font=('TkDefaultFont', 7))
        self.dec_key_note.grid(row=1, column=0, sticky='w')
        kb2 = tk.Frame(f)
        kb2.grid(row=2, column=2, padx=(4, 8), pady=3)
        self.dec_show_btn = tk.Button(kb2, width=6, command=self._toggle_key)
        self.dec_show_btn.pack(side='left', padx=(0, 2))
        self.dec_load_btn = tk.Button(kb2, command=self._load_key_file)
        self.dec_load_btn.pack(side='left')

        sf = tk.Frame(f)
        sf.grid(row=3, column=0, columnspan=3, sticky='w', padx=8, pady=(8, 2))
        self.dec_start_btn = tk.Button(sf, command=self._start_decode)
        self.dec_start_btn.pack(side='left', padx=(0, 10))
        self.dec_status_lbl = tk.Label(sf, font=('TkDefaultFont', 8))
        self.dec_status_lbl.pack(side='left')
        self.dec_status_val = tk.Label(sf, font=('TkDefaultFont', 8))
        self.dec_status_val.pack(side='left')

        self.dec_progress = ttk.Progressbar(
            f, variable=self.dec_progress_var, maximum=100,
            mode='determinate', length=300)
        self.dec_progress.grid(row=4, column=0, columnspan=3,
                               sticky='ew', padx=8, pady=(2, 4))

        # ── Stats panel ──────────────────────────────────────────────────────
        sf2 = tk.LabelFrame(f, padx=6, pady=4)
        sf2.grid(row=5, column=0, columnspan=3, sticky='ew', padx=8, pady=(0, 8))
        sf2.columnconfigure(1, weight=1)
        sf2.columnconfigure(3, weight=1)
        self._dec_stat_frame = sf2

        def _slbl(parent, r, c, tvar):
            lbl = tk.Label(parent, anchor='e', font=('TkDefaultFont', 8, 'bold'))
            lbl.grid(row=r, column=c, sticky='e', padx=(4, 2))
            val = tk.Label(parent, textvariable=tvar, anchor='w',
                           font=('TkDefaultFont', 8))
            val.grid(row=r, column=c + 1, sticky='w', padx=(0, 10))
            return lbl

        _sv = tk.StringVar(value=f"{self._BLOCK_W}×{self._BLOCK_H} px")
        _gv = tk.StringVar(value=self._grid_str)
        _bv = tk.StringVar(value=self._bpf_str)

        self._dec_lbl_elapsed   = _slbl(sf2, 0, 0, self.dec_elapsed_var)
        self._dec_lbl_remaining = _slbl(sf2, 0, 2, self.dec_remaining_var)
        self._dec_lbl_frame     = _slbl(sf2, 1, 0, self.dec_frame_var)
        self._dec_lbl_blocksize = _slbl(sf2, 1, 2, _sv)
        self._dec_lbl_grid      = _slbl(sf2, 2, 0, _gv)
        self._dec_lbl_blocks    = _slbl(sf2, 2, 2, _bv)
        self._dec_lbl_encrypt   = _slbl(sf2, 3, 0, self.dec_encrypt_var)

        self._dec_sv_fixed = [_sv, _gv, _bv]
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

    # ── footer ────────────────────────────────────────────────────────────────

    def _build_footer(self):
        self.footer = tk.Frame(self.root, relief='sunken', bd=1)
        self.footer.grid(row=2, column=0, sticky='ew')
        tk.Label(self.footer, text='Original code by KorocheVolgin: ',
                 font=('TkDefaultFont', 7)).pack(side='left', padx=(6, 0), pady=2)
        lnk1 = tk.Label(self.footer,
                         text='https://github.com/KorocheVolgin/YouTube-Cloude/',
                         font=('TkDefaultFont', 7, 'underline'), cursor='hand2')
        lnk1.pack(side='left', pady=2)
        lnk1.bind('<Button-1>',
                  lambda e: webbrowser.open('https://github.com/KorocheVolgin/YouTube-Cloude/'))
        tk.Label(self.footer, text='    UI and additional by BlackCAT304: ',
                 font=('TkDefaultFont', 7)).pack(side='left', pady=2)
        lnk2 = tk.Label(self.footer,
                         text='https://github.com/BlackCAT304-RT/FileToVideo',
                         font=('TkDefaultFont', 7, 'underline'), cursor='hand2')
        lnk2.pack(side='left', pady=2)
        lnk2.bind('<Button-1>',
                  lambda e: webbrowser.open('https://github.com/BlackCAT304-RT/FileToVideo'))

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
            # update file size stat immediately
            try:
                sz = os.path.getsize(p)
                self.enc_filesize_var.set(fmt_size(sz))
            except Exception:
                pass
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
            except Exception as e:
                messagebox.showerror("FileToVideo", str(e))

    # ── encode ────────────────────────────────────────────────────────────────

    def _start_encode(self):
        if self.is_running:
            return
        if not BACKEND_AVAILABLE:
            messagebox.showerror("FileToVideo", f"Backend not available — {_BACKEND_ERROR}")
            return
        inp = self.enc_in_var.get().strip()
        out = self.enc_out_var.get().strip()
        if not inp:
            messagebox.showwarning("FileToVideo", self.t('select_input'))
            return
        if not out:
            out = os.path.splitext(inp)[0] + '_encoded.mp4'
            self.enc_out_var.set(out)

        key = self.key_var.get().strip() or None

        # update encrypt stat
        enc_str = self.t('stat_on') if key else self.t('stat_off')
        self.enc_encrypt_var.set(enc_str)

        # update file size
        try:
            self.enc_filesize_var.set(fmt_size(os.path.getsize(inp)))
        except Exception:
            self.enc_filesize_var.set("—")

        self.enc_progress_var.set(0.0)
        self.enc_elapsed_var.set("00:00")
        self.enc_remaining_var.set("--:--")
        self.enc_frame_var.set("—")

        self._set_busy(True, 'encoding')
        self._start_timer('encode')

        threading.Thread(
            target=self._run_encode,
            args=(inp, out, key),
            daemon=True
        ).start()

    def _run_encode(self, inp, out, key):
        # suppress all prints from backend
        old_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        ok = False
        frames = 0
        try:
            result = YouTubeEncoder(key).encode(inp, out,
                                                progress_callback=self._make_enc_progress_cb())
            ok, frames = result
        except Exception:
            ok, frames = False, 0
        finally:
            sys.stdout.close()
            sys.stdout = old_stdout

        elapsed = time.time() - self._start_time
        final_pct = 100.0 if ok else 0.0

        def _finish():
            self.enc_progress_var.set(final_pct)
            self._stop_timer()
            self._set_busy(False, 'done' if ok else 'error')
            self._load_icon()

            t_str = fmt_time(elapsed)
            if ok:
                try:
                    sz = fmt_size(os.path.getsize(out))
                except Exception:
                    sz = "—"
                dur = f"{frames / self._FPS:.1f}s"
                msg = self.t('done_encode').format(
                    t=t_str, out=out, sz=sz, fr=frames, dur=dur)
                messagebox.showinfo(self.t('done_title'), msg)
            else:
                msg = self.t('err_encode').format(t=t_str)
                messagebox.showerror(self.t('err_title'), msg)

        self.root.after(0, _finish)

    # ── decode ────────────────────────────────────────────────────────────────

    def _start_decode(self):
        if self.is_running:
            return
        if not BACKEND_AVAILABLE:
            messagebox.showerror("FileToVideo", f"Backend not available — {_BACKEND_ERROR}")
            return
        inp = self.dec_in_var.get().strip()
        if not inp:
            messagebox.showwarning("FileToVideo", self.t('select_input'))
            return

        key = self.key_var.get().strip() or None
        enc_str = self.t('stat_on') if key else self.t('stat_off')
        self.dec_encrypt_var.set(enc_str)

        self.dec_progress_var.set(0.0)
        self.dec_elapsed_var.set("00:00")
        self.dec_remaining_var.set("--:--")
        self.dec_frame_var.set("—")

        self._set_busy(True, 'decoding')
        self._start_timer('decode')

        threading.Thread(
            target=self._run_decode,
            args=(inp, self.dec_out_var.get().strip() or '.', key),
            daemon=True
        ).start()

    def _run_decode(self, inp, out, key):
        old_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        ok = False
        frames = 0
        out_path = None
        try:
            ok, frames, out_path = YouTubeDecoder(key).decode(inp, out,
                                                              progress_callback=self._make_dec_progress_cb())
        except Exception:
            ok, frames, out_path = False, 0, None
        finally:
            sys.stdout.close()
            sys.stdout = old_stdout

        elapsed = time.time() - self._start_time
        final_pct = 100.0 if ok else 0.0

        def _finish():
            self.dec_progress_var.set(final_pct)
            self._stop_timer()
            self._set_busy(False, 'done' if ok else 'error')
            self._load_icon()

            t_str = fmt_time(elapsed)
            if ok or out_path:
                msg = self.t('done_decode').format(
                    t=t_str, out=out_path or out, fr=frames)
                messagebox.showinfo(self.t('done_title'), msg)
            else:
                msg = self.t('err_decode').format(t=t_str)
                messagebox.showerror(self.t('err_title'), msg)

        self.root.after(0, _finish)

    # ── busy state ────────────────────────────────────────────────────────────

    def _set_busy(self, busy, status='ready'):
        self.is_running = busy
        state = 'disabled' if busy else 'normal'
        self.enc_start_btn.config(state=state)
        self.dec_start_btn.config(state=state)
        txt = self.t(status)
        self.enc_status_val.config(text=txt)
        self.dec_status_val.config(text=txt)

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

        # Stat label texts
        self._enc_lbl_elapsed.config(text=self.t('stat_elapsed'))
        self._enc_lbl_remaining.config(text=self.t('stat_remaining'))
        self._enc_lbl_frame.config(text=self.t('stat_frame'))
        self._enc_lbl_filesize.config(text=self.t('stat_filesize'))
        self._enc_lbl_blocksize.config(text=self.t('stat_blocksize'))
        self._enc_lbl_grid.config(text=self.t('stat_grid'))
        self._enc_lbl_blocks.config(text=self.t('stat_blocks'))
        self._enc_lbl_fps.config(text=self.t('stat_fps'))
        self._enc_lbl_encrypt.config(text=self.t('stat_encrypt'))

        self._dec_lbl_elapsed.config(text=self.t('stat_elapsed'))
        self._dec_lbl_remaining.config(text=self.t('stat_remaining'))
        self._dec_lbl_frame.config(text=self.t('stat_frame'))
        self._dec_lbl_blocksize.config(text=self.t('stat_blocksize'))
        self._dec_lbl_grid.config(text=self.t('stat_grid'))
        self._dec_lbl_blocks.config(text=self.t('stat_blocks'))
        self._dec_lbl_encrypt.config(text=self.t('stat_encrypt'))

        self._refresh_tab_btns()


# ─────────────────────────────────────────────────────────────────────────────

def main():
    FileToVideoApp()


if __name__ == '__main__':
    main()
