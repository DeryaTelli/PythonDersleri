document.addEventListener("DOMContentLoaded", async function () {
  const token = localStorage.getItem("token");

  // Giriş yapan kullanıcı bilgilerini al
  if (token) {
    try {
      const response = await fetch("/api/users/me", {
        headers: {
          Authorization: "Bearer " + token,
        },
      });

      if (!response.ok) throw new Error("Unauthorized");

      const user = await response.json();
      localStorage.setItem("user", JSON.stringify(user));
      document.body.classList.add("logged-in");

      // Avatar baş harflerini ayarla
      const avatarElem = document.querySelector(".avatar");
      if (avatarElem) {
        let initials = "??";
        if (user.username) {
          const nameParts = user.username.trim().split(" ");
          initials =
            nameParts.length >= 2
              ? nameParts[0][0] + nameParts[1][0]
              : nameParts[0][0];
          initials = initials.toUpperCase();
        }
        avatarElem.textContent = initials;
      }

      // Menüleri göster/gizle
      document.querySelectorAll(".logged-in").forEach((el) => (el.style.display = "block"));
      document.querySelectorAll(".logged-out").forEach((el) => (el.style.display = "none"));

    } catch (err) {
      console.warn("Kullanıcı bilgisi alınamadı:", err);
      document.body.classList.remove("logged-in");
    }
  } else {
    // Giriş yapılmamışsa
    document.body.classList.remove("logged-in");
    document.querySelectorAll(".logged-in").forEach((el) => (el.style.display = "none"));
    document.querySelectorAll(".logged-out").forEach((el) => (el.style.display = "block"));
  }

  // Avatar menüsü toggle
  const avatarButton = document.querySelector(".avatar");
  const dropdownMenu = document.querySelector(".dropdown-menu");
  if (avatarButton && dropdownMenu) {
    avatarButton.addEventListener("click", function (e) {
      e.stopPropagation();
     dropdownMenu.parentElement.classList.toggle("open");

    });
    document.addEventListener("click", function () {
      dropdownMenu.classList.remove("open");
    });
    dropdownMenu.querySelectorAll("a").forEach(function (item) {
      item.addEventListener("click", function () {
        dropdownMenu.classList.remove("open");
      });
    });
  }

  // Logout işlemi
  const logoutLink = document.getElementById("logout-link");
  if (logoutLink) {
    logoutLink.addEventListener("click", function (e) {
      e.preventDefault();
      localStorage.clear();
      window.location.href = "/login";
    });
  }

  // Giriş formu
  const loginForm = document.querySelector("form.form");
  if (loginForm && document.getElementById("login-email")) {
    loginForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      const email = document.getElementById("login-email").value.trim();
      const password = document.getElementById("login-password").value;

      try {
        const response = await fetch("/api/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: new URLSearchParams({
            username: email,
            password: password,
          }),
        });

        const data = await response.json();

        if (response.ok) {
          localStorage.setItem("token", data.access_token);
          alert("Giriş başarılı!");
          window.location.href = "/dashboard";
        } else {
          alert(data.detail || "Giriş başarısız!");
        }
      } catch (err) {
        alert("Hata oluştu: " + err.message);
      }
    });
  }

  // Kayıt formu
  const registerForm = document.querySelector("form.form");
  if (registerForm && document.getElementById("reg-email")) {
    registerForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      const username = document.getElementById("reg-name").value.trim();
      const email = document.getElementById("reg-email").value.trim();
      const password = document.getElementById("reg-pass").value;
      const password2 = document.getElementById("reg-pass2").value;

      if (password !== password2) {
        alert("Şifreler eşleşmiyor!");
        return;
      }

      try {
        const response = await fetch("/api/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username,
            email,
            password,
          }),
        });

        const data = await response.json();

        if (response.ok) {
          alert("Kayıt başarılı! Giriş yapabilirsiniz.");
          window.location.href = "/login";
        } else {
          alert(data.detail || "Kayıt başarısız!");
        }
      } catch (err) {
        alert("Hata oluştu: " + err.message);
      }
    });
  }
});
