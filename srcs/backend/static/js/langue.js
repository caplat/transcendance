// let currentLang = "en";
// currentLang

const translations = {
  en: {
    mail: "Email adress",
    password: "Password",
    submit: "Submit",
    welcome: "Welcome",
    welcome2: "For try the experience, log in",
    title_game: "Choose your game",
    // title_settings: "Settings",
    games: "Games",
    friends: "Friends",
    chat: "Chat",
    user: "User",
    profile: "Profile",
    home: "Home",
    logout: "Logout",
    txt_first_page: "descriptif",
    enter: "Enter",
    settings: "Settings",
    multiplayers: "Multiplayers",
    tournament: "Tournament",
    register: "Register",
    login: "Log in",
    login42: "Login with 42",
    returnlogin: "Return for login",
    enjoyGames: "Log in to enjoy our games",
    friendsSend: "Friends request sent",
    friendReceive: "Friends request received",
    friendList: "Friends list",
    userList: "Users list",
    updateProfile: "Edit profile",
    update: "Update",
    changePassword: "Change password",
    deleteProfile: "Delete profile",
    add: "Add",
    play: "Play",
    block: "Block",
    unblock: "Unblock",
    remove: "Remove",
    accept: "Accept",
    refuse: "Refuse",
  },
  fr: {
    mail: "Adresse mail",
    password: "Mot de passe",
    welcome: "Bienvenue",
    welcome2: "Pour tenter l'expérience, connectez vous",
    title_game: "Choisissez votre jeu",
    // title_settings: "Paramètres",
    friends: "Liste d'amis",
    submit: "Valider",
    chat: "Messagerie",
    user: "Utilisateur",
    games: "Jeux",
    profile: "Profil",
    home: "Accueil",
    logout: "Se déconnecter",
    txt_first_page: "sur notre page de jeux",
    enter: "Entrer sur le site",
    settings: "Paramtères",
    multiplayers: "Plusieurs joueurs",
    tournament: "Tournois",
    register: "S'enregistrer",
    login: "Se connecter",
    login42: "Se connecter avec 42",
    returnlogin: "Retour à l'accueil",
    enjoyGames: "Connectez vous pour profiter de nos jeux",
    friendsSend: "Demandes d'amis envoyées",
    friendReceive: "Demandes d'amis reçues",
    friendList: "Liste d'amis",
    userList: "Liste des utilisateurs",
    updateProfile: "Modifier profil",
    update: "Mettre à jour",
    changePassword: "changer le mot de passe",
    deleteProfile: "Supprimer le profil",
    add: "Ajouter",
    play: "Jouer",
    block: "Bloquer",
    unblock: "Débloquer",
    remove: "Enlever",
    accept: "Accepter",
    refuse: "Refuser",
  },
  es: {
    mail: "Correo electrónico",
    password: "Contraseña",
    submit: "Entregar",
    welcome: "Bienvenido",
    welcome2: "Para probar la experiencia, inicia sesión",
    title_game: "Elige tu juego",
    // title_settings: "Ajustes",
    games: "Juegos",
    friends: "Amigos",
    chat: "Mensajería",
    user: "Usuario",
    home: "Bienvenida",
    logout: "Desconectar",
    txt_first_page: "En nuestra página de juegos",
    enter: "Ingrese al sitio",
    settings: "PAjustes",
    multiplayers: "Multijugadores",
    tournament: "Torneo",
    register: "Registro",
    login: "Acceso",
    login42: "Conéctate con 42",
    returnlogin: "Volver a iniciar sesión",
    profile: "Perfil",
    enjoyGames: "Inicia sesión para disfrutar de nuestros juegos",
    friendsSend: "Solicitudes de amistad enviadas",
    friendReceive: "Solicitudes de amistad recibidas",
    friendList: "Lista de amigos",
    userList: "Lista de usuarios",
    updateProfile: "Editar perfil",
    update: "Actualizar",
    changePassword: "Cambiar la contraseña",
    deleteProfile: "Eliminar perfil",
    add: "Agregar",
    play: "Jugar",
    block: "Bloquear",
    unblock: "Desatascar",
    remove: "Eliminar",
    accept: "Aceptar",
    refuse: "Rechazar",
  },
};

// const lang_json = "<getLanguage>";
// const result = JSON.parse(lang_json);
// console.log(result);

function toggleLanguage(str) {
  if (str === "en") {
    currentLang = "en";
  }
  if (str === "fr") {
    currentLang = "fr";
  }
  if (str === "es") {
    currentLang = "es";
  }
  console.log("before: " + str);
  updateContent();
  let langs = document.querySelector(".langs"),
    link = document.querySelectorAll(".langs a");

  link.forEach((el) => {
    el.addEventListener("click", () => {
      langs = document.querySelector(".langs");
      langs.querySelector(".active").classList.remove("active");
      el.classList.add("active");
    });
  });
}

function updateContent() {
  document.querySelectorAll("[data-translate]").forEach((element) => {
    const key = element.getAttribute("data-translate");
    // console.log(currentLang);
    element.textContent = translations[currentLang][key];
  });
}
