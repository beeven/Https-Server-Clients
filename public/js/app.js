ko.bindingHandlers.radio = {
    init: function (element, valueAccessor) {
        if (!ko.isObservable(valueAccessor())) {
            throw new Error('radio binding should be used only with observable values');
        }

        $(element).on('change', 'input:radio', function (e) {
            // we need to handle change event after bootsrap will handle its event
            // to prevent incorrect changing of radio button styles
            setTimeout(function() {
                var radio = $(e.target),
                    value = valueAccessor(),
                    newValue = radio.val();

                value(newValue);
            }, 0);
        });
    },

    update: function (element, valueAccessor) {
        var $radioButton = $(element).find('input[value="' + ko.unwrap(valueAccessor()) + '"]'),
            $radioButtonWrapper;

        if ($radioButton.length) {
            $radioButtonWrapper = $radioButton.parent();

            $radioButtonWrapper.siblings().removeClass('active');
            $radioButtonWrapper.addClass('active');

            $radioButton.prop('checked', true);
        } else {
            $radioButtonWrapper = $(element).find('.active');
            $radioButtonWrapper.removeClass('active');
            $radioButtonWrapper.find('input').prop('checked', false);
        }
    }
};

(function($){
    function MessageViewModel() {
        var that = this;
        that.url = ko.observable("");
        that.protocol = ko.observable("https");
        that.messageid = ko.observable("");
        that.datecreated = ko.observable("");
        that.entryno = ko.observable("");
        that.eportno = ko.observable("");
        that.noticetime = ko.observable("");
        that.returncode = ko.observable("");
        that.returninfo = ko.observable("");
        that.returntype = ko.observable("");
        that.taskid = ko.observable("");

        that.status = ko.observable("");
        that.msg = ko.observable("");

        that.fillForm = function(){
            that.messageid(("00000" + Math.floor(Math.random()*100000)).substr(-5,5));
            that.datecreated(moment().utc().format());
            that.entryno("515420151545" + ("000000" + Math.floor(Math.random()*1000000)).substr(-6,6));
            that.eportno("000000001023" + ("000000" + Math.floor(Math.random()*1000000)).substr(-6,6));
            that.noticetime(moment().utc().format());
            that.returncode(["025","011","013","017","021"][Math.floor(Math.random()*5)])
            that.returntype(Math.random() > 0.5 ? "TCS" : "QP")
            that.taskid("T1907843510020150514f4ff6" + ("0000" + Math.floor(Math.random()*1000000).toString(16)).substr(-4,4));
            that.returninfo(["直接申报成功","报关单放行","校验失败","任务号[" + that.taskid() +"]检验成功"][Math.floor(Math.random()*4)])
        }

        that.setDateCreated = function(){
            that.datecreated(moment().utc().format())
        }
        that.setNoticeTime = function(){
            that.noticetime(moment().utc().format());
        }

        that.submitForm = function(){
            var data = {
                protocol: that.protocol(),
                url: that.url(),
                messageid: that.messageid(),
                datecreated: that.datecreated(),
                entryno: that.entryno(),
                eportno: that.eportno(),
                noticetime: that.noticetime(),
                returncode: that.returncode(),
                returninfo: that.returninfo(),
                returntype: that.returntype(),
                taskid: that.taskid()
            }
            if(that.url().length < 1) {
                return
            }
            that.msg("Sending request...");
            //that.status(0);
            $.post("/TestMessage",data,function(res){
                //that.status(res.status);
                that.msg(res.msg + "\tServer response: " + res.response);
                console.log(res);
            })
        }
    }

    $(document).ready(function(){
        ko.applyBindings(MessageViewModel())
    })
})(jQuery);