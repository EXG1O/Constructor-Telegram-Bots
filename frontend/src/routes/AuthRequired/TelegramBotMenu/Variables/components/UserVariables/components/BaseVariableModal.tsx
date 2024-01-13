import React, { ReactElement, ReactNode, useMemo, useCallback, useState } from 'react';

import Modal, { ModalProps } from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';

import Loading from 'components/Loading';
import TinymceEditor from 'components/TinymceEditor';

export interface Data {
	name: string;
	value: string;
	description: string;
}

export interface BaseVariableModalProps extends ModalProps {
	initialData?: Data;
	loading: boolean;
	title: ReactNode;
	children?: (data: Data) => ReactNode;
}

function BaseVariableModal({ initialData, loading, title, children, ...props }: BaseVariableModalProps): ReactElement<BaseVariableModalProps> {
	const [data, setData] = useState<Data>(initialData ?? {
		name: '',
		value: '',
		description: '',
	});

	return (
		<Modal {...props}>
			<Modal.Header closeButton>
				<Modal.Title as='h5'>{title}</Modal.Title>
			</Modal.Header>
				{!loading ? (
					<Modal.Body className='vstack gap-2'>
						<Form.Control
							value={data.name}
							placeholder={gettext('Придумайте название переменной')}
							onChange={e => setData({ ...data, name: e.target.value })}
						/>
						<TinymceEditor
							value={data.value}
							init={useMemo(() => ({ placeholder: gettext('Введите значение переменной') }), [])}
							onEditorChange={useCallback((value: string) => setData({ ...data, value }), [])}
						/>
						<Form.Control
							value={data.description}
							placeholder={gettext('Введите описание переменной')}
							onChange={e => setData({ ...data, description: e.target.value })}
						/>
					</Modal.Body>
				) : (
					<Modal.Body className='d-flex justify-content-center align-items-center'>
						<Loading size='md' />
					</Modal.Body>
				)}
			{!loading ? children?.(data) : undefined}
		</Modal>
	);
}

export default BaseVariableModal;