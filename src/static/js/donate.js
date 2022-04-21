const collapsibleContent = document.querySelectorAll(".collapsible");
const select = document.querySelector('#select-transport')

const transportType = document.querySelectorAll('#transport-type');

collapsibleContent.forEach(element => {
    element.addEventListener('click', (event) => {
        const content = element.querySelector('.collapsible-content')
        if (event.path[1] == element) {
            if (content.classList.contains('hidden')) {
                content.classList.replace('hidden', 'block')
            } else {
                content.classList.replace('block', 'hidden')
            }
        }
    });
});

select.addEventListener('change', function() {
    transportType.forEach(element => {
        element.value = select.value;
      })
})