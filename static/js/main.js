console.log("it works!")
fetch("http://127.0.0.1:5000/api", { // Replace with serverapiendpoint
  method: "POST",
  body: JSON.stringify({
    apiTest: "yay it works!"
  }),
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
});