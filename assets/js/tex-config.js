MathJax = {
  tex: {
    inlineMath: [
      ["$", "$"],
      ["\\(", "\\)"],
    ],
    displayMath: [
      ["$$", "$$"],
      ["\\[", "\\]"],
    ],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    skipHtmlTags: ["script", "noscript", "style", "textarea", "pre"],
  },
};

window.addEventListener("load", (event) => {
  document.querySelectorAll("mjx-container").forEach(function (x) {
    x.parentElement.classList += "has-jax";
  });
});
