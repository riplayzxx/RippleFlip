// code for rolling

function rollAndAlert(label) {
    fetch("/api/roll", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            alert(`${label}: Rolled ${data.result}`);
        })
        .catch(err => alert("Error: " + err));
}

document.getElementById("buttonallin").addEventListener("click", function() {
    alert("Rolled all in!")
});

document.getElementById("button5k").addEventListener("click", function() {
    rollAndAlert("Rolled 5k")
});

document.getElementById("button10k").addEventListener("click", function() {
    rollAndAlert("Rolled 10k")
});

document.getElementById("button25k").addEventListener("click", function() {
    rollAndAlert("Rolled 25k")
});

document.getElementById("button100k").addEventListener("click", function() {
    rollAndAlert("Rolled 100k")
});

document.getElementById("button1m").addEventListener("click", function() {
    rollAndAlert("Rolled 1m")
});
