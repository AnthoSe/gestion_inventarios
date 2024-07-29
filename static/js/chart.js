// static/js/chart.js

document.addEventListener('DOMContentLoaded', (event) => {
    var ctx = document.getElementById('inventoryChart').getContext('2d');
    var inventoryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Total de Productos', 'Productos en Stock', 'Productos con Bajo Stock'],
            datasets: [{
                label: 'Cantidad',
                data: [totalProductos, productosEnStock, productosBajoStock],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
