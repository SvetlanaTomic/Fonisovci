$.ajaxSetup({cache: false});

function FonisovciViewModel() {
    var self = this;
    self.fonisovciURI = 'http://localhost:5000/fonis/api';
    self.username = "lana";
    self.password = "python";
    self.fonisovci = ko.observableArray();
    self.sum = ko.observable();
    self.qu = [{ id: 0, name: 'all' }, { id: 5, name: 'last 5' }, { id: 10 , name: 'last 10' }, { id: 50, name: 'last 50' }];
    self.queries=ko.observableArray(self.qu);
    self.selectedQueryNum = ko.observable();
    self.period=ko.observableArray(['all', 'today', 'this month']);
    self.selectedQueryPeriod=ko.observable('all');

    self.active=false;
    self.sjow=true;
    self.ajax = function (uri, method, data) {
        var request = {
            url: uri,
            type: method,
            processData: false,
            contentType: "application/json",
            accepts: "application/json",
            cache: false,
            dataType: "json",
            data: JSON.stringify(data),
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization",
                    "Basic " + btoa(self.username + ":" + self.password));
            },


            success: function(jqXHR){
                self.show=true;
            },


            error: function (jqXHR) {
                console.log("ajax error " + jqXHR.status);
            }

        }


        return $.ajax(request);
    }
    self.updateFonisovac = function (fonisovac, newFonisovac) {
        var i = self.fonisovci.indexOf(fonisovac);
        self.fonisovci()[i].uri(fonisovac.uri);
        self.fonisovci()[i].name(newFonisovac.name);
        self.fonisovci()[i].surname(newFonisovac.surname);
        self.fonisovci()[i].userID(newFonisovac.userID);
        self.fonisovci()[i].birthday(newFonisovac.birthday);


    }
    self.beginAdd = function () {
        $('#add').modal('show');
    }
    self.add = function (fonisovac) {
        self.ajax(self.fonisovciURI, 'POST', fonisovac).then(function () {
            self.get_everything();
        })

    }
    self.beginEdit = function (fonisovac) {
        editFonisovacViewModel.setFonisovac(fonisovac);
        $('#edit').modal('show');
    }
    self.edit = function (fonisovac, data) {
        if(self.active) {
            self.show=false;
            self.ajax().abort();
            console.log('I am killing process!')
        }
        self.ajax(fonisovac.uri(), 'PUT', data).then(function () {
            self.get_everything();
        })
    }
    self.remove = function (fonisovac) {
        if(self.active) {
            self.show=false;
            self.ajax().abort();

            console.log('I am killing process!')
        }
        self.ajax(fonisovac.uri(), 'DELETE').then(function () {
            self.get_everything();
        })
    }

    self.get_everything = function () {
        if(self.active) {
            self.show=false;
            self.newGet.abort();
            console.log('I am killing process!')
        }
        self.fonisovci.destroyAll();

        self.extension='/?d='+ self.selectedQueryPeriod();
        self.active=true;
        self.newGet=self.ajax(self.fonisovciURI + self.extension, 'GET').done(function (data) {
            if(self.show) {

                for (var i = 0; i < data.fonisovci.length; i++) {
                    self.fonisovci.push({
                        uri: ko.observable(data.fonisovci[i].uri),
                        name: ko.observable(data.fonisovci[i].name),
                        surname: ko.observable(data.fonisovci[i].surname),
                        birthday: ko.observable(data.fonisovci[i].birthday),
                        userID: ko.observable(data.fonisovci[i].userID),

                    });
                    self.active = false;
                }
            }
        })
    }
    /*
    self.ajax(self.fonisovciURI, 'GET').done(function (data) {
        for (var i = 0; i < data.fonisovci.length; i++) {
            self.fonisovci.push({
                uri: ko.observable(data.fonisovci[i].uri),
                name: ko.observable(data.fonisovci[i].name),
                surname: ko.observable(data.fonisovci[i].surname),
                birthday: ko.observable(data.fonisovci[i].birthday),
                value: ko.observable(data.fonisovci[i].value),
                userID: ko.observable(data.fonisovci[i].userID),

            });
        }
        self.sum(data.sum);
    });
    */
    self.getNewQuery= function () {
        self.get_everything();
        /*
        if(self.active) {
            self.xhr().abort();
            console.log('I am killing process!')
            return;
        }
        self.fonisovci.destroyAll();
        self.extension='/?n='+self.selectedQueryNum()+ '&d='+ self.selectedQueryPeriod();
        self.ajax(self.fonisovciURI+self.extension, 'GET').done(function (data) {
        for (var i = 0; i < data.fonisovci.length; i++) {
            self.fonisovci.push({
                uri: ko.observable(data.fonisovci[i].uri),
                name: ko.observable(data.fonisovci[i].name),
                surname: ko.observable(data.fonisovci[i].surname),
                birthday: ko.observable(data.fonisovci[i].birthday),
                value: ko.observable(data.fonisovci[i].value),
                userID: ko.observable(data.fonisovci[i].userID),

            });
        }
        self.sum(data.sum);
    });
    */

    }

/*
    self.setQuery = function () {
        if(self.availableQueries=="all")
            self.number=ko.applyBindings(0);
        else if (self.availableQueries=="this week")
            self.number=ko.applyBindings(7);
         else if (self.availableQueries=="this month")
            self.number=ko.applyBindings(30);
          else (self.availableQueries=="this year")
            self.number=ko.applyBindings(365);

    }
    */
}


function AddFonisovacViewModel() {
    var self = this;
    self.name = ko.observable();
    self.surname = ko.observable();
    self.birthday = ko.observable();
    self.value = ko.observable();
    self.userID = ko.observable();

    self.addFonisovac = function () {
        $('#add').modal('hide');
        self.exp={
            name: self.name(),
            surname: self.surname(),
            birthday: self.birthday(),
            value: self.value(),
            userID: self.userID()
        }
        if(self.exp['name']==undefined ||self.exp['surname']==undefined ||self.exp['birthday']==undefined  ){
            alert("Entered data ware not correct. Please fill all necessary fields correctly")
            //return;
        }

        fonisovciViewModel.add(self.exp);
        self.name("");
        self.surname("");
        self.birthday("2019-02-06");
        self.userID("");

    }
}

function EditFonisovacViewModel() {
    var self = this;
    self.name = ko.observable();
    self.surname = ko.observable();
    self.birthday = ko.observable();
    self.userID = ko.observable();

    self.setFonisovac = function (fonisovac) {
        self.fonisovac = fonisovac;

        self.name(fonisovac.name());
        self.surname(fonisovac.surname());
        console.log(fonisovac.birthday().toString());
        self.birthday(fonisovac.birthday().toString());
        self.userID(fonisovac.userID());
        $('edit').modal('show');
    }

    self.editFonisovac = function () {
        $('#edit').modal('hide');
        fonisovciViewModel.edit(self.fonisovac, {
            name: self.name(),
            surname: self.surname(),
            birthday: self.birthday(),
            userID: self.userID()
        });
    }


}

var fonisovciViewModel = new FonisovciViewModel();
var addFonisovacViewModel = new AddFonisovacViewModel();
var editFonisovacViewModel = new EditFonisovacViewModel();
ko.applyBindings(fonisovciViewModel, $('#main')[0]);
ko.applyBindings(addFonisovacViewModel, $('#add')[0]);
ko.applyBindings(editFonisovacViewModel, $('#edit')[0]);

