import React, { ReactElement, ReactNode, useState } from 'react';

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
	loading: boolean;
	initialData?: Data;
	title: ReactNode;
	children?: (data: Data) => ReactNode;
}

function BaseVariableModal({ loading, initialData, title, children, ...props }: BaseVariableModalProps): ReactElement<BaseVariableModalProps> {
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
				<>
					<Modal.Body className='vstack gap-2'>
						<Form.Control
							value={data.name}
							placeholder={gettext('Придумайте название переменной')}
							onChange={e => setData({ ...data, name: e.target.value })}
						/>
						<TinymceEditor
							value={data.value}
							init={{ placeholder: gettext('Введите значение переменной') }}
							onEditorChange={value => setData({ ...data, value })}
						/>
						<Form.Control
							value={data.description}
							placeholder={gettext('Введите описание переменной')}
							onChange={e => setData({ ...data, description: e.target.value })}
						/>
					</Modal.Body>
					{children && (
						<Modal.Footer>
							{children(data)}
						</Modal.Footer>
					)}
				</>
			) : (
				<Modal.Body className='d-flex justify-content-center align-items-center'>
					<Loading size='md' />
				</Modal.Body>
			)}
		</Modal>
	);
}

export default BaseVariableModal;