


  switch (page) {
    case "game":
      contentDiv.innerHTML = `<h2 data-translate="title_game">Games</h2> 
           <div class="container-fluid content-center text-center ">
              <div class="row">            
                <div class="col-img col-sm-6 col-md-6 col-lg-3 py-2 px-0 mx-0"><a href="#" onclick="changeContent('1vs1')"><img src= "../static/img/1vs1.png" class="choose-img" atl="1 versus 1"></a></div>
                <div class="col-img col-sm-6 col-md-6 col-lg-3 py-2 px-0 mx-0"><a href="#" onclick="changeContent('tournament')"><img src="../static/img/tournament.png" class="choose-img" atl="tournament"></a></div>
                <div class="col-img col-sm-6 col-md-6 col-lg-3 py-2 px-0 mx-0"><a href="#" onclick="changeContent('multiplayers')"><img src="../static/img/multi.png" class="choose-img" atl="multiplayers"></a> </div>
                <div class="col-img col-sm-6 col-md-6 col-lg-3 py-2 px-0 mx-0"><a href="#" onclick="changeContent('settings')"><img src="../static/img/settings.png" class="choose-img" atl="settings"></a> </div> 
             </div>
           </div>    
            `;
      break;
    case "settings":
      contentDiv.innerHTML = `<h2 data-translate="title_settings">Settings</h2> 
            <div class="container-fluid content-center text-center ">
              <div class="row">            
                
                </div>
            </div>    
              `;
      break;
    case "login":
      inner_div.innerHTML = `
        <nav class="navbar navbar-expand-lg bg-warning navbar-light">
        <div class="container-fluid">
          <a class="navbar-brand" href="#" onclick="changeContent('login')">PONG</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="#" onclick="changeContent('home')"data-translate="home">Home</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#" onclick="changeContent('chat')" data-translate="chat">Chat</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#" onclick="changeContent('game')" data-translate="games">Game</a>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false" data-translate= "user">
                  User
                </a>
                <ul class="dropdown-menu bg-warning-subtle">
                  <li><a class="dropdown-item" href="#" onclick="changeContent('profile')" data-translate="profile">Profile</a></li>
                  <li><a class="dropdown-item" href="#" onclick="changeContent('friends')" data-translate="friends">Friends</a></li>
                  <li><hr class="dropdown-divider"></li>
                  <li><a class="dropdown-item" href="#" onclick="changeContent('settings')"data-translate="settings">Settings</a></li>
                </ul>
              </li>
            </ul>
            <div class="langs">
              <a href="#" class="btn btn-primary active" onclick="toggleLanguage('en')" language="english">EN</a>
              <a href="#" class="btn btn-primary" onclick="toggleLanguage('fr')" language="french">FR</a>
              <a href="#" class="btn btn-primary" onclick="toggleLanguage('es')" language="spanish">ES</a>
            </div>
          </div>
        </div>
      </nav>
        `;
      /***************************************************************************************************** */

      contentDiv.innerHTML = `
        <h2 data-translate="login">Login</h2> 
      
          {% block content %}
          <h1> TEST </h1>
             <div class="form">
                <form methode="post" enctype="multipart/form-data" action="{% url 'add_user' %}" >
                   {%  csrf_token %}
                  {{ form.as_p }}
               </form>
               <button type="submit">Send</button>
             </div>
          {% endblock %}
 
         `;
      // waitPage();
      break;
    /***************************************************************************************************** */

    case "home":
      contentDiv.innerHTML = `  <h2 data-translate="welcome"> </h2>
            <div class="container-fluid  text-center ">
              <div class="row">     
                <div class="col-img col-sm-6 col-md-6 col-lg-4 py-2 px-0 mx-0">
                  <div class="row"> 
                    <h3 data-translate="games"> Games </h3>
                    <a href="#" onclick="changeContent('game')" ><img src= "../static/img/game.png" class="choose-img" atl="games"></a>
                  </div>
                </div> 
                <div class="col-img col-sm-6 col-md-6 col-lg-4 py-2 px-0 mx-0">
                  <div class="row"> 
                    <h3 data-translate="profile"> Profile </h3>
                    <a href="#" onclick="changeContent('user')"><img src="../static/img/profil.png" class="choose-img" atl="profil"></a>
                  </div>
                </div>
                <div class="col-img col-sm-6 col-md-6 col-lg-4 py-2 px-0 mx-0">
                  <div class="row"> 
                     <h3 data-translate="logout"> Logout </h3>
                     <a href="#" onclick="changeContent('logout')"><img src="../static/img/logout.png" class="choose-img" atl="logout"></a> </div>
                  </div>
                </div>
            </div>    
          </div>
                `;
      break;
    case "1vs1":
      contentDiv.innerHTML = `<h2>1 vs 1 </h2> 
           <div class="container-fluid text-center ">
              <div class="row" >    
                <div class="col" onload="draw();">     
                 <canvas id="window_game"> test</canvas>
                 </div>
              </div>
           </div>
                    `;
      break;
    case "multiplayers":
      contentDiv.innerHTML = `<h2 data-translate="multiplayers">Multiplayers</h2> 
        <div id="content_element" class="main-page">  
           <div class="container-fluid text-center ">
              <div class="row" >    
                <div class="col" onload="draw();">     
                 <canvas id="window_game"> test</canvas>
                 </div>
              </div>
           </div>
        </div>
                        `;
      break;
    case "tournament":
      contentDiv.innerHTML = `<h2 data-translate="tournament">Tournament</h2> 
           <div class="container-fluid text-center ">
              <div class="row" >    
                <div class="col" onload="draw();">     
                 <canvas id="window_game"> test</canvas>
                 </div>
              </div>
           </div>
            `;
      break;
    case "profile":
      contentDiv.innerHTML = `<h2 data-translate="profile">Profil</h2> 
             <div class="container-fluid content-center text-center ">
               <div class="row">            
                <p> profil(pseudo, photo +changement photo possible, date enregistrement, score + graphique,+ ?)</p>
                <a href="#"> <img src="https://placeholderimage.eu/api/50/50" class="choose-img"></a>
                </div>
             </div>    
        `;
      break;
    case "friends":
      contentDiv.innerHTML = `<h2 data-translate="friends">Friends</h2>  
          <div class="container-fluid content-center text-center ">
            <div class="row">            
              <p> friends list (acces profile, ajout, retirer, blacklist</p>
            </div>
          </div>    
        `;
      break;

    case "chat":
      contentDiv.innerHTML = `<h2 data-translate="chat"> Chat</h2> 
          <div class="container-fluid content-center text-center ">
              <div class="row">            
                <p> chat</p>
                </div>
          </div>    
          `;
      break;
    case "logout":
      contentDiv.innerHTML = `<h2 data-translate="logout">logout</h2> 
          <div class="container-fluid content-center text-center ">
              <div class="row">            
                    logout
              </div>
          </div>    
            `;
      break;

    default:
      contentDiv.innerHTML = "<h2>Page not found!</h2>";
  }
  updateContent();

function draw() {
  var canvas = document.getElementById("window_game");
  if (canvas.getContext) {
    var ctx = canvas.getContext("2d");
  }
}

// https://stackoverflow.com/questions/3547035/getting-html-form-values
