document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.querySelector('.sidebar');
    const toggleBtn = document.querySelector('.toggle-btn');
    const conteudo = document.querySelector('#conteudo');

    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('active');
        conteudo.classList.toggle('expandido');
    });

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
