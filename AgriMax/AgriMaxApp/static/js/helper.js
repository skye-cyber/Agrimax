indexi = 0
texti = `I recommend using the default selection [All] for higher accuracy`


async function model_helper() {
    const selectedValue = document.getElementById("model").value;
    if (selectedValue !== 'all') {
        if (indexi < texti.length) {
            document.getElementById("insight").innerHTML += texti.charAt(indexi);
            indexi++;
            setTimeout(model_helper, 20); // Adjust typing speed (milliseconds)
        }
    }
    else {
        if (indexi > 0) { //condition to check if indexi is greater than 0
            // Remove the last character from the displayed text
            const currentText = document.getElementById("insight").innerHTML;
            document.getElementById("insight").innerHTML = currentText.slice(0, -1);
            indexi--; // Decrement the index
            setTimeout(model_helper, 20); //typing speed (milliseconds)

        }
    }
}



