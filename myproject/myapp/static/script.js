document.getElementById("accessForm").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent page refresh

    let role = document.getElementById("role").value;
    let location = document.getElementById("location").value;
    let accessTime = document.getElementById("accessTime").value;

    let requestData = {
        role: role,
        location: location,
        accessTime: accessTime
    };

    fetch("/myapp/evaluate/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerHTML = `<p>Access Decision: ${data.decision}</p>`;
    })
    .catch(error => console.error("Error:", error));
});
