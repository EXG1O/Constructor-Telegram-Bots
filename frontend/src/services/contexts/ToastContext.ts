import { createContext } from 'react';

import { MessageToastProps } from 'components/MessageToast';

export interface ToastContextProps {
	createMessageToast: (props: Omit<MessageToastProps, 'onExited'>) => void;
}

const ToastContext = createContext<ToastContextProps | undefined>(undefined);

export default ToastContext;