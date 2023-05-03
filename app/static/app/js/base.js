// Espera a que se cargue el DOM
document.addEventListener('DOMContentLoaded', function() {
    // Obtiene el elemento con el ID 'logout-link'
    var logoutLink = document.getElementById('logout-link');
  
    // Define una variable para indicar si el usuario ha iniciado sesión o no
    var isAuthenticated = false;
  
    // Busca el elemento con el ID 'is-authenticated' y verifica si está presente en la página
    var isAuthenticatedElement = document.getElementById('is-authenticated');
    if (isAuthenticatedElement) {
      // Si el elemento está presente, actualiza el valor de la variable isAuthenticated
      isAuthenticated = isAuthenticatedElement.value === 'True';
    }
  
    // Verifica si el usuario ha iniciado sesión
    if (isAuthenticated) {
      // Agrega un event listener al enlace de cerrar sesión
      logoutLink.addEventListener('click', function(event) {
        event.preventDefault(); // Evita que el enlace se siga automáticamente
        Swal.fire({
          title: '¿Estás seguro de que quieres cerrar sesión?',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Sí, cerrar sesión',
          cancelButtonText: 'Cancelar',
          reverseButtons: true,
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.href = event.target.href; // Redirige al usuario a la página de cierre de sesión
          }
        });
      });
    }
  });