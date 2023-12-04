import { Toast as BaseToast } from 'bootstrap';

const containerElement = document.querySelector<HTMLDivElement>('#toastContainer')!;
const icons = {
	success: 'check-circle-fill',
	primary: 'info-circle-fill',
	danger: 'exclamation-triangle-fill',
}

export default class Toast extends BaseToast {
	public element: HTMLDivElement;

	public constructor(message: string, level: keyof typeof icons, delay: number = 6000) {
		const element = document.createElement('div');
		element.className = `toast text-bg-${level} mb-0 fade`;
		element.role = 'alert';
		element.setAttribute('aria-live', 'assertive');
		element.setAttribute('aria-atomic', 'true');
		element.innerHTML = `
			<div class="toast-body d-flex align-items-center gap-2">
				<i class="bi bi-${icons[level]}"></i>
				<strong class="text-break flex-fill">${message}</strong>
				<button class="btn-close" type="button" data-bs-dismiss="toast"></button>
			</div>
		`;
		containerElement.appendChild(element);

		super(element, {autohide: level !== 'danger', delay: delay});

		this.element = element;
		this.element.addEventListener('hidden.bs.toast', () => this.element.remove());
	}
}