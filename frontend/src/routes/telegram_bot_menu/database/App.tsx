import React, { ReactNode, useEffect, useState } from 'react';

import Card from 'react-bootstrap/Card';
import Stack from 'react-bootstrap/Stack';
import Button from 'react-bootstrap/Button';
import ListGroup from 'react-bootstrap/ListGroup';

import CreateRecordModal from './components/CreateDatabaseRecordModal';
import DatabaseRecord from './components/DatabaseRecord';

import useTelegramBot from 'services/hooks/useTelegramBot';

import { TelegramBotDatabaseRecordsAPI } from 'services/api/telegram_bots/main';
import { TelegramBotDatabaseRecord } from 'services/api/telegram_bots/types';
import { useNavigate } from 'react-router-dom';

function App(): ReactNode {
	const navigate = useNavigate()
	const { telegramBot } = useTelegramBot()

	const [showCreateRecordModal, setShowCreateRecordModal] = useState<boolean>(false);
	const [databaseRecords, setDatabaseRecords] = useState<TelegramBotDatabaseRecord[]>([]);

	useEffect(() => { updateDatabaseRecords() }, []);

	async function updateDatabaseRecords(): Promise<void> {
		const response = await TelegramBotDatabaseRecordsAPI.get(telegramBot.id);

		if (response.ok) {
			setDatabaseRecords(response.json);
		} else {
			navigate('/personal-cabinet/');
		}
	}

	return (
		<>
			<CreateRecordModal
				show={showCreateRecordModal}
				onCreate={updateDatabaseRecords}
				onHide={() => setShowCreateRecordModal(false)}
			/>
			<Card className='border'>
				<Card.Body className='vstack gap-2'>
					<Button
						variant='dark'
						size='sm'
						onClick={() => setShowCreateRecordModal(true)}
					>
						{gettext('Добавить запись')}
					</Button>
					{/* <Stack>
						
					</Stack> */}
					<ListGroup>
						{databaseRecords.map(databaseRecord => (
							<ListGroup.Item key={databaseRecord._id} className='p-3'>
								<DatabaseRecord databaseRecord={databaseRecord} />
							</ListGroup.Item>
						))}
					</ListGroup>
				</Card.Body>
			</Card>
		</>
	);
}

export default App;