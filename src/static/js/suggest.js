const suggestionNodeList = document.querySelector('#charity-suggestions').querySelectorAll('.suggestion');
const modalNode = document.querySelector('#modal');

const suggestedMapData = JSON.parse(document.getElementById(`mapEmbedSuggest`).textContent);

suggestionNodeList.forEach(element => {
    element.addEventListener('click', (event) => {
        toggleModal(suggestedMapData[event.path[0].id-1]);
    });
})


modalNode.addEventListener('click', (event) => {

    const getParentID = (id) => modalNode.querySelector(`#${id}`).closest('.modal-block');

    switch(event.target.id) {
        case 'accept-suggestion':
            // Data Stuff to prepare for Django to DB
            toggleModal(getParentID(event.target.id))
            break;
        case 'deny-suggestion':
            // Data Stuff to prepare for Django to DB
            toggleModal(getParentID(event.target.id))
            break;
        default:
            if (event.target.id === 'close-suggestion' ||  event.path[1].id === 'close-suggestion' || event.path[2].id === 'close-suggestion' || event.path[0].id.match('suggestion') || event.path[1].id.match('suggestion')) {
                toggleModal(getParentID('close-suggestion'))
            }
    }

})

const toggleModal = (modalData) => {
    if (modalNode.classList.contains('hidden')) {
        modalNode.classList.replace('hidden', 'modal-block');
        modalNode.querySelector('h3').innerText = modalData.name;
        modalNode.querySelector('#suggestion-address').value = modalData.address;
        modalNode.querySelector('#suggestion-geolocation').value = `Latitude: ${modalData.geolocation.longitude} | Longitude: ${modalData.geolocation.latitude}`;
        modalNode.querySelector('#suggestion-type').value = modalNode.type == 1 ? 'Charity Store' : 'Charity Bin';

    } else {
        modalNode.classList.replace('modal-block', 'hidden');
    }
}