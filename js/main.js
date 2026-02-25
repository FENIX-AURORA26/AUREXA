console.log("AUREXA site loaded.");

document.querySelectorAll(".card").forEach(card => {
    card.addEventListener("mouseover", () => {
        card.style.boxShadow = "0 0 20px #00B3FF";
    });
    card.addEventListener("mouseout", () => {
        card.style.boxShadow = "none";
    });
});
