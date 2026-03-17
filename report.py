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
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import re
import json
from datetime import datetime
from pathlib import Path

# --- OPTIMIZACIÓN DE HARDWARE (Tiger Lake i3) ---
torch.set_num_threads(4)
os.environ["KMP_BLOCKTIME"] = "1"

# =============================================================================
# 1. MOTOR GEOMÉTRICO RESMA (EL CEREBRO)
# =============================================================================
class RESMAEngine(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.lattice = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.GELU(),
            nn.Linear(256, 64)
        )
        self.ricci_metric = nn.Linear(64, 32)
        self.output = nn.Linear(32, 1)

    def forward(self, x):
        z = self.lattice(x)
        curvature = torch.tanh(self.ricci_metric(z))
        energy = torch.norm(curvature, p=2, dim=1, keepdim=True)
        return torch.sigmoid(self.output(curvature) + 0.1 * energy), energy

# =============================================================================
# 2. INTEGRACIÓN EN TU SISTEMA DE REPORTING
# =============================================================================

def apply_resma_intelligence(df):
    """
    Inyecta la IA RESMA en el flujo de datos de LazyOwn.
    Aprende de tus reglas y descubre lo que ellas no ven.
    """
    print("\n[*] Entrenando Motor de Inteligencia RESMA 5.2...")
    
    # Feature Engineering (Usando tus columnas)
    df['full_payload'] = df['command'].astype(str) + " " + df['args'].fillna('').astype(str)
    
    vectorizer = TfidfVectorizer(max_features=512, ngram_range=(1, 2))
    X_vec = vectorizer.fit_transform(df['full_payload']).toarray()
    X_tensor = torch.tensor(X_vec, dtype=torch.float32)

    # Ground Truth basado en TUS reglas
    y_reglas = (df['is_c2_or_postexploit'] | df['is_dangerous'] | df['contains_creds']).astype(float)
    y_tensor = torch.tensor(y_reglas.values, dtype=torch.float32).reshape(-1, 1)

    model = RESMAEngine(X_vec.shape[1])
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

    # Entrenamiento rápido para capturar la 'forma' de tus ataques
    model.train()
    for _ in range(40):
        optimizer.zero_grad()
        probs, _ = model(X_tensor)
        loss = F.binary_cross_entropy(probs, y_tensor)
        loss.backward()
        optimizer.step()

    # Inferencia: Buscando Amenazas Sombra
    model.eval()
    with torch.no_grad():
        final_probs, energy = model(X_tensor)
        df['ia_risk_score'] = final_probs.numpy()
        df['ia_energy'] = energy.numpy()

    # Umbral de anomalía geométrica (Percentil 97)
    threshold = np.percentile(df['ia_energy'], 97)
    df['is_shadow_threat'] = ((df['ia_energy'] > threshold) & (y_reglas == 0)).astype(int)
    
    return df

# =============================================================================
# 3. REPORTE FINAL (RESUMEN DE INTELIGENCIA)
# =============================================================================

def final_resma_report(df):
    shadows = df[df['is_shadow_threat'] == 1]
    
    print("\n" + "="*60)
    print("🔍 ANÁLISIS DE AMENAZAS RESMA 5.2")
    print("="*60)
    print(f"✅ Total Eventos:          {len(df)}")
    print(f"🚨 Detectados por Reglas:  {int((df['is_c2_or_postexploit'] | df['is_dangerous'] | df['contains_creds']).sum())}")
    print(f"🌀 Amenazas Sombra (IA):   {len(shadows)}")
    
    if len(shadows) > 0:
        print("\n[!] DESCUBRIMIENTOS SOMBRA (Alta Energía Estructural):")
        # Mostramos los comandos que la IA considera raros y tus reglas no pillaron
        for _, row in shadows.sort_values('ia_energy', ascending=False).head(5).iterrows():
            print(f"  • {row['command']} {row['args'][:60]}... (Energy: {row['ia_energy']:.4f})")
    
    return len(shadows)

# =============================================================================
# FLUJO PRINCIPAL
# =============================================================================

# Aquí es donde el script se ejecuta de verdad
def lol():
    filepath = "sessions/LazyOwn_session_report.csv"
    
    if os.path.exists(filepath):
        # 1. Cargar y limpiar (como tú lo haces)
        df = pd.read_csv(filepath)
        
        # Simulo tus flags para que el código funcione standalone
        # En tu script real, estas columnas ya existen
        df['is_dangerous'] = df['args'].str.contains('rm -rf|export', na=False)
        df['is_c2_or_postexploit'] = df['args'].str.contains('nc |powershell', na=False)
        df['contains_creds'] = df['args'].str.contains(':', na=False)

        # 2. Inyectar inteligencia
        df = apply_resma_intelligence(df)

        # 3. Mostrar reporte
        final_resma_report(df)
    else:
        print(f"❌ No se encontró el archivo {filepath}")

# Configuración de estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 8)
sns.set(font_scale=1.1)

# Directorios
OUTPUT_DIR = Path("sessions/reports")
STATIC = Path("static")
AI_MODEL_DIR = Path("sessions/ai_model")
OUTPUT_DIR.mkdir(exist_ok=True)
STATIC.mkdir(exist_ok=True)
AI_MODEL_DIR.mkdir(exist_ok=True)

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

def train_ai_model(df):
    """Entrena un modelo desde cero con todos los detalles de entrenamiento"""
    print("\n" + "="*60)
    print("🤖 ENTRENANDO MODELO DE INTELIGENCIA ARTIFICIAL DESDE CERO")
    print("="*60)
    
    # Crear etiqueta combinada
    df['es_malicioso'] = (
        df['is_c2_or_postexploit'] |
        df['is_dangerous'] |
        df['contains_creds']
    ).astype(int)

    # Filtrar datos válidos
    df_text = df.dropna(subset=['command', 'args']).copy()
    df_text['texto'] = df_text['command'].astype(str) + " " + df_text['args'].astype(str)

    X = df_text['texto']
    y = df_text['es_malicioso']

    print(f"✅ Datos para entrenamiento: {len(X)} comandos ({y.sum()} maliciosos, {len(y) - y.sum()} normales)")

    if y.sum() == 0:
        print("❌ No hay ejemplos maliciosos. No se puede entrenar.")
        return None, None

    # Vectorización
    print("\n🔄 Vectorizando texto (TF-IDF)...")
    vectorizer = TfidfVectorizer(
        max_features=1000,
        ngram_range=(1, 2),
        lowercase=True,
        token_pattern=r'(?u)\b\w+\b'
    )
    X_vec = vectorizer.fit_transform(X)

    # División train/test
    print("Dividiendo train/test (80%/20%)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_vec, y, test_size=0.2, random_state=42, stratify=y
    )
    # CORRECCIÓN: Usar .shape[0] en lugar de len() para matrices dispersas
    print(f"   • Entrenamiento: {X_train.shape[0]} comandos")
    print(f"   • Prueba: {X_test.shape[0]} comandos")

    # Entrenamiento
    print("\n🧠 Entrenando modelo Random Forest...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluación
    print("\n📊 EVALUACIÓN DEL MODELO")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"🎯 Precisión: {acc:.2%}")
    print("\n📋 Reporte de clasificación:")
    print(classification_report(y_test, y_pred, target_names=['Normal', 'Malicioso']))

    # Guardar modelo
    joblib.dump(model, AI_MODEL_DIR / "malicious_command_model.pkl")
    joblib.dump(vectorizer, AI_MODEL_DIR / "tfidf_vectorizer.pkl")
    print(f"\n💾 Modelo guardado en: {AI_MODEL_DIR}/")

    # Matriz de confusión
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Normal','Malicioso'], yticklabels=['Normal','Malicioso'])
    plt.title("Matriz de Confusión - Detección de Comandos Maliciosos")
    plt.savefig(OUTPUT_DIR / "confusion_matrix.png", dpi=150, bbox_inches='tight')
    plt.close()

    return model, vectorizer


def load_or_train_model(df):
    """Carga modelo existente o entrena uno nuevo, y lo actualiza con nuevos datos"""
    model_path = AI_MODEL_DIR / "malicious_command_model.pkl"
    vectorizer_path = AI_MODEL_DIR / "tfidf_vectorizer.pkl"

    df['es_malicioso'] = (
        df['is_c2_or_postexploit'] |
        df['is_dangerous'] |
        df['contains_creds']
    ).astype(int)
    df_text = df.dropna(subset=['command', 'args']).copy()
    df_text['texto'] = df_text['command'].astype(str) + " " + df_text['args'].astype(str)
    X_text = df_text['texto']
    y_true = df_text['es_malicioso']

    if model_path.exists() and vectorizer_path.exists():
        print("🔁 Cargando modelo previo...")
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)

        try:
            X_vec = vectorizer.transform(X_text)
            print(f"🔄 Reentrenando con {len(X_text)} nuevos comandos...")
            model.fit(X_vec, y_true)
            joblib.dump(model, model_path)
            print("✅ Modelo actualizado y guardado.")
        except Exception as e:
            print(f"⚠ Error al ajustar modelo: {e}. Reentrenando desde cero.")
            return train_ai_model(df)
    else:
        print("🧠 Modelo no encontrado. Entrenando desde cero...")
        return train_ai_model(df)

    return model, vectorizer

def apply_ai_predictions(df, model, vectorizer):
    """Aplica predicciones del modelo al DataFrame"""
    df_text = df[['command', 'args']].copy().dropna()
    df_text['texto'] = df_text['command'].astype(str) + " " + df_text['args'].astype(str)
    X_vec = vectorizer.transform(df_text['texto'])

    df_text['ia_malicious_score'] = model.predict_proba(X_vec)[:, 1]
    df_text['ia_prediccion'] = model.predict(X_vec)

    df = df.join(df_text[['ia_malicious_score', 'ia_prediccion']])
    df['ia_malicious_score'].fillna(0.0, inplace=True)
    df['ia_prediccion'].fillna(0, inplace=True)
    return df

def apply_ai_predictions(df, model, vectorizer):
    """Aplica predicciones del modelo al DataFrame"""
    df_text = df[['command', 'args']].copy().dropna()
    df_text['texto'] = df_text['command'].astype(str) + " " + df_text['args'].astype(str)
    X_vec = vectorizer.transform(df_text['texto'])

    df_text['ia_malicious_score'] = model.predict_proba(X_vec)[:, 1]
    df_text['ia_prediccion'] = model.predict(X_vec)

    df = df.join(df_text[['ia_malicious_score', 'ia_prediccion']])
    df['ia_malicious_score'].fillna(0.0, inplace=True)
    df['ia_prediccion'].fillna(0, inplace=True)
    return df

def analyze_ia_vs_rules(df):
    """Analiza discrepancias entre reglas y modelo IA"""
    print("\n" + "="*60)
    print("🔍 ANÁLISIS COMPARATIVO: REGLAS VS IA")
    print("="*60)

    regla_mal = (df['is_c2_or_postexploit'] | df['is_dangerous'] | df['contains_creds'])
    ia_mal = df['ia_prediccion'].astype(bool)

    nuevos_ia = df[~regla_mal & ia_mal]  # IA detecta, reglas no
    fallo_ia = df[regla_mal & ~ia_mal]  # Reglas detectan, IA no

    print(f"🟢 Comandos maliciosos (reglas): {regla_mal.sum()}")
    print(f"🟢 Comandos maliciosos (IA): {ia_mal.sum()}")
    print(f"🟡 Nuevos hallazgos (IA detectó, reglas no): {len(nuevos_ia)}")
    print(f"🔴 Falsos negativos (reglas sí, IA no): {len(fallo_ia)}")

    if len(nuevos_ia) > 0:
        print("\n💡 NUEVOS HALLAZGOS DE LA IA:")
        for _, row in nuevos_ia.head(5).iterrows():
            print(f"  [{row['domain']}] {row['command']} {row['args']} (score: {row['ia_malicious_score']:.3f})")

    if len(fallo_ia) > 0:
        print("\n⚠ CASOS DONDE LA IA FALLÓ:")
        for _, row in fallo_ia.head(5).iterrows():
            print(f"  [{row['domain']}] {row['command']} {row['args']}")

    return {
        "reglas_maliciosos": int(regla_mal.sum()),
        "ia_maliciosos": int(ia_mal.sum()),
        "nuevos_hallazgos_ia": len(nuevos_ia),
        "falsos_negativos_ia": len(fallo_ia)
    }
def load_and_clean_data_robust(filepath):
    """Cargar y limpiar los datos de forma robusta"""
    print("🔄 Cargando datos de forma robusta...")
    
    try:
        df = pd.read_csv(filepath, on_bad_lines='skip')
    except:
        df = parse_csv_manual(filepath)
    
    if df.empty:
        print("❌ No se cargaron datos.")
        return df

    print(f"✅ Datos cargados: {len(df)} registros")
    
    expected_columns = ['start','end','source_ip','source_port','destination_ip',
                       'destination_port','domain','subdomain','url','pivot_port',
                       'command','args']
    
    if len(df.columns) != len(expected_columns):
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
        for line in lines[1:]:
            try:
                reader = csv.reader(io.StringIO(line.strip()), delimiter=',', quotechar='"')
                row = next(reader)
                if len(row) < len(header):
                    row += [''] * (len(header) - len(row))
                elif len(row) > len(header):
                    row = row[:len(header)-1] + [','.join(row[len(header)-1:])]
                if len(row) == len(header):
                    rows.append(row)
            except:
                continue
        return pd.DataFrame(rows, columns=header) if rows else pd.DataFrame()
    except Exception as e:
        print(f"❌ Error: {e}")
        return pd.DataFrame()

def executive_kpis(df):
    total = len(df)
    suspicious = len(df[df['is_c2_or_postexploit']])
    dangerous = len(df[df['is_dangerous']])
    creds = len(df[df['contains_creds']])
    unique_domains = df['domain'].nunique()
    active_days = (df['start'].max() - df['start'].min()).days + 1

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
    
    print("\n" + "="*60)
    print("🎯 KPIs EJECUTIVOS DE SEGURIDAD")
    print("="*60)
    for k, v in kpis.items():
        print(f"  • {k:<35} : {v}")
    
    return kpis

def strategic_okrs(df, kpis):
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
    
    print("\n" + "="*60)
    print("🎯 OKRs ESTRATÉGICOS DE SEGURIDAD")
    print("="*60)
    for okr, data in okrs.items():
        print(f"📌 {okr}")
        for k, v in data.items():
            print(f"   • {k}: {v}")
        print()
    
    return okrs

def generate_visualizations(df, kpis):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    cat_counts = df['command_category'].value_counts().head(8)
    axes[0,0].pie(cat_counts, labels=cat_counts.index, autopct='%1.1f%%')
    axes[0,0].set_title("Distribución por Categoría de Comandos")
    
    hourly = df['hour'].value_counts().sort_index()
    axes[0,1].bar(hourly.index, hourly.values, color='skyblue')
    axes[0,1].set_title("Actividad por Hora del Día")
    axes[0,1].set_xlabel("Hora")
    axes[0,1].set_ylabel("Cantidad de Comandos")
    
    top_domains = df['domain'].value_counts().head(6)
    axes[1,0].barh(top_domains.index, top_domains.values, color='coral')
    axes[1,0].set_title("Top Dominios Atacados")
    axes[1,0].set_xlabel("Cantidad de Comandos")
    
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

def export_report(df, kpis, okrs, ia_analysis):
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "kpis": kpis,
            "okrs": okrs,
            "ia_analysis": ia_analysis
        },
        "detailed_analysis": {
            "basic_statistics": {
                "total_records": len(df),
                "unique_commands": df['command'].nunique(),
                "unique_source_ips": df['source_ip'].nunique(),
                "unique_domains": df['domain'].nunique(),
                "active_days": (df['start'].max() - df['start'].min()).days + 1
            },
            "ia_detection_stats": {
                "total_malicious_predicted": int(df['ia_prediccion'].sum()),
                "high_risk_commands": int((df['ia_malicious_score'] > 0.8).sum()),
                "nuevos_hallazgos_ia": ia_analysis["nuevos_hallazgos_ia"],
                "falsos_negativos_ia": ia_analysis["falsos_negativos_ia"]
            },
            "top_commands": df['command'].value_counts().head(10).to_dict(),
            "exposed_credentials": df[df['contains_creds']].head(10)[['command','args','domain','start']].to_dict('records'),
            "c2_commands": df[df['is_c2_or_postexploit']].head(10)[['command','args','domain','start']].to_dict('records'),
            "nuevos_hallazgos_ia": df[
                ~(df['is_c2_or_postexploit'] | df['is_dangerous'] | df['contains_creds']) & 
                (df['ia_prediccion'] == 1)
            ].head(10)[['command','args','domain','ia_malicious_score']].to_dict('records'),
            "falsos_negativos_ia": df[
                (df['is_c2_or_postexploit'] | df['is_dangerous'] | df['contains_creds']) & 
                (df['ia_prediccion'] == 0)
            ].head(10)[['command','args','domain']].to_dict('records')
        }
    }

    output_path = OUTPUT_DIR / "executive_report.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, default=str)
    print(f"💾 Reporte JSON exportado: {output_path}")
    os.system(f"python3 modules/vuln_bot_cli.py --file {output_path} --provider groq --mode console | gum format")

    

# Funciones de análisis (mantenidas igual)
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
            
def main():
    filepath = "sessions/LazyOwn_session_report.csv"
    print(f"📁 Analizando: {filepath}")
    
    if not os.path.exists(filepath):
        print("❌ ERROR: No se encontró el archivo CSV.")
        return
    
    df = load_and_clean_data_robust(filepath)
    if df.empty:
        return

    # --- IA: Cargar o reentrenar modelo ---
    model, vectorizer = load_or_train_model(df)
    if model is None or vectorizer is None:
        print("⚠️ No se pudo cargar o entrenar el modelo. Continuando sin IA...")
        return

    # --- Aplicar predicciones ---
    df = apply_ai_predictions(df, model, vectorizer)

    # --- Análisis técnico ---
    print("\n" + "="*60)
    print("📊 ANÁLISIS TÉCNICO DETALLADO")
    print("="*60)
    basic_statistics(df)
    command_analysis(df)
    network_analysis(df)
    temporal_analysis(df)
    statistical_analysis(df)
    security_insights(df)

    # --- Comparativa IA vs Reglas ---
    ia_analysis = analyze_ia_vs_rules(df)

    # --- KPIs y OKRs ---
    kpis = executive_kpis(df)
    okrs = strategic_okrs(df, kpis)
    generate_visualizations(df, kpis)
    export_report(df, kpis, okrs, ia_analysis)

    print("\n" + "="*60)
    print("✅ REPORTE DE SEGURIDAD COMPLETADO")
    print("="*60)
    print(f"📄 Artifacts generados en: ./{OUTPUT_DIR}/")
    print(f"   • security_dashboard.png")
    print(f"   • confusion_matrix.png")
    print(f"   • executive_report.json")
    lol()
if __name__ == "__main__":
    main()