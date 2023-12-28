import React, { ReactNode, useEffect, useState } from 'react';
import classNames from 'classnames';

import Card, { CardProps } from 'react-bootstrap/Card';
import ToggleButtonGroup from 'react-bootstrap/ToggleButtonGroup';
import ToggleButton, { ToggleButtonProps } from 'react-bootstrap/ToggleButton';
import RBButton from 'react-bootstrap/Button';

import Button from './Button';

import { DragDropContext, Droppable, Draggable, DropResult } from 'react-beautiful-dnd';

interface KeyboardToggleButtonProps extends Omit<ToggleButtonProps, 'key' | 'id' | 'value' | 'size' | 'variant' | 'onChange'> {
	value: Data['type'];
}

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

export interface MainProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialData?: Data;
	onChange: (data: Data) => void;
}

const keyboardToggleButtons: KeyboardToggleButtonProps[] = [
	{ value: 'default', children: gettext('Обычный') },
	{ value: 'inline', children: gettext('Встроенный') },
	{ value: 'payment', children: gettext('Платёжный') },
];

function Main({ initialData, onChange, ...props }: MainProps): ReactNode {
	const [data, setData] = useState<Data>(initialData ?? { type: 'default', buttons: [] });

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
		<Card {...props} className={classNames('border', props.className)}>
			<Card.Header as='h6' className='border-bottom text-center'>
				{gettext('Клавиатура')}
			</Card.Header>
			<Card.Body className='vstack gap-2 p-2'>
				<ToggleButtonGroup type='radio' name='keyboardTypes' defaultValue='default'>
					{keyboardToggleButtons.map((props, index) => (
						<ToggleButton
							{...props}
							key={index}
							id={`radioKeyboardType${props.value}`}
							size='sm'
							variant='outline-dark'
							onChange={() => setData({ ...data, type: props.value })}
						/>
					))}
				</ToggleButtonGroup>
				<div>
					<DragDropContext onDragEnd={handleButtonDragEnd}>
						<Droppable droppableId='keyboardButtons'>
							{provided => (
								<>
									<div ref={provided.innerRef} {...provided.droppableProps}>
										{data.buttons.map((button, index) => (
											<Draggable
												key={index}
												index={index}
												draggableId={`keyboardButton${index}`}
											>
												{provided => (
													<Button
														data={data}
														index={index}
														button={button}
														provided={provided}
														className='mb-1'
														onChange={handleButtonChange}
														onDelete={handleButtonDelete}
													/>
												)}
											</Draggable>
										))}
									</div>
									{provided.placeholder}
								</>
							)}
						</Droppable>
					</DragDropContext>
					<RBButton
						size='sm'
						variant='dark'
						className='w-100'
						onClick={() => setData({ ...data, buttons: [...data.buttons, { text: '' }] })}
					>
						{gettext('Добавить кнопку')}
					</RBButton>
				</div>
			</Card.Body>
		</Card>
	);
}

export default Main;