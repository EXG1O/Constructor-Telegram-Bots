import React, { ReactElement, HTMLAttributes } from 'react';
import classNames from 'classnames';

import './Section.scss';

import { PrivacyPolicySection } from 'services/api/privacy_policy/types';

export interface SectionProps extends Omit<HTMLAttributes<HTMLDivElement>, 'children'> {
	section: PrivacyPolicySection;
}

function Section({ section, ...props }: SectionProps): ReactElement<SectionProps> {
	return (
		<div {...props} className={classNames('privacy-policy-section', props.className)}>
			<h3 className='mb-1'>{section.title}</h3>
			<div dangerouslySetInnerHTML={{ __html: section.text }} />
		</div>
	);
}

export default Section;