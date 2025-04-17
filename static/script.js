function getTrustColor(score) {
  if (score >= 0.85) return "trust-high";
  if (score >= 0.6) return "trust-medium";
  return "trust-low";
}

function getRecommendations() {
  const interest = document.getElementById("interest").value;
  const loader = document.getElementById("loader");
  const resultsDiv = document.getElementById("results");

  // Show loader and clear results
  loader.style.display = "block";
  resultsDiv.innerHTML = "";

  fetch("/recommend", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ interest: interest })
  })
  .then(res => res.json())
  .then(data => {
    loader.style.display = "none"; // hide loader

    if (data.length === 0) {
      resultsDiv.innerHTML = "<p>No results found.</p>";
      return;
    }

    data.forEach(article => {
      const trustClass = getTrustColor(article.trust_score);
      const card = document.createElement("div");
      card.classList.add("result-card");
      card.innerHTML = `
        <h3>${article.title}</h3>
        <p><strong>Bias:</strong> ${article.bias}</p>
        <p><strong class="${trustClass}">Trust Score: ${article.trust_score}</strong></p>
        <p>${article.description}</p>
        <a href="${article.url}" target="_blank">🔗 Read full article</a>
      `;
      resultsDiv.appendChild(card);
    });
  })
  .catch(error => {
    loader.style.display = "none";
    resultsDiv.innerHTML = "<p>Error fetching results. Please try again.</p>";
    console.error(error);
  });
}


