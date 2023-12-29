import React, { ReactElement, useEffect, useState } from 'react';

import Toast from 'react-bootstrap/Toast';
import CloseButton from 'react-bootstrap/CloseButton';

export interface MessageToastProps {
	message: string;
	level: keyof typeof icons;
	delay?: number;
	onExited: () => void;
}

const icons = {
	success: 'check-circle-fill',
	primary: 'info-circle-fill',
	danger: 'exclamation-triangle-fill',
}

function MessageToast({ message, level, delay = 6000, onExited }: MessageToastProps): ReactElement<MessageToastProps> {
	const [show, setShow] = useState<boolean>(false);

	useEffect(() => setShow(true), []);

	const handleClose = () => setShow(false);

	return (
		<Toast
			className={`text-bg-${level} mb-0`}
			show={show}
			delay={delay}
			autohide={delay !== 0}
			onExited={onExited}
			onClose={handleClose}
		>
			<Toast.Body className='d-flex align-items-center gap-2'>
				<i className={`bi bi-${icons[level]}`} />
				<strong className='text-break flex-fill'>{message}</strong>
				<CloseButton onClick={handleClose} />
			</Toast.Body>
		</Toast>
	);
}

export default MessageToast;