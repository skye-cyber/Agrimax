/*------*/
const modal = document.getElementById('AnalyticsModal');
const closeModal = document.getElementById('close-modal');
const Bt = document.getElementById('analyticsShow');

Bt.addEventListener('click', () => {
    ShowAnalyTics();
});
closeModal.addEventListener('click', () =>{
    HideAnalyTics();
})
document.addEventListener('keydown', (event) =>{
    if (event.key === "Escape" && !event.shiftKey ){
        HideAnalyTics();
    }
});
// Function to show the modal
function ShowAnalyTics() {
    // Slide modal to 20% height and make it visible after 1 second
    setTimeout(() => {
        modal.classList.remove('hidden', 'left-[-100vw]');
        modal.offsetWidth;
        modal.classList.add('top-1/5', 'left-1/2', 'opacity-100', 'pointer-events-auto');
    }, 200); // 1 second delay

}

function HideAnalyTics(){
    // Slide modal to the left and fade out after 5 seconds
    modal.classList.remove('top-1/5', 'left-1/2', '-translate-x-1/2');
    modal.classList.add('left-0', '-translate-x-full', 'opacity-0', 'pointer-events-none');


    // Reset transform after fully fading out and moving off-screen
    setTimeout(() => {
        modal.classList.remove('left-0', '-translate-x-full', 'opacity-0', 'pointer-events-none');
        modal.classList.add('top-0', 'hidden', 'left-[-100vw]', '-translate-x-1/2', 'pointer-events-none');
    }, 1000); // 0.5s for fade out
}

function goFullscreen(element) {
    // Check if the Fullscreen API is available
    if (element.requestFullscreen) {
        element.requestFullscreen(); // Standard method
    } else if (element.mozRequestFullScreen) { // Firefox
        element.mozRequestFullScreen();
    } else if (element.webkitRequestFullscreen) { // Chrome, Safari, and Opera
        element.webkitRequestFullscreen();
    } else if (element.msRequestFullscreen) { // IE/Edge
        element.msRequestFullscreen();
    } else {
        alert("Fullscreen API is not supported on this browser.");
    }
}
