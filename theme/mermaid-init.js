// Dynamic Mermaid renderer for mdBook (Zero-Dependency)
document.addEventListener("DOMContentLoaded", function () {
  var blocks = document.querySelectorAll("code.language-mermaid");
  if (blocks.length > 0) {
    var script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js";
    script.onload = function () {
      mermaid.initialize({
        startOnLoad: false,
        theme: "neutral"
      });
      blocks.forEach(function (block) {
        var pre = block.parentElement;
        var div = document.createElement("div");
        div.className = "mermaid";
        div.textContent = block.textContent;
        if (pre && pre.parentNode) {
          pre.parentNode.replaceChild(div, pre);
        }
      });
      mermaid.run();
    };
    document.head.appendChild(script);
  }
});
