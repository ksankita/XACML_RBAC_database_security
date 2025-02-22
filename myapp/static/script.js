function requestAccess() {
    const resource = document.getElementById("resource").value;
    const location = document.getElementById("location").value;

    fetch("/check_access/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `resource=${resource}&location=${location}`
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = `Access: ${data.access}`;
    })
    .catch(error => console.error("Error:", error));
}
