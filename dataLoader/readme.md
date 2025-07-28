# DataLoader Module

Este módulo se encarga de cargar datos desde archivos Excel a la base de datos con generación automática de archivos SQL históricos.

## Funcionalidades

1. **Carga de datos**: Convierte archivos .xlsx en instrucciones SQL e inserta en tablas
2. **Generación de SQL histórico**: Después de cada inserción, genera archivos .sql con versionado
3. **Gestión de versiones**: Mantiene un historial de cambios para poder replicar inserts

## Uso

### Ejecutar carga de datos (con generación automática de SQL)
```bash
pwd && ls -la loader.py && python loader.py
```

### Gestionar versiones SQL
```bash
# Listar todas las versiones disponibles
python sql_version_manager.py list

# Ver detalles de una versión específica
python sql_version_manager.py show V1_20250728_143000

# Aplicar una versión específica a la base de datos
python sql_version_manager.py apply V1_20250728_143000

# Aplicar sin confirmación
python sql_version_manager.py apply V1_20250728_143000 --yes
```

## Estructura de archivos generados

Cada ejecución de `loader.py` genera una nueva versión en:
```
share/SQL/V{numero}_{timestamp}/
├── version_info.sql          # Metadatos de la versión
├── map.sql                   # INSERT statements para tabla map
├── centerpos2x.sql           # INSERT statements para tabla centerpos2x
├── bamboopattern.sql         # INSERT statements para tabla bamboopattern
└── largescreenpixelpos.sql   # INSERT statements para tabla largescreenpixelpos
```

## Ejemplo de versionado

- Primera ejecución: `V1_20250728_143000`
- Segunda ejecución: `V2_20250728_150000`
- Tercera ejecución: `V3_20250729_091500`

Esto permite mantener un historial completo de todos los cambios y poder revertir o replicar cualquier versión anterior.

## Servicios incluidos

- `SqlExportService`: Genera archivos SQL con versionado automático
- `SqlVersionManager`: Gestiona la aplicación de versiones específicas