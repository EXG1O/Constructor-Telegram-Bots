import * as bootstrap from 'bootstrap';

const toastContainer = document.querySelector('#toastContainer') as HTMLDivElement;
const toastIcons = {
	success: 'check-circle-fill',
	primary: 'info-circle-fill',
	danger: 'exclamation-triangle-fill',
}

export class Toast {
	public div: HTMLDivElement;
	public bootstrap: bootstrap.Toast;

	public constructor(
		message: string,
		level: 'success' | 'primary' | 'danger',
		timeout: number = 6000,
	) {
		this.div = document.createElement('div');
		this.div.className = `toast text-bg-${level} mb-0 fade`;
		this.div.role = 'alert';
		this.div.setAttribute('aria-live', 'assertive');
		this.div.setAttribute('aria-atomic', 'true');
		this.div.setAttribute('data-bs-autohide', (timeout !== 0).toString());
		this.div.setAttribute('data-bs-delay', timeout.toString());
		this.div.innerHTML = `
			<div class="toast-body d-flex align-items-center gap-2">
				<i class="bi bi-${toastIcons[level]}"></i>
				<strong class="text-break flex-fill">${message}</strong>
				<button class="btn-close" type="button" data-bs-dismiss="toast"></button>
			</div>
		`;
		toastContainer.appendChild(this.div);

		this.bootstrap = new bootstrap.Toast(this.div);
	}
	show = () => this.bootstrap.show();
	hide = () => this.bootstrap.hide();
}