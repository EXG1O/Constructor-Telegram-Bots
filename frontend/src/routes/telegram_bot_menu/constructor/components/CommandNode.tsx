import React, { ReactNode } from 'react';

import { NodeProps, Handle, Position } from 'reactflow';
import Stack from 'react-bootstrap/Stack';
import Button from 'react-bootstrap/Button';
import Image from 'react-bootstrap/Image';

import { NodeData } from './../App';

interface CommandNodeProps extends Omit<NodeProps, 'data'>{
	data: NodeData;
}

function CommandNode({ data }: CommandNodeProps): ReactNode {
	return (
		<Stack gap={2} style={{ width: '300px' }}>
			<div className='d-flex gap-1'>
				<Button
					size='sm'
					variant='danger'
					className='bi bi-trash px-1 py-0'
					style={{ fontSize: '16px' }}
				/>
				<Button
					size='sm'
					variant='secondary'
					className='bi bi-pencil-square px-1 py-0'
					style={{ fontSize: '16px' }}
				/>
			</div>
			<div className='bg-light border rounded text-break text-center px-3 py-2' style={{ position: 'relative' }}>
				<Handle
					id={`${data.id}:top:0`}
					type='target'
					position={Position.Top}
				/>
				{data.name}
			</div>
			{data.image && (
				<Image thumbnail className='p-0' src={data.image} />
			)}
			<div className='bg-light border rounded text-break px-3 py-2'>{data.message_text.text}</div>
			{data.keyboard?.buttons && (
				<Stack gap={1}>
					{data.keyboard.buttons.map(button => (
						<div
							key={button.id}
							className='text-bg-dark rounded text-break text-center px-3 py-2'
							style={{ position: 'relative' }}
						>
							<Handle
								id={`${data.id}:right:${button.id}`}
								type='source'
								position={Position.Right}
							/>
							{button.text}
							<Handle
								id={`${data.id}:left:${button.id}`}
								type='source'
								position={Position.Left}
							/>
						</div>
					))}
				</Stack>
			)}
		</Stack>
	);
}

export default CommandNode;