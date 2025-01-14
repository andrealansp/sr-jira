document.addEventListener("DOMContentLoaded", function () {
    let abertura_rmgv = document.getElementById('abertosrmgv')
    let abertura_fora_rmgv = document.getElementById('abertosforarmgv')
    let fechamento_rmgv = document.getElementById('fechadosrmgv')
    let fechamento_fora_rmgv =document.getElementById('fechadosforarmgv')
    let abertos =document.getElementById('abertos')
    let fechados =document.getElementById('fechados')

    axios.get("/preventivas/estatisticas")
        .then(function (response){
            abertura_rmgv.innerHTML = response.data["ABERTOS_RMGV"];
            abertura_fora_rmgv.innerHTML = response.data["ABERTOS_FORA_DIVISA"];
            fechamento_rmgv.innerHTML = response.data["FECHADOS_RMGV"];
            fechamento_fora_rmgv.innerHTML = response.data["FECHADOS_FORA_DIVISA"];
            abertos.innerHTML = response.data["CHAMADOS_ABERTOS"];
            fechados.innerHTML = response.data["FECHADOS_RMGV"] + response.data["FECHADOS_FORA_DIVISA"];
        })

})
