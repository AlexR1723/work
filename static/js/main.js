var time = 2, cc = 1;
$(window).scroll(function () {
    $('#counter-main').each(function () {
        var
            cPos = $(this).offset().top,
            topWindow = $(window).scrollTop();
        if (cPos < topWindow + 1000) {

            if (cc < 2) {
                $(".number").addClass("viz")
                $('div').each(function () {
                    var
                        i = 1,
                        num = $(this).data('num'),
                        step = 1000 * time / num,
                        that = $(this),
                        int = setInterval(function () {
                            if (i <= num) {
                                that.html(i);
                            } else {
                                cc = cc + 2;
                                clearInterval(int);

                            }
                            i++;
                        }, step);
                });
            }
        }
    });
});

$("#safety_btn_customer").click(function () {
    let cus = document.getElementById('safety_btn_customer')
    let exe = document.getElementById('safety_btn_executor')
    cus.removeAttribute('class', 'safety_btn_not_choosen')
    exe.removeAttribute('class', 'safety_btn_choosen')
    cus.setAttribute('class', 'safety_btn_choosen safety_btn')
    exe.setAttribute('class', 'safety_btn_not_choosen safety_btn')
    // let dcus = document.getElementById('div_customer')
    document.getElementById('div_executor').style.display = "none"
    document.getElementById('div_customer').style.display = "block"
});

$("#safety_btn_executor").click(function () {
    let cus = document.getElementById('safety_btn_customer')
    let exe = document.getElementById('safety_btn_executor')
    exe.removeAttribute('class', 'safety_btn_not_choosen')
    cus.removeAttribute('class', 'safety_btn_choosen')
    exe.setAttribute('class', 'safety_btn_choosen safety_btn')
    cus.setAttribute('class', 'safety_btn_not_choosen safety_btn')
    document.getElementById('div_customer').style.display = "none"
     document.getElementById('div_executor').style.display = "block"
});

$(document).ready(function() {
    $(".more_sub").click(function(){
        var el=$(this)
        el.addClass('d-none');
    });
})