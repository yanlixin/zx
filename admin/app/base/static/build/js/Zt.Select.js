/*
Description: $.fn.ztSelect 
Author: Kevin 
*/
; (function ($, window, document, undefined) {
    "use strict";

    var ztSelect = function (ele, opt) {
        this.defaults = {
            'url': '../../../../dict/dictforselect',
            'para': {},
            'ajaxType': 'post',
            'dict': '',
            'selectedValue': '-1',
            'extItems': [],
            'theme': 'bootstrap',
            'dropdownCssClass': 'customer-select2-container',
            'containerCssClass': 'select2-sm',
            'language': 'zh-CN',
            'width': '100%',
            'allowClear': false,
            'data': [],
            'dropdownAutoWidth': true,
            'placeholder':''
        };
        this.options = $.extend({}, this.defaults, opt)
        this.self = $(ele);
    }
    ztSelect.prototype = {
        Init: function () {
            var options = this.options;
            var self = this.self;
            if (options.data.length > 0) {
                options.data = $.merge(options.extItems, options.data);
            }
            else {
                var parms = { Dict: options.dict, Para: options.para };
                $.ajax({
                    url: options.url,
                    data: parms,
                    dataType: "json",
                    type: options.ajaxType,
                    async: false,
                    cache: false,
                    success: function (result) {
                        if (result.selectedValue != null && options.selectedValue == "") {
                            options.selectedValue = result.selectedValue;
                        }
                        options.data = $.merge(options.extItems, result.items);

                    }
                });
            }
            options.query = function (query) {
                var queryData = { results: [] };
                if (query.term == undefined || query.term == '') {
                    queryData.results = options.data;
                    query.callback(queryData);
                    return;
                }
                var queryTerm = query.term.toLowerCase();
                for (var i = 0 ; i < options.data.length; i++) {
                    if ((options.data[i].id + options.data[i].code + options.data[i].ext + options.data[i].text).toLowerCase().indexOf(queryTerm) != -1) {
                        queryData.results.push(options.data[i]);
                    }
                }
                query.callback(queryData);
            };
            if (self.attr("multiple") != undefined && self.attr("multiple").length > 0) {
                options.selectedValue = options.selectedValue.split(',');
            }
            if (self.attr("placeholder") != undefined) {
                options.placeholder = self.attr("placeholder");
            }
            if (options.selectedValue == "") {
                options.selectedValue = null;
            }
            self.select2(options).select2('val', options.selectedValue);

        },
    };

    $.fn.ztSelect = function (options) {
        var select = new ztSelect(this, options);
        select.Init();
        return select;
    }
})(jQuery, window, document);