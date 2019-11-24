// var time = 2, cc = 1;
// $(window).scroll(function () {
// //     $('#counter-main').each(function () {
// //         var
// //             cPos = $(this).offset().top,
// //             topWindow = $(window).scrollTop();
// //         if (cPos < topWindow + 1000) {
// //
// //             if (cc < 2) {
// //                 $(".number").addClass("viz")
// //                 $('div').each(function () {
// //                     var
// //                         i = 1,
// //                         num = $(this).data('num'),
// //                         step = 1000 * time / num,
// //                         that = $(this),
// //                         int = setInterval(function () {
// //                             if (i <= num) {
// //                                 that.html(i);
// //                             } else {
// //                                 cc = cc + 2;
// //                                 clearInterval(int);
// //
// //                             }
// //                             i++;
// //                         }, step);
// //                 });
// //             }
// //         }
// //     });
// // });

function counter(counts) {
    let blockStatus = true;
    let inc = 0
    let target_blocks = ['div_counter1', 'div_counter2', 'div_counter3']
    let target_blocks1 = [$("#counter1"), $("#counter2"), $("#counter3")]
    // let target_blocks = [$("#counter1"), $("#counter2"), $("#counter3"),]
    $(window).scroll(function () {
        for (let i = 0; i < target_blocks.length; i++) {
            let pos = $(window).scrollTop()
            // let block =target_blocks[i].position().top
            let height = $(window).height()
            let block = document.getElementById(target_blocks[i]).getBoundingClientRect().top
            // console.log(pos+' > '+height+'-'+block+'='+(height-block)+'  |  '+block2)
            // console.log('niz:'+(pos+height)+' block_pos:'+(pos - block)+' pos:'+pos+' height:'+height+' block:'+block)
            // let block1=target_blocks[i].getBoundingClientRect()
            // let block2=document.getElementById('counter1').getBoundingClientRect()
            // let pos1=$('#counter1').scrollTop()
            // let res = pos - block - (height*0.8)
            // let res = pos - block
            let res = height - block - (height * 0.3)
            // if(pos>res){
            //
            // }
            // var scrollEvent = ($(window).scrollTop() > (target_blocks[i].position().top -$(window).height()));
            if (res > 0 && blockStatus) {
                let start_val = document.getElementById(target_blocks[i]).textContent
                // start_val=start_val/2
                $({numberValue: start_val}).animate({numberValue: counts[i]}, {
                    duration: 5000, // Продолжительность анимации, где 500 - 0.5 одной секунды, то есть 500 миллисекунд
                    easing: "linear",
                    step: function (val) {
                        // $("#counter").html(Math.ceil(val)); // Блок, где необходимо сделать анимацию
                        target_blocks1[i].html(Math.ceil(val)); // Блок, где необходимо сделать анимацию
                    }
                });
                // console.log('added? inc=' + inc)
                inc++
            }
        }
        if (inc > 1) {
            blockStatus = false; // Запрещаем повторное выполнение функции до следующей перезагрузки страницы.
        }

    });
}

// var region = cities_dnr

// function region_cities(reg) {
//     ['cities_dnr', 'cities_lnr', 'cities_rus', 'cities_ukr'].forEach((item) => {
//         if (item != reg) {
//             document.getElementById(item).style.display = 'none'
//         }
//         else {
//              document.getElementById(item).style.display = 'flex'
//         }
//     })
// }

// $("#btn_city_dnr").click(function () {
//     region_cities('cities_dnr')
// });
// $("#btn_city_lnr").click(function () {
//     region_cities('cities_lnr')
// });
// $("#btn_city_rus").click(function () {
//     region_cities('cities_rus')
// });
// $("#btn_city_ukr").click(function () {
//     region_cities('cities_ukr')
// });

$("#main_input").keyup(function (event) {

    div = document.getElementById('res_list')


    // let str = document.getElementById('search_input').value
    let str = this.value
    let list_res = []
    // if (str.trim()== ""){
    //     div.setAttribute('style','display:none')
    //     div.innerHTML = ""
    // }
    if (str.trim().length > 1) {

        $.ajax({
            type: "GET",
            dataType: "json",
            data: {
                word: str,
            },
            url: '/Main/search_input/',
            success: function (data) {
                list_res = data;

                div.innerHTML = ""
                for (let i = 0; i < list_res.length; i++) {
                    let btn = document.createElement('button')
                    btn.setAttribute('class', 'search_input_drop_el w-100 px-2 py-2')
                    btn.setAttribute('form', list_res[i][0])
                    btn.setAttribute('type', 'submit')

                    let row = document.createElement('div')
                    row.setAttribute('class', 'row align-items-center')

                    let cat = document.createElement('div')
                    cat.setAttribute('class', 'col-12 col-sm-10 col-md-9 col-lg-9 col-xl-10')
                    let cat_p = document.createElement('p')
                    cat_p.setAttribute('class', 'm-0 w-100 fz_15rem text-left line_height_1')
                    cat_p.innerHTML = list_res[i][1]
                    cat.appendChild(cat_p)

                    let sub_cat = document.createElement('div')
                    sub_cat.setAttribute('class', 'col-12 col-sm-10 col-md-9 col-lg-9 col-xl-10')
                    let sub_cat_p = document.createElement('p')
                    sub_cat_p.setAttribute('class', 'm-0 w-100 fz_1rem color_gray text-left')
                    sub_cat_p.innerHTML = list_res[i][2]
                    sub_cat.appendChild(sub_cat_p)

                    let isp = document.createElement('div')
                    isp.setAttribute('class', 'col-4 col-sm-2 col-md-3 col-lg-3 col-xl-2 text-right d-none d-sm-block')
                    let isp_p = document.createElement('p')
                    isp_p.setAttribute('class', 'm-0 w-100 fz_1rem color_gray')

                    let isp_i = document.createElement('i')
                    isp_i.setAttribute('class','fas fa-user-friends')
                    isp_i.innerText='1000'
                    isp_p.appendChild(isp_i)
                    isp.appendChild(isp_p)

                    let zak = document.createElement('div')
                    zak.setAttribute('class', 'col-4 col-sm-2 col-md-3 col-lg-3 col-xl-2 text-right d-none d-sm-block')
                    let zak_p = document.createElement('p')
                    zak_p.setAttribute('class', 'm-0 w-100 fz_1rem color_gray')
                     let zak_i = document.createElement('i')
                    zak_i.setAttribute('class','fas fa-exclamation-triangle')
                    zak_i.innerText='1500'
                    zak_p.appendChild(zak_i)
                    zak.appendChild(zak_p)



                    let isp1 = document.createElement('div')
                    isp1.setAttribute('class', 'col-6 text-left d-block d-sm-none')
                    let isp_p1 = document.createElement('p')
                    isp_p1.setAttribute('class', 'm-0 w-100 fz_1rem color_gray')

                    let isp_i1 = document.createElement('i')
                    isp_i1.setAttribute('class','fas fa-user-friends')
                    isp_i1.innerText='1000'
                    isp_p1.appendChild(isp_i1)
                    isp1.appendChild(isp_p1)

                    let zak1 = document.createElement('div')
                    zak1.setAttribute('class', 'col-6 text-right d-block d-sm-none')
                    let zak_p1 = document.createElement('p')
                    zak_p1.setAttribute('class', 'm-0 w-100 fz_1rem color_gray')
                     let zak_i1 = document.createElement('i')
                    zak_i1.setAttribute('class','fas fa-exclamation-triangle')
                    zak_i1.innerText='1500'
                    zak_p1.appendChild(zak_i1)
                    zak1.appendChild(zak_p1)



                    let form = document.createElement('form')

                    form.setAttribute('method', 'get')
                    form.setAttribute('action', '/Products/Products_detail/')
                    form.setAttribute('id', list_res[i][0])
                    let hidden_input = document.createElement('input')
                    hidden_input.setAttribute('type', 'hidden')
                    hidden_input.setAttribute('id', list_res[i][0])
                    hidden_input.setAttribute('name', 'id')
                    form.appendChild(hidden_input)

                    row.appendChild(cat)
                    row.appendChild(isp)
                    row.appendChild(sub_cat)
                    row.appendChild(zak)
                    row.appendChild(isp1)
                    row.appendChild(zak1)
                    btn.appendChild(row)

                    div.appendChild(form)
                    div.appendChild(btn)

                     div.setAttribute('style', 'display:block')
                }
            },
            error: function (data) {
                alert('Error');
            }
        })


    } else {
        div.setAttribute('style', 'display:none')
        div.innerHTML = ""
    }
})

window.onload = function () {
    // let reg='cities_dnr'
    // region_cities(reg)


    try {
        // let target_blocks = [$("#counter1"), $("#counter2"), $("#counter3")]
        // let target_blocks = ['counter1', 'counter2', 'counter3']
        let check1 = document.getElementById('counter1')
        let check2 = document.getElementById('counter2')
        let check3 = document.getElementById('counter3')
        // if (target_blocks[0].length != 0 && target_blocks[1].length != 0 && target_blocks[2].length != 0) {
        if (check1 != null && check2 != null && check3 != null) {
            counter([10000, 10, 70000])
        }


    } catch (e) {

    }
    {

    }
    // if (window.location.href.indexOf('for_business')!= -1  || window.location.href.indexOf('for_business') != -1 || window.location.href.indexOf('main') != -1) {
    //     counter([10000,52222,70000])
    //
    // }
};


// $(function() {
// 		var target_block = $(".price"); // Ищем блок 		var blockStatus = true;
// 		$(window).scroll(function() {
// 			var scrollEvent = ($(window).scrollTop() > (target_block.position().top - $(window).height()));
// 			if(scrollEvent && blockStatus) {
// 				blockStatus = false; // Запрещаем повторное выполнение функции до следующей перезагрузки страницы.
// 				$({numberValue: 0}).animate({numberValue: 1000}, {
// 					duration: 500, // Продолжительность анимации, где 500 - 0.5 одной секунды, то есть 500 миллисекунд
// 					easing: "linear",
// 					step: function(val) {
// 						$(".price").html(Math.ceil(val)); // Блок, где необходимо сделать анимацию
// 					}
// 				});
// 			}
// 		});
// 	});


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

$(document).ready(function () {
    $(".more_sub").click(function () {
        var el = $(this);
        el.addClass('d-none');
    });
    $("#more_category").click(function () {
        var el = document.getElementById('more_category');
        if (el.textContent === "Больше категорий")
            el.textContent = "Меньше категорий";
        else
            el.textContent = "Больше категорий";
    });
    $('#inputGroupSelect04').change(function () {
        var value = $('#inputGroupSelect04 option:selected').val();
        if (value == 0)
            window.location.href = '/news/';
        else
            window.location.href = '/news/' + value;
    });
    $("#name").click(function () {
        $('#name').removeClass('br-red');
    });
    $("#email").click(function () {
        $('#email').removeClass('br-red');
    });
    $("#message").click(function () {
        $('#message').removeClass('br-red');
    });
    $("#send").click(function () {
        var name = $("#name").val();
        var email = $("#email").val();
        var theme = $("#theme").val();
        var message = $("#message").val();
        if (name == "") {
            $('#name').addClass('br-red');
        }
        if (email == "") {
            $('#email').addClass('br-red');
        }
        if (message == "") {
            $('#message').addClass('br-red');
        }
        if (name != "" && email != "" && message != "") {
            $.ajax({
                type: "GET",
                dataType: "json",
                url: 'send/',
                data: {
                    name: name,
                    email: email,
                    theme: theme,
                    message: message
                },
                success: function (data) {
                    $("#alert-success").show('slow');
                    setTimeout(function () {
                        $("#alert-success").hide('slow');
                    }, 5000);
                },
                error: function (data) {
                    $("#alert-danger").show('slow');
                    setTimeout(function () {
                        $("#alert-danger").hide('slow');
                    }, 5000);
                }
            })
        } else {
            $("#alert-danger").show('slow');
            setTimeout(function () {
                $("#alert-danger").hide('slow');
            }, 5000);
        }
    });
});