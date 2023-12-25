import React, { ReactNode, useEffect, useState } from 'react';

import 'reactflow/dist/style.css';
import './App.css';

import ReactFlow, {
	Controls,
	MiniMap,
	Background,
	BackgroundVariant,
	useEdgesState,
	useNodesState,
	NodeTypes,
	Connection,
	addEdge,
	Edge,
	Node,
	Panel,
} from 'reactflow';

import Button from 'react-bootstrap/Button';

import CommandNode from './components/CommandNode';

import useToast from 'services/hooks/useToast';
import useTelegramBot from 'services/hooks/useTelegramBot';

import CommandOffcanvas from './components/command_offcanvas/Main';

import { TelegramBotCommandDiagramAPI, TelegramBotCommandsDiagramAPI } from 'services/api/telegram_bots/main';
import { TelegramBotCommandDiagram } from 'services/api/telegram_bots/types';

export type NodeData = Omit<TelegramBotCommandDiagram, 'x' | 'y'>;

const nodeTypes: NodeTypes = { command: CommandNode };

function App(): ReactNode {
	const { createMessageToast } = useToast();
	const { telegramBot } = useTelegramBot();

	const [nodes, setNodes, onNodesChange] = useNodesState<NodeData>([]);
	const [edges, setEdges, onEdgesChange] = useEdgesState([]);

	const [showCommandOffcanvas, setShowCommandOffcanvas] = useState(false);

	useEffect(() => { update() }, []);

	async function update(): Promise<void> {
		const response = await TelegramBotCommandsDiagramAPI.get(telegramBot.id);

		if (response.ok) {
			setNodes(response.json.map(data => ({
				id: data.id.toString(),
				type: 'command',
				position: { x: data.x, y: data.y },
				data,
			})));

			const edges: Edge[] = [];

			response.json.forEach(command => {
				command.keyboard?.buttons.forEach(button => {
					if (
						button.telegram_bot_command_id !== null &&
						button.start_diagram_connector !== null &&
						button.end_diagram_connector !== null
					) {
						edges.push({
							id: `reactflow__edge-${button.start_diagram_connector}-${button.end_diagram_connector}`,
							source: command.id.toString(),
							sourceHandle: button.start_diagram_connector,
							target: button.telegram_bot_command_id.toString(),
							targetHandle: button.end_diagram_connector,
						});
					}
				});
			});

			setEdges(edges);
		}
	}

	function handleNodeDragStop(nodes: Node[] | undefined): void {
		nodes?.forEach(node => TelegramBotCommandDiagramAPI.updatePosition(telegramBot.id, parseInt(node.id), node.position));
	}

	async function handleConnect(connection: Connection): Promise<void> {
		if (
			connection.source !== null &&
			connection.sourceHandle !== null &&
			connection.target !== null &&
			connection.targetHandle !== null
		) {
			setEdges(edges => addEdge(connection, edges));

			const response = await TelegramBotCommandDiagramAPI.connect(
				telegramBot.id,
				parseInt(connection.source),
				{
					telegram_bot_command_id: parseInt(connection.target),
					telegram_bot_command_keyboard_button_id: parseInt(connection.sourceHandle.split(':')[2]),
					start_diagram_connector: connection.sourceHandle,
					end_diagram_connector: connection.targetHandle,
				},
			);

			createMessageToast({ message: response.json.message, level: response.json.level });
		}
	}

	return (
		<>
			<CommandOffcanvas show={showCommandOffcanvas} onHide={() => setShowCommandOffcanvas(false)} />
			<div className='border rounded' style={{ height: '80vh' }}>
				<ReactFlow
					nodes={nodes}
					edges={edges}
					nodeTypes={nodeTypes}
					onNodesChange={onNodesChange}
					onEdgesChange={onEdgesChange}
					onNodeDragStop={(event, node, nodes) => handleNodeDragStop(nodes)}
					isValidConnection={connection => connection.source !== connection.target}
					onConnect={handleConnect}
				>
					<Panel position='top-right'>
						<div className='d-flex justify-content-end gap-2'>
							<Button
								size='sm'
								variant='dark'
								onClick={() => setShowCommandOffcanvas(true)}
							>
								{gettext('Добавить команду')}
							</Button>
						</div>
					</Panel>
					<Controls />
					<MiniMap />
					<Background variant={BackgroundVariant.Dots} gap={24} size={1} />
				</ReactFlow>
			</div>
		</>
	);
}

export default App;