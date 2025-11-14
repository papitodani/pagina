"""
Payroll calculation logic
"""

def calcular_nomina(empleado, datos_nomina, config):
    """
    Calculate payroll for an employee based on work data
    
    Args:
        empleado: Employee object
        datos_nomina: Dictionary with work data (horas_extra, faltas, tardes, etc.)
        config: Configuration object with rates
    
    Returns:
        Dictionary with all calculated amounts
    """
    # Get base salary
    sueldo_diario = empleado.sueldo_diario
    dias_trabajados = datos_nomina.get('dias_trabajados', 15)
    
    # Calculate base salary
    sueldo_base = sueldo_diario * dias_trabajados
    
    # Calculate extra hours pay
    horas_extra = datos_nomina.get('horas_extra', 0)
    precio_hora_extra = config.get('PRECIO_HORA_EXTRA', 35)
    pago_extras = horas_extra * precio_hora_extra
    
    # Calculate absences adjustment (faltas se suman al sueldo)
    # 1 falta = +sueldo_diario (as specified in requirements)
    faltas = datos_nomina.get('faltas', 0)
    ajuste_faltas = faltas * sueldo_diario
    
    # Calculate bonuses
    bono_puntualidad = datos_nomina.get('bono_puntualidad', 0)
    bono_produccion = datos_nomina.get('bono_produccion', 0)
    total_bonos = bono_puntualidad + bono_produccion
    
    # Calculate deductions
    # Late arrivals deduction
    descuento_tardes = datos_nomina.get('descuento_tardes', 0)
    
    # Loan deduction (3% of amount owed)
    prestamo = datos_nomina.get('prestamo', 0)
    porcentaje_prestamo = config.get('PORCENTAJE_PRESTAMO', 3)
    descuento_prestamo = prestamo * (porcentaje_prestamo / 100)
    
    # Savings deduction
    caja_ahorro = datos_nomina.get('caja_ahorro', 0)
    
    # Total deductions
    total_descuentos = descuento_tardes + descuento_prestamo + caja_ahorro
    
    # Calculate total to pay
    # Total = Sueldo Base + Extras + Ajuste Faltas + Bonos - Descuentos
    total_pagar = sueldo_base + pago_extras + ajuste_faltas + total_bonos - total_descuentos
    
    return {
        'sueldo_base': round(sueldo_base, 2),
        'pago_extras': round(pago_extras, 2),
        'ajuste_faltas': round(ajuste_faltas, 2),
        'total_bonos': round(total_bonos, 2),
        'descuento_prestamo': round(descuento_prestamo, 2),
        'total_descuentos': round(total_descuentos, 2),
        'total_pagar': round(total_pagar, 2)
    }


def validar_datos_nomina(datos):
    """
    Validate payroll data
    
    Args:
        datos: Dictionary with payroll data
    
    Returns:
        Tuple (is_valid, error_message)
    """
    errores = []
    
    # Validate required fields
    if 'empleado_id' not in datos:
        errores.append('ID de empleado requerido')
    
    if 'periodo' not in datos:
        errores.append('Periodo requerido')
    
    # Validate numeric fields
    campos_numericos = [
        'dias_trabajados', 'horas_extra', 'faltas', 'tardes',
        'bono_puntualidad', 'bono_produccion', 'prestamo',
        'caja_ahorro', 'descuento_tardes'
    ]
    
    for campo in campos_numericos:
        if campo in datos:
            try:
                valor = float(datos[campo])
                if valor < 0:
                    errores.append(f'{campo} no puede ser negativo')
            except (ValueError, TypeError):
                errores.append(f'{campo} debe ser un número válido')
    
    # Validate days worked
    if 'dias_trabajados' in datos:
        dias = int(datos.get('dias_trabajados', 0))
        if dias < 0 or dias > 31:
            errores.append('Días trabajados debe estar entre 0 y 31')
    
    if errores:
        return False, '; '.join(errores)
    
    return True, None
