#!/bin/bash

# Menentukan direktori tempat alat akan diinstal
INSTALL_DIR="$HOME/tools"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Fungsi untuk mengkloning repositori dari GitHub
git_clone() {
    local repo_url=$1
    local tool_name=$2
    if [ -d "$tool_name" ]; then
        echo "$tool_name sudah ada, memperbarui..."
        cd "$tool_name" && git pull origin main && cd ..
    else
        echo "Mengkloning $tool_name..."
        git clone "$repo_url" "$tool_name"
    fi
}

# Menginstal alat dari GitHub
echo "Memulai pengunduhan alat..."

# CMSeeK
git_clone "https://github.com/Tuhinshubhra/CMSeeK.git" "CMSeeK"

# SubDomainizer
git_clone "https://github.com/nsonaniya2010/SubDomainizer.git" "SubDomainizer"

# Sublist3r
git_clone "https://github.com/aboul3la/Sublist3r.git" "Sublist3r"

# WhatWeb
git_clone "https://github.com/urbanadventurer/WhatWeb.git" "WhatWeb"

# ParamSpider
git_clone "https://github.com/devanshbatham/ParamSpider.git" "ParamSpider"

# jshole
git_clone "https://github.com/callforpapers-source/jshole.git" "jshole"

# Menginstal whois menggunakan apt-get jika belum terinstal
echo "Memeriksa dan menginstal whois..."
if ! command -v whois &> /dev/null; then
    echo "whois tidak ditemukan, menginstal whois..."
    sudo apt-get update
    sudo apt-get install -y whois
    sudo apt-get install dirsearch
    sudo apt-get install paramspider
else
    echo "whois sudah terinstal."
    echo "dirsearch sudah terinstal."
    echo "paramspider sudah terinstal."
fi

echo "Semua alat telah diunduh dan diinstal!"

# Menyelesaikan skrip
echo "Skrip selesai! Anda dapat memulai penggunaan alat-alat tersebut."

