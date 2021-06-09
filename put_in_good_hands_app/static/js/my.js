const form = document.querySelector("form#multistep");
const btnNext = form.querySelectorAll(".next-step");
const btnPrev = form.querySelectorAll(".prev-step");
const divForm = form.querySelectorAll("div[data-step]");
const divCounterStep = document.querySelector("div.form--steps-counter");
const spanCounter = divCounterStep.querySelector("span");
const pStep = document.querySelectorAll("div.form--steps-container p");
const waringDiv = document.querySelector("div.form--steps-instructions");

let currentStep = 1

function warring (pStep) {
    pStep.forEach(p => {
        if (p.dataset.step == currentStep) {
            p.classList.add("active");
        } else {
            p.className = "";
        }
    })
}

function activeDiv (divForm) {
    divForm.forEach(div => {
        if (div.dataset.step == currentStep) {
            div.classList.add("active")
        } else {
            div.className = ""
        }
    })
}
btnNext.forEach(btn => {
    btn.addEventListener("click", () => {
        currentStep++
        spanCounter.innerText = currentStep
        activeDiv(divForm);
        warring(pStep);
        if (currentStep == 5) {
            waringDiv.setAttribute("hidden", "");
        }
    })
})


btnPrev.forEach(btn => {
    btn.addEventListener("click", () => {
        currentStep--
        spanCounter.innerText = currentStep
        activeDiv(divForm);
        warring(pStep);
        if (currentStep != 5) {
            waringDiv.removeAttribute("hidden");
        }
    })
})

// function getContext () {
//     $.ajax({
//         url: 'http://127.0.0.1:8000/add-donation/',
//
//     })
// }

const checkboxSpanCategories = document.querySelectorAll(
    "span.checkbox");

checkboxSpanCategories.forEach(cat => {
    cat.addEventListener( "mousemove", () => {
        const inputCat = cat.previousElementSibling
        const categories = JSON.parse(document.getElementById("categories").textContent)
        const institutions = JSON.parse(document.getElementById("institutions").textContent)
        institutions[0] = '{';
        categories[0] = '{';
        institutions[-1] = '}';
        categories[-1] = '}';
        const institutionObjects = JSON.parse(institutions);
        const categoryObjects = JSON.parse(categories);

        console.log(categoryObjects);
        if (inputCat.checked) {
            console.log(inputCat);
        }
    })
})
