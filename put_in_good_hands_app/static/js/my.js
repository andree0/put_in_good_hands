const form = document.querySelector("form#multistep");
const btnNext = form.querySelectorAll(".next-step");
const btnPrev = form.querySelectorAll(".prev-step");
const divForm = form.querySelectorAll("div[data-step]");

let currentStep = 1
btnNext.forEach(btn => {
    btn.addEventListener("click", () => {
        let divStep = form.querySelector("div.active");
        divStep.classList.remove("active")
        currentStep++
        console.log(divStep);
        divForm.forEach(div => {
            if (div.dataset.step == currentStep) {
                div.classList.add("active")
            }
        })
    })
    })


btnPrev.forEach(btn => {
    btn.addEventListener("click", () => {
        let divStep = form.querySelector("div.active");
        divStep.classList.remove("active")
        currentStep--
        console.log(divStep);
        divForm.forEach(div => {
            if (div.dataset.step == currentStep) {
                div.classList.add("active")
            }
        })
    })
    })