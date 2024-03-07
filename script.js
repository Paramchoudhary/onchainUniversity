document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.content-section');
    const LOCAL_STORAGE_KEY = 'activeSectionId';

    // Function to hide all sections
    function hideAllSections() {
        sections.forEach(section => {
            section.classList.remove('active');
        });
    }

    // Function to show a section
    function showSection(sectionId) {
        const targetSection = document.querySelector(sectionId);
        if (targetSection) {
            hideAllSections();
            targetSection.classList.add('active');
            localStorage.setItem(LOCAL_STORAGE_KEY, sectionId);
        }
    }

    // Initialize the page with the first link open or the last visited section
    function initPage() {
        const savedSectionId = localStorage.getItem(LOCAL_STORAGE_KEY);
        if (savedSectionId) {
            showSection(savedSectionId);
        } else {
            const firstSectionId = navLinks[0].getAttribute('href');
            showSection(firstSectionId);
        }
    }

    navLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const targetId = this.getAttribute('href');
            showSection(targetId);
        });
    });

    initPage(); // Call this function to initialize the page based on localStorage or default to the first section
});
function checkAnswer() {
    const answer = document.getElementById('vec-answer').value;
    if (answer.trim().toLowerCase() === 'push') {
        document.getElementById('feedback').textContent = 'Correct!';
        document.getElementById('feedback').style.color = 'green';
    } else {
        document.getElementById('feedback').textContent = 'Wrong.';
        document.getElementById('feedback').style.color = 'red';
    }
}