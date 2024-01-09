import 'reactflow/dist/style.css';
import './index.css';

import React, {
	ReactElement,
	MouseEvent as ReactMouseEvent,
	MutableRefObject,
	memo,
	useEffect,
	useCallback,
	useRef,
} from 'react';
import { useRouteLoaderData } from 'react-router';

import ReactFlow, {
	Panel,
	Controls,
	MiniMap,
	Background,
	BackgroundVariant,
	useEdgesState,
	useNodesState,
	addEdge as addEdge_,
	updateEdge,
	NodeTypes,
	MarkerType,
	Connection,
	Node,
	Edge,
} from 'reactflow';

import Button from 'react-bootstrap/Button';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import { UpdateNodesRef } from '../../.';
import CommandNode from './components/CommandNode';

import useToast from 'services/hooks/useToast';

import { TelegramBotCommandDiagramAPI, TelegramBotCommandsDiagramAPI } from 'services/api/telegram_bots/main';
import { TelegramBotCommandDiagram } from 'services/api/telegram_bots/types';

export interface DiagramProps {
	innerRef?: MutableRefObject<UpdateNodesRef>;
	onAddCommandClick: () => void;
}

export interface NodeData extends Omit<TelegramBotCommandDiagram, 'x' | 'y'> {
	updateNodes: () => void;
}

const nodeTypes: NodeTypes = { command: CommandNode };

function Diagram({ innerRef, onAddCommandClick }: DiagramProps): ReactElement<DiagramProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();

	const [nodes, setNodes, onNodesChange] = useNodesState<NodeData>([]);
	const [edges, setEdges, onEdgesChange] = useEdgesState([]);
	const edgeUpdating = useRef<Edge | null>(null);

	const updateNodes = useCallback(async (): Promise<void> => {
		const response = await TelegramBotCommandsDiagramAPI.get(telegramBot.id);

		if (response.ok) {
			setNodes(response.json.map(command => {
				const { x, y, ...command_ } = command;

				return {
					id: command_.id.toString(),
					type: 'command',
					position: { x, y },
					data: { ...command_, updateNodes },
				}
			}));

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
	}, []);

	if (innerRef) {
		innerRef.current.updateNodes = updateNodes;
	}

	useEffect(() => { updateNodes() }, []);

	const handleNodeDragStop = useCallback((event: ReactMouseEvent, node: Node, nodes: Node[] | undefined): void => {
		nodes?.forEach(node => TelegramBotCommandDiagramAPI.updatePosition(
			telegramBot.id,
			parseInt(node.id),
			node.position,
		));
	}, []);

	const addEdge = useCallback(async (connection: Connection, shouldUpdateEdges: boolean = true, showMessageToast: boolean = true): Promise<void> => {
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
	}, []);

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

	const handleEdgeUpdateStart = useCallback((event: ReactMouseEvent, edge: Edge): void => {
		edgeUpdating.current = edge;
	}, []);

	const handleEdgeUpdate = useCallback((oldEdge: Edge, newConnection: Connection): void => {
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
	}, []);

	const handleEdgeUpdateEnd = useCallback((event: MouseEvent | TouchEvent, edge: Edge): void => {
		if (edgeUpdating.current) {
			deleteEdge(edge);
		}

		edgeUpdating.current = null;
	}, []);

	const handleValidConnection = useCallback((connection: Connection): boolean => {
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
	}, [edges]);

	return (
		<div className='border rounded' style={{ height: '80vh' }}>
			<ReactFlow
				fitView
				nodes={nodes}
				edges={edges}
				nodeTypes={nodeTypes}
				defaultEdgeOptions={{ markerEnd: { type: MarkerType.Arrow, strokeWidth: 1.8 } }}
				deleteKeyCode={null}
				onNodesChange={onNodesChange}
				onEdgesChange={onEdgesChange}
				onNodeDragStop={handleNodeDragStop}
				onEdgeUpdateStart={handleEdgeUpdateStart}
				onEdgeUpdate={handleEdgeUpdate}
				onEdgeUpdateEnd={handleEdgeUpdateEnd}
				isValidConnection={handleValidConnection}
				onConnect={addEdge}
			>
				<Panel position='top-right'>
					<div className='d-flex justify-content-end gap-2'>
						<Button
							size='sm'
							variant='dark'
							onClick={onAddCommandClick}
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
	);
}

export default memo(Diagram);