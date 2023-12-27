import 'reactflow/dist/style.css';
import './App.css';

import React, { ReactNode, useEffect, useRef, useState } from 'react';

import ReactFlow, {
	Panel,
	Controls,
	MiniMap,
	Background,
	BackgroundVariant,
	useEdgesState,
	useNodesState,
	Connection,
	NodeTypes,
	MarkerType,
	addEdge as addEdge_,
	updateEdge,
	Edge,
	Node,
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
	const edgeUpdating = useRef<Edge | null>(null);

	const [showCommandOffcanvas, setShowCommandOffcanvas] = useState(false);

	async function updateNodes(): Promise<void> {
		const response = await TelegramBotCommandsDiagramAPI.get(telegramBot.id);

		if (response.ok) {
			setNodes(response.json.map(data => ({
				id: data.id.toString(),
				type: 'command',
				position: { x: data.x, y: data.y },
				data,
			})));

			const newEdges: Edge[] = [];

			response.json.forEach(command => {
				command.keyboard?.buttons.forEach(button => {
					if (
						button.telegram_bot_command_id !== null &&
						button.start_diagram_connector !== null &&
						button.end_diagram_connector !== null
					) {
						newEdges.push({
							id: `reactflow__edge-${button.start_diagram_connector}-${button.end_diagram_connector}`,
							source: command.id.toString(),
							sourceHandle: button.start_diagram_connector,
							target: button.telegram_bot_command_id.toString(),
							targetHandle: button.end_diagram_connector,
						});
					}
				});
			});

			setEdges(newEdges);
		}
	}

	useEffect(() => { updateNodes() }, []);

	function handleNodeDragStop(nodes: Node[] | undefined): void {
		nodes?.forEach(node => TelegramBotCommandDiagramAPI.updatePosition(
			telegramBot.id,
			parseInt(node.id),
			node.position,
		));
	}

	async function addEdge(connection: Connection, shouldUpdateEdges: boolean = true, showMessageToast: boolean = true): Promise<void> {
		if (connection.source && connection.sourceHandle && connection.target && connection.targetHandle) {
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

			if (response.ok && shouldUpdateEdges) {
				setEdges(prevEdges => addEdge_(connection, prevEdges));
			}

			if (showMessageToast) {
				createMessageToast({ message: response.json.message, level: response.json.level });
			}
		}
	}

	async function deleteEdge(edge: Edge, shouldUpdateEdges: boolean = true, showMessageToast: boolean = true): Promise<void> {
		if (edge.sourceHandle) {
			const response = await TelegramBotCommandDiagramAPI.disconnect(
				telegramBot.id,
				parseInt(edge.source),
				{ telegram_bot_command_keyboard_button_id: parseInt(edge.sourceHandle.split(':')[2]) },
			);

			if (response.ok && shouldUpdateEdges) {
				setEdges(prevEdges => prevEdges.filter(e => e.id !== edge.id));
			}

			if (showMessageToast) {
				createMessageToast({ message: response.json.message, level: response.json.level });
			}
		}
	}

	function handleEdgeUpdateStart(edge: Edge): void {
		edgeUpdating.current = edge;
	}

	function handleEdgeUpdate(oldEdge: Edge, newConnection: Connection): void {
		if (
			edgeUpdating.current && (
				edgeUpdating.current.sourceHandle !== newConnection.sourceHandle ||
				edgeUpdating.current.targetHandle !== newConnection.targetHandle
			)
		) {
			const showMessageToast = (
				edgeUpdating.current.sourceHandle?.split(':')[2] !== newConnection.sourceHandle?.split(':')[2]
			) || (
				edgeUpdating.current.target !== newConnection.target
			);

			deleteEdge(oldEdge, false, showMessageToast);
			addEdge(newConnection, false, showMessageToast);

			setEdges(prevEdges => updateEdge(oldEdge, newConnection, prevEdges));
		}

		edgeUpdating.current = null;
	}

	function handleEdgeUpdateEnd(edge: Edge): void {
		if (edgeUpdating.current) {
			deleteEdge(edge);
		}

		edgeUpdating.current = null;
	}

	function handleValidConnection(connection: Connection): boolean {
		if (!(connection.source && connection.sourceHandle && connection.target && connection.targetHandle)) {
			return false;
		}

		if (connection.source === connection.target) {
			return false;
		}

		if (
			edgeUpdating.current && (
				(
					edgeUpdating.current.sourceHandle === connection.sourceHandle
				) || (
					edgeUpdating.current.sourceHandle?.split(':')[1] !== connection.sourceHandle?.split(':')[1] &&
					edgeUpdating.current.sourceHandle?.split(':')[2] === connection.sourceHandle?.split(':')[2]
				)
			)
		) {
			return true;
		}

		for (const edge of edges) {
			if (
				connection.sourceHandle === edge.sourceHandle ||
				connection.sourceHandle?.split(':')[2] === edge.sourceHandle?.split(':')[2]
			) {
				return false;
			}
		}

		return true;
	}

	function handleConnect(connection: Connection): void {
		addEdge(connection);
	}

	return (
		<>
			<CommandOffcanvas show={showCommandOffcanvas} onHide={() => setShowCommandOffcanvas(false)} />
			<div className='border rounded' style={{ height: '80vh' }}>
				<ReactFlow
					nodes={nodes}
					edges={edges}
					nodeTypes={nodeTypes}
					defaultEdgeOptions={{ markerEnd: { type: MarkerType.Arrow, strokeWidth: 1.8 } }}
					onNodesChange={onNodesChange}
					onEdgesChange={onEdgesChange}
					onNodeDragStop={(event, node, nodes) => handleNodeDragStop(nodes)}
					onEdgeUpdateStart={(event, edge) => handleEdgeUpdateStart(edge)}
					onEdgeUpdate={handleEdgeUpdate}
					onEdgeUpdateEnd={(event, edge) => handleEdgeUpdateEnd(edge)}
					isValidConnection={handleValidConnection}
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