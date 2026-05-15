# Backlog de Producto: Sistema de Gestión Tomilomos (MVP)

Este documento detalla las Historias de Usuario necesarias para la construcción del MVP de un sistema ERP/SaaS enfocado en gastronomía. Diseñado para ser modular, escalable y con foco en la rentabilidad.

---

## Módulo 1: Arquitectura Base y Configuración (SaaS Ready)

### 1.1 Creación del Perfil del Negocio
* **User Story:** Como administrador, quiero configurar los datos del local y moneda, para aislar mi información de futuros usuarios.
* **Lógica de Negocio (Contexto):** Es el cimiento de la escalabilidad. Garantiza que el sistema separe perfectamente tu operación actual de la de otros colegas en un entorno SaaS.
* **Criterios de Aceptación:**
    * El formulario exige Nombre comercial, Moneda base y Zona horaria.
    * El sistema asigna un identificador único de inquilino (`tenant_id`) a la cuenta.
    * Toda consulta a la base de datos filtra por defecto mediante este identificador.
* **Riesgo y Mitigación:** * *Riesgo:* Mezcla de información entre distintos negocios. 
    * *Mitigación:* Implementar el patrón de diseño "Multi-Tenant" en la base de datos desde el inicio.

### 1.2 Importación de Catálogo Actual
* **User Story:** Como usuario, quiero importar mis planillas de Google Sheets vía CSV, para evitar la carga manual del inventario inicial.
* **Lógica de Negocio (Contexto):** Reduce la fricción de entrada al sistema, permitiendo migrar la operativa actual de forma masiva y rápida.
* **Criterios de Aceptación:**
    * Proveer una plantilla CSV con columnas: Nombre, Unidad de medida, Costo.
    * Mostrar previsualización de los primeros 5 registros antes de confirmar.
    * Validar y señalar errores de formato en filas específicas.
* **Riesgo y Mitigación:** * *Riesgo:* Corrupción de datos por formatos de celda inválidos. 
    * *Mitigación:* Saneamiento automático de strings y validación de tipos de datos previo a la inserción.

---

## Módulo 2: Gestión de Insumos e Inventario

### 2.1 Alta de Materias Primas
* **User Story:** Como administrador, quiero registrar insumos con unidades y costos, para llevar un control exacto de mi mercadería física.
* **Lógica de Negocio (Contexto):** Estandariza la entrada de productos. Al definir unidades base (gr, ml, un), se evita el caos en el conteo de stock.
* **Criterios de Aceptación:**
    * Campos obligatorios: Nombre, Unidad de Medida Base y Costo de Compra.
    * El costo debe ser un valor numérico positivo.
    * Generar listado de "Insumos Activos" con buscador.
* **Riesgo y Mitigación:** * *Riesgo:* Inconsistencia en conversiones (comprar en Kg, usar en Gr). 
    * *Mitigación:* Guardar valores internos en la unidad mínima y realizar conversiones solo en la interfaz de usuario.

### 2.2 Ingreso de Stock (Compras)
* **User Story:** Como encargado, quiero sumar cantidades a los insumos existentes, para reflejar las compras a proveedores.
* **Lógica de Negocio (Contexto):** Mantiene el inventario real actualizado y permite registrar las fluctuaciones de costo sin perder el historial.
* **Criterios de Aceptación:**
    * Selección de insumo mediante buscador predictivo.
    * Actualización automática del stock total disponible tras la carga.
    * Actualización del costo unitario del insumo basado en la última compra.
* **Riesgo y Mitigación:** * *Riesgo:* Perder el rastro de la variación de precios por inflación. 
    * *Mitigación:* Implementar el método de Costo Promedio Ponderado para valuar el inventario.

---

## Módulo 3: Ingeniería de Menú (Escandallo)

### 3.1 Creación de Producto Final
* **User Story:** Como administrador, quiero crear productos de venta, para armar el menú que se ofrece al cliente.
* **Lógica de Negocio (Contexto):** Define el contenedor comercial. Separa la entidad "Insumo" (compra) de la entidad "Producto" (venta).
* **Criterios de Aceptación:**
    * Campos: Nombre del Producto, Categoría y Precio de Venta al Público (PVP).
    * Estado "Activo/Inactivo" funcional para visualización en el menú.
* **Riesgo y Mitigación:** * *Riesgo:* Productos creados sin precio de venta. 
    * *Mitigación:* Validación de campo obligatorio y mayor a cero para el PVP.

### 3.2 Definición de Recetas (Lista de Materiales)
* **User Story:** Como encargado, quiero asignar insumos específicos a un producto, para calcular el costo de elaboración exacto.
* **Lógica de Negocio (Contexto):** Es el núcleo de la inteligencia del sistema. Relaciona matemáticamente el producto con la materia prima consumida.
* **Criterios de Aceptación:**
    * Permitir añadir múltiples insumos a un Producto Final.
    * Definir cantidad consumida por insumo (ej. 150gr de carne).
    * Cálculo automático del costo directo total basado en los precios de insumos.
* **Riesgo y Mitigación:** * *Riesgo:* Complejidad técnica en recetas anidadas. 
    * *Mitigación:* Limitar el MVP a recetas de un solo nivel (materia prima directa).

---

## Módulo 4: Operaciones y Ventas

### 4.1 Registro de Venta Diaria
* **User Story:** Como vendedor, quiero registrar la cantidad de productos vendidos, para asentar los ingresos del turno.
* **Lógica de Negocio (Contexto):** Captura la transacción comercial que dispara el flujo de dinero y la salida de materiales del inventario.
* **Criterios de Aceptación:**
    * Interfaz ágil para selección de productos y cantidades.
    * Generación de ticket/registro con ID único y marca de tiempo.
    * Cálculo automático del total de la venta.
* **Riesgo y Mitigación:** * *Riesgo:* Lentitud en la carga durante horas pico. 
    * *Mitigación:* Optimización de la interfaz (UI) para uso en dispositivos móviles/tablets con pocos clics.

### 4.2 Descuento Automático de Inventario
* **User Story:** Como sistema, quiero reducir el stock de insumos al concretar una venta, para mantener el inventario sincronizado.
* **Lógica de Negocio (Contexto):** Automatiza la auditoría. Elimina la necesidad de conteos manuales diarios al reflejar el consumo teórico en tiempo real.
* **Criterios de Aceptación:**
    * Disparar la resta de stock al marcar la venta como "Confirmada".
    * Consultar la receta del producto y descontar proporcionalmente cada insumo.
    * Permitir stock negativo con alerta visual.
* **Riesgo y Mitigación:** * *Riesgo:* Bloqueo de ventas por falta de stock sistémico (aunque haya físico). 
    * *Mitigación:* No bloquear la venta, pero marcar el stock en rojo para auditoría.

---

## Módulo 5: Analítica y Rentabilidad

### 5.1 Reporte de Márgenes y Rentabilidad
* **User Story:** Como dueño, quiero visualizar un reporte de márgenes de ganancia por producto, para ajustar precios estratégicamente.
* **Lógica de Negocio (Contexto):** Transforma la operación en inteligencia. Permite saber qué productos son rentables y cuáles requieren revisión de costos.
* **Criterios de Aceptación:**
    * Tabla con: PVP, Costo MP, Margen Bruto ($ y %).
    * Campo para configurar "Gastos Variables" globales para cálculo de Margen Neto.
    * Filtros por categoría de producto.
* **Riesgo y Mitigación:** * *Riesgo:* Cálculo lento con grandes volúmenes de datos. 
    * *Mitigación:* Pre-calcular los costos de recetas ante cada cambio de precio de insumo, evitando cálculos al vuelo en el reporte.