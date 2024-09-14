(function(define) {
    'use strict';

    define([
        'jquery',
        'js/user_authn/login'
    ],
    function($, login) {
        return function() {
            let $logisElement = $('#login-container');
            login.init({el: $logisElement});
        };
    }
    );
}).call(this, define || RequireJS.define);