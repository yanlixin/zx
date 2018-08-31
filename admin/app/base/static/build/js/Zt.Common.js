
function getSubWinBody(fromid) {
    return $("[data-form-id='" + fromid + "']").parents(".ztModal-body").eq(0);
}

function ModuleStringToJson(str) {
    return JSON.parse(str.replace(/&quot;/g, '"'));
}

// 绑定CheckBox 事件
// obj : 范围对象
//controlid 全选框的id
function bindCheckbox(obj, controlid) {
    if (controlid == null || controlid == "") {
        controlid = "ck_select";
    }

    obj.on('change', "input[type='checkbox']", this, function () {
        var s = $(this)[0].checked;

        if (this.id == controlid) {
            $("input[type='checkbox']", obj).not("#" + controlid).each(function (index, item) {
                $(this)[0].checked = s;
            });
        } else {
            if ($("input[type='checkbox']", obj).not("[id=" + controlid + "]").not("input:checked").length == 0) {
                $("#" + controlid, obj)[0].checked = true;
            }
            else {
                $("#" + controlid, obj)[0].checked = false;
            }
        }
    });
}

//数字格式化
//s要格式化的字符, n保留小数点位数
function fmoney(s, n) {
    n = n > 0 && n <= 20 ? n : 2;
    s = parseFloat((s + "").replace(/[^\d\.-]/g, "")).toFixed(n) + "";
    var l = s.split(".")[0].split("").reverse(),
    r = s.split(".")[1];
    t = "";
    for (i = 0; i < l.length; i++) {
        t += l[i] + ((i + 1) % 3 == 0 && (i + 1) != l.length ? "," : "");
    }
    return t.split("").reverse().join("") + "." + r;
}

//Html标签转换
function HTMLEncodeFull(strVal) {
    if (strVal != undefined && strVal != "") {
        //strVal = ReplaceAll(strVal, "&", "&amp;");
        strVal = ReplaceAll(strVal, ">", "&gt;");
        strVal = ReplaceAll(strVal, "<", "&lt;");
        strVal = ReplaceAll(strVal, "\"", "&quot;");
        strVal = ReplaceAll(strVal, "\r", "");
    }
    return strVal;
}

//文本全部替换
function ReplaceAll(str, sptr, sptr1) {
    while (str.indexOf(sptr) >= 0) {
        str = str.replace(sptr, sptr1);
    }
    return str;
}

//json日期格式转换为正常格式
function jsonDateFormat(jsonDate, formart) {
    try {//出自http://www.cnblogs.com/ahjesus 尊重作者辛苦劳动成果,转载请注明出处,谢谢!

        var date;
        if (jsonDate.indexOf("Date") >= 0) {
            date = new Date(parseInt(jsonDate.replace("/Date(", "").replace(")/", ""), 10));
        }
        else {
            try {
                date = new Date(jsonDate);
            } catch (ex) {
                console.log(ex);
            }
            if (date == undefined) {

                if (window.navigator.userAgent.indexOf("Chrome") > -1) {
                    date = new Date(jsonDate.replace("T", " "));
                } else {
                    date = new Date(jsonDate);
                }
            }
        }

        var month = date.getMonth() + 1 < 10 ? "0" + (date.getMonth() + 1) : date.getMonth() + 1;
        var day = date.getDate() < 10 ? "0" + date.getDate() : date.getDate();
        var hours = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
        var minutes = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
        var seconds = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();
        var milliseconds = date.getMilliseconds();

        if (formart == "yyyy/MM/dd") {
            return date.getFullYear() + "/" + month + "/" + day;
        } else if (formart == "yyyy/MM/dd HH:mm:ss") {
            return date.getFullYear() + "/" + month + "/" + day + " " + hours + ":" + minutes + ":" + seconds;
        } else if (formart == "yyyy年MM月dd日") {
            return date.getFullYear() + "年" + month + "月" + day + "日";
        } else if (formart == "HH:mm") {
            return hours + ":" + minutes;
        }

        var rtnValue = date.getFullYear() + "/" + month + "/" + day + " " + hours + ":" + minutes + ":" + seconds + "." + milliseconds;
        return rtnValue.indexOf("T") != -1 ? rtnValue.replace("T", " ") : rtnValue;

    } catch (ex) {//出自http://www.cnblogs.com/ahjesus 尊重作者辛苦劳动成果,转载请注明出处,谢谢!
        return "";
    }
}

//发送异步请求，将结果输出到<div id="result"></div>中
//最后一个参数可以是"html"也可以是"text"
function gopage(query, obj) {
    console.log(obj);
    $(".nav").find("li").removeClass("active");
    $(".nav").find("i").css("color","");
    if (obj != null) {
        $(obj).children("i").css("color", "#1ab394");
        $(obj).parents("li").each(function (index, item) {
            $(this).addClass("active");
        })
    } else {
        $(".nav").find("ul").removeClass("in");
    }
    //清除datetime-picker在body留下的下拉框
    $(".datetimepicker.datetimepicker-dropdown-bottom-right.dropdown-menu").remove();

    $.post(query, function (data) {
        $("#MainPageContainer").children().remove();
        $("#MainPageContainer").html(data);
    }, "text"
    );
    //屏蔽超级链接跳转
    return false;
}

//跳转到一个已存在的菜单
function goMenuPage(url) {
    //页面跳转，添加充值信息后 立即跳转到批量充值列表
    url = url.toLocaleLowerCase();
    $("#side-menu").find("a").each(function (index, item) {
        if ($(item).attr("onclick") != undefined && $(item).attr("onclick").toLocaleLowerCase().indexOf(url) > -1) {
            $(item).click();
            return;
        }
    });
}

/**
* json对象转字符串形式
* @o {Object} Josn对象
* @returns {string} string
*/
function json2str(o) {
    var arr = [];
    var fmt = function (s) {
        if (typeof s == 'object' && s != null) return json2str(s);
        return /^(string|number)$/.test(typeof s) ? "'" + s + "'" : s;
    }
    for (var i in o) arr.push("'" + i + "':" + fmt(o[i]));
    return '{' + arr.join(',') + '}';
}


$.ajaxSetup({

    complete: function (request, status) {

        if (typeof (request) != 'undefined') {

            var responseText = request.getResponseHeader("X-Responded-JSON");

            if (responseText != null) {

                window.tipError('系统提示', '登录超时，请重新登录', null, null, function () {

                    window.location.href = window.location.href;

                });

            }

        }

    },

    error: function (jqXHR, textStatus, errorThrown) {

        var status = 0;

        switch (jqXHR.status) {

            case (500):

                //TODO 服务器系统内部错误

                status = 500;

                break;

            case (401):
                //TODO 未登录
                window.location.href = '~/';
                break;

            case (403):

                //TODO 无权限执行此操作

                status = 403;

                break;

            case (408):

                //TODO 请求超时

                status = 408;

                break;

            case (0):

                //TODO cancel

                break;
            default:

                status = 1;

                //TODO 未知错误

        }

        if (status > 0) {

        }

    }

});

$.extend($.fn.dataTable.defaults, {

    //"iDisplayLength": 15,
    //"aLengthMenu": [[15, 20, 25, 50, 100], [15, 20, 25, 50, 100]],
    //"sServerMethod": "POST",
    //"bServerSide": true,
    //"bFilter": false,
    //"bInfo": true,
    //"bProcessing": false,
    //"sDom": "<'top'f>rt<'row'<'col-sm-4'li><'col-sm-8'p>>",
    //"oLanguage": {
    //    "sLengthMenu": "每页 _MENU_ 条",
    //    "sZeroRecords": "没有数据",
    //    "sSearch": "查找",
    //    "oPaginate": {
    //        "sFirst": "首页",
    //        "sPrevious": "前一页",
    //        "sNext": "后一页",
    //        "sLast": "尾页"
    //    },
    //},

    "iDisplayLength": 20,
    "aLengthMenu": [[15, 20, 25, 50, 100], [15, 20, 25, 50, 100]],
    "sServerMethod": "POST",
    "bServerSide": true,
    "bFilter": false,
    info: true,
    "bProcessing": true,
    dom: "<'top'f>tr<'row'<'col-sm-4'li><'col-sm-8'p>>",
    language: {
        lengthMenu: "每页 _MENU_ 条",
        processing: "数据加载中。。。",
        info: ", 共 _TOTAL_ 条 ",
        infoEmpty: "",
        zeroRecords: "没有数据",
        emptyTable: "没有数据",
        loadingRecords: "",
        search: "查找",
        paginate: {
            first: "首页",
            previous: "前一页",
            next: "后一页",
            last: "尾页"
        },
    },
});
