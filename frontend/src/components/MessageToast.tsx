import React, { ReactElement, memo, useEffect, useState } from 'react';

import Toast from 'react-bootstrap/Toast';
import CloseButton from 'react-bootstrap/CloseButton';

type Levels = 'success' | 'info' | 'error';

export interface MessageToastProps {
	message: string;
	level: Levels;
	onExited: () => void;
}

const colors: Record<Levels, string> = {
	success: 'success',
	info: 'primary',
	error: 'danger',
}
const icons: Record<Levels, string> = {
	success: 'check-circle-fill',
	info: 'info-circle-fill',
	error: 'exclamation-triangle-fill',
}

function MessageToast({ message, level, onExited }: MessageToastProps): ReactElement<MessageToastProps> {
	const [show, setShow] = useState<boolean>(false);

	useEffect(() => setShow(true), []);

	return (
		<Toast
			autohide
			show={show}
			delay={6000}
			className={`text-bg-${colors[level]} mb-0`}
			onExited={onExited}
			onClose={() => setShow(false)}
		>
			<Toast.Body className='d-flex align-items-center gap-2'>
				<i className={`bi bi-${icons[level]}`} />
				<strong className='flex-fill text-break'>{message}</strong>
				<CloseButton onClick={() => setShow(false)} />
			</Toast.Body>
		</Toast>
	);
}

export default memo(MessageToast);