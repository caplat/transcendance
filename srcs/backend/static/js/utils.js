// tentative change rlangue

// async function get_lang() {
//   fetch("/get_lang/", {
//     method: "GET",
//     params: {
//       langue: "langue.js",
//     },
//   })
//     .then((response) => response.blob())
//     .then((blob) => {})
//     .catch((error) => console.log(error));
// }
// ajax({
//   url: "/profile/",
//   dataType: "json",
//   succes: function (data) {
//     $("#block-container").html(data.html);
//   },
// });

console.log("BTN")

if (document.querySelector("#ajax-call"))
{
  
  document.querySelector("#ajax-call").addEventListener("click", event => {
  event.preventDefault();
  console.log("BTN")
  let formData = new FormData();
  formData.append('a', document.querySelector("#a").value);
  formData.append('b', document.querySelector("#b").value);
  console.log("A : ", a, " B : ", b);
  // On récupère la valeur du jeton CSRF
  let csrfTokenValue = document.querySelector('[name=csrfmiddlewaretoken]').value;
  // const request = new Request('{% url "login" %}', {
      const request = new Request('user/login', {
      method: 'POST',
      body: formData,
      headers: {'X-CSRFToken': csrfTokenValue}  // On ajoute le token dans l'en-tête
  });

  // On exécute la requête
  // fetch(url)
  fetch(request)
      .then(response => response.json())
      .then((x) => x.text())
      .then((y) => {
      document.getElementById("content_element").innerHTML = y;
      });
  })

}
// async function loadPage(url) {
//   fetch(url)
//     .then(url => url)
//     .then((x) => x.text())
//     .then((y) => {
//       document.getElementById("content_element").innerHTML = y;
//     });
// }
