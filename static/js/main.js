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

// var list_categories;
var list_subcategories;

function load_categories() {
    const start = new Date().getTime();
    console.log("start " + start)
    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        // data: {
        //     word: str,
        // },
        url: '/Main/search_input/',
        success: function (data) {
            // list_categories = data;
            // list_categories = data[0];
            list_subcategories = data[1];
            var list_id = []
            for (let i = 0; i < data[0].length; i++) {
                list_id.push(data[0][i][0])
            }
            for (let i = 0; i < list_subcategories.length; i++) {
                let id = list_subcategories[i][2]
                let text = data[0][list_id.indexOf(id)][1]
                list_subcategories[i][2] = text;
            }
        },
        error: function (data) {
            alert('Error');
        }
    })
    const end = new Date().getTime();
    console.log("end " + end)
    console.log('time: ' + (end - start) + ' ms');
    // console.log('lenght ' + data[0].length)
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
function add_drop_item(list) {
    // div = document.getElementById('res_list')
    // div.innerHTML = ""
    let btn = document.createElement('button')
    btn.setAttribute('class', 'search_input_drop_el w-100 px-2 py-2')
    // btn.setAttribute('form', list[0])
    btn.setAttribute('form', 'main_input_form_header')
    // btn.setAttribute('type', 'submit')
    btn.setAttribute('type', 'button')

    let row = document.createElement('div')
    row.setAttribute('class', 'row align-items-center')

    let cat = document.createElement('div')
    cat.setAttribute('class', 'col-12 col-sm-10 col-md-9 col-lg-9 col-xl-10')
    let cat_p = document.createElement('p')
    cat_p.setAttribute('class', 'm-0 w-100 fz_15rem text-left line_height_1 cursor_inherit')
    cat_p.innerHTML = list[1]
    cat.appendChild(cat_p)

    let sub_cat = document.createElement('div')
    sub_cat.setAttribute('class', 'col-12 col-sm-10 col-md-9 col-lg-9 col-xl-10')
    let sub_cat_p = document.createElement('p')
    sub_cat_p.setAttribute('class', 'm-0 w-100 fz_1rem color_gray text-left cursor_inherit')
    sub_cat_p.innerHTML = list[2]
    sub_cat.appendChild(sub_cat_p)

    let isp = document.createElement('div')
    isp.setAttribute('class', 'col-4 col-sm-2 col-md-3 col-lg-3 col-xl-2 p-0 text-right d-none d-sm-block')
    let isp_p = document.createElement('p')
    isp_p.setAttribute('class', 'm-0 w-100 fz_1rem color_gray cursor_inherit')
    let isp_i = document.createElement('i')
    isp_i.setAttribute('class', 'fas fa-user-friends')
    isp_i.innerText = '1000'
    isp_p.appendChild(isp_i)
    isp.appendChild(isp_p)

    let zak = document.createElement('div')
    zak.setAttribute('class', 'col-4 col-sm-2 col-md-3 col-lg-3 col-xl-2 p-0 text-right d-none d-sm-block')
    let zak_p = document.createElement('p')
    zak_p.setAttribute('class', 'm-0 w-100 fz_1rem color_gray cursor_inherit')
    let zak_i = document.createElement('i')
    zak_i.setAttribute('class', 'fas fa-exclamation-triangle')
    zak_i.innerText = '1500'
    zak_p.appendChild(zak_i)
    zak.appendChild(zak_p)


    let isp1 = document.createElement('div')
    isp1.setAttribute('class', 'col-6 text-left d-block d-sm-none')
    let isp_p1 = document.createElement('p')
    isp_p1.setAttribute('class', 'm-0 w-100 fz_1rem color_gray')

    let isp_i1 = document.createElement('i')
    isp_i1.setAttribute('class', 'fas fa-user-friends')
    isp_i1.innerText = '1000'
    isp_p1.appendChild(isp_i1)
    isp1.appendChild(isp_p1)

    let zak1 = document.createElement('div')
    zak1.setAttribute('class', 'col-6 text-right d-block d-sm-none')
    let zak_p1 = document.createElement('p')
    zak_p1.setAttribute('class', 'm-0 w-100 fz_1rem color_gray')
    let zak_i1 = document.createElement('i')
    zak_i1.setAttribute('class', 'fas fa-exclamation-triangle')
    zak_i1.innerText = '1500'
    zak_p1.appendChild(zak_i1)
    zak1.appendChild(zak_p1)


    // let form = document.createElement('form')
    //
    // form.setAttribute('method', 'get')
    // form.setAttribute('action', '/dev/')
    // form.setAttribute('id', list[0])
    // let hidden_input = document.createElement('input')
    // hidden_input.setAttribute('type', 'hidden')
    // hidden_input.setAttribute('value', list[0])
    // hidden_input.setAttribute('name', 'id')
    // form.appendChild(hidden_input)

    row.appendChild(cat)
    row.appendChild(isp)
    row.appendChild(sub_cat)
    row.appendChild(zak)
    row.appendChild(isp1)
    row.appendChild(zak1)
    btn.appendChild(row)

    // div.appendChild(form)
    div.appendChild(btn)

    div.setAttribute('style', 'display:block')
}

$('#res_list_header').on( 'click', 'button ', function( event ) {

    document.getElementById('main_input_header').value=this.childNodes[0].childNodes[0].childNodes[0].textContent;
    $('#btn_head_submit').click()

});

$('#accordion_cities').on( 'click', 'a.link_cities ', function( event ) {

    // alert(this.innerHTML)
    // sessionStorage.setItem('myCat', 'Tom');
    // sessionStorage.setItem('city',this.innerHTML)
    // alert(sessionStorage.getItem('city'))

    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        data: {
            city: this.innerHTML,
            reg:this.dataset.region
        },
        url: '/Main/set_session_city/',
        success: function (data) {
            // alert(data)
            if(data='good'){
                location.reload()
            }
        },
        error: function (data) {
            alert('Error');
        }
    })


});

document.onclick = function (e) {
    // alert(e.target.id);
    let closest_head = (e.target).closest('div#res_list_header')
    if (document.getElementById('res_list_header').style.display == 'block' && closest_head == null) {
        // alert(e.target.tagName);
        console.log(closest_head)
        document.getElementById('res_list_header').innerHTML = ""
        document.getElementById('res_list_header').style.display = "none"
    }
    if (e.target.id == 'main_input_header') {
        show_item(document.getElementById('main_input_header').value, 0, 'res_list_header', 'main_input_header');
    }

    let closest_main = (e.target).closest('div#res_list')
    if (document.getElementById('res_list') != null && document.getElementById('res_list').style.display == 'block' && closest_main == null) {
        console.log(closest_main)
        document.getElementById('res_list').innerHTML = ""
        document.getElementById('res_list').style.display = "none"
    }
    if (e.target.id == 'main_input') {
        show_item(document.getElementById('main_input').value, 0, 'res_list', 'main_input');
    }
};

// var list_res;
var el_num = undefined;

function up_down_item(nav, el) {
    var elems = document.getElementsByClassName("search_input_drop_el");
    if (el_num == undefined && nav == 'down') {
        el_num = 0
    } else {
        if (el_num == undefined && nav == 'up') {
            el_num = elems.length - 1
        } else {
            if (nav == 'down') {
                el_num++
            } else {
                el_num--
            }
        }
    }
    if (el_num < 0) {
        el_num = elems.length - 1
    }
    if (el_num > elems.length - 1) {
        el_num = 0
    }
    for (let i = 0; i < elems.length; i++) {
        if (i != el_num) {
            elems[i].setAttribute('class', 'search_input_drop_el w-100 px-2 py-2')
        } else {
            elems[i].setAttribute('class', 'search_input_drop_el w-100 px-2 py-2 sid_focus')
            // let text = elems[i].childNodes[0].childNodes[0].childNodes[0].textContent;
            document.getElementById(el).value = elems[i].childNodes[0].childNodes[0].childNodes[0].textContent;
        }
    }
}

function show_item(val, code, list, el) {
    switch (code) {
        case 40:
            up_down_item('down', el)
            break;
        case 38:
            up_down_item('up', el)
            break;
        case 13:
            // $(".sid_focus")[0].click();
            let form = document.getElementsByClassName('sid_focus')[0].form;

            $('.sid_focus')[0].on('click', function () {
                $(form).submit();
            });
            break;
        default:
            div = document.getElementById(list)
            // div = document.getElementById('res_list')
            if (val != undefined) {
                let str = val.trim().toLowerCase();
                let arr = str.split(' ')
                let list_res = []
                if (str.length > 1) {
                    for (let i = 0; i < list_subcategories.length; i++) {
                        if (list_res.length >= 7) {
                            break;
                        } else {
                            let str_sub = list_subcategories[i][1].toLowerCase()
                            let cnt = 0;
                            for (let j = 0; j < arr.length; j++) {
                                var str1 = arr[j];
                                var have = str_sub.indexOf(str1);
                                if (have != -1) {
                                    cnt++;
                                }
                            }
                            if (cnt == arr.length) {
                                list_res.push(list_subcategories[i])
                            }
                        }
                    }
                    div.innerHTML = ""
                    el_num = undefined
                    for (let i = 0; i < list_res.length; i++) {
                        add_drop_item(list_res[i])
                    }
                } else {
                    div.setAttribute('style', 'display:none')
                    div.innerHTML = ""
                }
            }
    }
}

// $("#main_input").keyup(function (event) {
//     if (event.keyCode == 13) {
//         event.preventDefault();
//
//     }
// });
$("#main_input").keyup(function (event) {
    if (event.keyCode == 13) {
        event.preventDefault();
    } else {
        show_item(this.value, event.keyCode, 'res_list', 'main_input');
    }
    // switch (event.keyCode) {
    //     case 40:
    //         up_down_item('down')
    //         break;
    //     case 38:
    //         up_down_item('up')
    //         break;
    //     case 13:
    //         $(".sid_focus").click();
    //
    //         break;
    //     default:
    //         div = document.getElementById('res_list')
    //         let str = this.value.trim().toLowerCase();
    //         let arr = str.split(' ')
    //         let list_res = []
    //         if (str.length > 1) {
    //             for (let i = 0; i < list_subcategories.length; i++) {
    //                 if (list_res.length >= 7) {
    //                     break;
    //                 } else {
    //                     let str_sub = list_subcategories[i][1].toLowerCase()
    //                     let cnt = 0;
    //                     for (let j = 0; j < arr.length; j++) {
    //                         var str1 = arr[j];
    //                         var have = str_sub.indexOf(str1);
    //                         if (have != -1) {
    //                             cnt++;
    //                         }
    //                     }
    //                     if (cnt == arr.length) {
    //                         list_res.push(list_subcategories[i])
    //                     }
    //                 }
    //             }
    //             div.innerHTML = ""
    //             el_num = undefined
    //             for (let i = 0; i < list_res.length; i++) {
    //                 add_drop_item(list_res[i])
    //             }
    //         } else {
    //             div.setAttribute('style', 'display:none')
    //             div.innerHTML = ""
    //         }
    // }
})

$("#main_input_header").keyup(function (event) {
    if (event.keyCode == 13) {
        event.preventDefault();
    } else {
        show_item(this.value, event.keyCode, 'res_list_header', 'main_input_header');
    }
    // show_item(this.value,event.keyCode,'res_list');
    // switch (event.keyCode) {
    //     case 40:
    //         up_down_item('down')
    //         break;
    //     case 38:
    //         up_down_item('up')
    //         break;
    //     case 13:
    //         $(".sid_focus").click();
    //
    //         break;
    //     default:
    //         div = document.getElementById('res_list_header')
    //         let str = this.value.trim().toLowerCase();
    //         let arr = str.split(' ')
    //         let list_res = []
    //         if (str.length > 1) {
    //             for (let i = 0; i < list_subcategories.length; i++) {
    //                 if (list_res.length >= 7) {
    //                     break;
    //                 } else {
    //                     let str_sub = list_subcategories[i][1].toLowerCase()
    //                     let cnt = 0;
    //                     for (let j = 0; j < arr.length; j++) {
    //                         var str1 = arr[j];
    //                         var have = str_sub.indexOf(str1);
    //                         if (have != -1) {
    //                             cnt++;
    //                         }
    //                     }
    //                     if (cnt == arr.length) {
    //                         list_res.push(list_subcategories[i])
    //                     }
    //                 }
    //             }
    //             div.innerHTML = ""
    //             el_num = undefined
    //             for (let i = 0; i < list_res.length; i++) {
    //                 add_drop_item(list_res[i])
    //             }
    //         } else {
    //             div.setAttribute('style', 'display:none')
    //             div.innerHTML = ""
    //         }
    // }
})

window.onload = function () {
    // let reg='cities_dnr'
    // region_cities(reg)
    load_categories();

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
    $("#RegisterInputName").click(function () {
        $('#RegisterInputName').removeClass('br-red');
    });
    $("#RegisterInputSurname").click(function () {
        $('#RegisterInputSurname').removeClass('br-red');
    });
    $("#RegisterInputEmail1").click(function () {
        $('#RegisterInputEmail1').removeClass('br-red');
    });
    $("#RegisterInputPhone").click(function () {
        $('#RegisterInputPhone').removeClass('br-red');
    });
    $("#RegisterInputPassword1").click(function () {
        $('#RegisterInputPassword1').removeClass('br-red');
    });
    $("#RegisterInputPassword2").click(function () {
        $('#RegisterInputPassword2').removeClass('br-red');
    });
    $('#registry').click(function () {
        var name = $("#RegisterInputName").val();
        var surname = $("#RegisterInputSurname").val();
        var email = $("#RegisterInputEmail1").val();
        var tel = $("#RegisterInputPhone").val();
        var pass1 = $("#RegisterInputPassword1").val();
        var pass2 = $("#RegisterInputPassword2").val();
        var check = $("#RegisterInputCheckbox").is(':checked');

        if (name == "") $('#RegisterInputName').addClass('br-red');
        if (surname == "") $('#RegisterInputSurname').addClass('br-red');
        if (email == "") $('#RegisterInputEmail1').addClass('br-red');
        if (tel == "") $('#RegisterInputPhone').addClass('br-red');
        if (pass1 == "") $('#RegisterInputPassword1').addClass('br-red');
        if (pass2 == "") $('#RegisterInputPassword2').addClass('br-red');
        if (check==false)
            $("#alert-check").show('slow');
            setTimeout(function () {
                $("#alert-check").hide('slow');
            }, 5000);
            if (name != "" && surname != "" && email != "" && tel != "" && pass1 != "" && pass2 != "" && check == true) {
                if(pass1==pass2) {
                    $.ajax({
                        type: "GET",
                        dataType: "json",
                        url: 'registrate/',
                        data: {
                            name: name,
                            surname: surname,
                            email: email,
                            tel: tel,
                            pass1: pass1
                        },
                        success: function (data) {
                            if(data.data=='ok') {
                                $("#alert-success").show('slow');
                                setTimeout(function () {
                                    $("#alert-success").hide('slow');
                                }, 5000);
                            }
                            if(data.data=='error')
                            {
                                $("#alert-error").show('slow');
                                setTimeout(function () {
                                    $("#alert-error").hide('slow');
                                }, 5000);
                            }
                            if(data.data=='email')
                            {
                                $("#alert-email").show('slow');
                                setTimeout(function () {
                                    $("#alert-email").hide('slow');
                                }, 5000);
                            }
                        },
                        error: function (data) {
                            $("#alert-error").show('slow');
                            setTimeout(function () {
                                $("#alert-error").hide('slow');
                            }, 5000);
                        }
                    })
                }
                else
                {
                    $("#alert-pass").show('slow');
                    setTimeout(function () {
                        $("#alert-pass").hide('slow');
                    }, 5000);
                }
            } else {
                $("#alert-danger").show('slow');
                setTimeout(function () {
                    $("#alert-danger").hide('slow');
                }, 5000);
            }
    })
});

$(".settings-blk").ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});