class Vec2
{
	constructor(pX = 0, pY = 0)
	{
		this.x = pX;
		this.y = pY;
	}

	add(other)
	{
		this.x += other.x;
		this.y += other.y;
	}

	sub(other)
	{
		this.x -= other.x;
		this.y -= other.y;
	}

	multi(pScale)
	{
		this.x *= pScale;
		this.y *= pScale;
	}

	norme()
	{
		return Math.sqrt(Math.pow(this.x, 2) + Math.pow(this.y, 2));
	}

	normalize()
	{
		let n = this.norme();
		if (!n)
			return;
		this.x /= n;
		this.y /= n;
	}

	angleToVec2(pAngle)
	{
		this.x = Math.cos(pAngle);
		this.y = Math.sin(pAngle);
	}

	log()
	{
		return "[" + this.x + "," + this.y + "]";
	}
}	//	VEC2
