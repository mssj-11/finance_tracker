document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.delete-btn');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault(); // Evita la redirección inmediata

            const deleteUrl = this.getAttribute('href'); // Obtiene la URL del botón

            Swal.fire({
                title: '¿Estás seguro?',
                text: "¡Este gasto se eliminará permanentemente!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Sí, eliminar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Redirigir a la URL de eliminación si se confirma
                    window.location.href = deleteUrl;
                }
            });
        });
    });
});