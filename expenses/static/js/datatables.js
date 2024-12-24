let expensesTable = new DataTable('#expensesTable', {
    responsive: true,
    columnDefs: [
        { responsivePriority: 1, targets: -1 }  // Prioridad más alta a la última columna (acciones)
    ],
    layout:{
        topStart:{
            search:{
                placeholder: 'Buscar agentes'
            }
        },
        topEnd:{
            pageLength:{
                menu: [10, 25, 50, 100]
            }
        },
        bottomStart: 'paging',
        bottomEnd: 'info'
    },
    language:{
        search: '<i class="fa-solid fa-magnifying-glass text-secondary"></i>',
        lengthMenu: 'Mostrar _MENU_ gastos',
        info: 'Mostrando _START_ - _END_ de _TOTAL_ gastos',
        infoFiltered: '(Filtrado de _MAX_ gastos)',
        infoEmpty: 'No hay datos para mostrar ',
        zeroRecords: 'No se encontraron coincidencias',
        paginate: {
            first: '<i class="fa fa-angle-double-left"></i>',
            previous: '<i class="fa fa-angle-left"></i>',
            next: '<i class="fa fa-angle-right"></i>',
            last: '<i class="fa fa-angle-double-right"></i>'
        }
    },
    ordering: false  // Desactivar ordenamiento
});