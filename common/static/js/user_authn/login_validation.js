(function ($) { 
    'use strict';

    define(['jquery'],
        function($){
        let LoginValidation = {
            username: $('#signin-username'),
            password: $('#signin-password'),

            constraints : {
                username: {
                    presence: { allowEmpty: false, message: "is required" },
                    length: { minimum: 3, message: "must be at least 3 characters" }
                },
                password: {
                    presence: { allowEmpty: false, message: "is required" },
                    length: { minimum: 6, message: "must be at least 6 characters" }
                }
            },

            // Function to clear previous error messages
            clearErrorOnFocus: function() {
                document.getElementById('signin-username').addEventListener('focus', function() {
                    document.getElementById('error-username').innerText = '';
                    document.getElementById('form-error').classList.add('d-none'); // Hide form error
                });
                document.getElementById('signin-password').addEventListener('focus', function() {
                    document.getElementById('error-password').innerText = '';
                    document.getElementById('form-error').classList.add('d-none'); // Hide form error
                });
            },

            renderErrors: function (title, message) {
                let errorContainer = $("#form-error");
                let errorHtml = `<strong>${title}</strong><br>`;
                
                
                errorHtml += `<span>${message}</span>`;
                
                // Show the error message at the top
                errorContainer.html(errorHtml);
                errorContainer.removeClass('d-none'); // Make sure the error div is visible
            },

            liveValidate: function(event) {
                // Perform validations
                let isValid = true;
                const formValues = {
                    username: this.username.val(),
                    password: this.password.val(),
                };

                // Validate form values
                const errors = validate(formValues, this.constraints);

                // Clear previous errors
                document.getElementById('error-username').innerText = '';
                document.getElementById('error-password').innerText = '';
                document.getElementById('form-error').classList.add('d-none'); // Hide form error
                if (errors) {
                    // Show validation errors
                    if (errors.username) {
                        document.getElementById('error-username').innerText = errors.username[0];
                    }
                    if (errors.password) {
                        document.getElementById('error-password').innerText = errors.password[0];
                    }
                    isValid = false
                }

                return isValid
            }
        };
        return LoginValidation;
    });
})(jQuery);