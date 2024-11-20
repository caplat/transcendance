class Pad
{
	constructor(pName, pKeyCodeUp, pKeyCodeDown, pLimitUp, pLimitDown)
	{
		this.name = pName;
		this.speed = 1;

		this.limitUp = pLimitUp;
		this.limitDown = pLimitDown;
		
		this.keyUp = false;
		this.keyDown = false;
		this.keyCodeUp = pKeyCodeUp;
		this.keyCodeDown = pKeyCodeDown;
	}

	updateData(pData)
	{
		this.x = pData.x;
		this.y = pData.y;
		this.height = pData.h;
		this.width = pData.w;
		this.vx = pData.vx;
		this.vy = pData.vy;
		this.score = pData.score;
		// console.log('PAD : ', this)
	}

	update(socket)
	{
		let vy = this.vy;

		if (this.keyUp) {
			if (this.y - this.height /2 < this.limitUp + this.vy) {
				vy = this.y - this.height /2 - this.limitUp;
				if (!vy)
					return;
			};
			if (socket.readyState === WebSocket.OPEN) {
				let state = {
					'type': 'game.updatePad',
					'pad': this.name,
					'dir': 'up',
					'vy': vy
				};
				socket.send(JSON.stringify(state));
				// console.log('STATE : ', state);
			};
		};
		
		if (this.keyDown) {
			if (this.y + this.height/2 > this.limitDown - this.vy) {
				vy = this.limitDown - (this.y + this.height /2);
				if (!vy)
					return;
			};
			if (socket.readyState === WebSocket.OPEN) {
				let state = {
					'type': 'game.updatePad',
					'pad': this.name,
					'dir': 'down',
					'vy': vy
				};
				socket.send(JSON.stringify(state));
			};
		};
	}

	draw(pCtx)
	{
		pCtx.fillRect(this.x - this.width/2, this.y - this.height/2,
			this.width, this.height);
	}

	keyPressed(keyCode)
	{
		console.log('KEY : ', keyCode);
		switch(keyCode)
		{
			case this.keyCodeUp:
				this.keyUp = true;
				
				break;
			case this.keyCodeDown:
				this.keyDown = true;

				break;
			case 'KeyP':
				if (debug)
					this.log();
				break;
			default:
				break;
		}
	}

	keyReleased(keyCode)
	{
		switch(keyCode)
		{
			case this.keyCodeUp:
				this.keyUp = false;
				break;
			case this.keyCodeDown:
				this.keyDown = false;
				break;
			default:
				break;
		}
	}
}
