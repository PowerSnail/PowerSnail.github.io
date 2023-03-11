function mainLoop() {
  let lastModified = undefined;

  function processLastModified(newTime) {
    if (lastModified === undefined) {
      lastModified = newTime;
    } else if (newTime !== lastModified) {
      clearInterval(interval);
      window.location.reload();
    }
  }

  const interval = setInterval(
    () =>
      fetch("/_last_modified.txt")
        .then((response) => response.text())
        .then(processLastModified),
    2000
  );
}

mainLoop();