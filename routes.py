"""
API routes for the payroll application
"""
from flask import Blueprint, request, jsonify, send_file
from models import db, Empleado, Nomina, ConfiguracionGlobal
from utils.calculos import calcular_nomina, validar_datos_nomina
from utils.reportes import generar_pdf_nomina, generar_excel_nominas, generar_resumen_periodo
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')


# ============= EMPLEADOS ENDPOINTS =============

@api_bp.route('/empleados', methods=['GET'])
def get_empleados():
    """Get all active employees"""
    empleados = Empleado.query.filter_by(activo=True).all()
    return jsonify([e.to_dict() for e in empleados])


@api_bp.route('/empleados/<int:empleado_id>', methods=['GET'])
def get_empleado(empleado_id):
    """Get employee by ID"""
    empleado = Empleado.query.get_or_404(empleado_id)
    return jsonify(empleado.to_dict())


@api_bp.route('/empleados', methods=['POST'])
def create_empleado():
    """Create new employee"""
    data = request.get_json()
    
    if not data or 'nombre' not in data or 'sueldo_diario' not in data:
        return jsonify({'error': 'Nombre y sueldo diario son requeridos'}), 400
    
    try:
        empleado = Empleado(
            nombre=data['nombre'],
            sueldo_diario=float(data['sueldo_diario'])
        )
        db.session.add(empleado)
        db.session.commit()
        return jsonify(empleado.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/empleados/<int:empleado_id>', methods=['PUT'])
def update_empleado(empleado_id):
    """Update employee"""
    empleado = Empleado.query.get_or_404(empleado_id)
    data = request.get_json()
    
    try:
        if 'nombre' in data:
            empleado.nombre = data['nombre']
        if 'sueldo_diario' in data:
            empleado.sueldo_diario = float(data['sueldo_diario'])
        if 'activo' in data:
            empleado.activo = bool(data['activo'])
        
        db.session.commit()
        return jsonify(empleado.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/empleados/<int:empleado_id>', methods=['DELETE'])
def delete_empleado(empleado_id):
    """Soft delete employee (mark as inactive)"""
    empleado = Empleado.query.get_or_404(empleado_id)
    
    try:
        empleado.activo = False
        db.session.commit()
        return jsonify({'message': 'Empleado desactivado correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============= NOMINAS ENDPOINTS =============

@api_bp.route('/nominas', methods=['GET'])
def get_nominas():
    """Get all payroll records"""
    periodo = request.args.get('periodo')
    empleado_id = request.args.get('empleado_id')
    
    query = Nomina.query
    
    if periodo:
        query = query.filter_by(periodo=periodo)
    if empleado_id:
        query = query.filter_by(empleado_id=int(empleado_id))
    
    nominas = query.order_by(Nomina.fecha_calculo.desc()).all()
    return jsonify([n.to_dict() for n in nominas])


@api_bp.route('/nominas/<int:nomina_id>', methods=['GET'])
def get_nomina(nomina_id):
    """Get payroll record by ID"""
    nomina = Nomina.query.get_or_404(nomina_id)
    return jsonify(nomina.to_dict())


@api_bp.route('/nominas', methods=['POST'])
def create_nomina():
    """Create new payroll record"""
    data = request.get_json()
    
    # Validate data
    is_valid, error_msg = validar_datos_nomina(data)
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    try:
        # Get employee
        empleado = Empleado.query.get(data['empleado_id'])
        if not empleado:
            return jsonify({'error': 'Empleado no encontrado'}), 404
        
        # Get configuration
        from flask import current_app
        config = current_app.config
        
        # Calculate payroll
        calculos = calcular_nomina(empleado, data, config)
        
        # Create payroll record
        nomina = Nomina(
            empleado_id=data['empleado_id'],
            periodo=data['periodo'],
            dias_trabajados=int(data.get('dias_trabajados', 15)),
            horas_extra=float(data.get('horas_extra', 0)),
            faltas=int(data.get('faltas', 0)),
            tardes=int(data.get('tardes', 0)),
            bono_puntualidad=float(data.get('bono_puntualidad', 0)),
            bono_produccion=float(data.get('bono_produccion', 0)),
            prestamo=float(data.get('prestamo', 0)),
            caja_ahorro=float(data.get('caja_ahorro', 0)),
            descuento_tardes=float(data.get('descuento_tardes', 0)),
            sueldo_base=calculos['sueldo_base'],
            pago_extras=calculos['pago_extras'],
            ajuste_faltas=calculos['ajuste_faltas'],
            total_bonos=calculos['total_bonos'],
            descuento_prestamo=calculos['descuento_prestamo'],
            total_descuentos=calculos['total_descuentos'],
            total_pagar=calculos['total_pagar']
        )
        
        db.session.add(nomina)
        db.session.commit()
        return jsonify(nomina.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/nominas/<int:nomina_id>', methods=['PUT'])
def update_nomina(nomina_id):
    """Update payroll record"""
    nomina = Nomina.query.get_or_404(nomina_id)
    data = request.get_json()
    
    try:
        # Get employee
        empleado = Empleado.query.get(nomina.empleado_id)
        
        # Update work data if provided
        if 'dias_trabajados' in data:
            nomina.dias_trabajados = int(data['dias_trabajados'])
        if 'horas_extra' in data:
            nomina.horas_extra = float(data['horas_extra'])
        if 'faltas' in data:
            nomina.faltas = int(data['faltas'])
        if 'tardes' in data:
            nomina.tardes = int(data['tardes'])
        if 'bono_puntualidad' in data:
            nomina.bono_puntualidad = float(data['bono_puntualidad'])
        if 'bono_produccion' in data:
            nomina.bono_produccion = float(data['bono_produccion'])
        if 'prestamo' in data:
            nomina.prestamo = float(data['prestamo'])
        if 'caja_ahorro' in data:
            nomina.caja_ahorro = float(data['caja_ahorro'])
        if 'descuento_tardes' in data:
            nomina.descuento_tardes = float(data['descuento_tardes'])
        
        # Recalculate payroll
        from flask import current_app
        config = current_app.config
        
        datos_nomina = {
            'dias_trabajados': nomina.dias_trabajados,
            'horas_extra': nomina.horas_extra,
            'faltas': nomina.faltas,
            'tardes': nomina.tardes,
            'bono_puntualidad': nomina.bono_puntualidad,
            'bono_produccion': nomina.bono_produccion,
            'prestamo': nomina.prestamo,
            'caja_ahorro': nomina.caja_ahorro,
            'descuento_tardes': nomina.descuento_tardes
        }
        
        calculos = calcular_nomina(empleado, datos_nomina, config)
        
        nomina.sueldo_base = calculos['sueldo_base']
        nomina.pago_extras = calculos['pago_extras']
        nomina.ajuste_faltas = calculos['ajuste_faltas']
        nomina.total_bonos = calculos['total_bonos']
        nomina.descuento_prestamo = calculos['descuento_prestamo']
        nomina.total_descuentos = calculos['total_descuentos']
        nomina.total_pagar = calculos['total_pagar']
        
        db.session.commit()
        return jsonify(nomina.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/nominas/<int:nomina_id>', methods=['DELETE'])
def delete_nomina(nomina_id):
    """Delete payroll record"""
    nomina = Nomina.query.get_or_404(nomina_id)
    
    try:
        db.session.delete(nomina)
        db.session.commit()
        return jsonify({'message': 'Nómina eliminada correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============= CALCULOS ENDPOINT =============

@api_bp.route('/calcular', methods=['POST'])
def calcular():
    """Calculate payroll without saving"""
    data = request.get_json()
    
    if not data or 'empleado_id' not in data:
        return jsonify({'error': 'ID de empleado requerido'}), 400
    
    try:
        empleado = Empleado.query.get(data['empleado_id'])
        if not empleado:
            return jsonify({'error': 'Empleado no encontrado'}), 404
        
        from flask import current_app
        config = current_app.config
        
        calculos = calcular_nomina(empleado, data, config)
        return jsonify(calculos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= REPORTES ENDPOINTS =============

@api_bp.route('/reportes/pdf/<int:nomina_id>', methods=['GET'])
def generar_pdf(nomina_id):
    """Generate PDF report for payroll record"""
    nomina = Nomina.query.get_or_404(nomina_id)
    empleado = Empleado.query.get(nomina.empleado_id)
    
    try:
        pdf_buffer = generar_pdf_nomina(nomina, empleado)
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'nomina_{empleado.nombre}_{nomina.periodo}.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/reportes/excel', methods=['GET'])
def generar_excel():
    """Generate Excel report for all payroll records"""
    periodo = request.args.get('periodo')
    
    query = Nomina.query
    if periodo:
        query = query.filter_by(periodo=periodo)
    
    nominas = query.all()
    
    # Get all employees
    empleados = {e.id: e for e in Empleado.query.all()}
    
    try:
        excel_buffer = generar_excel_nominas(nominas, empleados)
        filename = f'nominas_{periodo if periodo else "todas"}.xlsx'
        return send_file(
            excel_buffer,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/reportes/resumen', methods=['GET'])
def resumen_periodo():
    """Get summary for a payroll period"""
    periodo = request.args.get('periodo')
    if not periodo:
        return jsonify({'error': 'Periodo requerido'}), 400
    
    nominas = Nomina.query.filter_by(periodo=periodo).all()
    resumen = generar_resumen_periodo(nominas, periodo)
    
    return jsonify(resumen)


# ============= CONFIGURACION ENDPOINTS =============

@api_bp.route('/configuracion', methods=['GET'])
def get_configuracion():
    """Get global configuration"""
    from flask import current_app
    config = current_app.config
    
    return jsonify({
        'precio_hora_extra': config.get('PRECIO_HORA_EXTRA', 35),
        'bono_puntualidad_default': config.get('BONO_PUNTUALIDAD_DEFAULT', 100),
        'bono_produccion_default': config.get('BONO_PRODUCCION_DEFAULT', 100),
        'porcentaje_prestamo': config.get('PORCENTAJE_PRESTAMO', 3)
    })


@api_bp.route('/periodos', methods=['GET'])
def get_periodos():
    """Get all unique periods"""
    periodos = db.session.query(Nomina.periodo).distinct().order_by(Nomina.periodo.desc()).all()
    return jsonify([p[0] for p in periodos])
