async function mainLoop() {
  let lastModified = "";
  
  while (true) {
    await new Promise(r => setTimeout(r, 2000));
    try {
      const response = await fetch("/_last_modified.json");
      const data = await response.json();
      const time = data["last_modified"];
  
      if (!lastModified) {
        lastModified = time;
      } else if (time !== lastModified) {
        window.location.reload();
      }
    } catch (e) {
      // Do nothing
    }
  }
}

mainLoop();