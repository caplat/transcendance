class Game
{
	constructor(pNomberPlayer)
	{
		this.nomberPlayer = pNomberPlayer;
        this.canvas = document.getElementById("window_game");
        this.ctx = this.canvas.getContext("2d");
        this.height = this.canvas.height;
        this.width = this.canvas.width;
        this.lastUpdate = 0;
        this.timer = 0;
        this.play = false
        this.users = []
        // console.log(this)
	}
    
    load(pPads, pBall, pUserA, pUserB)
    {
        this.pads = pPads
        this.ball = pBall
    }

    initUsers(pUserA, pUserB)
    {
        this.users[0] = pUserA
        this.users[1] = pUserB

        // console.log('USER A : ', this.users[0]);
        // console.log('USER B : ', this.users[1]);
    }

    update(socket)
    {
        this.pads.forEach((pad) => pad.update(socket));
       
        // this.ball.update(this.pads);
    }

    draw()
    {
	    this.ctx.clearRect(0, 0, this.width, this.height);

		drawLine(this.ctx, new Vec2(this.width/2, 0),
					new Vec2(this.width/2, this.height), 15, 10);

		drawText(this.ctx, "48px serif", this.pads[0].score,
					this.width/2 - 20, 60, "right");
		drawText(this.ctx, "48px serif", this.pads[1].score,
					this.width/2 + 20, 60, "left");

        this.pads.forEach((pad) => pad.draw(this.ctx));

        this.ball.draw(this.ctx);
    }
}
