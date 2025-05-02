document.addEventListener('DOMContentLoaded', () => {
  // Mobile menu toggle
  const toggler = document.querySelector('.navbar-toggler');
  const menu = document.querySelector('.navbar-menu');
  
  if (toggler && menu) {
      toggler.addEventListener('click', () => {
          menu.classList.toggle('active');
      });
      
      // Close menu when clicking outside
      document.addEventListener('click', e => {
          if (menu && toggler && !menu.contains(e.target) && !toggler.contains(e.target)) {
              menu.classList.remove('active');
          }
      });
  }
  
  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
          const href = this.getAttribute('href');
          
          // Only apply smooth scroll if the element exists
          const targetElement = document.querySelector(href);
          if (targetElement) {
              e.preventDefault();
              targetElement.scrollIntoView({
                  behavior: 'smooth',
                  block: 'start'
              });
          }
      });
  });
});
