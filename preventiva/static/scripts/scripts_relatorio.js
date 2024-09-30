document.addEventListener('readystatechange', function(event) {
    console.log(event.target.readyState); // check for more states
    if (event.target.readyState === "complete") {
        alert("Relatório Carregado com Sucesso !");
    }
});