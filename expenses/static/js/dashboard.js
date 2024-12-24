// dashboard.js - Lógica de gráficos interactivos
// Obtener los datos enviados por Django desde el contexto renderizado
const expensesByCategory = JSON.parse('{{ expenses_by_category|safe }}');
    
// Extraer datos para el gráfico
const categories = expensesByCategory.map(item => item.category);
const amounts = expensesByCategory.map(item => item.total_amount);

// Datos simulados para el gráfico
const data = [
    {
        type: 'bar',
        x: categories,
        y: amounts,
        marker: {
            color: ['#3357FF', '#33FF57', '#FF5733', '#F3FF33', '#d8bfd8'],  // color: ['#FF5733', '#33FF57', '#3357FF', '#F3FF33'],
            line: {
                width: 2
            }
        }
    }
];

// Configuración del diseño
const layout = {
    //title: 'Distribución de Gastos',
    title: {
        text: 'Distribución de Gastos', // Texto del título
        font: {
            size: 20  // Tamaño de la fuente del título
        }
    },
    xaxis: {
        title: 'Categorías'
    },
    yaxis: {
        title: 'Monto ($)'
    },
    margin: {
        t: 40,
        l: 50,
        r: 10,
        b: 50
    }
};

var config = {responsive: true}

// Renderiza el gráfico en el div con id "chart"
Plotly.newPlot('chart', data, layout, config);
