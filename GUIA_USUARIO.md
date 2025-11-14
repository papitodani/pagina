# Guía del Usuario - Sistema de Nóminas

## 📖 Introducción

Bienvenido al Sistema de Gestión de Nóminas. Esta guía te ayudará a utilizar todas las funcionalidades del sistema de manera efectiva.

## 🚀 Primeros Pasos

### Acceso al Sistema

1. Abre tu navegador web
2. Navega a `http://localhost:5000` (o la dirección proporcionada)
3. Verás el Dashboard principal

## 📊 Dashboard (Pantalla Principal)

El dashboard muestra:
- **Total de Empleados**: Número de empleados activos
- **Nóminas Procesadas**: Total de nóminas en el sistema
- **Este Periodo**: Nóminas del periodo actual
- **Total a Pagar**: Suma del periodo actual
- **Nóminas Recientes**: Últimas 5 nóminas procesadas

### Acciones Rápidas
- **Nueva Nómina**: Ir directamente a crear una nómina
- **Calculadora Rápida**: Calcular sin guardar
- **Ver Reportes**: Acceder a reportes y exportaciones

## 👥 Gestión de Empleados

### Crear un Nuevo Empleado

1. Ve a **Nóminas** → pestaña **Empleados**
2. Clic en **"Nuevo Empleado"**
3. Completa el formulario:
   - **Nombre Completo**: Nombre del empleado
   - **Sueldo Diario**: Salario por día en pesos
4. Clic en **"Guardar"**

### Editar un Empleado

1. En la lista de empleados, clic en el botón **"Editar"** (icono de lápiz)
2. Modifica los datos necesarios
3. Guarda los cambios

### Desactivar un Empleado

1. Clic en el botón **"Eliminar"** (icono de basura)
2. Confirma la acción
3. El empleado se marca como inactivo (no se elimina del sistema)

## 💰 Crear una Nómina

### Paso 1: Seleccionar Empleado

1. Ve a **Nóminas** → pestaña **Nueva Nómina**
2. Selecciona el empleado del menú desplegable
3. El sueldo diario se muestra en la opción seleccionada

### Paso 2: Ingresar Periodo

Ingresa el periodo de la nómina:
- Formato: `YYYY-MM-DD a YYYY-MM-DD`
- Ejemplo: `2024-11-01 a 2024-11-15`

### Paso 3: Datos de Trabajo

**Días Trabajados** (1-31)
- Por defecto: 15 días
- Modifica según corresponda

**Horas Extra**
- Número de horas trabajadas adicionales
- Se pagan a $35 pesos por hora

**Faltas**
- Número de días de ausencia
- **Importante**: Las faltas SE SUMAN al sueldo (no se restan)
- Cada falta suma 1 día de sueldo al total

**Tardes**
- Número de llegadas tarde
- El descuento es configurable en el siguiente campo

### Paso 4: Bonos

**Bono de Puntualidad**
- Por defecto: $100 pesos
- Modifica según política de la empresa
- Se otorga por asistencia puntual

**Bono de Producción**
- Por defecto: $100 pesos
- Se da entre 5 empleados según desempeño

### Paso 5: Descuentos

**Descuento por Tardes**
- Monto variable según número de tardes
- Ingresa el monto total a descontar

**Préstamo Total**
- Monto total del préstamo activo
- **Se descuenta el 3%** del total
- Ejemplo: Préstamo de $1,000 → Descuento de $30

**Caja de Ahorro**
- Monto que el empleado ahorra
- Se descuenta directamente del total

### Paso 6: Calcular y Guardar

1. Clic en **"Calcular"** para ver vista previa
2. El sistema muestra todos los cálculos
3. Revisa que todo esté correcto
4. Clic en **"Guardar Nómina"**

## 🧮 Calculadora Rápida

Para hacer cálculos sin guardar en el sistema:

1. Ve a **Calculadora** en el menú
2. Ingresa el sueldo diario
3. Completa los demás campos
4. **Los cálculos se actualizan automáticamente**
5. Útil para simular diferentes escenarios

### Ejemplo de Cálculo

**Entrada:**
- Sueldo diario: $250
- Días trabajados: 15
- Horas extra: 10
- Faltas: 1
- Bono puntualidad: $100
- Bono producción: $100
- Préstamo: $1,000
- Descuento tardes: $50
- Caja ahorro: $200

**Resultado:**
- Sueldo base: $3,750 (15 × $250)
- Pago extras: $350 (10 × $35)
- Ajuste faltas: $250 (1 × $250) ← Se suma
- Total bonos: $200
- Desc. préstamo: $30 (3% de $1,000)
- Total descuentos: $280
- **TOTAL A PAGAR: $4,270**

## 📋 Historial de Nóminas

### Ver Todas las Nóminas

1. Ve a **Nóminas** → pestaña **Nóminas**
2. Verás una tabla con todas las nóminas
3. Puedes filtrar por periodo usando el selector

### Columnas de la Tabla

- **ID**: Número único de la nómina
- **Empleado**: Nombre del empleado
- **Periodo**: Fechas de la nómina
- **Días**: Días trabajados
- **Extras**: Horas extra trabajadas
- **Bonos**: Total de bonos
- **Descuentos**: Total de deducciones
- **Total**: Monto a pagar

### Acciones en Nóminas

- **PDF**: Descargar recibo en PDF
- **Eliminar**: Borrar la nómina (requiere confirmación)

## 📊 Reportes

### Exportar a PDF

1. Ve a **Reportes**
2. Selecciona un periodo (o todos)
3. Se muestra lista de nóminas
4. Clic en cualquier nómina para descargar su PDF
5. El PDF incluye:
   - Datos del empleado
   - Desglose completo
   - Percepciones y deducciones
   - Total a pagar

### Exportar a Excel

1. Ve a **Reportes**
2. Selecciona un periodo (opcional)
3. Clic en **"Descargar Excel"**
4. Se descarga un archivo `.xlsx` con:
   - Todas las nóminas del periodo
   - Formato tabular profesional
   - Listo para análisis

### Resumen por Periodo

1. Ve a **Reportes** → sección **Resumen por Periodo**
2. Selecciona un periodo
3. Clic en **"Generar Resumen"**
4. Verás:
   - Total de empleados
   - Suma de sueldos base
   - Total de bonos
   - Total de descuentos
   - **Gran total a pagar**

### Estadísticas por Empleado

1. Ve a **Reportes** → sección **Estadísticas por Empleado**
2. Selecciona un empleado
3. Clic en **"Ver Estadísticas"**
4. Verás historial completo de nóminas del empleado

## 📱 Uso en Dispositivos Móviles

El sistema es completamente responsive:

- **Menú de navegación**: Se colapsa en un botón hamburguesa
- **Tablas**: Se desplazan horizontalmente si es necesario
- **Formularios**: Se adaptan al tamaño de pantalla
- **Botones**: Tamaño táctil apropiado

## 💡 Consejos y Mejores Prácticas

### Nomenclatura de Periodos

Usa un formato consistente:
- Quincenal: `2024-11-01 a 2024-11-15`, `2024-11-16 a 2024-11-30`
- Semanal: `2024-11-01 a 2024-11-07`
- Mensual: `2024-11-01 a 2024-11-30`

### Respaldo de Datos

- El sistema guarda todo en `nominas.db`
- Haz respaldos periódicos de este archivo
- Ubicación: carpeta `instance/` del proyecto

### Corrección de Errores

Si creaste una nómina con datos incorrectos:
1. Elimina la nómina incorrecta
2. Crea una nueva con los datos correctos

### Bonos de Producción

Se recomienda:
1. Calcular todas las nóminas primero
2. Identificar los 5 empleados con mejor desempeño
3. Asignar el bono de producción solo a esos 5

## ❓ Preguntas Frecuentes

**P: ¿Por qué las faltas aumentan el total?**
R: Según las reglas del sistema, cada falta suma un día de sueldo al total. Esto es intencional y sigue la política especificada.

**P: ¿Puedo cambiar el precio de las horas extra?**
R: Sí, pero requiere modificar el archivo `config.py`. Por defecto es $35.

**P: ¿Cómo elimino permanentemente un empleado?**
R: Los empleados no se eliminan, solo se desactivan. Esto mantiene el historial intacto.

**P: ¿Puedo editar una nómina ya creada?**
R: Por el momento, debes eliminar y recrear la nómina. Se recomienda revisar bien antes de guardar.

**P: ¿El sistema calcula impuestos?**
R: No, este sistema solo calcula el neto según las reglas especificadas. Los impuestos deben manejarse por separado.

## 🆘 Soporte

Si encuentras algún problema:
1. Verifica que todos los datos ingresados sean correctos
2. Revisa la consola del navegador (F12) para errores
3. Contacta al administrador del sistema
4. Reporta issues en el repositorio de GitHub

## 📞 Contacto

Para más información o soporte técnico, contacta al administrador del sistema.

---

**Versión del documento**: 1.0  
**Última actualización**: Noviembre 2024
