function kelvinToRGB(kelvin) {
  const temp = kelvin / 100;
  let r, g, b;

  if (temp <= 66) {
    r = 255;
    g = temp;
    g = 99.4708025861 * Math.log(g) - 161.1195681661;
    if (temp <= 19) {
      b = 0;
    } else {
      b = temp - 10;
      b = 138.5177312231 * Math.log(b) - 305.0447927307;
    }
  } else {
    r = temp - 60;
    r = 329.698727446 * Math.pow(r, -0.1332047592);
    g = temp - 60;
    g = 288.1221695283 * Math.pow(g, -0.0755148492);
    b = 255;
  }

  r = Math.round(Math.min(255, Math.max(0, r)));
  g = Math.round(Math.min(255, Math.max(0, g)));
  b = Math.round(Math.min(255, Math.max(0, b)));

  return { r, g, b };
}

function BulbCard(element) {
  const id = element.dataset.id;
  let powerSwitch = document.getElementById(`powerSwitch${id}`);
  let brightnessSlider = document.getElementById(`brightnessSlider${id}`);
  let temperatureSlider = document.getElementById(`temperatureSlider${id}`);
  let redSlider = document.getElementById(`redSlider${id}`);
  let greenSlider = document.getElementById(`greenSlider${id}`);
  let blueSlider = document.getElementById(`blueSlider${id}`);
  let colorPreview = document.getElementById(`colorPreview${id}`);

  let currentMode = element.dataset.mode;
  let mode = element.dataset.mode;

  let currentPower = powerSwitch.checked;
  let power = powerSwitch.checked;

  let currentColor = {
    brightness: brightnessSlider.value,
    r: redSlider.value,
    g: greenSlider.value,
    b: blueSlider.value,
    k: temperatureSlider.value,
  };

  let color = {
    brightness: brightnessSlider.value,
    r: redSlider.value,
    g: greenSlider.value,
    b: blueSlider.value,
    k: temperatureSlider.value,
  };

  function setColor(newColor = {}) {
    let preview = {}
    if (mode == "color") {
      preview = { r: color.r, g: color.g, b: color.b };
    } else if (mode == "temp") {
      preview = kelvinToRGB(color.k);
    }

    if (newColor?.r || newColor?.g || newColor?.b) {
      mode = "color";
      element.dataset.mode = "color";

      components = ["r", "g", "b"];
      for (component of components) {
        preview[component] = newColor[component] ?? color[component];
        color[component] = newColor[component] ?? color[component];
      }
    } else if (newColor?.k) {
      mode = "temp";
      element.dataset.mode = "temp";

      preview = kelvinToRGB(newColor.k);
      color.k = newColor.k;
    }

    color.brightness = newColor?.brightness ?? color.brightness;

    colorPreview.style.backgroundColor = `rgb(${preview.r}, ${preview.g}, ${preview.b})`;
    return preview;
  }

  function getState() {
    return {
      index: id,
      power,
      mode,
      brightness: color.brightness,
      temperature: color.k,
      color: { r: color.r, g: color.g, b: color.b },
    };
  }

  function revertState() {
    let { brightness, r, g, b, k } = currentColor;
    color = { brightness, r, g, b, k };
    power = currentPower;
    mode = currentMode;
    element.dataset.mode = currentMode;
    powerSwitch.checked = currentPower;
    brightnessSlider.value = brightness;
    redSlider.value = r;
    greenSlider.value = g;
    blueSlider.value = b;
    temperatureSlider.value = k;
    if (mode == "color") {
      setColor({ r, g, b });
    } else {
      setColor({ k });
    }
  }

  powerSwitch.addEventListener("click", () => {
    power = powerSwitch.checked;
  });

  brightnessSlider.addEventListener("input", () => {
    setColor({ brightness: brightnessSlider.value });
  });

  redSlider.addEventListener("input", () => {
    setColor({ r: redSlider.value });
  });

  greenSlider.addEventListener("input", () => {
    setColor({ g: greenSlider.value });
  });

  blueSlider.addEventListener("input", () => {
    setColor({ b: blueSlider.value });
  });

  temperatureSlider.addEventListener("input", () => {
    setColor({ k: temperatureSlider.value });
  });

  return {
    element,
    id,
    mode,
    power,
    color,
    currentPower,
    currentColor,
    revertState,
    getState,
  };
}

async function postRequest(data, location = " ") {
  const url = window.location.protocol + "//" + window.location.host + location;

  let response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return response
}

function reset(bulbs) {
  for (let bulb of bulbs) {
    bulb.revertState();
  }
}

function sync(bulbs) {
  let data = { devices: bulbs.map((bulb) => bulb.getState()) };
  postRequest(data, "/sync");
}
