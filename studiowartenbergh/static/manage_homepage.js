window.addEventListener('load', function() {

    var modal = document.getElementsByClassName('modal')[0]
    // Transitioning to the modal
    var items = Array.from(document.getElementsByClassName('item-container'));
    items.forEach(function(container) {
        container.lastElementChild.onclick = function(e) {
            var itemToDisplay = modal.appendChild(container.firstElementChild)
            modal.style.display = 'block' // show modal
            itemToDisplay.style.display = 'inline-block' // show item
        }
    })


    // Transitioning back from the modal
    window.onclick = function(e) {
        /*
         * If we're showing the modal: 
        * Lookup the item's corresponding container by id.
        * Insert the full item back into the item container as the first
        * child.
        */ 
        if (e.target == modal && e.target.style.display == 'block') {
            var elemToMove = modal.removeChild(modal.firstElementChild)
            var parent = document.getElementById(elemToMove.id)
            parent.insertBefore(elemToMove, parent.firstElementChild)
            elemToMove.style.display = 'none';
            modal.style.display = 'none';
        }
    }


}, false)
