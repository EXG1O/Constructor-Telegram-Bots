import React, { ReactElement, HTMLAttributes } from 'react';
import classNames from 'classnames';

export type FooterProps = HTMLAttributes<HTMLDivElement>;

function Footer({ className, ...props }: FooterProps): ReactElement<FooterProps> {
	return <div {...props} className={classNames('offcanvas-footer', className)} />;
}

export default Footer;