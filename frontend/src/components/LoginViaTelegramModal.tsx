import React, { ReactElement, memo } from 'react';

import { QRCodeCanvas } from 'qrcode.react';
import Modal, { ModalProps } from 'react-bootstrap/Modal';

type LoginViaTelegramModalProps = Omit<ModalProps, 'children'>;

function LoginViaTelegramModal(props: LoginViaTelegramModalProps): ReactElement<LoginViaTelegramModalProps> {
	return (
		<Modal {...props}>
			<Modal.Header closeButton className='border-bottom-0' />
			<Modal.Body className='text-center pt-0 pb-4'>
				<div className='d-flex justify-content-center mb-3'>
					<div className='border border-3 rounded-3 p-3'>
						<QRCodeCanvas value='' size={256} />
					</div>
				</div>
				<h3 className='fw-semibold mb-1'>{gettext('Telegram не открылся?')}</h3>
				<p className='mb-1'>{gettext('Отсканируйте QR-код с устройства на котором установлен Telegram.')}</p>
				<a href='https://t.me/?start=login' target='_blank'>{gettext('Перейти по ссылке')}</a>
			</Modal.Body>
		</Modal>
	);
}

export default memo(LoginViaTelegramModal);