#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 LazyOwn Security Intelligence Report
Generador de métricas ejecutivas para Gerencia de Ciberseguridad
KPIs, OKRs, detección de amenazas y análisis forense
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import csv
import io
import os
import re
import json
from pathlib import Path
import os
warnings.filterwarnings('ignore')

# Configuración de estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 8)
sns.set(font_scale=1.1)

# Directorio de salida
OUTPUT_DIR = Path("sessions/reports")
STATIC = Path("static")
OUTPUT_DIR.mkdir(exist_ok=True)

# 📊 Categorías de comandos (expandidas)
COMMAND_CATEGORIES = {
    'nmap': 'recon', 'gobuster': 'recon', 'dirb': 'recon', 'nikto': 'recon',
    'sqlmap': 'exploit', 'hydra': 'brute_force', 'john': 'brute_force',
    'hashcat': 'brute_force', 'echo': 'data_write', 'searchsploit': 'exploit_research',
    'sudo': 'privilege_escalation', 'msfconsole': 'exploit', 'msfvenom': 'payload_creation',
    'cp': 'file_transfer', 'mv': 'file_transfer', 'wget': 'download',
    'curl': 'download', 'nc': 'network', 'netcat': 'network', 'ssh': 'remote_access',
    'telnet': 'remote_access', 'ftp': 'remote_access', 'smbclient': 'remote_access',
    'git': 'recon', 'whois': 'recon', 'dig': 'recon', 'nslookup': 'recon',
    'upx': 'packer', 'python3': 'scripting', 'python': 'scripting', 'perl': 'scripting',
    'powershell': 'execution', 'cmd': 'execution', 'cmd.exe': 'execution',
    'certutil': 'download', 'bitsadmin': 'download', 'regsvr32': 'lolbin',
    'rundll32': 'lolbin', 'wmic': 'lolbin', 'schtasks': 'persistence',
    'at': 'persistence', 'sc': 'persistence', 'psexec': 'lateral_movement',
    'evil-winrm': 'remote_access', 'crackmapexec': 'lateral_movement'
}

# ⚠ Palabras clave de comandos peligrosos
DANGEROUS_KEYWORDS = [
    'rm -rf', 'chmod 777', 'mkfs', 'dd if=', 'format', 'delete', 'del ',
    'rmdir', 'shutdown', 'poweroff', 'iptables -F'
]

# 🎯 Patrones de C2 y post-explotación
C2_INDICATORS = [
    r'bash -i.*>& /dev/tcp',  # Reverse shell
    r'nc .* -e',              # Netcat reverse shell
    r'powershell.*-Enc',      # PowerShell encoded
    r'certutil.*-decode',     # Certutil como downloader
    r'bitsadmin.*Transfer',   # BitsAdmin C2
    r'Invoke-WebRequest',     # PowerShell download
    r'wget.*http.*\.exe',     # Descarga de binarios
    r'curl.*http.*\.dll',
    r'python.*-m http',       # Servidor HTTP rápido
    r'echo.*base64.*\|.*bash' # Payloads ofuscados
]

def load_and_clean_data_robust(filepath):
    """Cargar y limpiar los datos de forma robusta"""
    print("🔄 Cargando datos de forma robusta...")
    
    try:
        df = pd.read_csv(filepath, error_bad_lines=False)
    except:
        try:
            df = pd.read_csv(filepath, on_bad_lines='skip')
        except:
            print("⚠  Usando método de parsing manual...")
            df = parse_csv_manual(filepath)
    
    if df.empty:
        print("❌ No se cargaron datos. Verifica el archivo.")
        return df

    print(f"✅ Datos cargados: {len(df)} registros")
    
    expected_columns = ['start','end','source_ip','source_port','destination_ip',
                       'destination_port','domain','subdomain','url','pivot_port',
                       'command','args']
    
    if len(df.columns) != len(expected_columns):
        print(f"⚠  Ajustando columnas ({len(df.columns)} → 12)...")
        df = df.reindex(columns=expected_columns, fill_value='')

    df['start'] = pd.to_datetime(df['start'], errors='coerce')
    df['end'] = pd.to_datetime(df['end'], errors='coerce')
    df = df.dropna(subset=['start', 'end'])
    
    df['duration'] = (df['end'] - df['start']).dt.total_seconds()
    df['hour'] = df['start'].dt.hour
    df['day_of_week'] = df['start'].dt.day_name()
    df['date'] = df['start'].dt.date
    
    df['command_length'] = df['command'].astype(str).str.len()
    df['args_length'] = df['args'].astype(str).str.len()
    
    df['contains_creds'] = df['args'].str.contains(":", na=False) & df['args'].str.contains(">", na=False)
    df['is_dangerous'] = df['args'].apply(lambda x: any(kw in str(x) for kw in DANGEROUS_KEYWORDS))
    df['command_category'] = df['command'].apply(lambda c: COMMAND_CATEGORIES.get(str(c).lower(), 'other'))
    df['is_c2_or_postexploit'] = df['args'].apply(lambda x: any(re.search(pat, str(x), re.IGNORECASE) for pat in C2_INDICATORS))
    
    print(f"✅ Datos procesados: {len(df)} registros válidos")
    return df

def parse_csv_manual(filepath):
    rows = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
        header = lines[0].strip().split(',')
        
        for i, line in enumerate(lines[1:], 1):
            try:
                reader = csv.reader(io.StringIO(line.strip()), delimiter=',', quotechar='"')
                row = next(reader)
                if len(row) < len(header):
                    row += [''] * (len(header) - len(row))
                elif len(row) > len(header):
                    row = row[:len(header)-1] + [','.join(row[len(header)-1:])]
                if len(row) == len(header):
                    rows.append(row)
            except Exception as e:
                continue
        return pd.DataFrame(rows, columns=header) if rows else pd.DataFrame()
    except Exception as e:
        print(f"❌ Error crítico en parsing manual: {e}")
        return pd.DataFrame()

def executive_kpis(df):
    """Genera KPIs para gerencia"""
    print("\n" + "="*60)
    print("🎯 KPIs EJECUTIVOS DE SEGURIDAD")
    print("="*60)
    
    total = len(df)
    suspicious = len(df[df['is_c2_or_postexploit']])
    dangerous = len(df[df['is_dangerous']])
    creds = len(df[df['contains_creds']])
    unique_domains = df['domain'].nunique()
    active_days = (df['start'].max() - df['start'].min()).days + 1
    
    # 🔑 KPIs Clave
    kpis = {
        "Total de Actividad de Red Team": total,
        "Comandos Sospechosos (C2/Post-Exploit)": suspicious,
        "Tasa de Actividad Sospechosa (%)": f"{(suspicious / total * 100):.2f}%",
        "Comandos Peligrosos": dangerous,
        "Credenciales Expuestas": creds,
        "Dominios Comprometidos": unique_domains,
        "Duración de la Campaña (días)": active_days,
        "Comandos por Día (promedio)": f"{total / active_days:.1f}"
    }
    
    for k, v in kpis.items():
        print(f"  • {k:<35} : {v}")
    
    return kpis

def strategic_okrs(df, kpis):
    """Genera OKRs estratégicos"""
    print("\n" + "="*60)
    print("🎯 OKRs ESTRATÉGICOS DE SEGURIDAD")
    print("="*60)
    
    okrs = {
        "OKR 1: Reducir exposición de credenciales": {
            "Objetivo": "Eliminar escritura de credenciales en texto plano",
            "Meta": "0 comandos con 'echo' escribiendo credenciales",
            "Actual": kpis["Credenciales Expuestas"],
            "Estado": "🔴 Crítico" if kpis["Credenciales Expuestas"] > 0 else "🟢 Cumplido"
        },
        "OKR 2: Prevenir post-explotación": {
            "Objetivo": "Detección y bloqueo de técnicas de C2",
            "Meta": "0 comandos ofuscados o de reverse shell",
            "Actual": kpis["Comandos Sospechosos (C2/Post-Exploit)"],
            "Estado": "🔴 Crítico" if kpis["Comandos Sospechosos (C2/Post-Exploit)"] > 0 else "🟢 Cumplido"
        },
        "OKR 3: Fortalecer postura de seguridad": {
            "Objetivo": "Reducir uso de comandos peligrosos",
            "Meta": "Menos del 1% de comandos peligrosos",
            "Actual": f"{(kpis['Comandos Peligrosos'] / kpis['Total de Actividad de Red Team'] * 100):.2f}%",
            "Estado": "🟡 Advertencia" if kpis["Comandos Peligrosos"] > 0 else "🟢 Cumplido"
        }
    }
    
    for okr, data in okrs.items():
        print(f"📌 {okr}")
        for k, v in data.items():
            print(f"   • {k}: {v}")
        print()
    
    return okrs

def generate_visualizations(df, kpis):
    """Genera gráficos para reporte"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Distribución por categorías
    cat_counts = df['command_category'].value_counts().head(8)
    axes[0,0].pie(cat_counts, labels=cat_counts.index, autopct='%1.1f%%')
    axes[0,0].set_title("Distribución por Categoría de Comandos")
    
    # 2. Actividad por hora
    hourly = df['hour'].value_counts().sort_index()
    axes[0,1].bar(hourly.index, hourly.values, color='skyblue')
    axes[0,1].set_title("Actividad por Hora del Día")
    axes[0,1].set_xlabel("Hora")
    axes[0,1].set_ylabel("Cantidad de Comandos")
    
    # 3. Dominios más atacados
    top_domains = df['domain'].value_counts().head(6)
    axes[1,0].barh(top_domains.index, top_domains.values, color='coral')
    axes[1,0].set_title("Top Dominios Atacados")
    axes[1,0].set_xlabel("Cantidad de Comandos")
    
    # 4. Indicadores de riesgo
    risks = [
        kpis["Comandos Sospechosos (C2/Post-Exploit)"],
        kpis["Comandos Peligrosos"],
        kpis["Credenciales Expuestas"]
    ]
    axes[1,1].bar(["C2/Post-Exploit", "Peligrosos", "Credenciales"], risks, color=['red', 'orange', 'purple'])
    axes[1,1].set_title("Indicadores de Riesgo")
    axes[1,1].set_ylabel("Cantidad")
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "security_dashboard.png", dpi=150, bbox_inches='tight')
    plt.savefig(STATIC / "security_dashboard.png", dpi=150, bbox_inches='tight')
    print(f"📊 Gráfico guardado: {OUTPUT_DIR}/security_dashboard.png")

def export_report(df, kpis, okrs):
    """Exporta reporte completo a JSON, incluyendo todo lo mostrado por pantalla"""
    
    # 🔹 Estadísticas básicas
    basic_stats = {
        "total_records": len(df),
        "unique_commands": df['command'].nunique(),
        "unique_source_ips": df['source_ip'].nunique(),
        "unique_domains": df['domain'].nunique(),
        "period_start": df['start'].min().isoformat() if not df.empty else None,
        "period_end": df['start'].max().isoformat() if not df.empty else None,
        "active_days": (df['start'].max() - df['start'].min()).days + 1 if not df.empty else 0
    }

    # 🔹 Top comandos
    top_commands = df['command'].value_counts().head(15).to_dict()

    # 🔹 Distribución por categorías
    category_distribution = df['command_category'].value_counts().to_dict()

    # 🔹 Top IPs
    top_ips = df['source_ip'].value_counts().head(10).to_dict()

    # 🔹 Top dominios
    top_domains = df['domain'].value_counts().head(10).to_dict()

    # 🔹 Actividad por hora
    hourly_activity = df['hour'].value_counts().sort_index().to_dict()

    # 🔹 Estadísticas de duración
    duration_stats = df['duration'].describe().to_dict()

    # 🔹 Credenciales expuestas
    creds_df = df[df['contains_creds']]
    exposed_creds = creds_df[['command', 'args', 'domain', 'start']].head(10).to_dict('records') if len(creds_df) > 0 else []

    # 🔹 Comandos peligrosos
    danger_df = df[df['is_dangerous']]
    dangerous_commands = danger_df[['command', 'args', 'domain', 'start']].head(10).to_dict('records') if len(danger_df) > 0 else []

    # 🔹 Comandos sospechosos de C2/post-exploit
    c2_df = df[df['is_c2_or_postexploit']]
    c2_commands = c2_df[['command', 'args', 'domain', 'start']].head(10).to_dict('records') if len(c2_df) > 0 else []

    # 🔹 Resumen completo
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "kpis": kpis,
            "okrs": okrs
        },
        "detailed_analysis": {
            "basic_statistics": basic_stats,
            "top_commands": [{"command": k, "count": v} for k, v in top_commands.items()],
            "command_category_distribution": [{"category": k, "count": v} for k, v in category_distribution.items()],
            "top_source_ips": [{"ip": k, "count": v} for k, v in top_ips.items()],
            "top_domains": [{"domain": k, "count": v} for k, v in top_domains.items()],
            "hourly_activity": [{"hour": int(k), "count": v} for k, v in hourly_activity.items()],
            "command_duration_stats_seconds": duration_stats,
            "exposed_credentials": exposed_creds,
            "dangerous_commands": dangerous_commands,
            "c2_postexploitation_commands": c2_commands
        },
        "raw_data_sample": df[['start', 'command', 'args', 'source_ip', 'domain', 'command_category', 'is_c2_or_postexploit', 'is_dangerous']].head(50).to_dict('records')
    }

    # Guardar JSON
    output_path = OUTPUT_DIR / "executive_report.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, default=str)  # default=str maneja fechas y tipos no serializables

    print(f"💾 Reporte JSON completo exportado: {output_path}")
    os.system(f"python3 modules/vuln_bot_cli.py --file {output_path} --provider groq --mode console | gum format")

def main():
    filepath = "sessions/LazyOwn_session_report.csv"
    print(f"📁 Analizando: {filepath}")
    
    if not os.path.exists(filepath):
        print("❌ ERROR: No se encontró el archivo CSV. Verifica la ruta.")
        return
    
    df = load_and_clean_data_robust(filepath)
    if df.empty:
        return
    
    # Ejecutar todos los análisis
    print("\n" + "="*60)
    print("📊 ANÁLISIS TÉCNICO DETALLADO")
    print("="*60)
    
    # Reutilizamos funciones de tu report.py
    basic_statistics(df)
    command_analysis(df)
    network_analysis(df)
    temporal_analysis(df)
    statistical_analysis(df)
    security_insights(df)
    
    # Nuevos análisis ejecutivos
    kpis = executive_kpis(df)
    okrs = strategic_okrs(df, kpis)
    generate_visualizations(df, kpis)
    export_report(df, kpis, okrs)
    
    print("\n" + "="*60)
    print("✅ REPORTE DE SEGURIDAD COMPLETADO")
    print("="*60)
    print(f"📄 Artifacts generados en: ./{OUTPUT_DIR}/")
    print(f"   • security_dashboard.png")
    print(f"   • executive_report.json")

# Copiamos las funciones de tu report.py
def basic_statistics(df):
    print("\n📈 ESTADÍSTICAS BÁSICAS")
    print("-"*60)
    print(f"Total de registros: {len(df):,}")
    print(f"Total de comandos únicos: {df['command'].nunique():,}")
    print(f"Total de IPs de origen únicas: {df['source_ip'].nunique():,}")
    print(f"Total de dominios únicos: {df['domain'].nunique():,}")
    try:
        print(f"Período de datos: {df['start'].min()} a {df['start'].max()}")
        print(f"Días de actividad: {(df['start'].max() - df['start'].min()).days}")
    except:
        print("⚠  No se pudieron calcular fechas")

def command_analysis(df):
    print("\n🖥  ANÁLISIS DE COMANDOS")
    print("-"*60)
    top_commands = df['command'].value_counts().head(15)
    print("Top 15 comandos más utilizados:")
    for i, (cmd, count) in enumerate(top_commands.items(), 1):
        print(f"  {i:2d}. {cmd:<20} ({count:,} veces)")

    categories = df['command_category'].value_counts()
    print("\nDistribución por categorías:")
    for cat, count in categories.items():
        percentage = (count / len(df)) * 100
        print(f"  {cat:<20} {count:,} ({percentage:.1f}%)")

def network_analysis(df):
    print("\n🌐 ANÁLISIS DE RED")
    print("-"*60)
    top_ips = df['source_ip'].value_counts().head(10)
    print("Top 10 IPs de origen más activas:")
    for ip, count in top_ips.items():
        print(f"  {ip:<15} ({count:,} comandos)")

    top_domains = df['domain'].value_counts().head(10)
    print("\nTop 10 dominios más frecuentes:")
    for domain, count in top_domains.items():
        print(f"  {domain:<30} ({count:,} comandos)")

def temporal_analysis(df):
    print("\n⏰ ANÁLISIS TEMPORAL")
    print("-"*60)
    hourly_activity = df['hour'].value_counts().sort_index()
    print("Distribución de actividad por hora:")
    for hour, count in hourly_activity.items():
        print(f"  {hour:02d}:00 - {hour:02d}:59  {count:,} comandos")

def statistical_analysis(df):
    print("\n📊 ANÁLISIS ESTADÍSTICO")
    print("-"*60)
    duration_stats = df['duration'].describe()
    print("Estadísticas de duración de comandos (segundos):")
    for stat, value in duration_stats.items():
        print(f"  {stat:<10} {value:.4f}")

def security_insights(df):
    print("\n🛡  INSIGHTS DE SEGURIDAD")
    print("-"*60)
    creds_df = df[df['contains_creds']]
    if len(creds_df) > 0:
        print("🚨 CREDENCIALES ENCONTRADAS:")
        sample_creds = creds_df[['command', 'args', 'domain']].head(5)
        for _, row in sample_creds.iterrows():
            print(f"  Comando: {row['command']}")
            print(f"  Args: {row['args']}")
            print(f"  Dominio: {row['domain']}")
            print("  " + "-"*50)

    danger_df = df[df['is_dangerous']]
    if len(danger_df) > 0:
        print(f"\n⚠  COMANDOS PELIGROSOS ({len(danger_df)} encontrados):")
        danger_sample = danger_df[['command', 'args', 'domain']].head(5)
        for _, row in danger_sample.iterrows():
            print(f"  Comando: {row['command']}")
            print(f"  Args: {row['args']}")
            print(f"  Dominio: {row['domain']}")
            print("  " + "-"*50)

if __name__ == "__main__":
    main()
