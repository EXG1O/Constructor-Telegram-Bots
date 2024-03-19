import React, { ReactElement, Children, cloneElement } from 'react';

import { BaseModalProps } from '@restart/ui/Modal';
import BaseModal from 'react-bootstrap/Modal';

import Loading from './Loading';

export interface ModalProps extends Omit<
	BaseModalProps,
	'role' |
	'renderBackdrop' |
	'renderDialog' |
	'transition' |
	'backdropTransition' |
	'children'
> {
	loading?: boolean;
    size?: 'sm' | 'lg' | 'xl';
    fullscreen?: true | string | 'sm-down' | 'md-down' | 'lg-down' | 'xl-down' | 'xxl-down';
    bsPrefix?: string;
    centered?: boolean;
    backdropClassName?: string;
    animation?: boolean;
    dialogClassName?: string;
    contentClassName?: string;
    dialogAs?: React.ElementType;
    scrollable?: boolean;
	children?: ReactElement;
}

/** The wrapper component adds support for the `loading` prop to the Modal component from `react-bootstrap`. */
function Modal({ loading, backdrop, keyboard, children, ...props }: ModalProps): ReactElement<ModalProps> {
	return (
		<BaseModal
			{...props}
			backdrop={loading ? 'static' : backdrop}
			keyboard={loading ? false : keyboard}
		>
			{children && Children.map(children, child => {
				if (child.type === BaseModal.Header) {
					return cloneElement(child, { closeButton: loading ? false : child.props.closeButton });
				} else if (!loading) {
					return child;
				}
			})}
			{loading && (
				<BaseModal.Body className='d-flex justify-content-center'>
					<Loading size='md' />
				</BaseModal.Body>
			)}
		</BaseModal>
	);
}

export default Object.assign(Modal, BaseModal);