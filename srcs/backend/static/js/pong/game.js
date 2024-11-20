function startPongGame() {
	let game;
	let nombrePlayer = 2;
	let debug = false;

	const host = window.location.host;
	const path = window.location.pathname;
	const pageTypeGame = path.split('/')[2];
	const pageId = path.split('/')[3];

	console.log('Host : ', host);
	console.log('Path : ', path);
	console.log('Type Game : ', pageTypeGame);
	console.log('Page id : ', pageId);


	const user_id = getCookie('user_id');
	console.log('User id : ', user_id);


	const socket = new WebSocket(`ws://${host}/ws/games/${pageTypeGame}/${pageTypeGame}/${pageId}/`);

	function connectWebSocket() {
		socket.onopen = function(event) {
			console.log("Connected to WebSocket");
		};

		
		socket.onmessage = function(e) {
			let data = JSON.parse(e.data);
			// console.log('Message recu du serveur : ', data);
			
			if (data.type === 'game.loading') {
				// console.log('Message recu du serveur : ', data);
				console.log('LOADING');

				return
			}
			if (data.type === 'game.ready') {
				console.log('Message recu du serveur : ', data);
				console.log('READY');

				game_data = JSON.parse(data.game)
				game.initUsers(game_data.users['A'], game_data.users['B']);
				return
			}
			// console.log('Message recu du serveur : ', data);

			if (data.type === 'game.update') {
				padA_data = JSON.parse(data.padA);
				padB_data = JSON.parse(data.padB);
				ball_data = JSON.parse(data.ball);
				game_data = JSON.parse(data.game);
				
				// console.log('PAD A : ', padA_data);
				// console.log('PAD B : ', padB_data);
				// console.log('BALL : ', ball_data);
				// console.log('GAME : ', game_data);
				
				game.pads[0].updateData(padA_data)
				game.pads[1].updateData(padB_data)
				if (game_data.type != '1vs1') {
					// console.log('2VS2')
					padC_data = JSON.parse(data.padC);
					padD_data = JSON.parse(data.padD);
					
					game.pads[2].updateData(padC_data)
					game.pads[3].updateData(padD_data)

				}
					
				game.ball.updateData(ball_data)
					
				game.play = game_data.play;

				game.update(socket);
				game.draw();
			}
		};

		socket.onclose = function(event) {
			console.log("WebSocket closed. Reconnecting...");
			setTimeout(function() {
				connectWebSocket();  // Reconnectez après un délai
			}, 1000);
		};

		socket.onerror = function(error) {
			console.error("WebSocket error: ", error);
		};
	}

	function getCookie(name) {
		const value = `;${document.cookie}`;
		console.log('VALUE : ', value);
		const parts = value.split(`${name}=`);
		console.log('PARTS : ', parts);
		if (parts.length === 2) return parts.pop().split(';').shift();
	}

	function init()
	{
		if (debug)
			console.log("Init");
		
		game = new Game(nombrePlayer);

		let pads2 = [
			new Pad('A', 'KeyW', 'KeyS', 0, game.height),
			new Pad('B', 'ArrowUp', 'ArrowDown', 0, game.height)
		];
		let pads4 = [
			new Pad('A', 'KeyW', 'KeyS', 0, game.height),
			new Pad('B', 'ArrowUp', 'ArrowDown', 0, game.height),
			new Pad('C', 'KeyA', 'KeyD', 0, game.height),
			new Pad('D', 'ArrowRight', 'ArrowLeft', 0, game.height)
		];
		let ball = new Ball;

		game.load(pads4, ball)

		document.addEventListener("keydown", keyPressed, false);
		document.addEventListener("keyup", keyReleased, false);
	}

	function keyPressed(t)
	{
		t.preventDefault();
		// if (debug)
		// 	console.log("Key Pressed : " + t.code);
		// console.log("GAME PAD : ", game.pads);

		for (let i=0; i < 2; i++)
		{
			// console.log("USERS[i] : " + game.users[i]);
			// console.log("USER ID : " + user_id);
			if (game.users[i] == user_id)
				game.pads[i].keyPressed(t.code);
		}

		if (!game.play)
			game.ball.keyPressed(t.code, socket);
	}

	function keyReleased(t)
	{
		t.preventDefault();
		// if (debug)
		// 	console.log("Key Released : " + t.code);
		
		for (let i=0; i < 2; i++)
		{
			if (game.users[i] == user_id)
				game.pads[i].keyReleased(t.code);
		}
	}

	init();
	connectWebSocket();
}
