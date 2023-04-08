let resetButton = document.getElementById("resetButton")
let syncButton = document.getElementById("syncButton")
let bulbElements = [...document.getElementsByClassName('bulb-card')]

bulbs = bulbElements.map((element) => BulbCard(element))

resetButton.addEventListener('click', () => {reset(bulbs)})
syncButton.addEventListener('click', () => {sync(bulbs)})