#!/bin/bash

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

echo "Memulai pengunduhan alat..."

git_clone "https://github.com/Tuhinshubhra/CMSeeK.git" "CMSeeK"
git_clone "https://github.com/nsonaniya2010/SubDomainizer.git" "SubDomainizer"
git_clone "https://github.com/aboul3la/Sublist3r.git" "Sublist3r"
git_clone "https://github.com/urbanadventurer/WhatWeb.git" "WhatWeb"
git_clone "https://github.com/devanshbatham/ParamSpider.git" "ParamSpider"
git_clone "https://github.com/callforpapers-source/jshole.git" "jshole"

echo "Memeriksa dan menginstal whois..."
if ! command -v whois &> /dev/null; then
    echo "whois tidak ditemukan, menginstal whois..."
    sudo apt-get update
    sudo apt-get install -y whois
else
    echo "whois sudah terinstal."
fi

echo "Semua alat telah diunduh dan diinstal!"
echo "Skrip selesai! Anda dapat memulai penggunaan alat-alat tersebut."
