function getAngle(A, B)
{
	let dx = B.x - A.x;
	let dy = B.y - A.y;
	let angle = Math.atan2(dy, dx); // Angle radians
	return angle;
}

// angleToVec2(pAngle)
// {
// 	this.x = Math.cos(pAngle);
// 	this.y = Math.sin(pAngle);
// }

// pBall.v.angleToVec2(getAngle(pPad, pos));

function checkCollide(pPad, pBall)
{
	let pos = new Vec2(pBall.pos.x, pBall.pos.y);
	let speed = new Vec2(pBall.v.x / pBall.speed, pBall.v.y / pBall.speed);

	if (pos.x - pBall.radius > pPad.x + pPad.width/2
		&& pos.x - pBall.radius + pBall.v.x > pPad.x + pPad.width/2
		|| pos.x + pBall.radius < pPad.x - pPad.width/2
		&& pos.x + pBall.radius + pBall.v.x < pPad.x - pPad.width/2)
		return 1;


	for( let i = 0; i < pBall.speed; i++)
	{
		pos.add(speed);

		if (pos.x - pBall.radius < 5 || pos.x + pBall.radius > canvas.width - 5)
			break;

		if (pos.y - pBall.radius <= (pPad.y + pPad.height/2)
			&& pos.y + pBall.radius >= (pPad.y - pPad.height/2))
		{
			if (Math.abs(pPad.x - pos.x) > pPad.width/2)
				continue;

			// Multiplier par coefficient de grandeur (grand, petit pad)
			pBall.v.angleToVec2(getAngle(pPad, pos));
			pBall.pos = pos;

			if (this.UpSpeed)
				this.speed += 0.2;

			if (pBall.last != pBall.beforeLast && pBall.last != pPad.id)
				pBall.beforeLast = pBall.last;
			pBall.last = pPad.id;

			return 0;
		}
	}
	return 1;
}

function checkCollides(pPads, pBall)
{
	if (checkCollide(pPads[0], pBall) && checkCollide(pPads[1], pBall))
		// && (typeGame == TypeGame.solo || typeGame == TypeGame.duo
		// 	|| (checkCollide(pPads[2], pBall) && checkCollide(pPads[3], pBall))))
		return 1;
	return 0;
}

function checkItem(pItem, pBall)
{
	let pos = new Vec2(pBall.pos.x, pBall.pos.y);
	let speed = new Vec2(pBall.v.x / pBall.speed, pBall.v.y / pBall.speed);

	for( let s = 0; s < pBall.speed; s++)
	{
		pos.add(speed);

		for (let i = 0; pItem[i]; i++)
		{
			let item = pItem[i];

			if (!item.visible)
				continue;
			if (pBall.pos.x - pBall.radius >= item.x
				&& pBall.pos.x + pBall.radius <= item.x + item.size
				&& pBall.pos.y - pBall.radius >= item.y
				&& pBall.pos.y + pBall.radius <= item.y + item.size)
			{
				item.visible = false;
				if (!pBall.last)
					continue;
				item.enabled = true;
				item.cible = pBall.last;
			}
		}
	}
}
