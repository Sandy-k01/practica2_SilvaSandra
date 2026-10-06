# Práctica Individual N° 2 — Formulación y análisis preliminar de un sistema real

**Estudiante:** Sandra Silva
**Materia:** Simulación — Ingeniería de Sistemas (UBi)
**Caso elegido:** Tiempo de atención en cajas de un supermercado

## Descripción

Se analiza el tiempo que tarda un cajero en atender a un cliente en un
supermercado. Se trabaja con 30 observaciones (simuladas con una
distribución Exponencial, semilla fija = 2026, para que el resultado sea
reproducible). Se calculan estadísticos descriptivos, se detectan valores
atípicos con Z-Score y se redacta un informe técnico con la interpretación
y la conclusión.

## Estructura del repositorio

```
practica2_SilvaSandra/
├── datos/
│   └── datos.csv          Datos crudos (30 observaciones)
├── scripts/
│   └── analisis.py        Script de análisis (genera datos, estadísticos,
│                           outliers e informe)
├── reporte/
│   └── informe.txt         Informe técnico generado por el script
└── README.md               Este archivo
```

## Requisitos

- Python 3.10 o superior
- Librerías: `numpy`, `pandas`, `scipy`

Instalación:

```bash
pip install numpy pandas scipy
```

## Cómo ejecutar

Desde la **raíz** de esta carpeta (`practica2_SilvaSandra`):

```bash
python scripts/analisis.py
```

El script:

1. Si `datos/datos.csv` no existe, lo genera (semilla fija = 2026).
2. Si ya existe, lo reutiliza, para que los resultados sean siempre los
   mismos.
3. Calcula los estadísticos descriptivos de la variable principal.
4. Detecta outliers con el criterio `|Z-Score| >= 2.5`.
5. Genera automáticamente `reporte/informe.txt` con las 10 secciones
   requeridas.

## Resultados obtenidos

| Magnitud | Con outlier (30 datos) | Depurado (29 datos) |
|---|---|---|
| Media | 3.65 min | 3.14 min |
| Desviación estándar | 3.74 min | 2.55 min |
| Outlier detectado | Observación 25, 18.40 min, Z = 4.01 | — |

## Notas

- El detalle completo de la formulación del problema, los supuestos, el
  análisis y la conclusión está en `reporte/informe.txt`.
- La observación 25 (18.40 min) es un valor atípico introducido a
  propósito, que simula una incidencia puntual en caja (por ejemplo, un
  reclamo o un billete falso), para poder mostrar la detección de
  outliers con Z-Score.
