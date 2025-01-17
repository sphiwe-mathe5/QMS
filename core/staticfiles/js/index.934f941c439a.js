function togglePopup() {
  const popup = document.getElementById("userPopup");
  if (popup.style.display === "none" || popup.style.display === "") {
    popup.style.display = "block";
  } else {
    popup.style.display = "none";
  }
}
window.onclick = function (event) {
  const popup = document.getElementById("userPopup");
  if (!event.target.matches("#userIcon") && !popup.contains(event.target)) {
    popup.style.display = "none";
  }
};
document
  .getElementById("scrollToTopButton")
  .addEventListener("click", function () {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });
