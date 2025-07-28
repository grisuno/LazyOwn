#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 LazyOwn Dataset Explorer - Versión Robusta
Scientific Data Analysis Script con manejo de errores en CSV
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import csv
import io
warnings.filterwarnings('ignore')

# Configuración de estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)

def load_and_clean_data_robust(filepath):
    """Cargar y limpiar los datos de forma robusta"""
    print("🔄 Cargando datos de forma robusta...")
    
    # Leer el archivo y manejar errores de parsing
    try:
        # Primero intentamos leer con error_bad_lines=False (pandas < 1.3.0)
        df = pd.read_csv(filepath, error_bad_lines=False)
    except:
        try:
            # Para pandas >= 1.3.0, usamos on_bad_lines
            df = pd.read_csv(filepath, on_bad_lines='skip')
        except:
            # Método manual de parsing
            print("⚠️  Usando método de parsing manual...")
            df = parse_csv_manual(filepath)
    
    print(f"✅ Datos cargados: {len(df)} registros")
    
    # Limpiar y procesar datos
    expected_columns = ['start','end','source_ip','source_port','destination_ip',
                       'destination_port','domain','subdomain','url','pivot_port',
                       'command','args']
    
    if len(df.columns) != len(expected_columns):
        print(f"⚠️  Número inesperado de columnas: {len(df.columns)}. Ajustando...")
        # Ajustar nombres de columnas
        if len(df.columns) >= 12:
            df.columns = expected_columns
        else:
            # Rellenar con columnas vacías si faltan
            for i in range(len(df.columns), 12):
                df[f'extra_col_{i}'] = ''
            df.columns = expected_columns[:len(df.columns)] + [f'extra_col_{i}' for i in range(len(df.columns), 12)]
    
    # Convertir fechas
    df['start'] = pd.to_datetime(df['start'], errors='coerce')
    df['end'] = pd.to_datetime(df['end'], errors='coerce')
    
    # Eliminar filas con fechas inválidas
    df = df.dropna(subset=['start', 'end'])
    
    # Calcular duración
    df['duration'] = (df['end'] - df['start']).dt.total_seconds()
    
    # Extraer características temporales
    df['hour'] = df['start'].dt.hour
    df['day_of_week'] = df['start'].dt.day_name()
    df['date'] = df['start'].dt.date
    
    # Longitudes
    df['command_length'] = df['command'].astype(str).str.len()
    df['args_length'] = df['args'].astype(str).str.len()
    
    # Detección de credenciales
    df['contains_creds'] = df['args'].str.contains(":", na=False) & df['args'].str.contains(">", na=False)
    
    # Comandos peligrosos
    dangerous_keywords = ['rm -rf', 'chmod 777', 'mkfs', 'dd if=', 'format', 'delete']
    df['is_dangerous'] = df['args'].apply(lambda x: any(kw in str(x) for kw in dangerous_keywords))
    
    # Categorización de comandos
    def categorize_command(cmd):
        mapping = {
            'nmap': 'recon',
            'gobuster': 'recon',
            'dirb': 'recon',
            'nikto': 'recon',
            'sqlmap': 'exploit',
            'hydra': 'brute_force',
            'john': 'brute_force',
            'hashcat': 'brute_force',
            'echo': 'data_write',
            'searchsploit': 'exploit_research',
            'sudo': 'privilege_escalation',
            'msfconsole': 'exploit',
            'msfvenom': 'payload_creation',
            'cp': 'file_transfer',
            'mv': 'file_transfer',
            'wget': 'download',
            'curl': 'download',
            'nc': 'network',
            'netcat': 'network',
            'ssh': 'remote_access',
            'telnet': 'remote_access',
            'ftp': 'remote_access',
            'smbclient': 'remote_access',
            'git': 'recon',
            'whois': 'recon',
            'dig': 'recon',
            'nslookup': 'recon'
        }
        return mapping.get(str(cmd).lower(), 'other')
    
    df['command_category'] = df['command'].apply(categorize_command)
    
    print(f"✅ Datos procesados: {len(df)} registros válidos")
    return df

def parse_csv_manual(filepath):
    """Método manual de parsing para CSV problemáticos"""
    rows = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        # Leer manualmente las primeras líneas para determinar el formato
        lines = file.readlines()
        
    header = lines[0].strip().split(',')
    
    # Procesar cada línea
    for i, line in enumerate(lines[1:], 1):
        try:
            # Usar csv.reader para manejar comas en campos
            reader = csv.reader(io.StringIO(line.strip()), delimiter=',', quotechar='"')
            row = next(reader)
            
            # Ajustar número de campos
            if len(row) < len(header):
                # Rellenar con valores vacíos
                row.extend([''] * (len(header) - len(row)))
            elif len(row) > len(header):
                # Combinar campos extra en el último campo (args)
                row = row[:len(header)-1] + [','.join(row[len(header)-1:])]
            
            # Asegurar que tenemos el número correcto de campos
            if len(row) == len(header):
                rows.append(row)
            else:
                print(f"⚠️  Línea {i+1} ignorada: número incorrecto de campos ({len(row)})")
                
        except Exception as e:
            print(f"⚠️  Error en línea {i+1}: {str(e)}")
            continue
    
    # Crear DataFrame
    if rows:
        df = pd.DataFrame(rows, columns=header)
        return df
    else:
        raise Exception("No se pudieron parsear los datos")

def basic_statistics(df):
    """Estadísticas básicas"""
    print("\n" + "="*60)
    print("📈 ESTADÍSTICAS BÁSICAS")
    print("="*60)
    
    print(f"Total de registros: {len(df):,}")
    print(f"Total de comandos únicos: {df['command'].nunique():,}")
    print(f"Total de IPs de origen únicas: {df['source_ip'].nunique():,}")
    print(f"Total de dominios únicos: {df['domain'].nunique():,}")
    try:
        print(f"Período de datos: {df['start'].min()} a {df['start'].max()}")
        print(f"Días de actividad: {(df['start'].max() - df['start'].min()).days}")
    except:
        print("⚠️  No se pudieron calcular fechas")

def command_analysis(df):
    """Análisis de comandos"""
    print("\n" + "="*60)
    print("🖥️  ANÁLISIS DE COMANDOS")
    print("="*60)
    
    # Top 15 comandos más usados
    try:
        top_commands = df['command'].value_counts().head(15)
        print("Top 15 comandos más utilizados:")
        for i, (cmd, count) in enumerate(top_commands.items(), 1):
            print(f"  {i:2d}. {cmd:<20} ({count:,} veces)")
    except Exception as e:
        print(f"⚠️  Error en análisis de comandos: {e}")
    
    # Categorías de comandos
    try:
        print("\nDistribución por categorías:")
        categories = df['command_category'].value_counts()
        for cat, count in categories.items():
            percentage = (count / len(df)) * 100
            print(f"  {cat:<20} {count:,} ({percentage:.1f}%)")
    except Exception as e:
        print(f"⚠️  Error en categorías: {e}")
    
    # Comandos con credenciales
    try:
        creds_count = df['contains_creds'].sum()
        print(f"\nComandos que escriben credenciales: {creds_count:,} ({(creds_count/len(df)*100):.2f}%)")
    except Exception as e:
        print(f"⚠️  Error en detección de credenciales: {e}")
    
    # Comandos peligrosos
    try:
        danger_count = df['is_dangerous'].sum()
        print(f"Comandos potencialmente peligrosos: {danger_count:,} ({(danger_count/len(df)*100):.2f}%)")
    except Exception as e:
        print(f"⚠️  Error en detección de comandos peligrosos: {e}")

def network_analysis(df):
    """Análisis de red"""
    print("\n" + "="*60)
    print("🌐 ANÁLISIS DE RED")
    print("="*60)
    
    try:
        # IPs más activas
        print("Top 10 IPs de origen más activas:")
        top_ips = df['source_ip'].value_counts().head(10)
        for ip, count in top_ips.items():
            print(f"  {ip:<15} ({count:,} comandos)")
    except Exception as e:
        print(f"⚠️  Error en análisis de IPs: {e}")
    
    try:
        # Dominios más atacados
        print("\nTop 10 dominios más frecuentes:")
        top_domains = df['domain'].value_counts().head(10)
        for domain, count in top_domains.items():
            print(f"  {domain:<30} ({count:,} comandos)")
    except Exception as e:
        print(f"⚠️  Error en análisis de dominios: {e}")

def temporal_analysis(df):
    """Análisis temporal"""
    print("\n" + "="*60)
    print("⏰ ANÁLISIS TEMPORAL")
    print("="*60)
    
    try:
        # Actividad por hora
        print("Distribución de actividad por hora:")
        hourly_activity = df['hour'].value_counts().sort_index()
        for hour, count in hourly_activity.items():
            print(f"  {hour:02d}:00 - {hour:02d}:59  {count:,} comandos")
    except Exception as e:
        print(f"⚠️  Error en análisis horario: {e}")
    
    try:
        # Actividad por día de la semana
        print("\nActividad por día de la semana:")
        daily_activity = df['day_of_week'].value_counts()
        for day, count in daily_activity.items():
            print(f"  {day:<10} {count:,} comandos")
    except Exception as e:
        print(f"⚠️  Error en análisis diario: {e}")

def statistical_analysis(df):
    """Análisis estadístico"""
    print("\n" + "="*60)
    print("📊 ANÁLISIS ESTADÍSTICO")
    print("="*60)
    
    try:
        # Estadísticas de duración
        print("Estadísticas de duración de comandos (segundos):")
        duration_stats = df['duration'].describe()
        for stat, value in duration_stats.items():
            print(f"  {stat:<10} {value:.4f}")
    except Exception as e:
        print(f"⚠️  Error en estadísticas de duración: {e}")
    
    try:
        # Estadísticas de longitud
        print("\nEstadísticas de longitud de comandos:")
        cmd_length_stats = df['command_length'].describe()
        for stat, value in cmd_length_stats.items():
            print(f"  {stat:<10} {value:.2f}")
    except Exception as e:
        print(f"⚠️  Error en estadísticas de comandos: {e}")
    
    try:
        print("\nEstadísticas de longitud de argumentos:")
        args_length_stats = df['args_length'].describe()
        for stat, value in args_length_stats.items():
            print(f"  {stat:<10} {value:.2f}")
    except Exception as e:
        print(f"⚠️  Error en estadísticas de argumentos: {e}")

def security_insights(df):
    """Insights de seguridad"""
    print("\n" + "="*60)
    print("🛡️  INSIGHTS DE SEGURIDAD")
    print("="*60)
    
    try:
        # Credenciales encontradas
        creds_df = df[df['contains_creds']]
        if len(creds_df) > 0:
            print("🚨 CREDENCIALES ENCONTRADAS:")
            sample_creds = creds_df[['command', 'args', 'domain']].head(5)
            for _, row in sample_creds.iterrows():
                print(f"  Comando: {row['command']}")
                print(f"  Args: {row['args']}")
                print(f"  Dominio: {row['domain']}")
                print("  " + "-"*50)
    except Exception as e:
        print(f"⚠️  Error en análisis de credenciales: {e}")
    
    try:
        # Comandos peligrosos
        danger_df = df[df['is_dangerous']]
        if len(danger_df) > 0:
            print(f"\n⚠️  COMANDOS PELIGROSOS ({len(danger_df)} encontrados):")
            danger_sample = danger_df[['command', 'args', 'domain']].head(5)
            for _, row in danger_sample.iterrows():
                print(f"  Comando: {row['command']}")
                print(f"  Args: {row['args']}")
                print(f"  Dominio: {row['domain']}")
                print("  " + "-"*50)
    except Exception as e:
        print(f"⚠️  Error en análisis de comandos peligrosos: {e}")

def main():
    """Función principal"""
    try:
        # Cargar datos
        filepath = "sessions/LazyOwn_session_report.csv"  # Ajusta la ruta según tu archivo
        df = load_and_clean_data_robust(filepath)
        
        # Ejecutar todos los análisis
        basic_statistics(df)
        command_analysis(df)
        network_analysis(df)
        temporal_analysis(df)
        statistical_analysis(df)
        security_insights(df)
        
        print("\n" + "="*60)
        print("✅ ANÁLISIS COMPLETADO")
        print("="*60)
        print("Resumen:")
        print(f"  • Total de comandos analizados: {len(df):,}")
        try:
            creds_count = df['contains_creds'].sum()
            danger_count = df['is_dangerous'].sum()
            print(f"  • Comandos con credenciales: {creds_count:,}")
            print(f"  • Comandos peligrosos: {danger_count:,}")
            print(f"  • IPs únicas: {df['source_ip'].nunique():,}")
            print(f"  • Dominios únicos: {df['domain'].nunique():,}")
        except:
            pass
        
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo CSV. Verifica la ruta.")
    except Exception as e:
        print(f"❌ Error durante el análisis: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
