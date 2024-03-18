import React, { ReactElement, HTMLAttributes } from 'react';
import classNames from 'classnames';

import './Section.scss';

import { Section as _Section } from 'services/api/donations/types';

export interface SectionProps extends HTMLAttributes<HTMLDivElement> {
	section: _Section;
}

function Section({ section, ...props }: SectionProps): ReactElement<SectionProps> {
	return (
		<div {...props} className={classNames('donation-section', props.className)}>
			<h3 className='mb-1'>{section.title}</h3>
			<div dangerouslySetInnerHTML={{ __html: section.text }} />
		</div>
	);
}

export default Section;