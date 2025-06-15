// Example: fetch product data from the API
fetch('/products')
  .then(res => res.json())
  .then(data => console.log(data));
