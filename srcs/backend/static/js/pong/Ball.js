class Ball
{
	updateData(pData) {
		this.x = pData.x
		this.y = pData.y
		this.r = pData.r
	}

	draw(pCtx)
	{
		pCtx.save();

		pCtx.beginPath();
		pCtx.arc(this.x, this.y, this.r, 0, 2 * Math.PI);
		pCtx.fillStyle = 'blue'; // Couleur de remplissage
		pCtx.fill(); // Remplir le cercle
		pCtx.strokeStyle = 'black'; // Couleur de bordure
		pCtx.stroke();
		
		pCtx.restore();
	}

	keyPressed(keyCode, socket)
	{
		if (keyCode == 'Space') {
			if (socket.readyState === WebSocket.OPEN) {
				socket.send(JSON.stringify({'type': 'game.play'}));
			};
		};
	
	}
}
