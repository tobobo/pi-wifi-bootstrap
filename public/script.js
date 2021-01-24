const form = document.getElementById('credentials');

form.addEventListener('submit', async e => {
  e.preventDefault();
  
  const body = new FormData(e.target);

  await fetch('/set_credentials', {
    method: 'POST',
    body,
  });
});
