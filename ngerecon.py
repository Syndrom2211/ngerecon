import subprocess
import os
import re
from tqdm import tqdm
import pyfiglet

# Fungsi untuk menjalankan perintah dan menyimpan hasil di file .txt
def run_command(command, tool_name, output_file, cwd=None, max_progress=None):
    
    if "dirsearch" in command:
        command += " --no-color"
    
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)
    
    # Menghitung total_lines jika tidak ada max_progress yang diberikan
    if not max_progress:
        total_lines = sum(1 for _ in process.stdout)
        process.stdout.close()
        process.wait()
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)
    else:
        total_lines = max_progress

    with open(output_file, "w") as f_output, tqdm(total=total_lines, desc=f"{tool_name} Progress", 
                      bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]", ncols=100) as pbar:
        lines_processed = 0
        for output in process.stdout:
            cleaned_output = re.sub(r'\x1b\[[0-9;]*m', '', output)
            f_output.write(cleaned_output)
            pbar.update(1)
            lines_processed += 1
            if max_progress and lines_processed >= max_progress:
                break
        process.stdout.close()
        process.wait()
        
        # Ensure progress bar reaches 100% if fewer lines were processed
        pbar.n = total_lines
        pbar.refresh()

# Menampilkan ASCII Art
def display_ascii():
    ascii_banner = pyfiglet.figlet_format("nge-RECON 1.0")
    print(ascii_banner)
    print("Tools untuk informasi website\nOleh: Adam Sasmita - @adamsasmi\n")

# Fungsi utama
def main():
    domain = input("Masukkan nama domain (contoh: example.com): ").strip()
    display_ascii()
    
    output_folder = "results"
    os.makedirs(output_folder, exist_ok=True)

    commands = [
        (f"echo 'y' | python3 CMSeeK/cmseek.py -u {domain}", "Cek CMS", f"{output_folder}/cmseek_output.txt", 100),
        (f"python3 SubDomainizer/SubDomainizer.py -u {domain} -o {output_folder}/subdomainizer_output.txt", "Cari subdomain", f"{output_folder}/subdomainizer_output.txt", 100),
        (f"python3 Sublist3r/sublist3r.py -d {domain} -o {output_folder}/sublist3r_output.txt", "Cari subdomain tambahan", f"{output_folder}/sublist3r_output.txt", 150),
        (f"./WhatWeb/whatweb {domain}", "Identifikasi website", f"{output_folder}/whatweb_output.txt", 100),
        (f"dirsearch -u {domain} -e all -o {output_folder}/dirsearch_output.txt", "Cari file web", f"{output_folder}/dirsearch_output.txt", 100),
        (f"paramspider -d {domain} > {output_folder}/paramspider_output.txt", "Cari parameter web", f"{output_folder}/{domain}.txt", 100),
        (f"whois {domain}", "Whois domain", f"{output_folder}/whois_output.txt", 50),
        (f"python3 jshole.py -u {domain}", "Cari file JS", f"{output_folder}/jshole_output.txt", 100, "jshole"),
    ]

    # Menjalankan semua command
    for command, tool_name, output_file, max_progress, *cwd in commands:
        run_command(command, tool_name, output_file, cwd[0] if cwd else None, max_progress)
    
    # Membuat file HTML untuk hasil scan
    with open(f"{output_folder}/hasil_nyari_info.html", "w") as f:
        f.write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Hasil Scan Domain {domain}</title>
                    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
                    <style>
                        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f8f9fa; }}
                        h1, h2 {{ color: #007bff; font-size: 1.75rem; font-weight: 600; }}
                        .section {{ margin-bottom: 20px; }}
                        .card {{ box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); border: none; }}
                        .card-header {{ background-color: #007bff; color: white; font-size: 1.25rem; font-weight: bold; }}
                        .card-body {{ background-color: #f4f4f4; max-height: 300px; overflow-y: scroll; padding: 15px; border-radius: 5px; }}
                        .output {{ white-space: pre-wrap; word-wrap: break-word; }}
                    </style></head><body class="container">
                    <h1>Domain Website: {domain}</h1>""")

        file_titles = {
            "cmseek_output.txt": "Cek CMS",
            "subdomainizer_output.txt": "Cari subdomain",
            "sublist3r_output.txt": "Cari subdomain tambahan",
            "whatweb_output.txt": "Identifikasi website",
            "dirsearch_output.txt": "Cari file web",
            f"{domain}.txt": "Cari parameter web",
            "whois_output.txt": "Whois domain",
            "jshole_output.txt": "Cari file JS"
        }

        for filename, title in file_titles.items():
            with open(f"{output_folder}/{filename}", 'r') as content_file:
                content = content_file.read()
                f.write(f"""
                    <div class="section">
                        <div class="card">
                            <div class="card-header">{title}</div>
                            <div class="card-body output"><pre>{content}</pre></div>
                        </div>
                    </div>""")

        f.write("</body></html>")
        
    print("Selesai! Hasil scan telah tersimpan di folder results berupa HTML!")

if __name__ == "__main__":
    main()

