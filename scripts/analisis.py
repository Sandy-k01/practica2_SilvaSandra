"""
Práctica Individual N° 2 - Formulación y análisis preliminar de un sistema real
Caso: Tiempo de atención en cajas de un supermercado

Este script:
1. Genera (o lee, si ya existe) el archivo de datos datos/datos.csv.
2. Calcula estadísticos descriptivos de la variable principal.
3. Detecta valores atípicos (outliers) con Z-Score.
4. Redacta automáticamente el informe en reporte/informe.txt.

Ejecutar desde la raíz de la carpeta practica2_SilvaSandra:
    python scripts/analisis.py
"""

import os

import numpy as np
import pandas as pd
from scipy import stats

# -----------------------------------------------------------------
# Datos del estudiante y del caso
# -----------------------------------------------------------------
NOMBRE_ESTUDIANTE = "Sandra Silva"
TITULO_CASO = "Tiempo de atención en cajas de un supermercado"
UMBRAL_Z = 2.5          # criterio de exclusión |Z| >= umbral
SEMILLA = 2026          # semilla fija, para que los datos sean reproducibles

# Rutas relativas a la raíz del proyecto (practica2_SilvaSandra/)
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DATOS = os.path.join(RAIZ, "datos", "datos.csv")
RUTA_INFORME = os.path.join(RAIZ, "reporte", "informe.txt")


def generar_datos(ruta_csv, n=30, semilla=SEMILLA):
    """Genera n observaciones sintéticas del tiempo de atención en caja (minutos).

    Se usa una distribución Exponencial, típica de tiempos de servicio en
    sistemas de atención (muchos tiempos cortos, pocos tiempos largos), y se
    agrega manualmente un valor extremo (observación 25) para poder mostrar
    la detección de outliers con Z-Score.
    """
    rng = np.random.default_rng(semilla)
    tiempos = rng.exponential(scale=3.2, size=n).round(2)
    tiempos[24] = 18.40  # outlier intencional: caja con incidencia (billete falso, reclamo, etc.)

    df = pd.DataFrame({
        "id_observacion": np.arange(1, n + 1),
        "caja": rng.integers(1, 6, size=n),               # caja atendida (1 a 5)
        "tiempo_atencion_min": tiempos
    })
    df.to_csv(ruta_csv, index=False)
    return df


def calcular_estadisticos(serie):
    return {
        "n": int(serie.count()),
        "media": float(serie.mean()),
        "mediana": float(serie.median()),
        "desv_std": float(serie.std(ddof=1)),
        "minimo": float(serie.min()),
        "maximo": float(serie.max()),
        "cv": float(serie.std(ddof=1) / serie.mean()),
    }


def detectar_outliers(df, columna, umbral=UMBRAL_Z):
    df = df.copy()
    df["z_score"] = np.abs(stats.zscore(df[columna]))
    outliers = df[df["z_score"] >= umbral]
    limpios = df[df["z_score"] < umbral]
    return df, outliers, limpios


def escribir_informe(ruta, est_todos, est_limpios, outliers, df_completo):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("INFORME TÉCNICO - PRÁCTICA INDIVIDUAL N° 2\n")
        f.write("=" * 70 + "\n\n")

        f.write("1. NOMBRE DEL ESTUDIANTE\n")
        f.write(f"{NOMBRE_ESTUDIANTE}\n\n")

        f.write("2. TÍTULO DEL CASO\n")
        f.write(f"{TITULO_CASO}\n\n")

        f.write("3. FORMULACIÓN DEL PROBLEMA\n")
        f.write(
            "En un supermercado se han recibido quejas de clientes por demoras en las\n"
            "cajas durante las horas de mayor afluencia. La administración necesita\n"
            "conocer el comportamiento real del tiempo de atención por cliente, para\n"
            "identificar si existen casos atípicos (incidencias puntuales) que distorsionen\n"
            "el promedio y, más adelante, poder dimensionar el número de cajas necesarias.\n\n"
        )

        f.write("4. VARIABLE PRINCIPAL\n")
        f.write(
            "Tiempo de atención en caja (tiempo_atencion_min): minutos que tarda el\n"
            "cajero en atender a un cliente, desde que empieza a registrar los productos\n"
            "hasta que entrega el comprobante de pago. Es una variable cuantitativa\n"
            "continua, medida en minutos.\n\n"
        )

        f.write("5. SUPUESTOS\n")
        f.write(
            "- Los datos son simulados (sintéticos), generados con una distribución\n"
            "  Exponencial (media 3.2 min), semilla fija (2026) para reproducibilidad.\n"
            "- Se asume que cada observación es independiente de las demás.\n"
            "- Se incluyó deliberadamente un valor extremo (observación 25 = 18.40 min)\n"
            "  para representar una incidencia real (por ejemplo, un reclamo o un billete\n"
            "  falso) y poder ilustrar la detección de outliers.\n"
            "- Criterio de exclusión de outliers: |Z-Score| >= 2.5.\n\n"
        )

        f.write("6. ESTADÍSTICOS DESCRIPTIVOS (con los 30 datos originales)\n")
        f.write(f"- n                    : {est_todos['n']}\n")
        f.write(f"- Media                : {est_todos['media']:.2f} min\n")
        f.write(f"- Mediana              : {est_todos['mediana']:.2f} min\n")
        f.write(f"- Desviación estándar  : {est_todos['desv_std']:.2f} min\n")
        f.write(f"- Mínimo               : {est_todos['minimo']:.2f} min\n")
        f.write(f"- Máximo               : {est_todos['maximo']:.2f} min\n")
        f.write(f"- Coef. de variación   : {est_todos['cv']:.2f}\n\n")

        f.write("7. VALORES ATÍPICOS (OUTLIERS) DETECTADOS CON Z-SCORE\n")
        f.write(f"Criterio: se excluye toda observación con |Z| >= {UMBRAL_Z}\n\n")
        if len(outliers) > 0:
            f.write(f"Se detectaron {len(outliers)} outlier(s):\n")
            f.write(outliers[["id_observacion", "tiempo_atencion_min", "z_score"]].to_string(index=False))
            f.write("\n\n")
        else:
            f.write("No se detectaron outliers con el criterio establecido.\n\n")

        f.write("8. ANÁLISIS DESCRIPTIVO DE LA VARIABLE (datos depurados)\n")
        f.write(f"- n depurado           : {est_limpios['n']}\n")
        f.write(f"- Media                : {est_limpios['media']:.2f} min\n")
        f.write(f"- Mediana              : {est_limpios['mediana']:.2f} min\n")
        f.write(f"- Desviación estándar  : {est_limpios['desv_std']:.2f} min\n")
        f.write(f"- Mínimo               : {est_limpios['minimo']:.2f} min\n")
        f.write(f"- Máximo               : {est_limpios['maximo']:.2f} min\n")
        f.write(f"- Coef. de variación   : {est_limpios['cv']:.2f}\n\n")

        f.write("9. INTERPRETACIÓN TÉCNICA\n")
        f.write(
            f"La media de atención sin depurar ({est_todos['media']:.2f} min) está inflada\n"
            f"por el valor atípico de {outliers['tiempo_atencion_min'].iloc[0]:.2f} min "
            f"(Z = {outliers['z_score'].iloc[0]:.2f}),\n"
            f"muy por encima del umbral de {UMBRAL_Z}. Al depurar ese dato, la media baja a\n"
            f"{est_limpios['media']:.2f} min, un valor más representativo del servicio normal.\n"
            f"El coeficiente de variación depurado ({est_limpios['cv']:.2f}) sigue siendo alto,\n"
            "lo que indica que el tiempo de atención es bastante variable incluso sin\n"
            "incidencias, algo típico de un proceso con distribución Exponencial\n"
            "(muchos clientes rápidos y algunos pocos que tardan bastante más).\n\n"
        )

        f.write("10. CONCLUSIÓN\n")
        f.write(
            "El sistema de cajas del supermercado presenta un tiempo de atención\n"
            f"promedio de {est_limpios['media']:.2f} minutos por cliente en condiciones\n"
            "normales. Se identificó una observación atípica que corresponde a una\n"
            "incidencia puntual y no a la operación habitual, por lo que debe excluirse\n"
            "del análisis de desempeño regular, aunque sí debe registrarse aparte como\n"
            "evento especial. Se recomienda recolectar más datos en distintos horarios y,\n"
            "en una siguiente etapa, formular un modelo de colas (por ejemplo, M/M/1 o\n"
            "M/M/c) para evaluar el número óptimo de cajas abiertas en horas pico.\n\n"
        )

        f.write("=" * 70 + "\n")
        f.write(f"Total de observaciones procesadas: {len(df_completo)}\n")
        f.write("=" * 70 + "\n")


def main():
    print("=" * 60)
    print("PRÁCTICA INDIVIDUAL N° 2 - ANÁLISIS PRELIMINAR")
    print(TITULO_CASO)
    print("=" * 60)

    os.makedirs(os.path.dirname(RUTA_DATOS), exist_ok=True)
    os.makedirs(os.path.dirname(RUTA_INFORME), exist_ok=True)

    # 1) Datos: si ya existe datos/datos.csv se reutiliza (reproducibilidad);
    #    si no existe, se genera.
    if os.path.exists(RUTA_DATOS):
        print(f"\nLeyendo datos existentes: {RUTA_DATOS}")
        df = pd.read_csv(RUTA_DATOS)
    else:
        print(f"\nGenerando datos sintéticos (semilla={SEMILLA}) en: {RUTA_DATOS}")
        df = generar_datos(RUTA_DATOS)

    print(f"Observaciones: {len(df)}")

    # 2) Estadísticos con todos los datos
    est_todos = calcular_estadisticos(df["tiempo_atencion_min"])
    print("\n--- ESTADÍSTICOS (datos originales) ---")
    for k, v in est_todos.items():
        print(f"{k}: {v:.4f}" if isinstance(v, float) else f"{k}: {v}")

    # 3) Z-Score y outliers
    df_z, outliers, df_limpio = detectar_outliers(df, "tiempo_atencion_min")
    print(f"\n--- OUTLIERS (|Z| >= {UMBRAL_Z}) ---")
    if len(outliers) > 0:
        print(outliers[["id_observacion", "tiempo_atencion_min", "z_score"]].to_string(index=False))
    else:
        print("No se detectaron outliers.")

    # 4) Estadísticos depurados
    est_limpios = calcular_estadisticos(df_limpio["tiempo_atencion_min"])
    print("\n--- ESTADÍSTICOS (datos depurados) ---")
    for k, v in est_limpios.items():
        print(f"{k}: {v:.4f}" if isinstance(v, float) else f"{k}: {v}")

    # 5) Informe técnico
    escribir_informe(RUTA_INFORME, est_todos, est_limpios, outliers, df)
    print(f"\nInforme generado en: {RUTA_INFORME}")

    print("\n" + "=" * 60)
    print("Proceso finalizado.")
    print("=" * 60)


if __name__ == "__main__":
    main()
