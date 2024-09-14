(function ($) { 
    'use strict';

    define(['jquery'],
        function($){
        let LoginValidation = {
            username: $('#signin-username'),
            password: $('#signin-password'),

            renderErrors: function(title, errorMessages) {
                $('#error-container').html('<h3>' + title + '</h3><ul>' + errorMessages.map(msg => '<li>' + msg + '</li>').join('') + '</ul>');
            },

            liveValidate: function(event) {
                // Perform validations
                let isValid = true;
                let errors = [];

                if (!this.username.val()) {
                    isValid = false;
                    errors.push('Username is required.');
                } else if (this.username.val().length < 3) {
                    isValid = false;
                    errors.push('Username must be at least 3 characters long.');
                }

                if (!this.password.val()) {
                    isValid = false;
                    errors.push('Password is required.');
                } else if (this.password.val().length < 6) {
                    isValid = false;
                    errors.push('Password must be at least 6 characters long.');
                }

                // Render errors if validation fails
                if (!isValid) {
                    this.renderErrors('Validation Errors', errors);
                }

                return isValid
            }
        };
        return LoginValidation;
    });
})(jQuery);