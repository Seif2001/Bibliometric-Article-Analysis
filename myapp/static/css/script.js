let inputDoi;

function inputButton() {
  inputDoi = document.getElementById("doi").value;
  const myArray = inputDoi.split(",");
  console.log(myArray);

  for (doi in myArray) {
    myArray[doi] = myArray[doi].replace(/\s+/g, "");
    console.log(myArray[doi]);
  }
}
