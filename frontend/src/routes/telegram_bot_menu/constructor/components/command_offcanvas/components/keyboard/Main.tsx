import React, { ReactNode, useEffect, useState } from 'react';

import Card from 'react-bootstrap/Card';
import Stack from 'react-bootstrap/Stack'
import ToggleButtonGroup from 'react-bootstrap/ToggleButtonGroup';
import ToggleButton from 'react-bootstrap/ToggleButton';
import RBButton from 'react-bootstrap/Button';

import Button from './Button';

import { DragDropContext, Droppable, Draggable, DropResult } from 'react-beautiful-dnd';

export interface ButtonData {
	id?: number;
	row?: number;
	text: string;
	url?: string;
}

export interface Data {
	type: 'default' | 'inline' | 'payment';
	buttons: ButtonData[];
}

interface Types {
	value: Data['type'];
	text: string;
}

const types: Types[] = [
	{
		value: 'default',
		text: gettext('Обычный'),
	},
	{
		value: 'inline',
		text: gettext('Встроенный'),
	},
	{
		value: 'payment',
		text: gettext('Платёжный'),
	},
];

export interface MainProps {
	onChange: (data: Data) => void;
}

function Main({ onChange }: MainProps): ReactNode {
	const [data, setData] = useState<Data>({ type: 'default', buttons: [] });

	useEffect(() => onChange(data), [data]);

	function handleButtonChange(index: number, button: ButtonData): void {
		setData({ ...data, buttons: data.buttons.map((button_, index_) => index_ === index ? button : button_) });
	}

	function handleButtonDelete(index: number): void {
		const buttons = [...data.buttons];

		buttons.splice(index, 1);

		setData({ ...data, buttons });
	}

	function handleButtonDragEnd(result: DropResult): void {
		if (result.destination) {
			const buttons = [...data.buttons];

			const [movedButton] = buttons.splice(result.source.index, 1);
			buttons.splice(result.destination.index, 0, movedButton);

			setData({ ...data, buttons });
		}
	}

	return (
		<Card className='border'>
			<Card.Header as='h6' className='border-bottom text-center'>
				{gettext('Клавиатура')}
			</Card.Header>
			<Card.Body className='p-2'>
				<Stack gap={2}>
					<ToggleButtonGroup type='radio' name='keyboardTypes' defaultValue='default'>
						{types.map((type, index) => (
							<ToggleButton
								key={index}
								size='sm'
								variant='outline-dark'
								id={`radioKeyboardType${type.value}`}
								value={type.value}
								onChange={() => setData({ ...data, type: type.value })}
							>
								{type.text}
							</ToggleButton>
						))}
					</ToggleButtonGroup>
					<Stack gap={1}>
						<DragDropContext onDragEnd={handleButtonDragEnd}>
							<Droppable droppableId='keyboardButtons'>
								{provided => (
									<>
										<Stack ref={provided.innerRef} {...provided.droppableProps} gap={1}>
											{data.buttons.map((button, index) => (
												<Draggable
													key={index}
													draggableId={`keyboardButton${index}`}
													index={index}
												>
													{provided => (
														<Button
															data={data}
															index={index}
															button={button}
															provided={provided}
															onChange={handleButtonChange}
															onDelete={handleButtonDelete}
														/>
													)}
												</Draggable>
											))}
										</Stack>
										{provided.placeholder}
									</>
								)}
							</Droppable>
						</DragDropContext>
						<RBButton
							size='sm'
							variant='dark'
							onClick={() => setData({ ...data, buttons: [...data.buttons, { text: '' }] })}
						>
							{gettext('Добавить кнопку')}
						</RBButton>
					</Stack>
				</Stack>
			</Card.Body>
		</Card>
	);
}

export default Main;