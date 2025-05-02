document.addEventListener('DOMContentLoaded', () => {
    const toggler = document.querySelector('.navbar-toggler');
    const menu    = document.querySelector('.navbar-menu');
  
    toggler.addEventListener('click', () => {
      menu.classList.toggle('active');
    });
  
    // close when clicking outside
    document.addEventListener('click', e => {
      if (!menu.contains(e.target) && !toggler.contains(e.target)) {
        menu.classList.remove('active');
      }
    });
  
    // smooth anchors (optional)
    document.querySelectorAll('a[href^="#"]').forEach(a => {
      a.addEventListener('click', e => {
        e.preventDefault();
        document.querySelector(a.getAttribute('href'))
                .scrollIntoView({ behavior: 'smooth' });
      });
    });
  });
  