$(document).ready(function() {
    let currentStep = 1

    function warring(pStep) {
        pStep.each(function () {
            if ($(this).data("step") == currentStep) {
                $(this).addClass("active")
            } else {
                $(this).removeClass("active")
            }
        })
    }

    function activeDiv(divForm) {
        divForm.each(function () {
            if ($(this).data("step") == currentStep) {
                $(this).addClass("active")
            } else {
                $(this).removeClass("active")
            }
        })
    }

    function filterCategory() {
        const institutions = JSON.parse($("#institutions").text())
        institutions[0] = '{';
        institutions[-1] = '}';
        $(JSON.parse(institutions)).each(function () {
            const divStep3 = $(`div[data-step="3"] input[value="${$(this)
                    .prop("pk")}"`).parent().parent()
            divStep3.hide(this)
            const iCat = $($(this).prop("fields"))
                .attr("categories")
            if (iCat.length) {
                $("div[data-step='1'] span.checkbox").each(function () {
                    const inputCat = $(this).prev()
                    if ($(inputCat).prop( "checked" )) {
                        iCat.forEach(function (c) {
                            if (c == $(inputCat).val()) {
                                divStep3.show(this)
                            }
                        })
                    }
                })
            }
        })
    }

    $("form#multistep .next-step").click(function () {
        if (currentStep == 1) {
            filterCategory();
        }
        currentStep++
        $("div.form--steps-counter span").text(currentStep)
        activeDiv($("div[data-step]"));
        warring($("div.form--steps-container p"));
        if (currentStep == 5) {
            $("div.form--steps-instructions").hide();
        }
    })

    $("form#multistep .prev-step").click(function () {
        currentStep--
        $("div.form--steps-counter span").text(currentStep)
        activeDiv($("div[data-step]"));
        warring($("div.form--steps-container p"));
        if (currentStep != 5) {
            $("div.form--steps-instructions").show();
        }
    })
})