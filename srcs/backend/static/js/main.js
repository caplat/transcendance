let cur_url = "";
history.pushState({ key: "value" }, "", document.URL);

window.onpopstate = function (event) {
  if (event.state != "null") {
    console.log("doc : " + document.location.pathname);
    loadPage(document.location.pathname);
  }
};

function loadPage(url) {
  console.log("fetch:" + url);
  fetch(url)
    .then((url) => url)
    .then((x) => x.text())
    .then((y) => {
      document.getElementById("content_element").innerHTML = y;
    });

  cur_url = url;
  // console.log("fetch cur url:" + url);
}

function addHistory(url) {
  // text = url.includes("/user/delete_profile/");
  // console.log("text: " + text);
  if (
    url.includes("/user/delete_profile/") == true ||
    url.includes("/user/logout/") == true
  ) {
    url = "/";
  }
  history.pushState({}, "", url);
  window.addEventListener("popstate", (event) => {
    console.log(
      `location: ${document.location}, state: ${JSON.stringify(event.state)}`
    );
  });
  checkGameUrl();
}

document.addEventListener("submit", function (event) {
  if (
    event.target &&
    (event.target.id === "user/login/" ||
      event.target.id === "user/register/" ||
      event.target.id === "user/updateProfile/" ||
      event.target.id === "user/pass/" ||
      event.target.id === "matchmaking/tournament/create/" ||
     (event.target.id.startsWith("matchmaking/tournament/") &&
     event.target.id.endsWith("/") &&
     Number(
       event.target.id.split("/")[2] >= 1 &&
         Number(event.target.id.split("/")[2]) <= 20
     )) ||
      event.target.id === "games/list/")
  ) {
    console.log("redirrrrrr*****s")
    event.preventDefault();
    let formData = new FormData(event.target);

    let url = event.target.id;
    if (event.target.id == "games/list/") url += event.target.className + "/";
    console.log("URL : ", url);

    fetch("/" + url, {
      method: "POST",
      body: formData,
      headers: { "X-Requested-With": "XMLHttpRequest" },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) document.getElementById("error").innerText = data.error;
        else if (data.redirect) {
          // console.log("submit");
          // console.log("submit:" + data.url);

          loadPage(data.url);
          addHistory(data.url);
          document.getElementById("error").innerText = "";
        }
      });
  }
});

document.addEventListener("click", function (event) {
  if (!event.target) return;

  if (event.target.id != " ") {
    targetID = "/" + event.target.id + "/";
  } else {
    console.log("test**");
    targetID = "/";
  }

  if (event.target.tagName === "A") {
    event.preventDefault();

    if (targetID) {
      console.log("A");
      // console.log(" id " + event.target.id);
      // loadPage("/" + event.target.id);
      // addHistory("/" + event.target.id);
      loadPage(targetID);
      addHistory(targetID);
    }
  } else if (event.target.tagName === "IMG") {
    // console.log("IMG");
    event.preventDefault();
    if (targetID) {
      console.log("IMG");
      // console.log("*****" + targetID);
      // loadPage("/" + event.target.id);
      // addHistory("/" + event.target.id);
      loadPage(targetID);
      addHistory(targetID);
    }
  }
});

function checkGameUrl() {
  const currentUrl = window.location.pathname; // Récupère uniquement le chemin sans le domaine
  console.log("CUR : ", currentUrl);
  const game1vs1Match = currentUrl.match(/^\/games\/1vs1\/\d+\/?$/);
  const game2vs2Match = currentUrl.match(/^\/games\/2vs2\/\d+\/?$/);
  // console.log("MATCH 1 : ", game1vs1Match);
  // console.log("MATCH 2 : ", game2vs2Match);

  if (game1vs1Match || game2vs2Match) {
    setTimeout(() => {
      startPongGame();
    }, 1000);
  }
}

window.addEventListener("popstate", function () {
  checkGameUrl();
});

document.addEventListener("DOMContentLoaded", function () {
  console.log("CONTENT");
  checkGameUrl();
});
