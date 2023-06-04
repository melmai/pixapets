const typeField = document.getElementById('pet_type');
const breedField = document.getElementById('breed');
let options;

typeField.addEventListener("change", () => {

  type = typeField.value.toLowerCase();

  if (type !== "all") {
    breedField.disabled = false;

    fetch(`/breeds/${type}`)
    .then(res => res.json())
    .then(data => {
      options = "";
      for (let breed of data) {
        options += `<option value="${breed[0]}">${breed[1]}</option>`;
      }
      breedField.innerHTML = options;
    })
  } else {
    breedField.disabled = true;
    breedField.innerHTML = `<option value="all">All Breeds</option>`;
  }
});