$(document).ready(function() {
    $('.add-to-cart').click(function() {
      console.log('agregado al carrito')
      var productId = $(this).data('product-id');
      var quantity = $(this).closest('.input-group').find('input[type="number"]').val();
      $.post('/cart/add/', {'product_id': productId, 'quantity': quantity}, function(data) {
        // Actualiza la vista del carrito o muestra un mensaje de confirmación
      });
    });
  });