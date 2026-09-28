document.documentElement.classList.add("js");

document.addEventListener("DOMContentLoaded", function () {
  // Respect user accessibility settings and skip animation.
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }

  var elements = document.querySelectorAll(".fade-reveal");

  // Keep all content visible when IntersectionObserver is unavailable.
  if (!("IntersectionObserver" in window)) {
    elements.forEach(function (el) {
      el.classList.add("visible");
    });
    return;
  }

  // Observe reveal elements once to keep runtime overhead low.
  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: "0px 0px -60px 0px" }
  );

  elements.forEach(function (el) {
    observer.observe(el);
  });
});
