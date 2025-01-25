
 // Text to be typed out
 //var headtext = ``
 var headtext = `Empower Your Farm with Intelligent Crop Recommendations`
 var text = `Get insights on soil health, manage your farm history, and stay ahead with weather forecasts.`

 // Index to track the current character being typed
var index = 0;
var index2 = 0;

//Function to simulate typing effect
async function typeWriterhead() {
     if (index < headtext.length) {
         document.getElementById("intro1").innerHTML += headtext.charAt(index);
        index++;
        setTimeout(typeWriterhead, 30); // Adjust typing speed (milliseconds)
            }
        }

async function typeWriter() {
     if (index2 < text.length) {
         document.getElementById("intro2").innerHTML += text.charAt(index2);
         index2++;
         setTimeout(typeWriter, 40); // Adjust typing speed (milliseconds)
             }
         }


document.addEventListener('DOMContentLoaded', function(){
    // call the function
    typeWriterhead()

    typeWriter()
});
