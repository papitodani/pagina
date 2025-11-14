/**
 * Client-side payroll calculations
 */

const PayrollCalculator = {
    // Configuration defaults
    config: {
        PRECIO_HORA_EXTRA: 35,
        PORCENTAJE_PRESTAMO: 3,
        BONO_PUNTUALIDAD_DEFAULT: 100,
        BONO_PRODUCCION_DEFAULT: 100
    },

    /**
     * Calculate payroll based on input data
     */
    calculate(data) {
        const {
            sueldo_diario = 0,
            dias_trabajados = 15,
            horas_extra = 0,
            faltas = 0,
            tardes = 0,
            bono_puntualidad = 0,
            bono_produccion = 0,
            descuento_tardes = 0,
            prestamo = 0,
            caja_ahorro = 0
        } = data;

        // Calculate base salary
        const sueldo_base = parseFloat(sueldo_diario) * parseInt(dias_trabajados);

        // Calculate extra hours pay
        const pago_extras = parseFloat(horas_extra) * this.config.PRECIO_HORA_EXTRA;

        // Calculate absences adjustment (faltas se suman al sueldo)
        const ajuste_faltas = parseInt(faltas) * parseFloat(sueldo_diario);

        // Calculate bonuses
        const total_bonos = parseFloat(bono_puntualidad) + parseFloat(bono_produccion);

        // Calculate deductions
        const descuento_prestamo = parseFloat(prestamo) * (this.config.PORCENTAJE_PRESTAMO / 100);
        const total_descuentos = parseFloat(descuento_tardes) + descuento_prestamo + parseFloat(caja_ahorro);

        // Calculate total to pay
        const total_pagar = sueldo_base + pago_extras + ajuste_faltas + total_bonos - total_descuentos;

        return {
            sueldo_base: this.roundMoney(sueldo_base),
            pago_extras: this.roundMoney(pago_extras),
            ajuste_faltas: this.roundMoney(ajuste_faltas),
            total_bonos: this.roundMoney(total_bonos),
            descuento_prestamo: this.roundMoney(descuento_prestamo),
            total_descuentos: this.roundMoney(total_descuentos),
            total_pagar: this.roundMoney(total_pagar)
        };
    },

    /**
     * Round money to 2 decimal places
     */
    roundMoney(amount) {
        return Math.round(parseFloat(amount) * 100) / 100;
    },

    /**
     * Validate calculation inputs
     */
    validate(data) {
        const errors = [];

        // Validate sueldo_diario
        if (!data.sueldo_diario || parseFloat(data.sueldo_diario) < 0) {
            errors.push('Sueldo diario debe ser mayor a 0');
        }

        // Validate dias_trabajados
        if (data.dias_trabajados !== undefined) {
            const dias = parseInt(data.dias_trabajados);
            if (isNaN(dias) || dias < 0 || dias > 31) {
                errors.push('Días trabajados debe estar entre 0 y 31');
            }
        }

        // Validate numeric fields
        const numericFields = [
            'horas_extra', 'faltas', 'tardes', 'bono_puntualidad',
            'bono_produccion', 'descuento_tardes', 'prestamo', 'caja_ahorro'
        ];

        numericFields.forEach(field => {
            if (data[field] !== undefined) {
                const value = parseFloat(data[field]);
                if (isNaN(value) || value < 0) {
                    errors.push(`${field} debe ser un número válido y no negativo`);
                }
            }
        });

        return {
            valid: errors.length === 0,
            errors: errors
        };
    },

    /**
     * Format currency for display
     */
    formatCurrency(amount) {
        return new Intl.NumberFormat('es-MX', {
            style: 'currency',
            currency: 'MXN'
        }).format(amount || 0);
    },

    /**
     * Calculate percentage
     */
    calculatePercentage(amount, percentage) {
        return this.roundMoney(parseFloat(amount) * (parseFloat(percentage) / 100));
    },

    /**
     * Get breakdown of calculations
     */
    getBreakdown(data) {
        const calc = this.calculate(data);
        
        return {
            percepciones: [
                { label: 'Sueldo Base', amount: calc.sueldo_base, formula: `${data.dias_trabajados} días × $${data.sueldo_diario}` },
                { label: 'Horas Extra', amount: calc.pago_extras, formula: `${data.horas_extra} hrs × $${this.config.PRECIO_HORA_EXTRA}` },
                { label: 'Ajuste Faltas', amount: calc.ajuste_faltas, formula: `${data.faltas} faltas × $${data.sueldo_diario}` },
                { label: 'Bono Puntualidad', amount: data.bono_puntualidad || 0, formula: 'Directo' },
                { label: 'Bono Producción', amount: data.bono_produccion || 0, formula: 'Directo' }
            ],
            deducciones: [
                { label: 'Descuento Tardes', amount: data.descuento_tardes || 0, formula: 'Directo' },
                { label: 'Préstamo (3%)', amount: calc.descuento_prestamo, formula: `$${data.prestamo} × 3%` },
                { label: 'Caja Ahorro', amount: data.caja_ahorro || 0, formula: 'Directo' }
            ],
            totals: {
                percepciones: calc.sueldo_base + calc.pago_extras + calc.ajuste_faltas + calc.total_bonos,
                deducciones: calc.total_descuentos,
                neto: calc.total_pagar
            }
        };
    },

    /**
     * Update configuration
     */
    updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
    }
};

// Export for use in templates
if (typeof window !== 'undefined') {
    window.PayrollCalculator = PayrollCalculator;
}

// Export for Node.js if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PayrollCalculator;
}
