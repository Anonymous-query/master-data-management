(function (define) {
  "use strict";

  define(["jquery", "js/user_authn/login_validation"], function (
    $,
    LoginValidation
  ) {
    let LoginView = {
      nextUrl: '/dashboard',

      username: $("#signin-username"),
      password: $("#signin-password"),

      authComplete: function (model) {
        model.redirect(model.nextUrl);
      },

      saveError: function(error) {
        let errorCode = 'We couldn\'t sign you in.';
        let msg;
        if (error.status === 0) {
          msg = 'An error has occurred. Check your Internet connection and try again.';
        } else if (error.status === 500) {
          msg = 'An error has occurred. Try refreshing the page, or check your Internet connection.'; // eslint-disable-line max-len
        } else if (error.responseJSON !== undefined && error.responseJSON.error_code === 'inactive-user') {
          msg = 'In order to sign in, you need to activate your account.';
        } else if (error.responseJSON !== undefined) {
          msg = error.responseJSON.value;
          errorCode = error.responseJSON.error_code;
        } else {
          msg = 'An unexpected error has occurred.';
        }
        LoginValidation.renderErrors(errorCode, msg);
      },

      login: function (data, model) {
        let headers = {'X-CSRFToken': Cookies.get('csrftoken')};

        $.ajax({
          url: "/api/user/account/login_session/", // Update with your login endpoint
          method: "POST",
          data: data,
          headers: headers,
          success: function (response) {
            model.authComplete(model);
          },
          error: function (error) {
            model.saveError(error);
          },
        });
      },

      redirect: function (url) {
        window.location.replace(url);
      },

      getFormData: function () {
        return {
          username: this.username.val(),
          password: this.password.val(),
        };
      },

      submitForm: function (event) {
        event.preventDefault();

        let data = this.getFormData();
        let isValid = LoginValidation.liveValidate(event);
        if (isValid) {
          let model = this
          this.login(data, model);
        }
      },

      init: function() {
        // Bind form submit event
        $('#login-action').on('click', this.submitForm.bind(this));
        LoginValidation.clearErrorOnFocus()
      }
    };
    // Initialize the LoginView
    return LoginView;
  });
}).call(this, define || RequireJS.define);
