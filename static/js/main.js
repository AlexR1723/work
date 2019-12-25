function counter(counts,is_scroll) {
    let blockStatus = true;
    let inc = 0
    let target_blocks = ['div_counter1', 'div_counter2', 'div_counter3']
    let target_blocks1 = [$("#counter1"), $("#counter2"), $("#counter3")]
    // let target_blocks = [$("#counter1"), $("#counter2"), $("#counter3"),]
    if (is_scroll==true){
        $(window).scroll(function () {
        for (let i = 0; i < target_blocks.length; i++) {
            let pos = $(window).scrollTop()
            let height = $(window).height()
            let block = document.getElementById(target_blocks[i]).getBoundingClientRect().top
            let res = height - block - (height * 0.3)
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
    else {
        for (let i = 0; i < target_blocks.length; i++) {
            // let pos = $(window).scrollTop()
            // let height = $(window).height()
            // let block = document.getElementById(target_blocks[i]).getBoundingClientRect().top
            // let res = height - block - (height * 0.3)
            // if (res > 0 && blockStatus) {
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
                // inc++
            // }
        }
        // if (inc > 1) {
        //     blockStatus = false; // Запрещаем повторное выполнение функции до следующей перезагрузки страницы.
        // }
    }

}

var list_subhelp;

function load_help() {
    // const start = new Date().getTime();
    // console.log("start " + start)
    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        url: 'load_input_help',
        success: function (data) {
            list_subhelp = data
        },
        error: function (data) {
            alert('Error');
        }
    })
    // const end = new Date().getTime();
    // console.log("end " + end)
    // console.log('time: ' + (end - start) + ' ms');
}

var list_subcategories;

function load_categories() {
    // const start = new Date().getTime();
    // console.log("start " + start)
    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        url: 'search_input_category',
        success: function (data) {
            list_subcategories = data[1];
            var list_id = []
            for (let i = 0; i < data[0].length; i++) {
                list_id.push(data[0][i][0])
            }
            for (let i = 0; i < list_subcategories.length; i++) {
                let id = list_subcategories[i][1]
                let text = data[0][list_id.indexOf(id)][1]
                list_subcategories[i][1] = text;
            }
        },
        error: function (data) {
            alert('Error');
        }
    })
    // const end = new Date().getTime();
    // console.log("end " + end)
    // console.log('time: ' + (end - start) + ' ms');
}

function add_drop_item(list, is_help, block) {
    let btn = document.createElement('button')
    btn.setAttribute('class', 'search_input_drop_el w-100 p-0  px-2 py-1')
    btn.setAttribute('type', 'button')

    let div = document.getElementById(block)

    let row = document.createElement('div')
    row.setAttribute('class', 'row align-items-center')

    let cat = document.createElement('div')
    cat.setAttribute('class', 'col-12 col-sm-10 col-md-9 col-lg-9 col-xl-10 p-0')
    let cat_p = document.createElement('p')
    cat_p.setAttribute('class', 'm-0 w-100 fz_13rem text-left line_height_1 cursor_inherit')

    if (is_help != 'help_input') {
        cat_p.innerHTML = list[0]
        cat.appendChild(cat_p)

        let sub_cat = document.createElement('div')
        sub_cat.setAttribute('class', 'col-12 col-sm-10 col-md-9 col-lg-9 col-xl-10 p-0')
        let sub_cat_p = document.createElement('p')
        sub_cat_p.setAttribute('class', 'm-0 w-100 fz_1rem color_gray text-left cursor_inherit')
        // sub_cat_p.setAttribute('class', 'search_dropdowns_headers fz_1rem color_gray')
        sub_cat_p.innerHTML = list[1]
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

        row.appendChild(cat)
        row.appendChild(isp)
        row.appendChild(sub_cat)
        row.appendChild(zak)
        row.appendChild(isp1)
        row.appendChild(zak1)
        btn.appendChild(row)
        div.appendChild(btn)
    } else {
        cat_p.innerHTML = list
        cat.appendChild(cat_p)
        row.appendChild(cat)
        btn.appendChild(row)
        div.appendChild(btn)
    }
    div.setAttribute('style', 'display:block')
}

$('#res_list_header').on('click', 'button ', function (event) {
    let text = this.childNodes[0].childNodes[0].childNodes[0].textContent;
    document.getElementById('main_input_header').value = text
    window.location.href = "/find/" + text.trim().toLowerCase();
});

$('#res_list_input').on('click', 'button ', function (event) {
    let text = this.childNodes[0].childNodes[0].childNodes[0].textContent;
    document.getElementById('help_input').value = text
    // window.location.href = "/help/find_help/" + text.trim().toLowerCase();
    window.location.href = "/help/questions/" + text.trim().toLowerCase();
});

$("#btn_head_submit").click(function (event) {
    let text = document.getElementById('main_input_header').value
    if (text.trim() != '') {
        let btn_text = document.getElementsByClassName('sid_focus')[0]
        if (btn_text != undefined && btn_text.childNodes[0].childNodes[0].childNodes[0].textContent == text.trim()) {
            window.location.href = "/category/sub_category/" + text.trim().toLowerCase();
        }
        // else {
        //     window.location.href = "/help/find_help/" + text.trim().toLowerCase();
        // }
    }
});

$("#btn_main_submit").click(function (event) {
    let text = document.getElementById('main_input').value
    if (text.trim() != '') {
        let btn_text = document.getElementsByClassName('sid_focus')[0]
        if (btn_text != undefined && btn_text.childNodes[0].childNodes[0].childNodes[0].textContent == text.trim()) {
            window.location.href = "/category/sub_category/" + text.trim().toLowerCase();
        }
    }
});

$("#btn_help_submit").click(function (event) {
    let text = document.getElementById('help_input').value
    if (text.trim() != '') {
        // window.location.href = "/help/find_help/" + text.trim().toLowerCase();
        // window.location.href = "/help/questions/" + text.trim().toLowerCase();
        let btn_text = document.getElementsByClassName('sid_focus')[0]
        if (btn_text != undefined && btn_text.childNodes[0].childNodes[0].childNodes[0].textContent == text.trim()) {
            window.location.href = "/help/questions/" + text.trim().toLowerCase();
        } else {
            window.location.href = "/help/find_help/" + text.trim().toLowerCase();
        }
    }


});

$('#accordion_cities').on('click', 'a.link_cities ', function (event) {
    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        data: {
            city: this.innerHTML,
            reg: this.dataset.region
        },
        url: '/Main/set_session_city/',
        success: function (data) {
            if (data = 'good') {
                location.reload()
            }
        },
        error: function (data) {
            alert('Error');
        }
    })
});//выбор города

document.onclick = function (e) {
    // alert(e.target.id);
    let closest_head = (e.target).closest('div#res_list_header')
    if (document.getElementById('res_list_header') != null && document.getElementById('res_list_header').style.display == 'block' && closest_head == null) {
        // alert(e.target.tagName);
        // console.log(closest_head)
        document.getElementById('res_list_header').innerHTML = ""
        document.getElementById('res_list_header').style.display = "none"
    }
    if (e.target.id == 'main_input_header') {
        show_item(document.getElementById('main_input_header').value, 0, 'res_list_header', 'main_input_header');
    }

    let closest_main = (e.target).closest('div#res_list')
    if (document.getElementById('res_list') != null && document.getElementById('res_list').style.display == 'block' && closest_main == null) {
        // console.log(closest_main)
        document.getElementById('res_list').innerHTML = ""
        document.getElementById('res_list').style.display = "none"
    }
    if (e.target.id == 'main_input') {
        show_item(document.getElementById('main_input').value, 0, 'res_list', 'main_input');
    }

    let closest_input = (e.target).closest('div#res_list_input')
    if (document.getElementById('res_list_input') != null && document.getElementById('res_list_input').style.display == 'block' && closest_input == null) {
        // alert(e.target.tagName);
        // console.log(closest_input)
        document.getElementById('res_list_input').innerHTML = ""
        document.getElementById('res_list_input').style.display = "none"
    }
    if (e.target.id == 'help_input') {
        show_item(document.getElementById('help_input').value, 0, 'res_list_input', 'help_input');
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
            elems[i].setAttribute('class', 'w-100 align-items-center px-2 py-1 search_input_drop_el')
        } else {
            elems[i].setAttribute('class', 'w-100 align-items-center px-2 py-1 search_input_drop_el sid_focus')
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
            let text = document.getElementById(el).value
            if (el != 'help_input') {
                if (text.trim() != '') {
                    window.location.href = "/category/sub_category/" + val.trim().toLowerCase();
                }
            } else {

                // let text = document.getElementById('help_input').value
                if (text.trim() != '') {
                    let btn_text = document.getElementsByClassName('sid_focus')[0]
                    if (btn_text != undefined && btn_text.childNodes[0].childNodes[0].childNodes[0].textContent == val.trim()) {
                        window.location.href = "/help/questions/" + val.trim().toLowerCase();
                    } else {
                        window.location.href = "/help/find_help/" + val.trim().toLowerCase();
                    }
                }
            }
            break;
        default:
            var res;
            if (el != 'help_input') {
                res = list_subcategories
            } else {
                res = list_subhelp
            }
            let div = document.getElementById(list)
            if (val != undefined) {
                let str = val.trim().toLowerCase();
                let arr = str.split(' ')
                let list_res = []
                if (str.length > 1) {
                    for (let i = 0; i < res.length; i++) {
                        if (list_res.length >= 7) {
                            break;
                        } else {
                            if (el != 'help_input') {
                                var str_sub = res[i][0].toLowerCase()
                            } else {
                                var str_sub = res[i].toLowerCase()
                            }
                            let cnt = 0;
                            for (let j = 0; j < arr.length; j++) {
                                var str1 = arr[j];
                                var have = str_sub.indexOf(str1);
                                if (have != -1) {
                                    cnt++;
                                }
                            }
                            if (cnt == arr.length) {
                                list_res.push(res[i])
                            }
                        }
                    }
                    div.innerHTML = ""
                    el_num = undefined
                    for (let i = 0; i < list_res.length; i++) {
                        add_drop_item(list_res[i], el, list)
                    }
                } else {
                    div.setAttribute('style', 'display:none')
                    div.innerHTML = ""
                }
            }
    }
}

$("#help_input").keyup(function (event) {
    show_item(this.value, event.keyCode, 'res_list_input', 'help_input');
})

$("#main_input").keyup(function (event) {
    show_item(this.value, event.keyCode, 'res_list', 'main_input');
})

$("#main_input_header").keyup(function (event) {
    show_item(this.value, event.keyCode, 'res_list_header', 'main_input_header');
})

// $("#main_input_body").keyup(function (event) {
//     show_item(this.value, event.keyCode, 'res_list_main', 'main_input_body');
// })
// $("#a_search_input").click(function (event) {
//     event.preventDefault();
//     let text = document.getElementById('main_input_header').value
//     let link = "{% url 'Question_category' %}" + text
//     this.href = link
// });
$("#login_email").keyup(function (event) {
    // show_item(this.value, event.keyCode, 'res_list_input', 'help_input');
    if (event.keyCode == 13) {
        login()
    }
})
$("#login_pass").keyup(function (event) {
    if (event.keyCode == 13) {
        login()
    }
})

$('#task_filter_select').change(function () {
    var value = $('#task_filter_select option:selected').val();
    if (value == 0)
        // window.location.href = '/profile/customer_tasks/';
        window.location.href = '/profile/task/';
    else
        // window.location.href = '/profile/customer_tasks/' + value;
        window.location.href = '/profile/task/' + value;
});
$('#task_filter_select_exec_cat').change(function () {
    var cat = $('#task_filter_select_exec_cat option:selected').val();
    var stat = $('#task_filter_select_exec_stat option:selected').val();
    if (cat==0 && stat==0){
         // window.location.href = '/profile/executor_tasks/';
         window.location.href = '/profile/task/';
    }
    if (cat!=0 && stat==0){
         // window.location.href = '/profile/executor_tasks/category='+cat;
         window.location.href = '/profile/task/category='+cat;
    }
    if (cat==0 && stat!=0){
         // window.location.href = '/profile/executor_tasks/stat='+stat;
         window.location.href = '/profile/task/stat='+stat;
    }
    if (cat!=0 && stat!=0){
         // window.location.href = '/profile/executor_tasks/category='+cat+'/stat='+stat;
         window.location.href = '/profile/task/category='+cat+'/stat='+stat;
    }
})
$('#task_filter_select_exec_stat').change(function () {
    var cat = $('#task_filter_select_exec_cat option:selected').val();
    var stat = $('#task_filter_select_exec_stat option:selected').val();
    if (cat==0 && stat==0){
         window.location.href = '/profile/executor_tasks/';
    }
    if (cat!=0 && stat==0){
         window.location.href = '/profile/executor_tasks/category='+cat;
    }
    if (cat==0 && stat!=0){
         window.location.href = '/profile/executor_tasks/stat='+stat;
    }
    if (cat!=0 && stat!=0){
         window.location.href = '/profile/executor_tasks/category='+cat+'/stat='+stat;
    }
});
// let double = function(num)
// function send_ajax(url,values){
let send_ajax = function (url, values) {
    let result
    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        url: url,
        data: {
            values: values
        },
        success: function (data) {
            result = data
        },
        error: function (data) {
            result = 'error'
        }
    })
    return result
}

$("#btn_del_ads").click(function (event) {
    let id = this.dataset.id
    console.log(id)
    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        url: 'user_delete_ads',
        data: {
            id: id
        },
        success: function (data) {
            // alert(data)
            if (data==true){
                // alert('Объявление успешно удалено. Авто закрытие через 5 секунд')
                // setTimeout(5000)
                window.location.href= '/profile/advert/';
            }
            else {
                window.location.href= '/login';
            }
        },
        error: function (data) {
           alert('error')
        }
    })
});

window.onload = function () {
    load_categories();
    if (window.location.href.indexOf('help_category') != -1 || window.location.href.indexOf('help') != -1) {
        load_help();
    }
    try {
        let check1 = document.getElementById('counter1')
        let check2 = document.getElementById('counter2')
        let check3 = document.getElementById('counter3')
        // if (check1 != null && check2 != null && check3 != null && window.location.href.indexOf('register') == -1) {
        if (check1 != null && check2 != null && check3 != null) {
            // counter([10000, 10, 70000])
            let is_not_main=false
            if (window.location.href.indexOf('register') != -1) {
                let vals = send_ajax('get_counter_values', 'register_exec,count_tasks,register_perf')
                counter([vals[0], vals[1], vals[2]],false)
                is_not_main=true
            }
            if (window.location.href.indexOf('rabota') != -1) {
                let vals = send_ajax('get_counter_values', 'today_create_tasks,register_exec,complete_tasks')
                counter([vals[0], vals[1], vals[2]],true)
                is_not_main=true
            }
            if (window.location.href.indexOf('for_business') != -1) {
                let vals = send_ajax('get_counter_values', 'today_create_tasks,register_exec,complete_tasks')
                counter([vals[0], vals[1], vals[2]],true)
                is_not_main=true
            }
            if (window.location.href.indexOf('about') != -1) {
                let vals = send_ajax('get_counter_values', 'count_users,avialable_tasks,avialable_tasks')
                counter([vals[0], vals[1], vals[2]],true)
                is_not_main=true
            }
            if (is_not_main==false){
                let vals = send_ajax('get_counter_values', 'register_exec,count_tasks,register_perf')
                counter([vals[0], vals[1], vals[2]],true)
            }

        }
    } catch (e) {

    }
};

$("#btn_profile_change_pass").click(function () {
    let pass = document.getElementsByClassName('passwords')

    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        data: {
            old: pass[0].value,
            new1: pass[1].value,
            new2: pass[2].value,
        },
        url: 'change_password',
        success: function (data) {
            // alert(data)
            if (data == true) {
                pass[0].value = ''
                pass[1].value = ''
                pass[2].value = ''

                document.getElementById('alert-success_pass').innerHTML = 'Пароль успешно изменён'
                $("#alert-success_pass").show('slow');
                setTimeout(function () {
                    $("#alert-success_pass").hide('slow');
                }, 5000);
            } else {
                document.getElementById('alert-danger_pass').innerHTML = data
                $("#alert-danger_pass").show('slow');
                setTimeout(function () {
                    $("#alert-danger_pass").hide('slow');
                }, 5000);
            }
        },
        error: function (data) {
            alert('Error');
        }
    })
});

function login() {
    let email = document.getElementById('login_email')
    let pass = document.getElementById('login_pass')
    document.getElementById('login_email').setAttribute('class', 'form-control')
    document.getElementById('login_pass').setAttribute('class', 'form-control')
    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        data: {
            email: email.value,
            pass: pass.value
        },
        url: 'login_user',
        success: function (data) {
            if (data == true) {
                window.location.href = '/'
            } else {
                if (data == false) {
                    data = 'Заполните поля!'
                    document.getElementById('login_email').setAttribute('class', 'form-control br-red')
                    document.getElementById('login_pass').setAttribute('class', 'form-control br-red')
                }
                document.getElementById('alert-danger').innerHTML = data
                $("#alert-danger").show('slow');
                setTimeout(function () {
                    $("#alert-danger").hide('slow');
                }, 5000);
            }
        },
        error: function (data) {
            alert('Error');
        }
    })
}

$("#btn_login").click(function () {
    login()
})

$("#btn_add_photo").click(function () {
    let files = $('#img')[0].files
    // var fd = new FormData();
    // // fd.append("CustomField", "This is some extra data");
    // for (let i = 0; i < files.length; i++) {
    //     fd.append(i, files[i]);
    // }
    $.ajax({
        url: "load_photos",
        type: "GET",
        data: {
            files: files
        },
        processData: false,  // tell jQuery not to process the data
        contentType: false,   // tell jQuery not to set contentType
        success: function (data) {
            alert(data);
        },
        error: function (data) {
            alert('Error');
        }
    });
})

$('#form_add_img').on('submit', function (e) {
    e.preventDefault();
    // var data = new FormData($('#form_add_img').get(0));
    // var data1 = new FormData($('#form_add_img'))
    let files = $('#img')[0].files
    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        data: {
            files: files
        },
        url: 'login_user',
        success: function (data) {

        },
        error: function (data) {
            alert('Error');
        }
    })
    // $.ajax({
    //     url: :"/URL",
    //     method: "POST",
    //     data: data,
    //     success: function(data){},
    //     error: function(data){},
    //     processData: false,
    //     contentType: false,
    // });
});

// $("#images_input").click(function () {
//     let files=this.value

// $.ajax({
//     type: "GET",
//     dataType: "json",
//     async: false,
//     data: {
//         email: email.value,
//         pass: pass.value
//     },
//     url: 'login_user',
//     success: function (data) {
//
//     },
//     error: function (data) {
//         alert('Error');
//     }
// })
// })
// Отметить checkbox
// $('#checkbox').prop('checked', true);
//
// // Снять checkbox
// $('#checkbox').prop('checked', false);

$('#nav-contact-tab').click(function () {
    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        url: 'get_status',
        success: function (data) {
            if (data != false) {
                $('#email-notice_input').prop('checked', data[0]);
                $('#email-dispatch_input').prop('checked', data[1]);
            } else {
                document.getElementById('alert-danger_notice').innerHTML = data
                $("#alert-danger_notice").show('slow');
                setTimeout(function () {
                    $("#alert-danger_notice").hide('slow');
                }, 5000);
            }

        },
        error: function (data) {
            document.getElementById('alert-danger_notice').innerHTML = 'Ошибка, попробуйте позже'
            $("#alert-danger_notice").show('slow');
            setTimeout(function () {
                $("#alert-danger_notice").hide('slow');
            }, 5000);
        }
    })
});

$('#email-notice_input').click(function () {
    let status
    if ($(this).is(':checked')) {
        status = true
    } else {
        status = false
    }
    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        data: {
            status: status
        },
        url: 'get_notice_status',
        success: function (data) {
            document.getElementById('alert-success_notice').innerHTML = data
            $("#alert-success_notice").show('slow');
            setTimeout(function () {
                $("#alert-success_notice").hide('slow');
            }, 5000);
        },
        error: function (data) {
            document.getElementById('alert-danger_notice').innerHTML = data
            $("#alert-danger_notice").show('slow');
            setTimeout(function () {
                $("#alert-danger_notice").hide('slow');
            }, 5000);
        }
    })
});

$('#email-dispatch_input').click(function () {
    let status;
    if ($(this).is(':checked')) {
        status = true
    } else {
        status = false
    }
    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        data: {
            status: status
        },
        url: 'get_new_order',
        success: function (data) {
            document.getElementById('alert-success_notice').innerHTML = data
            $("#alert-success_notice").show('slow');
            setTimeout(function () {
                $("#alert-success_notice").hide('slow');
            }, 5000);
        },
        error: function (data) {
            document.getElementById('alert-danger_notice').innerHTML = data
            $("#alert-danger_notice").show('slow');
            setTimeout(function () {
                $("#alert-danger_notice").hide('slow');
            }, 5000);
        }
    })
});

let index_cat = 0;
$('#profile_list_categories').on('click', 'input', function (event) {
    let id = this.id
    let status;
    if ($(this).is(':checked')) {
        status = true
    } else {
        status = false
    }
    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        data: {
            id: id,
            status: status
        },
        url: 'profile_set_subcategories',
        success: function (data) {
            $('#' + id).prop('checked', status);
            add_alert_suc(index_cat);
            index_cat = index_cat + 1;
        },
        error: function (data) {
            $('#' + id).prop('checked', !status);
            add_alert_error(index_cat);
            index_cat = index_cat + 1;
        }
    })
});
let index_city = 0;
$('#profile_list_cities').on('click', 'input', function (event) {
    let id = this.id
    let status;
    if ($(this).is(':checked')) {
        status = true
    } else {
        status = false
    }

    $.ajax({
        type: "GET",
        dataType: "json",
        async: false,
        data: {
            id: id,
            status: status
        },
        url: 'profile_set_cities',
        success: function (data) {
            $('#' + id).prop('checked', status);
            add_alert_suc(index_city);
            index_city = index_city + 1;
        },
        error: function (data) {
            $('#' + id).prop('checked', !status);
            add_alert_error(index_city);
            index_city = index_city + 1;
        }
    })
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
    $('#all_ads_filter_select').change(function () {
        var value = $('#all_ads_filter_select option:selected').val();
        if (value == 0)
            window.location.href = '/profile/advert/';
        else
            window.location.href = '/profile/advert/' + value;
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
        if (check == false)
            $("#alert-check").show('slow');
        setTimeout(function () {
            $("#alert-check").hide('slow');
        }, 5000);
        if (name != "" && surname != "" && email != "" && tel != "" && pass1 != "" && pass2 != "" && check == true) {
            if (pass1 == pass2) {
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
                        if (data.data == 'ok') {
                            $("#alert-success").show('slow');
                            setTimeout(function () {
                                $("#alert-success").hide('slow');
                            }, 5000);
                        }
                        if (data.data == 'error') {
                            $("#alert-error").show('slow');
                            setTimeout(function () {
                                $("#alert-error").hide('slow');
                            }, 5000);
                        }
                        if (data.data == 'email') {
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
            } else {
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

$(".btn-all").click(function () {
    $('.btn-delivery').removeClass('active');
    $('.btn-all').toggleClass('active');
});
$(".btn-delivery").click(function () {
    $('.btn-all').removeClass('active');
    $('.btn-delivery').toggleClass('active');
});
$(".btn-add-folder").click(function () {
    $('.add-folder_input').removeClass('d-none');
    $('.add-folder_input').addClass('d-flex');
});
$(".settings-blk").ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
});
$(".choose_blk").ready(function () {
    $('.panel-heading').click(function () {
        $(this).toggleClass('in').next().slideToggle();
        $('.panel-heading').not(this).removeClass('in').next().slideUp();
    });
});
$(".days").ready(function () {
    $('li>span').click(function () {
        $(this).toggleClass('active');
    });
});
$(".choose-type_radio").click(function () {
    $('.date-select').removeClass('d-none');
    $('.date-select').addClass('d-block');
});
$(".any-time_radio").click(function () {
    $('.date-select').removeClass('d-block');
    $('.date-select').addClass('d-none');
});
// $("#about_me_edit").click(function () {
//     var btn=document.getElementById('about_ok');
//     btn.classList.remove('d-none');
//     var pen=document.getElementById('about_me_edit');
//     pen.classList.add('d-none');
//     var birtday=document.getElementById('birthday');
//     birtday.removeAttribute('readonly');
//     var gender=document.getElementById('gender');
//     gender.removeAttribute('readonly');
//     var about=document.getElementById('about');
//     about.removeAttribute('readonly');
// });
// $("#phone_edit").click(function () {
//     var btn=document.getElementById('phone_ok');
//     btn.classList.remove('d-none');
//     var pen=document.getElementById('phone_edit');
//     pen.classList.add('d-none');
//     var phone=document.getElementById('phone');
//     phone.removeAttribute('readonly');
// });
$("#photo_edit").click(function () {
    var lbl = document.getElementById('file_label_edit');
    lbl.classList.add('d-none');
    var form = document.getElementById('file_ok');
    form.classList.remove('d-none');

});
$("#profile_edit").click(function () {
    var lbl = document.getElementById('profile_edit');
    lbl.classList.add('d-none');
    var birtday_l = document.getElementById('birthday-label');
    birtday_l.classList.add('d-none');
    var birtday = document.getElementById('birthday-input');
    birtday.classList.remove('d-none');
    birtday.classList.add('d-inline-block');
    var gender_l = document.getElementById('gender-label');
    gender_l.classList.add('d-none');
    var gender = document.getElementById('gender-input');
    gender.classList.remove('d-none');
    gender.classList.add('d-inline-block');
    var about_l = document.getElementById('about-label');
    about_l.classList.add('d-none');
    var about = document.getElementById('about-input');
    about.classList.remove('d-none');
    about.classList.add('d-inline-block');
    var phone_l = document.getElementById('phone-label');
    phone_l.classList.add('d-none');
    var phone = document.getElementById('phone-input');
    phone.classList.remove('d-none');
    phone.classList.add('d-inline-block');
    // var info_block=document.getElementById('info-inf-blk');
    // info_block.classList.remove('d-none');
    $('.collapse').collapse('show');
});
$("#cancel_info_btn").click(function () {
    var lbl = document.getElementById('profile_edit');
    lbl.classList.remove('d-none');
    // var form=document.getElementById('file_ok');
    // form.classList.add('d-none');
    var birtday_l = document.getElementById('birthday-label');
    birtday_l.classList.remove('d-none');
    var birtday = document.getElementById('birthday-input');
    birtday.classList.add('d-none');
    birtday.classList.remove('d-inline-block');
    var gender_l = document.getElementById('gender-label');
    gender_l.classList.remove('d-none');
    var gender = document.getElementById('gender-input');
    gender.classList.add('d-none');
    gender.classList.remove('d-inline-block');
    var about_l = document.getElementById('about-label');
    about_l.classList.remove('d-none');
    var about = document.getElementById('about-input');
    about.classList.add('d-none');
    about.classList.remove('d-inline-block');
    var phone_l = document.getElementById('phone-label');
    phone_l.classList.remove('d-none');
    var phone = document.getElementById('phone-input');
    phone.classList.add('d-none');
    phone.classList.remove('d-inline-block');
    // var info_block=document.getElementById('info-inf-blk');
    // info_block.classList.add('d-none');
    $('.collapse').collapse('hide');
});
$("#save_info_btn").click(function () {
    var date = $("#birthday-input").val();
    var gender = $('#gender-input option:selected').val();
    var about = $("#about-input").val();
    var phone = $("#phone-input").val();
    if (date != "" && gender != "" && about != "" && phone != "") {
        $("#save_profile").click();
    } else {
        $("#alert-danger").show('slow');
        setTimeout(function () {
            $("#alert-danger").hide('slow');
        }, 5000);
    }


    // $.ajax({
    //     type: "POST",
    //     cache: false,
    //     contentType: false,
    //     processData: false,
    //     url: 'profile/save/',
    //     data:formData,
    //     success: function (data) {
    //         alert('ok');
    //         },
    //     error: function (data) {
    //         alert('er');
    //     }
    // })
});

// $ ( ' input [name = "date"] ' ). daterangepicker ();

$(function () {
    $('#date').daterangepicker({
        singleDatePicker: true,
    });
});

$("#task_category").change(function () {
    var cat = $('#task_category option:selected').val();
    if (cat != 0) {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: '/profile/task/subcategory_find/',
            data: {
                id: cat
            },
            success: function (data) {
                outputSubcategory(data);
            },
            error: function (data) {
                alert('Error');
            }
        })
    } else {
        $('#modelAvto').attr('disabled', true);
    }
});

function outputSubcategory(data) {
    $('#task_subcategory').removeAttr('disabled');
    var select = document.getElementById('task_subcategory');
    while (select.length != 0) {
        select.remove(0);
    }
    // var option = document.createElement("option");
    //    option.value = 0;
    //    option.text = '-Выберите модель-';
    //    select.appendChild(option);
    for (var i = 0; i < data.data.length; i = i + 2) {
        var option = document.createElement("option");
        option.value = data.data[i];
        option.text = data.data[i + 1];
        select.appendChild(option);
    }
}

$("#customer").click(function () {

    $.ajax({
        type: "GET",
        dataType: "json",
        url: '/profile/customer/',
        success: function (data) {
            location.reload(true)
        },
        error: function (data) {
            alert('Error');
        }
    })
});
$("#executor").click(function () {

    $.ajax({
        type: "GET",
        dataType: "json",
        url: '/profile/executor/',
        success: function (data) {
            location.reload(true)
        },
        error: function (data) {
            alert('Error');
        }
    })
});

function add_alert_suc(index) {
    var el = document.getElementById('alerts-block');
    var row = document.createElement('div');
    row.setAttribute('class', 'row justify-content-center');
    var al = document.createElement('div');
    al.setAttribute('class', 'alert alert-success suc-city');
    al.setAttribute('role', 'alert');
    al.setAttribute('id', 'alert_success' + index);
    al.setAttribute('style', 'display: none;');
    al.textContent = 'Сохранено!';
    row.insertAdjacentHTML('beforeend', al.outerHTML);
    el.insertAdjacentHTML('beforeend', row.outerHTML);
    $("#alert_success" + index).show('slow');
    setTimeout(function () {
        $("#alert_success" + index).hide('slow');
    }, 5000);
}

function add_alert_error(index) {
    var el = document.getElementById('alerts-block');
    var row = document.createElement('div');
    row.setAttribute('class', 'row justify-content-center');
    var al = document.createElement('div');
    al.setAttribute('class', 'alert alert-danger error-city');
    al.setAttribute('role', 'alert');
    al.setAttribute('id', 'alert' + index);
    al.setAttribute('style', 'display: none;');
    al.textContent = 'Что-то пошлоне так, попробуйте позже!';
    row.insertAdjacentHTML('beforeend', al.outerHTML);
    el.insertAdjacentHTML('beforeend', row.outerHTML);
    $("#alert" + index).show('slow');
    setTimeout(function () {
        $("#alert" + index).hide('slow');
    }, 5000);
}

$(document).ready(function () {

    $('input[type="file"]#files').change(function () {
        if ($(this).val() != '') {
            if ($(this)[0].files.length == 1) {
                $('.js-fileName').text($(this).val());
            } else {
                $('.js-fileName').text('Выбрано файлов: ' + $(this)[0].files.length);
            }
        } else {
            $('.js-fileName').text('Выберите файлы');
        }
    });

    $('input[type="file"]#file_main').change(function () {
        if ($(this).val() != '') {
            if ($(this)[0].files.length == 1) {
                $('.js-fileNameMain').text($(this).val());
            } else {
                $('.js-fileNameMain').text('Выбрано файлов: ' + $(this)[0].files.length);
            }
        } else {
            $('.js-fileNameMain').text('Выберите файлы');
        }
    });

});

$(document).ready(function () {
    $("#liDropdown").hover(() => {
            if ($("#liDropdown").hasClass("show")) {
                $("#liDropdown").removeClass("show")
                $("#divDropdown-menu").removeClass("show")
                document.getElementById("navbarDropdown").setAttribute("aria-expanded", "false")

            } else {
                if ($("#liDropdown").hasClass("active")) {
                    document.getElementById("liDropdown").setAttribute("class", "nav-item dropdown show active")
                } else {
                    document.getElementById("liDropdown").setAttribute("class", "nav-item dropdown show")
                }
                document.getElementById("navbarDropdown").setAttribute("aria-expanded", "true")
                document.getElementById("divDropdown-menu").setAttribute("class", "dropdown-menu show")
            }

        }
    )
});
$("#portfolio_edit").click(function () {
    var el = document.getElementsByClassName('trash_portfolio');
    for (i = 0; i < el.length; i++) {
        el[i].classList.remove('d-none');
    }
    $("#portfolio_del_block").removeClass('d-none');
});
$("#cencel_portfolio_del_btn").click(function () {
    var el = document.getElementsByClassName('trash_portfolio');
    for (i = 0; i < el.length; i++) {
        el[i].classList.add('d-none');
    }
    $("#portfolio_del_block").addClass('d-none');
});
$(".trash_portfolio").click(function () {
    // var el=$(this);
    if (this.classList.contains('far')) {
        this.classList.remove(('far'));
        this.classList.add('fas');
    } else {
        this.classList.remove(('fas'));
        this.classList.add('far');
    }
});
$("#portfolio_del_btn").click(function () {
    $('#myModal').modal('show')
    var list = ""
    var el = document.getElementsByClassName('trash_portfolio');
    var form = document.getElementById('delete_portfolio_icon');
    for (i = 0; i < el.length; i++) {
        if (el[i].classList.contains('fas')) {
            // list=list+
            var id = el[i].previousElementSibling;
            list = list + id.value + ",";
        }
    }
    var inp = document.createElement('input');
    inp.setAttribute('type', 'hidden');
    inp.setAttribute('name', "delete_id");
    inp.setAttribute('value', list);
    // form.insertAdjacentHTML('beforeend',inp.outerHTML);
    form.insertAdjacentHTML('beforeend', inp.outerHTML);

});
$(".trash_advert_photo").click(function () {
    // var el=$(this);
    if (this.classList.contains('far')) {
        this.classList.remove(('far'));
        this.classList.add('fas');
    } else {
        this.classList.remove(('fas'));
        this.classList.add('far');
    }
});
$('#check_edit_advert').click(function () {
    var list = ""
    var el = document.getElementsByClassName('trash_advert_photo');
    for (i = 0; i < el.length; i++) {
        if (el[i].classList.contains('fas')) {
            // list=list+
            var id = el[i].previousElementSibling;
            list = list + id.value + ",";
        }
    }
    var inp =document.getElementById('del_list');
    inp.setAttribute('value',list);

    var title=$('#title').val();
    if(title==""){
        $('#title').addClass('br-red');
    }
    else{
        $('#save_edit_advert').click();
    }
});

$("#task_category").click(function () {
    $('#task_category').removeClass('br-red');
});
$("#task_subcategory").click(function () {
    $('#task_subcategory').removeClass('br-red');
});
$("#input_text").click(function () {
    $('#input_text').removeClass('br-red');
});
$("#description").click(function () {
    $('#description').removeClass('br-red');
});
$("#input_addr").click(function () {
    $('#input_addr').removeClass('br-red');
});
$("#input_price").click(function () {
    $('#input_price').removeClass('br-red');
});
$('#btn_task_check').click(function () {
     var categ = $("#task_category option:selected").val();
     var subcateg=$("#task_subcategory option:selected").val();
     var title=$("#input_text").val();
     var description=$("#description").val();
     var address=$("#input_addr").val();
     var price=$("#input_price").val();

    if (categ == 0) $('#task_category').addClass('br-red');
    if (subcateg == 0) $('#task_subcategory').addClass('br-red');
    if (title == "") $('#input_text').addClass('br-red');
    if (description == "") $('#description').addClass('br-red');
    if (address == "") $('#input_addr').addClass('br-red');
    if (price == "") $('#input_price').addClass('br-red');
    if(categ != 0 && subcateg != 0 && title != "" && description != "" && address != "" && price != ""){
        $('#btn_task_submit').click();
    }
    else
    {
        $("#alert-danger").show('slow');
            setTimeout(function () {
                $("#alert-danger").hide('slow');
            }, 5000);
    }
});
