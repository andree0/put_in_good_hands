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
            .text(`${$("input[name='bags']").val() ? $("input[name='bags']").val() : 0} ${bagName} w kategorii "${checkedCategory}"`)

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

    function clearCheckedOrganization () {
        $("input[name='organization']").each(function () {
            this.checked = false 
        })
    }

    $("form#multistep .next-step").attr("disabled", true)

    $("div[data-step='1'] div.form-group--checkbox").click(function () {
        let checkInputCategory = false
        $("input[name='categories']").each(function () {
            if ($(this).prop("checked")) {
                checkInputCategory = true
            } 
            if (checkInputCategory) {
                $("form#multistep .next-step").first().removeAttr("disabled")
            } else {
                $("form#multistep .next-step").first().attr("disabled", true)
            }       
        })
    })

    $("div[data-step='2'] input[name='bags']").change(function () {
        if ($(this).val() > 0) {
            $("div[data-step='2'] button.next-step").removeAttr("disabled")
        } else {
            $("div[data-step='2'] button.next-step").attr("disabled", true)
        }
    })

    $("div[data-step='3'] div.form-group--checkbox").click(function () {
        let checkInputOrganization = false
        $("input[name='organization']").each(function () {
            if ($(this).prop("checked")) {
                checkInputOrganization = true
            } 
            if (checkInputOrganization) {
                $("div[data-step='3'] button.next-step").removeAttr("disabled")
            }         
        })
    })

    function validationStep4 () {
        let address = false
        let city = false
        let postcode = false
        let phone = false
        let dateInput = false
        let timeInput = false
    
        if ($("input[name='address']").val()) {
            if (/\d/.test($("input[name='address']").val())) {
                $("input[name='address']").css("border", "1px solid #3c3c3c")
                address = true
            } else {
                $("input[name='address']").css("border-color", "red")
                address = false
            }            
        } else {
            address = false
        }


        if ($("input[name='city']").val()) {
            city = true
        } else {
            city = false
        }

        if ($("input[name='postcode']").val()) {
            if (/[0-9]{2}-[0-9]{3}/.test($("input[name='postcode']").val()) && $("input[name='postcode']").val().length == 6) {
                $("input[name='postcode']").css("border", "1px solid #3c3c3c")
                postcode = true
            } else {
                $("input[name='postcode']").css("border-color", "red")
                postcode = false
            }            
        } else {
            postcode = false
        }


        if($("input[name='phone']").val()) {
            if (/[1-9]{1}[0-9]{8}/.test($("input[name='phone']").val()) && $("input[name='phone']").val().length == 9) {
                $("input[name='phone']").css("border", "1px solid #3c3c3c")
                phone = true
            } else {
                $("input[name='phone']").css("border-color", "red")
                phone = false
            }            
        } else {
            phone = false
        }

        const selectedDateArray = $("input[name='date']").val().split('-')
        const currentDate = new Date()
        const inputDay = parseInt(selectedDateArray[2])
        const inputMonth = parseInt(selectedDateArray[1]) - 1
        const inputYear = parseInt(selectedDateArray[0])

        if ($("input[name='date']").val()) {
            if (new Date(inputYear, inputMonth, inputDay) > currentDate) {
                $("input[name='date']").css("border", "1px solid #3c3c3c")
                dateInput = true
            } else {
                $("input[name='date']").css("border-color", "red")
                dateInput = false
            }
        } else {
            dateInput = false
        }        

        if ($("input[name='time']").val()) {
            timeInput = true
        } else {
            timeInput = false
        } 

        if (address && city && postcode && phone && dateInput && timeInput) {
            $("div[data-step='4'] button.next-step").removeAttr("disabled")
        } else {
            $("div[data-step='4'] button.next-step").attr("disabled", true)
        }
    }

    $("form#multistep").submit(function (e) {
        if (!$("div[data-step='5']").hasClass("active")) {
            e.preventDefault();
        }
        
    })


    $("form#multistep").change(function () {
        validationStep4();
    })

    $("input[name='categories']").change(function () {
        $("div[data-step='3'] button.next-step").attr("disabled", true)
        clearCheckedOrganization();
    })

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

    $("input[value='Nieodebrany']").click(function (e) {
        e.preventDefault();
    })

    $("input[value='Odebrany']").click(function (e) {
        if ($(this).hasClass('active')) {
            e.preventDefault();
        } else {
            const confirmation = confirm("Operacja jest nieodwracalna. Czy jesteś pewny, że chcesz zmienić status Swojego daru na 'Odebrany' ?")
            if (confirmation) {
                alert("Dziękujemy za przekazanie daru. \n Życzymy miłego dnia. ;)")
            } else {
                e.preventDefault();
            }
        }
    })

    $(".errorlist").css({"color": "red", "font-size": "14px"})

    $("form#settings_form").append($("<div>").addClass("form-group").append($("input#id_password").addClass("form-control")).append($("div#confirm_buutons")))

})