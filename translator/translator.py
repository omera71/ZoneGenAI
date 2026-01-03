#!/usr/bin/env python3
"""
Translator CLI dengan Multiple Providers Gratis
Author: Your Name
Version: 1.0.0
"""

import argparse
import os
import sys
from typing import List, Dict, Optional, Tuple
import time
from dataclasses import dataclass
from pathlib import Path
from colorama import init, Fore, Style
from tqdm import tqdm
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Initialize colorama for Windows
init(autoreset=True)

@dataclass
class TranslationResult:
    """Data class untuk menyimpan hasil terjemahan"""
    original: str
    translated: str
    source_lang: str
    target_lang: str
    provider: str
    confidence: float = 1.0

class TranslatorCLI:
    """Main class untuk aplikasi translator CLI"""
    
    # Mapping kode bahasa yang didukung
    SUPPORTED_LANGUAGES = {
        'id': 'Indonesian',
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh-cn': 'Chinese (Simplified)',
        'zh-tw': 'Chinese (Traditional)',
        'ar': 'Arabic',
        'ru': 'Russian',
        'pt': 'Portuguese',
        'it': 'Italian',
        'nl': 'Dutch',
        'tr': 'Turkish',
        'vi': 'Vietnamese',
        'th': 'Thai',
        'hi': 'Hindi'
    }
    
    # Provider yang tersedia
    PROVIDERS = {
        'google': 'Google Translate (gratis)',
        'mymemory': 'MyMemory (gratis, batas 500 karakter/hari)',
        'libre': 'LibreTranslate (gratis, perlu self-host atau public server)',
    }
    
    def __init__(self):
        self.results: List[TranslationResult] = []
        self.initialize_providers()
    
    def initialize_providers(self):
        """Initialize translation providers"""
        self.providers = {}
        
        # Coba inisialisasi Google Translate
        try:
            from googletrans import Translator as GoogleTranslator
            self.providers['google'] = GoogleTranslator()
            print(f"{Fore.GREEN}✓ Google Translate provider loaded")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠ Google Translate tidak tersedia: {e}")
        
        # Coba inisialisasi Deep Translator
        try:
            from deep_translator import MyMemoryTranslator, GoogleTranslator as DeepGoogle
            self.providers['mymemory'] = MyMemoryTranslator
            # self.providers['deepl'] = DeeplTranslator  # Tidak gratis
            print(f"{Fore.GREEN}✓ MyMemory translator loaded")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠ Deep Translator tidak tersedia: {e}")
    
    def detect_language(self, text: str) -> str:
        """Deteksi bahasa teks input"""
        try:
            if 'google' in self.providers:
                result = self.providers['google'].detect(text)
                return result.lang
        except:
            pass
        
        # Fallback: cek beberapa karakter pertama
        # Ini adalah deteksi sederhana, bisa diperluas
        if any(char in text for char in 'абвгдежзийклмнопрстуфхцчшщъыьэюя'):
            return 'ru'
        elif any(char in text for char in 'あいうえおかきくけこさしすせそたちつてと'):
            return 'ja'
        elif any(char in text for char in '가나다라마바사아자차카타파하'):
            return 'ko'
        else:
            return 'en'  # Default ke Inggris
    
    def translate_with_provider(self, text: str, target_lang: str, source_lang: str = 'auto', provider: str = 'google') -> Optional[TranslationResult]:
        """Terjemahkan teks dengan provider tertentu"""
        try:
            if provider == 'google' and 'google' in self.providers:
                translator = self.providers['google']
                
                # Untuk Google Translate
                if source_lang == 'auto':
                    source_lang = self.detect_language(text)
                
                result = translator.translate(text, dest=target_lang, src=source_lang)
                
                return TranslationResult(
                    original=text,
                    translated=result.text,
                    source_lang=result.src,
                    target_lang=target_lang,
                    provider='Google Translate',
                    confidence=getattr(result, 'confidence', 0.0)
                )
            
            elif provider == 'mymemory' and 'mymemory' in self.providers:
                # MyMemory Translator
                if source_lang == 'auto':
                    source_lang = self.detect_language(text)
                
                translator = self.providers['mymemory'](source=source_lang, target=target_lang)
                translated = translator.translate(text)
                
                return TranslationResult(
                    original=text,
                    translated=translated,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    provider='MyMemory',
                    confidence=0.8
                )
            
            else:
                print(f"{Fore.RED}Provider {provider} tidak tersedia")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}Error dengan provider {provider}: {str(e)}")
            return None
    
    def translate_file(self, input_file: str, output_file: str, target_lang: str, 
                      source_lang: str = 'auto', provider: str = 'google', 
                      batch_size: int = 10) -> bool:
        """Terjemahkan konten file teks"""
        
        if not os.path.exists(input_file):
            print(f"{Fore.RED}File input tidak ditemukan: {input_file}")
            return False
        
        # Baca file input
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(input_file, 'r', encoding='latin-1') as f:
                    content = f.read()
            except:
                print(f"{Fore.RED}Gagal membaca file. Coba konversi encoding ke UTF-8.")
                return False
        
        if not content.strip():
            print(f"{Fore.YELLOW}File kosong atau hanya berisi spasi")
            return False
        
        # Split menjadi baris atau paragraf
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        if not lines:
            print(f"{Fore.YELLOW}Tidak ada teks untuk diterjemahkan")
            return False
        
        print(f"\n{Fore.CYAN}Memulai terjemahan...")
        print(f"{Fore.WHITE}File input  : {input_file}")
        print(f"{Fore.WHITE}File output : {output_file}")
        print(f"{Fore.WHITE}Bahasa target: {self.SUPPORTED_LANGUAGES.get(target_lang, target_lang)}")
        print(f"{Fore.WHITE}Provider    : {self.PROVIDERS.get(provider, provider)}")
        print(f"{Fore.WHITE}Jumlah baris: {len(lines)}")
        print("-" * 50)
        
        # Proses terjemahan dengan progress bar
        self.results = []
        successful = 0
        failed = 0
        
        with tqdm(total=len(lines), desc="Translating", unit="line") as pbar:
            for i, line in enumerate(lines):
                # Skip jika kosong
                if not line.strip():
                    self.results.append(TranslationResult(
                        original=line,
                        translated="",
                        source_lang=source_lang,
                        target_lang=target_lang,
                        provider=provider,
                        confidence=0.0
                    ))
                    pbar.update(1)
                    continue
                
                # Terjemahkan baris
                result = self.translate_with_provider(
                    text=line,
                    target_lang=target_lang,
                    source_lang=source_lang,
                    provider=provider
                )
                
                if result:
                    self.results.append(result)
                    successful += 1
                else:
                    # Jika gagal, simpan teks asli
                    self.results.append(TranslationResult(
                        original=line,
                        translated=f"[TRANSLATION FAILED] {line}",
                        source_lang=source_lang,
                        target_lang=target_lang,
                        provider=provider,
                        confidence=0.0
                    ))
                    failed += 1
                
                # Delay kecil untuk menghindari rate limiting
                if i % 5 == 0:
                    time.sleep(0.1)
                
                pbar.update(1)
        
        # Tulis hasil ke file output
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Hasil Terjemahan\n")
                f.write(f"# Input: {input_file}\n")
                f.write(f"# Output: {output_file}\n")
                f.write(f"# Bahasa target: {target_lang}\n")
                f.write(f"# Provider: {provider}\n")
                f.write(f"# Tanggal: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                
                for result in self.results:
                    if result.original.strip():
                        f.write(f"Original ({result.source_lang}):\n{result.original}\n\n")
                        f.write(f"Translated ({result.target_lang}):\n{result.translated}\n")
                        f.write(f"[Provider: {result.provider}, Confidence: {result.confidence:.2f}]\n")
                        f.write("-" * 30 + "\n\n")
            
            print(f"\n{Fore.GREEN}✓ Terjemahan selesai!")
            print(f"{Fore.WHITE}Sukses: {successful} baris")
            print(f"{Fore.YELLOW}Gagal : {failed} baris")
            print(f"{Fore.CYAN}Hasil disimpan di: {output_file}")
            
            # Tampilkan preview
            self.show_preview()
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Error menulis file output: {str(e)}")
            return False
    
    def show_preview(self, num_lines: int = 3):
        """Tampilkan preview hasil terjemahan"""
        print(f"\n{Fore.CYAN}Preview hasil terjemahan (baris pertama {num_lines}):")
        print("-" * 50)
        
        for i, result in enumerate(self.results[:num_lines]):
            if result.original.strip():
                print(f"{Fore.YELLOW}[Baris {i+1}]")
                print(f"{Fore.WHITE}Original  : {result.original[:80]}..." 
                      if len(result.original) > 80 else f"{Fore.WHITE}Original  : {result.original}")
                print(f"{Fore.GREEN}Translated: {result.translated[:80]}..." 
                      if len(result.translated) > 80 else f"{Fore.GREEN}Translated: {result.translated}")
                print(f"{Fore.BLUE}Provider: {result.provider} | Confidence: {result.confidence:.2f}")
                print()
    
    def show_statistics(self):
        """Tampilkan statistik terjemahan"""
        if not self.results:
            print(f"{Fore.YELLOW}Belum ada data terjemahan")
            return
        
        total = len(self.results)
        successful = len([r for r in self.results if r.confidence > 0])
        avg_confidence = sum(r.confidence for r in self.results) / total if total > 0 else 0
        
        print(f"\n{Fore.CYAN}Statistik Terjemahan:")
        print(f"{Fore.WHITE}Total baris     : {total}")
        print(f"{Fore.GREEN}Berhasil        : {successful}")
        print(f"{Fore.YELLOW}Gagal           : {total - successful}")
        print(f"{Fore.BLUE}Rata2 confidence: {avg_confidence:.2%}")
        
        # Tampilkan distribusi provider
        providers = {}
        for result in self.results:
            providers[result.provider] = providers.get(result.provider, 0) + 1
        
        print(f"\n{Fore.CYAN}Distribusi Provider:")
        for provider, count in providers.items():
            percentage = (count / total) * 100
            print(f"{Fore.WHITE}{provider:20}: {count:3} baris ({percentage:.1f}%)")

def print_banner():
    """Tampilkan banner aplikasi"""
    banner = f"""
{Fore.CYAN}{"="*60}
{Fore.GREEN}       TRANSLATOR CLI - MULTIPLE PROVIDERS
{Fore.CYAN}{"="*60}
{Fore.YELLOW}Spesifikasi:
{Fore.WHITE}• RAM: 16GB
{Fore.WHITE}• Storage: 500GB HD
{Fore.WHITE}• OS: Windows 11
{Fore.WHITE}• Python: 3.14.2
{Fore.CYAN}{"="*60}
    """
    print(banner)

def main():
    """Main function untuk CLI"""
    parser = argparse.ArgumentParser(
        description='Translator CLI dengan Multiple Providers Gratis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Contoh penggunaan:
  {sys.argv[0]} -i input.txt -o output_id.txt -t id
  {sys.argv[0]} -i dokumen.txt -o terjemahan.txt -t en -p mymemory
  {sys.argv[0]} -i teks.txt -o hasil.txt -t ja -s en -p google

Bahasa yang didukung: {', '.join([f'{k} ({v})' for k, v in TranslatorCLI.SUPPORTED_LANGUAGES.items()])}
        """
    )
    
    parser.add_argument('-i', '--input', required=True, help='File input teks')
    parser.add_argument('-o', '--output', required=True, help='File output hasil terjemahan')
    parser.add_argument('-t', '--target', required=True, help='Kode bahasa target (contoh: id, en, es)')
    parser.add_argument('-s', '--source', default='auto', help='Kode bahasa sumber (default: auto-detect)')
    parser.add_argument('-p', '--provider', default='google', 
                       choices=['google', 'mymemory'],
                       help='Provider terjemahan (default: google)')
    parser.add_argument('-b', '--batch', type=int, default=10, help='Ukuran batch untuk terjemahan')
    parser.add_argument('--list-langs', action='store_true', help='Tampilkan daftar bahasa yang didukung')
    parser.add_argument('--list-providers', action='store_true', help='Tampilkan daftar provider')
    parser.add_argument('--stats', action='store_true', help='Tampilkan statistik setelah selesai')
    parser.add_argument('--preview', type=int, default=3, help='Jumlah baris preview (default: 3)')
    
    args = parser.parse_args()
    
    # Tampilkan banner
    print_banner()
    
    # Inisialisasi translator
    translator = TranslatorCLI()
    
    # Jika hanya menampilkan list
    if args.list_langs:
        print(f"\n{Fore.CYAN}Daftar Bahasa yang Didukung:")
        for code, name in translator.SUPPORTED_LANGUAGES.items():
            print(f"{Fore.WHITE}{code:10} : {name}")
        return
    
    if args.list_providers:
        print(f"\n{Fore.CYAN}Daftar Provider yang Tersedia:")
        for code, name in translator.PROVIDERS.items():
            print(f"{Fore.WHITE}{code:15} : {name}")
        return
    
    # Validasi bahasa target
    if args.target not in translator.SUPPORTED_LANGUAGES:
        print(f"{Fore.YELLOW}Peringatan: Bahasa target '{args.target}' tidak dalam daftar standar")
        print(f"{Fore.WHITE}Mencoba tetap melanjutkan...")
    
    # Validasi file input
    if not os.path.exists(args.input):
        print(f"{Fore.RED}Error: File input '{args.input}' tidak ditemukan")
        sys.exit(1)
    
    # Proses terjemahan
    success = translator.translate_file(
        input_file=args.input,
        output_file=args.output,
        target_lang=args.target,
        source_lang=args.source,
        provider=args.provider,
        batch_size=args.batch
    )
    
    # Tampilkan statistik jika diminta
    if args.stats and success:
        translator.show_statistics()
    
    if success:
        print(f"\n{Fore.GREEN}Proses selesai dengan sukses!")
        sys.exit(0)
    else:
        print(f"\n{Fore.RED}Proses gagal!")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}\nProses dihentikan oleh pengguna.")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Error tidak terduga: {str(e)}")
        sys.exit(1)