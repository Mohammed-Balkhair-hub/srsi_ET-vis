/* SRSI ET Vis — shared interactions */

(function () {
  document.documentElement.classList.add("js");

  // Smooth reveal for cards / sections
  const revealEls = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("is-visible");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("is-visible"));
  }

  // Section nav: highlight active chip while scrolling
  const chips = document.querySelectorAll(".section-nav a[href^='#']");
  const sections = [...chips]
    .map((a) => document.querySelector(a.getAttribute("href")))
    .filter(Boolean);

  if (chips.length && sections.length && "IntersectionObserver" in window) {
    const navIO = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (!e.isIntersecting) return;
          const id = "#" + e.target.id;
          chips.forEach((c) => c.classList.toggle("is-active", c.getAttribute("href") === id));
        });
      },
      { rootMargin: "-35% 0px -55% 0px", threshold: 0 }
    );
    sections.forEach((s) => navIO.observe(s));
  }

  // Pause other videos when one plays
  const videos = document.querySelectorAll("video.lesson-video");
  videos.forEach((v) => {
    v.addEventListener("play", () => {
      videos.forEach((other) => {
        if (other !== v) other.pause();
      });
    });
  });
})();
