(() => {
let questions;
let previousQuestions = [];
let questionDiv;
let newButton;

const API_URL = "/questions";
const QUESTION_CACHE_LENGTH = 10;


window.onload = () => {
    // set up element vars
    questionDiv = document.querySelector("#question");
    newButton = document.querySelector("#new");

    newButton.onclick = newQuestion;

    // retrieve question list from API
    let xhr = new XMLHttpRequest();
    xhr.open("GET", API_URL);
    xhr.responseType = "json";
    xhr.onload = () => { 
        questions = xhr.response.questions;
        newButton.disabled = false;
        newQuestion();
    };
    xhr.send();

    // read in previous questions
    if(!window.localStorage.previousQuestions) return;
    try {
        previousQuestions = JSON.parse(window.localStorage.previousQuestions);
    } catch(e) {
        console.error(e);
    }
}

const newQuestion = () => {
    // pick random number not in list of previous questions
    let randomIndex;
    do{
        randomIndex = Math.floor(Math.random() * questions.length);
    }
    while(previousQuestions.includes(randomIndex));

    // update display with new question
    questionDiv.innerHTML = questions[randomIndex];
    updatePreviousQuestions(randomIndex);

};

// update list of previous questions
const updatePreviousQuestions = (index) => {
    previousQuestions.unshift(index);

    if(QUESTION_CACHE_LENGTH > 0 && previousQuestions.length > QUESTION_CACHE_LENGTH) {
        previousQuestions.pop();
    }

    window.localStorage.previousQuestions = JSON.stringify(previousQuestions);
}
})();

