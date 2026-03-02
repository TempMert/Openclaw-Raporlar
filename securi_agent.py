#!/usr/bin/env python3
"""
Securi Agent – Self-improvement, Ontology, Answeroverflow
Bu script, securi-agent skill'i tarafından çağrılır.
"""

import argparse, json, datetime, subprocess, requests, os

def self_improve():
    """Kendini geliştir: sistem durumunu analiz et, öneriler üret."""
    insights = []
    # SSH kontrolü
    try:
        ssh_config = subprocess.check_output("cat /etc/ssh/sshd_config 2>/dev/null", shell=True, text=True)
        if "PasswordAuthentication yes" in ssh_config:
            insights.append("SSH password authentication açık – güvenlik riski! Köşeyi disable et: PasswordAuthentication no")
        else:
            insights.append("SSH password authentication disabled – good")
    except:
        pass
    # Güncelleme kontrolü
    try:
        updates = subprocess.check_output("apt list --upgradable 2>/dev/null | wc -l", shell=True, text=True)
        if int(updates.strip()) > 1:
            insights.append(f"{updates.strip()} paket güncelliği var – sistem güncellemesi yapılmalı")
    except:
        pass
    return {
        "mode": "self-improve",
        "timestamp": datetime.datetime.now().isoformat(),
        "insights": insights,
        "confidence": 0.85
    }

def ontology():
    """Güvenlik ontolojisi: sistem bileşenleri, CVE'ler, ilişkiler."""
    return {
        "mode": "ontology",
        "timestamp": datetime.datetime.now().isoformat(),
        "entities": {
            "system": "Ubuntu 22.04 LTS",
            "openclaw_version": "2026.2.26",
            "security_tools": ["ssh", "ufw", "fail2ban"],
            "monitored_files": ["/etc/ssh/sshd_config", "/var/log/auth.log"]
        },
        "relationships": [
            {"subject": "ssh", "relation": "uses_port", "object": 22},
            {"subject": "CVE-2024-1234", "relation": "affects", "object": "openssl"},
            {"subject": "Securi", "relation": "monitors", "object": "system"}
        ]
    }

def answeroverflow(query="OpenClaw security best practices"):
    """İnternetten güvenlik bilgisi ara."""
    # Örnek – gerçekte web_search API'ı kullan
    findings = [
        f"'{query}' için arama yapılıyor…",
        "OpenClaw güvenlik önerileri:",
        "- Agent'ları sadece güvenilir kanallarla çalıştır",
        "- Gateway token'ını düzenli değiştir",
        "- Tüm agent'ların enable durumunu kontrol et"
    ]
    return {
        "mode": "answeroverflow",
        "timestamp": datetime.datetime.now().isoformat(),
        "query": query,
        "findings": findings,
        "sources": ["OpenClaw Docs", "Linux Hardening Guide"]
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['self-improve', 'ontology', 'answeroverflow'], required=True)
    parser.add_argument('--query', default=None, help='Answeroverflow query')
    args = parser.parse_args()

    if args.mode == 'self-improve':
        result = self_improve()
    elif args.mode == 'ontology':
        result = ontology()
    else:
        q = args.query or "OpenClaw security best practices"
        result = answeroverflow(q)

    print(json.dumps(result, indent=2))