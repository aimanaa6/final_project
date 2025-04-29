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

function resetRecipe() {
    document.querySelectorAll('#ingredients-list input, #steps-list input').forEach(input => {
      input.checked = false;
    });
}

const items = document.querySelectorAll('.img-hover');
items.forEach(item => {
  item.addEventListener('mouseover', () => item.classList.add('bounce'));
  item.addEventListener('mouseout', () => item.classList.remove('bounce'));
});

