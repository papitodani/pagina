"""
Configuration file for the payroll application
"""
import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///nominas.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Payroll configuration
    PRECIO_HORA_EXTRA = 35  # pesos por hora
    BONO_PUNTUALIDAD_DEFAULT = 100  # pesos
    BONO_PRODUCCION_DEFAULT = 100  # pesos
    PORCENTAJE_PRESTAMO = 3  # 3% sobre el préstamo
    
    # Application settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    JSON_AS_ASCII = False  # Support Spanish characters
