// get the pet type and breed fields
const typeField = document.getElementById('pet_type');
const breedField = document.getElementById('breed');
let options;

typeField.addEventListener("change", () => {
  // get value of pet type and the form
  type = typeField.value;
  const filter = document.getElementById('dashboard-filter');

  // change the action of the form based on the pet type
  if (typeField.value === "cat") {
    filter.setAttribute("action", "/pets/cat");
  } else {
    filter.setAttribute("action", "/pets/dog");
  }

  // fetch the breeds for the selected pet type
  fetch(`/breeds/${type}`)
  .then(res => res.json())
  .then(data => {
    options = "";

    // create the options for the breed select field
    for (let breed of data) {
      options += `<option value="${breed[0]}">${breed[1]}</option>`;
    }

    // set the options for the breed select field
    breedField.innerHTML = options;
  })
});