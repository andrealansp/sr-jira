document.addEventListener("DOMContentLoaded", function () {
  function removerClasseDoFormularioPorTag(classeParaRemover, indiceDoFormulario = 0) {
  // 1. Encontrar todos os elementos 'form' na página
  const formularios = document.getElementsByTagName('form');

  // Verificar se algum formulário foi encontrado
  if (formularios.length === 0) {
    console.warn("Nenhum formulário encontrado na página.");
    return;
  }else{
  console.log("Quantidade de formulários encontrado " + formularios.length);
  }

  // Verificar se o índice especificado é válido
  if (indiceDoFormulario < 0 || indiceDoFormulario >= formularios.length) {
    console.warn(`Índice de formulário inválido: ${indiceDoFormulario}. Existem apenas ${formularios.length} formulário(s).`);
    return;
  }

  // 2. Selecionar o formulário desejado pelo índice
  // Por padrão, pega o primeiro formulário (índice 0)
  const formulario = formularios[indiceDoFormulario];

  // 3. Obter todos os elementos filhos do formulário selecionado
  const elementosDoFormulario = formulario.querySelectorAll('*');

  // 4. Iterar sobre cada elemento e remover a classe
  elementosDoFormulario.forEach(elemento => {
    if (elemento.classList.contains(classeParaRemover)) {
      elemento.classList.remove(classeParaRemover);
      // Opcional: Para depuração
      // console.log(`Classe "${classeParaRemover}" removida de:`, elemento);
    }
  });

  console.log(`Classe "${classeParaRemover}" removida de todos os elementos do formulário (índice ${indiceDoFormulario}).`);
}
setTimeout(function() {
  removerClasseDoFormularioPorTag("is-valid",1); // Remove a classe 'campo-erro' do primeiro formulário
}, 5000);

})
