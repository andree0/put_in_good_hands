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

    function summaryData () {
        const checkedCategory = $("input[name='categories']:checked").first().next().next().text()
        let bagName = 'worków'
        if ($("input[name='bags']").val() == 1) {
            bagName = 'worek'
        }
        else if (['2', '3', '4'].includes($("input[name='bags']").val())) {
            bagName = 'worki'
        }
        $("div[data-step='5'] span.summary--text").first()
            .text(`${$("input[name='bags']").val() ? $("input[name='bags']").val() : 0} ${bagName} w kategorii ${checkedCategory}`)

        $("div[data-step='5'] span.summary--text").last()
            .text(`Dla fundacji "${$("div[data-step='3'] input[name='organization']:checked").next().next().children().first().text()}"`)

        $("h4:contains('Adres odbioru:')").next().children().first()
            .text(`${$("input[name='address']").val()}`).next()
            .text(`${$("input[name='city']").val()}`).next()
            .text(`${$("input[name='postcode']").val()}`).next()
            .text(`${$("input[name='phone']").val()}`)

        $("h4:contains('Termin odbioru:')").next().children().first()
            .text(`${$("input[name='date']").val()}`).next()
            .text(`${$("input[name='time']").val()}`).next()
            .text(`${$("textarea[name='more_info']").val() ? $("textarea[name='more_info']").val() : 'Brak uwag'}`)

    }

    $("form#multistep .next-step").click(function () {
        if (currentStep == 1) {
            filterCategory();
        }
        if (currentStep == 4) {
            summaryData()
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