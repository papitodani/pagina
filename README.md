# Sistema de Gestión de Nóminas

Sistema completo de gestión y cálculo de nóminas desarrollado con Flask, Bootstrap y SQLite.

## 🚀 Características

- **Dashboard Interactivo**: Vista general de estadísticas y métricas
- **Gestión de Empleados**: Crear, editar y administrar empleados
- **Cálculo Automático**: Cálculo en tiempo real de nóminas
- **Calculadora Rápida**: Herramienta para calcular nóminas sin guardarlas
- **Historial de Nóminas**: Seguimiento completo de todas las nóminas procesadas
- **Reportes PDF**: Generación de recibos de nómina en PDF
- **Exportación Excel**: Exportar datos a Excel para análisis
- **Interfaz Responsive**: Compatible con dispositivos móviles, tablets y desktop

## 📋 Reglas de Cálculo

1. **Extras**: $35 pesos por hora (configurable)
2. **Descuento por Faltas**: Se suma al sueldo (1 falta = +sueldo diario)
3. **Bono de Puntualidad**: $100 pesos (configurable por empleado)
4. **Bono de Producción**: $100 pesos (configurable por empleado)
5. **Préstamo (3%)**: Se calcula sobre lo que deben, se descuenta del total
6. **Caja de Ahorro**: Se descuenta del total a pagar
7. **Tardes**: Descuento variable (definible en la interfaz)

## 🛠️ Stack Técnico

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Base de Datos**: SQLite
- **Reportes**: 
  - PDF: ReportLab
  - Excel: OpenPyXL

## 📁 Estructura del Proyecto

```
pagina/
├── app.py                  # Aplicación Flask principal
├── config.py              # Configuración
├── models.py              # Modelos de base de datos
├── routes.py              # Rutas API
├── requirements.txt       # Dependencias Python
├── templates/            # Templates HTML
│   ├── base.html         # Template base
│   ├── index.html        # Dashboard
│   ├── nomina.html       # Gestión de nóminas
│   ├── reportes.html     # Reportes
│   └── calculadora.html  # Calculadora rápida
├── static/              # Archivos estáticos
│   ├── css/
│   │   └── style.css    # Estilos personalizados
│   └── js/
│       ├── app.js       # JavaScript principal
│       └── calculos.js  # Lógica de cálculos
└── utils/               # Utilidades
    ├── calculos.py      # Lógica de cálculos backend
    └── reportes.py      # Generación de reportes
```

## 🚀 Instalación y Uso

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/papitodani/pagina.git
   cd pagina
   ```

2. **Crear entorno virtual** (recomendado):
   ```bash
   python -m venv venv
   
   # En Windows:
   venv\Scripts\activate
   
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**:
   ```bash
   python app.py
   ```

5. **Abrir en el navegador**:
   ```
   http://localhost:5000
   ```

## 📱 Uso de la Aplicación

### Dashboard
- Vista general con estadísticas
- Acceso rápido a funciones principales
- Nóminas recientes

### Gestión de Empleados
1. Ir a **Nóminas** → pestaña **Empleados**
2. Hacer clic en **Nuevo Empleado**
3. Ingresar nombre y sueldo diario
4. Guardar

### Crear Nómina
1. Ir a **Nóminas** → pestaña **Nueva Nómina**
2. Seleccionar empleado
3. Ingresar datos:
   - Periodo
   - Días trabajados
   - Horas extra
   - Faltas y tardes
   - Bonos
   - Préstamos y deducciones
4. El cálculo se actualiza automáticamente
5. Guardar nómina

### Calculadora Rápida
1. Ir a **Calculadora**
2. Ingresar sueldo diario y demás datos
3. Ver resultado en tiempo real
4. No se guarda en el sistema

### Generar Reportes
1. Ir a **Reportes**
2. Opciones disponibles:
   - **PDF individual**: Por nómina
   - **Excel consolidado**: Todas las nóminas
   - **Resumen por periodo**: Estadísticas

## 🔧 Configuración

Las configuraciones se pueden modificar en `config.py`:

```python
PRECIO_HORA_EXTRA = 35        # Precio por hora extra
BONO_PUNTUALIDAD_DEFAULT = 100  # Bono de puntualidad
BONO_PRODUCCION_DEFAULT = 100   # Bono de producción
PORCENTAJE_PRESTAMO = 3         # Porcentaje de préstamo
```

## 📊 API Endpoints

### Empleados
- `GET /api/empleados` - Listar empleados
- `POST /api/empleados` - Crear empleado
- `PUT /api/empleados/<id>` - Actualizar empleado
- `DELETE /api/empleados/<id>` - Desactivar empleado

### Nóminas
- `GET /api/nominas` - Listar nóminas
- `POST /api/nominas` - Crear nómina
- `PUT /api/nominas/<id>` - Actualizar nómina
- `DELETE /api/nominas/<id>` - Eliminar nómina
- `POST /api/calcular` - Calcular nómina sin guardar

### Reportes
- `GET /api/reportes/pdf/<id>` - Generar PDF
- `GET /api/reportes/excel` - Exportar Excel
- `GET /api/reportes/resumen?periodo=<periodo>` - Resumen

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 👨‍💻 Autor

**papitodani**

## 📞 Soporte

Para soporte o preguntas, por favor abrir un issue en el repositorio de GitHub.