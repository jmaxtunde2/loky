  document.addEventListener('DOMContentLoaded', function() {
    var sidebar = document.getElementById('sidebar');
    var menuButton = document.getElementById('menuButton');
    var menuButtonText = menuButton.querySelector('span');

    // Function to toggle menu text
    function toggleMenuText() {
      if (sidebar.classList.contains('show')) {
        menuButtonText.textContent = 'Close Menu';
      } else {
        menuButtonText.textContent = 'Open Menu';
      }
    }

    // Initial text based on sidebar state
    toggleMenuText();

    // Add event listener to toggle text on collapse event
    sidebar.addEventListener('shown.bs.collapse', toggleMenuText);
    sidebar.addEventListener('hidden.bs.collapse', toggleMenuText);
  });
