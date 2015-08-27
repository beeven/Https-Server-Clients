(function($){
    function CertInfoViewModel(){
        var that = this;
        that.O = ko.observable("");
        that.OU = ko.observable("");
        that.CN = ko.observable("");
        that.Names = ko.observableArray([]);
        that.Addrs = ko.observableArray([]);
        that.newName = ko.observable("");
        that.newAddr = ko.observable("");

        that.addName = function(){
            that.Names.push({"name":that.newName()});
        }
        that.removeName = function(item){
            that.Names.remove(item);
        }

        that.addAddr = function(){
            that.Addrs.push({"ip": that.newAddr()});
        }
        that.removeAddr = function(item){
            that.Addr.remove(item);
        }

    }

    

    $(document).ready(function(){
        ko.applyBindings(CertInfoViewModel())
    })
})(jQuery);