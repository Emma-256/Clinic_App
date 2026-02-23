/*  Optional: JavaScript to add 'scrolled' class for enhanced shadow on scroll */

 window.addEventListener('scroll', function() {
    const nav = document.querySelector('.navbar.sticky-top');
    if (window.scrollY > 10) {
        nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    });

