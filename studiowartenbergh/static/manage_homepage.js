window.addEventListener('load', function() {
    var modal = document.getElementsByClassName('modal')[0]
    window.onclick = function(e) {
        if (e.target == modal) {
            modal.style.display = 'none';
        }
    }

    var items = document.getElementsByClassName('item-abstract');

    for (var i = 0; i < items.length; i++) {
        var item = items[i];
        item.onclick = function() {
            var fullItem = item.parentElement.firstElementChild
            modal.appendChild(fullItem)
            modal.style.display = 'block' // show modal
            fullItem.style.display = 'inline-block' // show modal
        }
    }

}, false)
