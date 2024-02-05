import React, { ReactElement, ReactNode, useState } from 'react';

import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';

import Loading from 'components/Loading';
import TelegramQuillEditor from 'components/TelegramQuillEditor';

export interface Data {
	name: string;
	value: string;
	description: string;
}

export interface VariableModalProps {
	show: boolean;
	loading?: boolean;
	initialData?: Data;
	title: ReactNode;
	children?: (data: Data) => ReactNode;
	onHide: () => void;
}

const defaultData: Data = {
	name: '',
	value: '',
	description: '',
}

function VariableModal({ loading, initialData, title, children, ...props }: VariableModalProps): ReactElement<VariableModalProps> {
	const [data, setData] = useState<Data>(initialData ?? defaultData);

	return (
		<Modal
			{...props}
			onExited={() => setData(defaultData)}
		>
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
						<TelegramQuillEditor
							height={220}
							value={data.value}
							placeholder={gettext('Введите значение переменной')}
							onChange={value => setData({ ...data, value })}
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

export default VariableModal;