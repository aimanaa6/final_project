function filterItems(type) {
  const allCards = document.querySelectorAll('.menu-grid .card');
  allCards.forEach(card => {
    const cardType = card.getAttribute('data-type');
    if (type === 'all' || cardType === type) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}