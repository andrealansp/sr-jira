document.addEventListener("DOMContentLoaded", function () {
    const pgurl = window.location.href;
    document.querySelectorAll('li a').forEach((element) => {
        if (element.parentElement.classList.contains('active')) {
            element.parentElement.classList.remove('active');
        }
        if (element.href === pgurl) {
            element.parentElement.classList.add('active')
        }
    })
})
