import React, { ReactElement, useEffect, useState } from 'react';

import Toast from 'react-bootstrap/Toast';
import CloseButton from 'react-bootstrap/CloseButton';

export interface MessageToastProps {
	message: string;
	level: keyof typeof icons;
	onExited: () => void;
}

const icons = {
	success: 'check-circle-fill',
	primary: 'info-circle-fill',
	danger: 'exclamation-triangle-fill',
}

function MessageToast({ message, level, onExited }: MessageToastProps): ReactElement<MessageToastProps> {
	const [show, setShow] = useState<boolean>(false);

	useEffect(() => setShow(true), []);

	return (
		<Toast
			className={`text-bg-${level} mb-0`}
			show={show}
			autohide
			delay={6000}
			onExited={onExited}
			onClose={() => setShow(false)}
		>
			<Toast.Body className='d-flex align-items-center gap-2'>
				<i className={`bi bi-${icons[level]}`} />
				<strong className='text-break flex-fill'>{message}</strong>
				<CloseButton onClick={() => setShow(false)} />
			</Toast.Body>
		</Toast>
	);
}

export default MessageToast;