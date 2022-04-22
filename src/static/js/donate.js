const select = document.querySelector('#select-transport')
const transportType = document.querySelectorAll('#transport-type');

select.addEventListener('change', function() {
    transportType.forEach(element => {
        element.value = select.value;
      })
})