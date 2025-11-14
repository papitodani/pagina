"""
Database models for the payroll application
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Empleado(db.Model):
    """Employee model"""
    __tablename__ = 'empleados'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    sueldo_diario = db.Column(db.Float, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    nominas = db.relationship('Nomina', backref='empleado', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'sueldo_diario': self.sueldo_diario,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat()
        }

class Nomina(db.Model):
    """Payroll record model"""
    __tablename__ = 'nominas'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    periodo = db.Column(db.String(50), nullable=False)  # e.g., "2024-01-01 a 2024-01-15"
    fecha_calculo = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Work data
    dias_trabajados = db.Column(db.Integer, default=15)
    horas_extra = db.Column(db.Float, default=0)
    faltas = db.Column(db.Integer, default=0)
    tardes = db.Column(db.Integer, default=0)
    
    # Bonuses
    bono_puntualidad = db.Column(db.Float, default=0)
    bono_produccion = db.Column(db.Float, default=0)
    
    # Deductions
    prestamo = db.Column(db.Float, default=0)  # amount owed
    caja_ahorro = db.Column(db.Float, default=0)
    descuento_tardes = db.Column(db.Float, default=0)
    
    # Calculated amounts
    sueldo_base = db.Column(db.Float, nullable=False)
    pago_extras = db.Column(db.Float, default=0)
    ajuste_faltas = db.Column(db.Float, default=0)
    total_bonos = db.Column(db.Float, default=0)
    descuento_prestamo = db.Column(db.Float, default=0)
    total_descuentos = db.Column(db.Float, default=0)
    total_pagar = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'empleado_id': self.empleado_id,
            'empleado_nombre': self.empleado.nombre if self.empleado else None,
            'periodo': self.periodo,
            'fecha_calculo': self.fecha_calculo.isoformat(),
            'dias_trabajados': self.dias_trabajados,
            'horas_extra': self.horas_extra,
            'faltas': self.faltas,
            'tardes': self.tardes,
            'bono_puntualidad': self.bono_puntualidad,
            'bono_produccion': self.bono_produccion,
            'prestamo': self.prestamo,
            'caja_ahorro': self.caja_ahorro,
            'descuento_tardes': self.descuento_tardes,
            'sueldo_base': self.sueldo_base,
            'pago_extras': self.pago_extras,
            'ajuste_faltas': self.ajuste_faltas,
            'total_bonos': self.total_bonos,
            'descuento_prestamo': self.descuento_prestamo,
            'total_descuentos': self.total_descuentos,
            'total_pagar': self.total_pagar
        }

class ConfiguracionGlobal(db.Model):
    """Global configuration model for payroll settings"""
    __tablename__ = 'configuracion_global'
    
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(50), unique=True, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(200))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'clave': self.clave,
            'valor': self.valor,
            'descripcion': self.descripcion,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat()
        }
