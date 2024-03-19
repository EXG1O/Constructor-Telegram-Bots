import React, { ReactElement, Children, cloneElement } from 'react';

import BaseModal, { ModalProps as BaseModalProps } from 'react-bootstrap/Modal';

import Loading from './Loading';

export interface ModalProps extends BaseModalProps {
	loading?: boolean;
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
					return cloneElement(child, { closeButton: !loading });
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