(function (define) {
  "use strict";

  define(["jquery", "js/user_authn/login_validation"], function (
    $,
    LoginValidation
  ) {
    let LoginView = {
      username: $("#signin-username"),
      password: $("#signin-password"),

      loginCompleted: function () {
        this.redirect("/dashboard");
      },

      login: function (data) {
        $.ajax({
          url: "/login", // Update with your login endpoint
          method: "POST",
          data: data,
          success: function (response) {
            this.loginCompleted();
          },
          error: function (xhr) {
            LoginValidation.renderErrors("Login Error", [
              "Invalid username or password",
            ]);
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
          this.login(data);
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
