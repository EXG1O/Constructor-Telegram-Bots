import './main.css';

document.querySelectorAll<HTMLButtonElement>('.btn-update').forEach(updateButtonElement => {
	updateButtonElement.addEventListener('click', (): void => {
		if (updateButtonElement.getAttribute('aria-updating') === 'false') {
			updateButtonElement.setAttribute('aria-updating', 'true');
			setTimeout((): void => updateButtonElement.setAttribute('aria-updating', 'false'), 900);
		}
	})
});