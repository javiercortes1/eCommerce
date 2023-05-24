$(document).ready(function() {
    var barrelsData = {{ barrels_data|safe }};
    
    $('#calendar').fullCalendar({
      selectable: true,
      events: barrelsData,
      select: function(start, end) {
        // Aquí puedes implementar la lógica para realizar el arriendo en esas fechas seleccionadas
        alert('Fecha seleccionada: ' + start.format('YYYY-MM-DD') + ' - ' + end.format('YYYY-MM-DD'));
      }
    });
});