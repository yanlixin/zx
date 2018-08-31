//定义提示框的构造函数
var SweetModal = function (ele, opt) {

    this.$element = ele,
    this.defaults = {
        'title': '提示',
        'text': '',
        'parms': null,
        'confirmButtonColor': '#DD6B55',
        'confirmButtonText': '确定',
        'cancelButtonText': '取消',
        'closeOnConfirm': false,
        'closeOnCancel': false,
        'showCancelButton': true,
        'type': 'warning',//['error', 'warning', 'info', 'success', 'input', 'prompt']
        'clickobj':null,
        'fnConfirmCallback': null,

    },

    this.options = $.extend({}, this.defaults, opt)
}

//实现Alert
ZTAlert = function (options) {
    //创建Beautifier的实体

    var alert = new SweetModal(this, options);
    swal({
        title: alert.options.title,
        text: alert.options.text,
        type: alert.options.type,
    })
}

ZTConfirm = function (options) {
    var confirm = new SweetModal(this, options);
    var s = swal({
        title: confirm.options.title,
        text: confirm.options.text,
        type: confirm.options.type,
        showCancelButton: confirm.options.showCancelButton,
        confirmButtonColor: confirm.options.confirmButtonColor,
        confirmButtonText: confirm.options.confirmButtonText,
        cancelButtonText: confirm.options.cancelButtonText,
        closeOnConfirm: confirm.options.closeOnConfirm,
    }, function (isConfirm) {
        if (isConfirm) {
            confirm.options.fnConfirmCallback(confirm.options.parms);
        }
    });
}


ZTWizardConfirm = function (options) {
    var confirm = new SweetModal(this, options);
    var s = swal({
        title: confirm.options.title,
        text: confirm.options.text,
        type: confirm.options.type,
        showCancelButton: confirm.options.showCancelButton,
        confirmButtonColor: confirm.options.confirmButtonColor,
        confirmButtonText: confirm.options.confirmButtonText,
        cancelButtonText: confirm.options.cancelButtonText,
        closeOnConfirm: confirm.options.closeOnConfirm,
    }, function (isConfirm) {
        if (isConfirm) {
            $(".sweet-alert .cancel").click();
            confirm.options.fnConfirmCallback(confirm.options.parms);
        }
    });
}