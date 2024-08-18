let cityOptions = [];

document.addEventListener('DOMContentLoaded', function() {
    fetch('/load-cities/')
        .then(response => response.json())
        .then(data => {
            cityOptions = data.cities;
        })
        .catch(error => console.error('Error loading cities:', error));
});


const resultsBox = document.querySelector('.results-box');
const cityInput = document.getElementById('location');


cityInput.onkeyup = function(){
    let result = [];
    let input = cityInput.value;
    if (input.length){
        result = cityOptions.filter((city) => {
            return city.toLowerCase().startsWith(input.toLowerCase());
        });
        console.log(result);
    }
    display(result);

    if(!result.length){
        resultsBox.innerHTML = "";
    }
}

function display(result){
    const content = result.map((list)=>{
        return "<li onclick=selectInput(this) >" + list + "</li>";
    });

    resultsBox.innerHTML = "<ul>" + content.join('') + "</ul>";
}

function selectInput(list){
    cityInput.value = list.innerHTML;
    resultsBox.innerHTML = "";
}