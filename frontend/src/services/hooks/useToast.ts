import { useContext } from 'react';

import ToastContext, { ToastContextProps } from 'services/contexts/ToastContext';

function useToast(): ToastContextProps {
	const toastContext = useContext<ToastContextProps | undefined>(ToastContext);

	if (toastContext === undefined) {
		throw new Error('useToast must be used with a ToastProvider!');
	}

	return toastContext;
}

export default useToast;