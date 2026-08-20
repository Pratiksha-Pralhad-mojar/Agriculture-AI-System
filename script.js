// Function to navigate to different pages or sections
function navigateTo(page) {
    switch (page) {
        case 'cropRecommendation':
            window.location.href = 'cropRecommendation.html'; // Redirect to cropRecommendation.html
            break;
        case 'leafDisease':
            window.location.href = 'disease.html'; // Redirect to leafDisease.html
            break;
        case 'fertilizerRecommendation':
            window.location.href = 'fertilizerRecommendation.html'; // Redirect to fertilizerRecommendation.html
            break;
        default:
            console.log('Page not found!');
    }
}

