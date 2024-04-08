import React, { ReactElement, HTMLAttributes } from 'react';
import classNames from 'classnames';

export type BlockProps = HTMLAttributes<HTMLDivElement>;

function Block({ className, ...props }: BlockProps): ReactElement {
	return <div {...props} className={classNames('border rounded', className)} />;
}

export default Block