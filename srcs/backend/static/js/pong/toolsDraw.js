function drawLine(pCtx, pStart, pEnd, pLine, pSpace)
{
	pCtx.beginPath();
	pCtx.setLineDash([pLine, pSpace]);	// [trait, espace]
	pCtx.moveTo(pStart.x, pStart.y);	// Debut
	pCtx.lineTo(pEnd.x, pEnd.y);		// Fin
	pCtx.stroke();
}

function drawText(pCtx, pFont, pText, pX, pY, pTextAlign)
{
	pCtx.font = pFont;
	if (pTextAlign)
		pCtx.textAlign = pTextAlign;
	pCtx.fillText(pText, pX, pY);
}
