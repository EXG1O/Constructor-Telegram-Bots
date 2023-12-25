import { useContext } from 'react';

import ToastContext, { ToastContextProps } from 'services/contexts/ToastContext';

function useToast(): ToastContextProps {
	const toast = useContext<ToastContextProps | undefined>(ToastContext);

	if (toast === undefined) {
		throw new Error('useToast must be used with a ToastProvider!');
	}

	return toast;
}

export default useToast;