// =============================================
// CARROSSEL DA EQUIPE - CORRIGIDO
// =============================================

document.addEventListener('DOMContentLoaded', function() {
    // Elementos do carrossel da equipe
    const teamPrev = document.querySelector('.nossa-equipe .prev');
    const teamNext = document.querySelector('.nossa-equipe .next');
    const teamCarousel = document.querySelector('.nossa-equipe .carousel');
    const teamCarouselContainer = document.querySelector('.nossa-equipe .carousel-container');
    const teamItems = document.querySelectorAll('.nossa-equipe .carousel-item');

    // Verifica se os elementos do carrossel existem
    if (!teamCarousel || teamItems.length === 0) {
        console.log('Carrossel da equipe não encontrado');
        return;
    }

    let teamIndex = 0;
    let teamAutoPlay;
    const totalTeamItems = teamItems.length;

    // Função para mostrar o item atual do carrossel
    function showTeamItem(idx) {
        teamIndex = idx;
        teamCarousel.style.transform = `translateX(-${teamIndex * 100}%)`;
    }

    // Avançar para o próximo item
    function nextTeamItem() {
        teamIndex = (teamIndex + 1) % totalTeamItems;
        showTeamItem(teamIndex);
    }

    // Voltar para o item anterior
    function prevTeamItem() {
        teamIndex = (teamIndex - 1 + totalTeamItems) % totalTeamItems;
        showTeamItem(teamIndex);
    }

    // Iniciar autoplay (4 segundos)
    function startAutoPlay() {
        teamAutoPlay = setInterval(nextTeamItem, 4000);
    }

    // Parar autoplay
    function stopAutoPlay() {
        clearInterval(teamAutoPlay);
    }

    // Event listeners para os botões de navegação
    if (teamNext) {
        teamNext.addEventListener('click', () => {
            stopAutoPlay();
            nextTeamItem();
            startAutoPlay();
        });
    }

    if (teamPrev) {
        teamPrev.addEventListener('click', () => {
            stopAutoPlay();
            prevTeamItem();
            startAutoPlay();
        });
    }

    // Pausar autoplay quando o mouse estiver sobre o carrossel
    if (teamCarouselContainer) {
        teamCarouselContainer.addEventListener('mouseenter', stopAutoPlay);
        teamCarouselContainer.addEventListener('mouseleave', startAutoPlay);
    }

    // Inicializar carrossel
    showTeamItem(teamIndex);
    startAutoPlay();
});