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
            let height =$(window).height()
            let block = document.getElementById(target_blocks[i]).getBoundingClientRect().top
            // console.log(pos+' > '+height+'-'+block+'='+(height-block)+'  |  '+block2)
            // console.log('niz:'+(pos+height)+' block_pos:'+(pos - block)+' pos:'+pos+' height:'+height+' block:'+block)
            // let block1=target_blocks[i].getBoundingClientRect()
            // let block2=document.getElementById('counter1').getBoundingClientRect()
            // let pos1=$('#counter1').scrollTop()
            // let res = pos - block - (height*0.8)
            // let res = pos - block
            let res = height - block-(height*0.3)
            // if(pos>res){
            //
            // }
            // var scrollEvent = ($(window).scrollTop() > (target_blocks[i].position().top -$(window).height()));
            if (res > 0 && blockStatus) {
                let start_val=document.getElementById(target_blocks[i]).textContent
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