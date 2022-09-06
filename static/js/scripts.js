function fetchData(cities) {
    var select = document.getElementById("city");
    var region = document.getElementById("region").value;
    removeOptions(select);
    var elmts = cities[region];
    for (var i = 0; i < elmts.length; i++) {
        var optn = elmts[i];
        var el = document.createElement("option");
        el.textContent = optn;
        el.value = optn;
        select.appendChild(el);
    }
}


async function postTimezones() {
    // document.timezone.submit();
    const form = document.getElementById('timezone');
    const region = form.region.value;
    const city = form.city.value;

    try {
        const result = await fetch('/setTimezone', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "region": region, "city": city }),
        });
        const data = await result.json();
        console.log(data)
        if (result.ok) {
            location.assign('/settings');
        }
    } catch (err) {
        console.log(err);
    }
}


function removeOptions(selectElement) {
    var i, L = selectElement.options.length - 1;
    for (i = L; i >= 0; i--) {
        selectElement.remove(i);
    }
}


function checkValue(sender) {
    let min = sender.min;
    let max = sender.max;
    let value = parseInt(sender.value);
    if (value > max) {
        sender.value = max;
    } else if (value < min) {
        sender.value = min;
    }
}
