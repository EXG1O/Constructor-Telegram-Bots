import React, { HTMLAttributes, ReactElement } from 'react';
import classNames from 'classnames';

import './Section.scss';

import { Section as _Section } from 'services/api/instruction/types';

export interface SectionProps extends Omit<HTMLAttributes<HTMLDivElement>, 'children'> {
	section: _Section;
}

function Section({ section, ...props }: SectionProps): ReactElement<SectionProps> {
	return (
		<div {...props} className={classNames('instruction-section', props.className)}>
			<h3 className='mb-1'>{section.title}</h3>
			<div dangerouslySetInnerHTML={{ __html: section.text }} />
		</div>
	);
}

export default Section;