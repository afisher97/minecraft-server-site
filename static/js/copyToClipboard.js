function copyToClipboard(value) {
    // Create a temporary input element to copy the value
    var tempInput = document.createElement("input");

    // Check if value is a string (IP address) or an element ID
    if (value.includes(".")) {
        tempInput.value = value; // If it's a string like mc1.averyfisher.com
    } else {
        var element = document.getElementById(value);
        tempInput.value = element.innerText; // Copy text content of the element
    }

    document.body.appendChild(tempInput);
    tempInput.select();
    tempInput.setSelectionRange(0, 99999); // For mobile devices
    document.execCommand("copy");
    document.body.removeChild(tempInput);
    alert("Copied the IP: " + tempInput.value);
}
