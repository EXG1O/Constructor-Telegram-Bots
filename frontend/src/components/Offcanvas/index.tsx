import React, { ReactElement, ReactNode, Children, cloneElement } from 'react';

import BaseOffcanvas from 'react-bootstrap/Offcanvas';
import { BaseModalProps } from '@restart/ui/Modal';

import Loading from '../Loading';

import Footer from './components/Footer';

export interface OffcanvasProps extends Omit<
	BaseModalProps,
	'role' |
	'renderBackdrop' |
	'renderDialog' |
	'transition' |
	'backdrop' |
	'backdropTransition' |
	'keyboard' |
	'children'
> {
	loading?: boolean;
	bsPrefix?: string;
    backdropClassName?: string;
    scroll?: boolean;
    placement?: 'start' | 'end' | 'top' | 'bottom';
    responsive?: 'sm' | 'md' | 'lg' | 'xl' | 'xxl';
    renderStaticNode?: boolean;
	children?: ReactNode;
}

/** The wrapper component adds support for the `loading` prop to the Offcanvas component from `react-bootstrap`. */
function Offcanvas({ loading, children, ...props }: OffcanvasProps): ReactElement<OffcanvasProps> {
	return (
		<BaseOffcanvas {...props}>
			{children && Children.map(children as ReactElement, child => {
				if (child.type === BaseOffcanvas.Header) {
					return cloneElement(child, { closeButton: loading ? false : child.props.closeButton });
				} else if (!loading) {
					return child;
				}
			})}
			{loading && (
				<BaseOffcanvas.Body className='d-flex justify-content-center'>
					<Loading size='md' className='align-self-center' />
				</BaseOffcanvas.Body>
			)}
		</BaseOffcanvas>
	);
}

export default Object.assign(Offcanvas, { ...BaseOffcanvas, Footer });