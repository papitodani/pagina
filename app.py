"""
Main Flask application for payroll management system
"""
from flask import Flask, render_template
from config import Config
from models import db, Empleado, ConfiguracionGlobal
from routes import api_bp


def create_app(config_class=Config):
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Initialize default configuration if not exists
        if ConfiguracionGlobal.query.count() == 0:
            configuraciones = [
                ConfiguracionGlobal(
                    clave='precio_hora_extra',
                    valor=35,
                    descripcion='Precio por hora extra en pesos'
                ),
                ConfiguracionGlobal(
                    clave='bono_puntualidad',
                    valor=100,
                    descripcion='Bono de puntualidad por defecto'
                ),
                ConfiguracionGlobal(
                    clave='bono_produccion',
                    valor=100,
                    descripcion='Bono de producción por defecto'
                ),
                ConfiguracionGlobal(
                    clave='porcentaje_prestamo',
                    valor=3,
                    descripcion='Porcentaje de descuento sobre préstamo'
                )
            ]
            for config in configuraciones:
                db.session.add(config)
            db.session.commit()
    
    # Template routes
    @app.route('/')
    def index():
        """Dashboard page"""
        return render_template('index.html')
    
    @app.route('/nomina')
    def nomina():
        """Payroll management page"""
        return render_template('nomina.html')
    
    @app.route('/reportes')
    def reportes():
        """Reports page"""
        return render_template('reportes.html')
    
    @app.route('/calculadora')
    def calculadora():
        """Quick payroll calculator page"""
        return render_template('calculadora.html')
    
    return app


if __name__ == '__main__':
    import os
    app = create_app()
    # Debug mode should be disabled in production
    # Set FLASK_DEBUG=1 environment variable for development
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
